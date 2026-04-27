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

    float z_real = 0.0f;
    float z_imag = 0.0f;
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

MAX_ITER = 100
X_MIN, X_MAX = -2.5, 1.0
Y_MIN, Y_MAX = -1.25, 1.25
BENCHMARK_SIZES = [1024, 2048]
RUNS = 3

#old numba times
NUMBA_F32_TIMES = {
    1024: 0.071,
    2048: 0.285,
}

NUMBA_F64_TIMES = {
    1024: 0.311,
    2048: 1.234,
}


def run_mandelbrot_gpu_f32(queue, kernel, ctx, N, max_iter=MAX_ITER, runs=RUNS,
                           x_min=X_MIN, x_max=X_MAX, y_min=Y_MIN, y_max=Y_MAX):
    """Run one warmup and then return the image and median GPU f32 runtime."""
    image = np.zeros((N, N), dtype=np.int32)
    image_dev = cl.Buffer(ctx, cl.mem_flags.WRITE_ONLY, image.nbytes)

    args = (
        image_dev,
        np.float32(x_min), np.float32(x_max),
        np.float32(y_min), np.float32(y_max),
        np.int32(N), np.int32(max_iter),
    )

    #warmup
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


def save_comparison_plot(gpu_f32_times, filename="mandelbrot_gpu_f32_vs_numba_f64.png"):
    labels = []
    times = []

    for N in BENCHMARK_SIZES:
        labels.extend([f"GPU f32\n{N}x{N}", f"Numba f64\n{N}x{N}"])
        times.extend([gpu_f32_times[N], NUMBA_F64_TIMES[N]])

    plt.figure()
    plt.bar(labels, times)
    plt.yscale("log")
    plt.ylabel("Runtime [s] (log scale)")
    plt.title(f"Mandelbrot runtime comparison, max_iter={MAX_ITER}")
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()


def print_results_table(gpu_f32_times):
    header = (
        "N", "GPU f32 [s]", "Numba f64 [s]", "Numba f64 / GPU f32", "Numba f32 [s]"
    )
    print("\n" + "{:<8} {:>14} {:>15} {:>22} {:>14}".format(*header))
    print("-" * 78)

    for N in BENCHMARK_SIZES:
        gpu_time = gpu_f32_times[N]
        numba_f64_time = NUMBA_F64_TIMES[N]
        numba_f32_time = NUMBA_F32_TIMES[N]
        speedup = numba_f64_time / gpu_time
        print(
            f"{N:<8} "
            f"{gpu_time:>14.6f} "
            f"{numba_f64_time:>15.6f} "
            f"{speedup:>21.2f}x "
            f"{numba_f32_time:>14.6f}"
        )


def main():
    ctx = cl.create_some_context(interactive=False)
    queue = cl.CommandQueue(ctx)
    dev = ctx.devices[0]

    print(f"Device: {dev.name}")
    print(f"Compute units: {dev.max_compute_units}")
    print(f"max_iter={MAX_ITER}, timed runs={RUNS}, statistic=median")
    print("Comparing OpenCL GPU f32 against supplied older Numba f64 timings.")

    program = cl.Program(ctx, KERNEL_SRC_F32).build()
    kernel = cl.Kernel(program, "mandelbrot_f32")

    gpu_f32_times = {}
    largest_image = None

    for N in BENCHMARK_SIZES:
        image, elapsed = run_mandelbrot_gpu_f32(queue, kernel, ctx, N, runs=RUNS)
        gpu_f32_times[N] = elapsed
        print(f"GPU f32 {N}x{N}: {elapsed * 1e3:.1f} ms median over {RUNS} runs")
        print(f"Numba f64 {N}x{N}: {NUMBA_F64_TIMES[N] * 1e3:.1f} ms")
        print(f"Speedup vs Numba f64 at N={N}: {NUMBA_F64_TIMES[N] / elapsed:.2f}x")

    print_results_table(gpu_f32_times)

    save_comparison_plot(gpu_f32_times)
    print("\nSaved mandelbrot_gpu_f32.png")
    print("Saved mandelbrot_gpu_f32_vs_numba_f64.png")


if __name__ == "__main__":
    main()
