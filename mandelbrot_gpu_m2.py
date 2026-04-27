import os
import statistics
import time

import matplotlib.pyplot as plt
import numpy as np
import pyopencl as cl


KERNEL_SRC_F32 = """
__kernel void mandelbrot_f32(
    __global int *result,
    const float x_min, const float x_max,
    const float y_min, const float y_max,
    const int N, const int max_iter)
{
    int col = get_global_id(0);
    int row = get_global_id(1);

    if (col >= N || row >= N) return;

    float c_real = x_min + col * (x_max - x_min) / (float)N;
    float c_imag = y_min + row * (y_max - y_min) / (float)N;

    float z_real = 0.0f, z_imag = 0.0f;
    int iter = 0;
    while (iter < max_iter && z_real * z_real + z_imag * z_imag <= 4.0f) {
        float z_real_temp = z_real * z_real - z_imag * z_imag + c_real;
        z_imag = 2.0f * z_real * z_imag + c_imag;
        z_real = z_real_temp;
        iter++;
    }

    result[row * N + col] = iter;
}
"""


KERNEL_SRC_F64 = """
#pragma OPENCL EXTENSION cl_khr_fp64 : enable

__kernel void mandelbrot_f64(
    __global int *result,
    const double x_min, const double x_max,
    const double y_min, const double y_max,
    const int N, const int max_iter)
{
    int col = get_global_id(0);
    int row = get_global_id(1);

    if (col >= N || row >= N) return;

    double c_real = x_min + col * (x_max - x_min) / (double)N;
    double c_imag = y_min + row * (y_max - y_min) / (double)N;

    double z_real = 0.0, z_imag = 0.0;
    int iter = 0;
    while (iter < max_iter && z_real * z_real + z_imag * z_imag <= 4.0) {
        double z_real_temp = z_real * z_real - z_imag * z_imag + c_real;
        z_imag = 2.0 * z_real * z_imag + c_imag;
        z_real = z_real_temp;
        iter++;
    }

    result[row * N + col] = iter;
}
"""


MAX_ITER = 200
X_MIN, X_MAX = -2.5, 1.0
Y_MIN, Y_MAX = -1.25, 1.25
BENCHMARK_SIZES = [1024, 2048]
RUNS = 3


def run_mandelbrot_f32(queue, kernel, ctx, N, max_iter=MAX_ITER, runs=RUNS,
                       x_min=X_MIN, x_max=X_MAX, y_min=Y_MIN, y_max=Y_MAX):
    """Run one f32 warmup, then return the final image and median runtime."""
    image = np.zeros((N, N), dtype=np.int32)
    image_dev = cl.Buffer(ctx, cl.mem_flags.WRITE_ONLY, image.nbytes)

    args = (
        image_dev,
        np.float32(x_min), np.float32(x_max),
        np.float32(y_min), np.float32(y_max),
        np.int32(N), np.int32(max_iter),
    )

    kernel(queue, (N, N), None, *args)
    queue.finish()

    timings = []
    for _ in range(runs):
        t0 = time.perf_counter()
        kernel(queue, (N, N), None, *args)
        queue.finish()
        timings.append(time.perf_counter() - t0)

    cl.enqueue_copy(queue, image, image_dev)
    queue.finish()
    return image, statistics.median(timings)


def run_mandelbrot_f64(queue, kernel, ctx, N, max_iter=MAX_ITER, runs=RUNS,
                       x_min=X_MIN, x_max=X_MAX, y_min=Y_MIN, y_max=Y_MAX):
    """Run one f64 warmup, then return the final image and median runtime."""
    image = np.zeros((N, N), dtype=np.int32)
    image_dev = cl.Buffer(ctx, cl.mem_flags.WRITE_ONLY, image.nbytes)

    args = (
        image_dev,
        np.float64(x_min), np.float64(x_max),
        np.float64(y_min), np.float64(y_max),
        np.int32(N), np.int32(max_iter),
    )

    kernel(queue, (N, N), None, *args)
    queue.finish()

    timings = []
    for _ in range(runs):
        t0 = time.perf_counter()
        kernel(queue, (N, N), None, *args)
        queue.finish()
        timings.append(time.perf_counter() - t0)

    cl.enqueue_copy(queue, image, image_dev)
    queue.finish()
    return image, statistics.median(timings)


def save_image(image, filename):
    plt.figure()
    plt.imshow(image, cmap="hot", origin="lower")
    plt.axis("off")
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close()


def save_timing_plot(results, filename="mandelbrot_m2_f32_vs_f64.png"):
    labels = []
    times = []

    for N in BENCHMARK_SIZES:
        for precision in ("f32", "f64"):
            key = (precision, N)
            if key in results:
                labels.append(f"{precision} {N}")
                times.append(results[key])

    plt.figure()
    plt.bar(labels, times)
    plt.yscale("log")
    plt.ylabel("Runtime [s] (median, log scale)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()


def main():
    ctx = cl.create_some_context(interactive=False)
    queue = cl.CommandQueue(ctx)
    dev = ctx.devices[0]

    print(f"Device: {dev.name}")
    print(f"Compute units: {dev.max_compute_units}")

    if "cl_khr_fp64" in dev.extensions:
        print("Native fp64 extension found: cl_khr_fp64")
    else:
        print("No cl_khr_fp64 extension found. Float64 may fail or be emulated/very slow.")

    prog_f32 = cl.Program(ctx, KERNEL_SRC_F32).build()
    kernel_f32 = cl.Kernel(prog_f32, "mandelbrot_f32")

    kernel_f64 = None
    try:
        prog_f64 = cl.Program(ctx, KERNEL_SRC_F64).build()
        kernel_f64 = cl.Kernel(prog_f64, "mandelbrot_f64")
    except Exception as exc:
        print("Could not build f64 kernel. Skipping f64 benchmark.")
        print(f"Build error: {exc}")

    results = {}
    last_f32_image = None
    last_f64_image = None

    for N in BENCHMARK_SIZES:
        image_f32, elapsed_f32 = run_mandelbrot_f32(queue, kernel_f32, ctx, N, runs=RUNS)
        results[("f32", N)] = elapsed_f32
        last_f32_image = image_f32
        print(f"GPU f32 {N}x{N}: {elapsed_f32 * 1e3:.1f} ms median over {RUNS} runs")

        if kernel_f64 is not None:
            image_f64, elapsed_f64 = run_mandelbrot_f64(queue, kernel_f64, ctx, N, runs=RUNS)
            results[("f64", N)] = elapsed_f64
            last_f64_image = image_f64
            slowdown = elapsed_f64 / elapsed_f32
            print(f"GPU f64 {N}x{N}: {elapsed_f64 * 1e3:.1f} ms median over {RUNS} runs")
            print(f"f64/f32 slowdown at N={N}: {slowdown:.2f}x")

    if last_f32_image is not None:
        save_image(last_f32_image, "mandelbrot_gpu_f32.png")
    if last_f64_image is not None:
        save_image(last_f64_image, "mandelbrot_gpu_f64.png")

    save_timing_plot(results)


if __name__ == "__main__":
    main()
