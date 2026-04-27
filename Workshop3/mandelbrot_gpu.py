import time

import matplotlib.pyplot as plt
import numpy as np
import pyopencl as cl


KERNEL_SRC = """
__kernel void mandelbrot(
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


def run_mandelbrot(prog, queue, image_dev, N, max_iter, x_min, x_max, y_min, y_max):
    prog.mandelbrot(
        queue,
        (N, N),
        None,
        image_dev,
        np.float32(x_min),
        np.float32(x_max),
        np.float32(y_min),
        np.float32(y_max),
        np.int32(N),
        np.int32(max_iter),
    )


def main():
    #create OpenCL context, queue, and program.
    ctx = cl.create_some_context(interactive=False)
    queue = cl.CommandQueue(ctx)
    prog = cl.Program(ctx, KERNEL_SRC).build()

    N, MAX_ITER = 2048, 200
    X_MIN, X_MAX = -2.5, 1.0
    Y_MIN, Y_MAX = -1.25, 1.25

    #image is allocated on the host, and a corresponding buffer is created on the device.
    image = np.zeros((N, N), dtype=np.int32)
    image_dev = cl.Buffer(ctx, cl.mem_flags.WRITE_ONLY, image.nbytes)

    run_mandelbrot(prog, queue, image_dev, N, MAX_ITER, X_MIN, X_MAX, Y_MIN, Y_MAX)
    queue.finish()

    t0 = time.perf_counter()
    run_mandelbrot(prog, queue, image_dev, N, MAX_ITER, X_MIN, X_MAX, Y_MIN, Y_MAX)
    queue.finish()
    elapsed = time.perf_counter() - t0

    #copy result back after the timed kernel execution.
    cl.enqueue_copy(queue, image, image_dev)
    queue.finish()

    print(f"GPU {N}x{N}: {elapsed * 1e3:.1f} ms")

    plt.imshow(image, cmap="hot", origin="lower")
    plt.axis("off")
    plt.savefig("mandelbrot_gpu.png", dpi=150, bbox_inches="tight")


if __name__ == "__main__":
    main()