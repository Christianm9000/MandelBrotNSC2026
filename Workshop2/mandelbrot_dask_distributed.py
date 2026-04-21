from dask.delayed import delayed
from dask.distributed import Client, LocalCluster
import dask
import matplotlib.pyplot as plt
import numpy as np
import statistics
import time
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


@njit(cache=True)
def mandelbrot_serial(N, x_min, x_max, y_min, y_max, max_iter):
    return mandelbrot_chunk(0, N, N, x_min, x_max, y_min, y_max, max_iter)


def make_row_chunks(N, n_chunks):
    n_tasks = max(1, min(n_chunks, N))
    base = N // n_tasks
    rem = N % n_tasks

    bounds = []
    row = 0
    for i in range(n_tasks):
        size = base + (1 if i < rem else 0)
        row_end = row + size
        bounds.append((row, row_end))
        row = row_end

    return bounds


def mandelbrot_dask(N, x_min, x_max, y_min, y_max, max_iter, n_chunks):
    tasks = [
        delayed(mandelbrot_chunk)(
            row_start, row_end, N, x_min, x_max, y_min, y_max, max_iter
        )
        for row_start, row_end in make_row_chunks(N, n_chunks)
    ]

    parts = dask.compute(*tasks)
    return np.vstack(parts)


def warmup_worker(N, x_min, x_max, y_min, y_max, max_iter):
    mandelbrot_chunk(0, min(8, N), N, x_min, x_max, y_min, y_max, max_iter)
    return True


def timed_serial_baseline(N, x_min, x_max, y_min, y_max, max_iter, repeats=3):
    # Driver-side JIT warm-up excluded from timing.
    mandelbrot_serial(N, x_min, x_max, y_min, y_max, max_iter)

    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        mandelbrot_serial(N, x_min, x_max, y_min, y_max, max_iter)
        times.append(time.perf_counter() - t0)
    return statistics.median(times)


if __name__ == "__main__":
    N = 1024
    x_min, x_max = -2.0, 1.0
    y_min, y_max = -1.5, 1.5
    max_iter = 100
    n_workers = 6
    chunk_multipliers = [1, 2, 4, 6, 8, 16]
    plot_path = "dask_chunk_sweep.png"

    t_serial = timed_serial_baseline(N, x_min, x_max, y_min, y_max, max_iter)
    print(f"Serial baseline T1: {t_serial:.4f} s\n")

    #cluster = LocalCluster(n_workers=n_workers, threads_per_worker=1, processes=True, dashboard_address=None)
    #client = Client(cluster)

    client = Client("tcp://10.92.0.156:8786")

    try:
        # Warm up Numba JIT in all worker processes before the sweep.
        client.run(warmup_worker, N, x_min, x_max, y_min, y_max, max_iter)

        results = []
        best_result = None

        print("n_chunks | time (s) | vs 1x | speedup | LIF")
        print("-" * 46)

        for mult in chunk_multipliers:
            n_chunks = mult * n_workers

            times = []
            for _ in range(3):
                t0 = time.perf_counter()
                result = mandelbrot_dask(
                    N,
                    x_min,
                    x_max,
                    y_min,
                    y_max,
                    max_iter=max_iter,
                    n_chunks=n_chunks,
                )
                times.append(time.perf_counter() - t0)

            t_par = statistics.median(times)
            vs_1x = t_par / t_serial
            speedup = t_serial / t_par
            lif = n_workers * t_par / t_serial - 1.0

            # Keep the computation alive so Dask cannot optimize it away.
            checksum = int(result.sum())

            row = {
                "n_chunks": n_chunks,
                "time": t_par,
                "vs_1x": vs_1x,
                "speedup": speedup,
                "lif": lif,
                "checksum": checksum,
            }
            results.append(row)

            if best_result is None or t_par < best_result["time"]:
                best_result = row

            print(
                f"{n_chunks:8d} | "
                f"{t_par:8.4f} | "
                f"{vs_1x:5.2f}x | "
                f"{speedup:7.2f}x | "
                f"{lif:5.3f}"
            )

        n_chunks_optimal = best_result["n_chunks"]
        t_min = best_result["time"]
        lif_min = best_result["lif"]

        print("\nRecord:")
        print(f"n_chunks_optimal = {n_chunks_optimal}")
        print(f"t_min            = {t_min:.4f} s")
        print(f"LIF_min          = {lif_min:.3f}")
        print(f"checksum(best)   = {best_result['checksum']}")

        xs = [r["n_chunks"] for r in results]
        ys = [r["time"] for r in results]

        plt.figure(figsize=(7, 4.5))
        plt.plot(xs, ys, marker="o")
        plt.xscale("log")
        plt.xlabel("n_chunks")
        plt.ylabel("wall time (s)")
        plt.title("Dask local chunk-count sweep")
        plt.grid(True, which="both", alpha=0.3)
        plt.tight_layout()
        plt.savefig(plot_path, dpi=150)
        plt.close()

        print(f"Saved plot to {plot_path}")
    finally:
        client.close()
        #cluster.close()
