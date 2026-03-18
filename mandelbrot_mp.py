import multiprocessing as mp
import numpy as np
import matplotlib.pyplot as plt
import time, os, statistics
from numba import njit

@njit(cache=True)
def mandelbrot_pixel(c_real, c_imag, max_iter):
    z_real, z_imag = 0.0, 0.0
    for i in range(max_iter):
        z_real2 = z_real * z_real
        z_imag2 = z_imag * z_imag
        if z_real2 + z_imag2 > 4.0:
            return i
        z_imag = 2 * z_real * z_imag + c_imag
        z_real = z_real2 - z_imag2 + c_real
    return max_iter


@njit(cache=True)
def mandelbrot_chunk(row_start, row_end, N, x_min, x_max, y_min, y_max, max_iter):
    out = np.empty((row_end - row_start, N), dtype=np.int32)

    dx = (x_max - x_min) / N
    dy = (y_max - y_min) / N

    for r in range(row_end - row_start):
        y = y_min + (row_start + r) * dy
        for c in range(N):
            x = x_min + c * dx
            out[r, c] = mandelbrot_pixel(x, y, max_iter)

    return out


def mandelbrot_serial(N, x_min, x_max, y_min, y_max, max_iter):
    return mandelbrot_chunk(0, N, N, x_min, x_max, y_min, y_max, max_iter)


def visualize(mandelbrot_set, x_min, x_max, y_min, y_max):
    plt.imshow(mandelbrot_set, extent=(x_min, x_max, y_min, y_max), cmap='inferno')
    plt.colorbar()
    plt.title("Mandelbrot Set")
    plt.xlabel("Re")
    plt.ylabel("Im")
    plt.show()


def _worker(args):
    return mandelbrot_chunk(*args)


def build_chunks(N, x_min, x_max, y_min, y_max, max_iter, n_chunks):
    chunk_size = max(1, N // n_chunks)
    chunks = []
    row = 0

    while row < N:
        row_end = min(row + chunk_size, N)
        chunks.append((row, row_end, N, x_min, x_max, y_min, y_max, max_iter))
        row = row_end

    return chunks


def mandelbrot_parallel(N, x_min, x_max, y_min, y_max, max_iter=100, n_workers=4, n_chunks=None, pool=None):
    if n_chunks is None:
        n_chunks = n_workers

    chunks = build_chunks(N, x_min, x_max, y_min, y_max, max_iter, n_chunks)

    # reuse caller-managed pool: no warmup
    if pool is not None:
        parts = pool.map(_worker, chunks)
        return np.vstack(parts)

    #create pool and do one warmup
    with mp.Pool(processes=n_workers) as p:
        tiny = [(0, min(8, N), N, x_min, x_max, y_min, y_max, max_iter)]
        p.map(_worker, tiny)   #warm up worker JIT
        parts = p.map(_worker, chunks)

    return np.vstack(parts)


if __name__ == "__main__":
    N = 1024
    x_min, x_max = -2.0, 1.0
    y_min, y_max = -1.5, 1.5
    max_iter = 100

    mandelbrot_serial(N, x_min, x_max, y_min, y_max, max_iter)  # main-process warmup

    serial_times = []
    for _ in range(3):
        t0 = time.perf_counter()
        mandelbrot_serial(N, x_min, x_max, y_min, y_max, max_iter)
        serial_times.append(time.perf_counter() - t0)
    t_serial = statistics.median(serial_times)

    print(f"Serial median time: {t_serial:.4f} s")

    for n_workers in range(1, os.cpu_count() + 1):
        with mp.Pool(processes=n_workers) as pool:
            #warm up workers once
            mandelbrot_parallel(
                N, x_min, x_max, y_min, y_max,
                max_iter=max_iter, n_workers=n_workers,
                n_chunks=n_workers, pool=pool
            )