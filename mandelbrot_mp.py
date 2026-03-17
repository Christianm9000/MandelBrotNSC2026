import multiprocessing as mp
import numpy as np
import matplotlib.pyplot as plt
import time, os, statistics
from numba import njit

@njit
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


@njit
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


def build_chunks(N, x_min, x_max, y_min, y_max, max_iter, n_workers):
    chunk_size = max(1, N // n_workers)
    chunks = []
    row = 0

    while row < N:
        row_end = min(row + chunk_size, N)
        chunks.append((row, row_end, N, x_min, x_max, y_min, y_max, max_iter))
        row = row_end

    return chunks


def mandelbrot_parallel(N, x_min, x_max, y_min, y_max, max_iter, n_workers=4):
    chunks = build_chunks(N, x_min, x_max, y_min, y_max, max_iter, n_workers)

    with mp.Pool(processes=n_workers) as pool:
        parts = pool.map(_worker, chunks)

    return np.vstack(parts)


if __name__ == "__main__":
    N = 1024
    x_min, x_max = -2.0, 1.0
    y_min, y_max = -1.5, 1.5
    max_iter = 100

    # -----------------------------
    # 1) Main-process JIT warmup
    # -----------------------------
    # This ensures Numba has already compiled the serial path before serial timing.
    mandelbrot_serial(N, x_min, x_max, y_min, y_max, max_iter)

    # -----------------------------
    # 2) Serial baseline (median of 3)
    # -----------------------------
    serial_times = []
    for _ in range(3):
        t0 = time.perf_counter()
        mandelbrot_set_serial = mandelbrot_serial(N, x_min, x_max, y_min, y_max, max_iter)
        serial_times.append(time.perf_counter() - t0)

    t_serial = statistics.median(serial_times)
    print(f"Serial median time: {t_serial:.4f} s")

    best_result = None

    # -----------------------------
    # 3) Sweep worker counts
    # -----------------------------
    for n_workers in range(1, os.cpu_count() + 1):
        chunks = build_chunks(N, x_min, x_max, y_min, y_max, max_iter, n_workers)

        # Pool creation is outside the timed region
        with mp.Pool(processes=n_workers) as pool:
            # Untimed warmup:
            # this triggers Numba compilation inside each worker process
            pool.map(_worker, chunks)

            times = []
            for _ in range(3):
                t0 = time.perf_counter()
                parts = pool.map(_worker, chunks)
                result = np.vstack(parts)   # include assembly time
                times.append(time.perf_counter() - t0)

            t_par = statistics.median(times)
            if n_workers == 1:
                t_serial = t_par  # sanity check: 1 worker should match serial time

        speedup = t_serial / t_par
        efficiency = speedup / n_workers

        print(
            f"{n_workers:2d} workers: "
            f"{t_par:.4f} s, "
            f"speedup={speedup:.2f}x, "
            f"efficiency={efficiency * 100:.1f}%"
        )