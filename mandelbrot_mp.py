import multiprocessing as mp
import numpy as np
import matplotlib.pyplot as plt
import time, os, statistics
from numba import njit

@njit
def mandelbrot_pixel(c_real, c_imag, max_iter):
    # The scalar kernel to compute the Mandelbrot value for a single pixel
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
    # Computes pixel coordinates from row_start to row_end - no arrays received as input. Returns a (row_end - row_start) x N int32 array of Mandelbrot values.
    out = np.empty((row_end - row_start, N), dtype=np.int32)

    dx = (x_max - x_min) / N # Step size in the x direction
    dy = (y_max - y_min) / N # Step size in the y direction

    for r in range(row_end - row_start):
        y = y_min + (row_start + r) * dy # Compute the y coordinate for the current row
        for c in range(N):
            x = x_min + c * dx # Compute the x coordinate for the current column
            out[r, c] = mandelbrot_pixel(x, y, max_iter)

    return out

def mandelbrot_serial(N, x_min, x_max, y_min, y_max, max_iter):
    # Serial implementation of the Mandelbrot set computation. Calls mandelbrot_chunk for the entire image and returns the resulting array.
    return mandelbrot_chunk(0, N, N, x_min, x_max, y_min, y_max, max_iter)

def vizualize(mandelbrot_set):
    # Visualizes the Mandelbrot set using matplotlib.
    plt.imshow(mandelbrot_set, extent=(x_min, x_max, y_min, y_max), cmap='inferno')
    plt.colorbar()
    plt.title("Mandelbrot Set")
    plt.xlabel("Re")
    plt.ylabel("Im")
    plt.show()

def _worker(args):
    # Worker function for multiprocessing. Unpacks the arguments and calls mandelbrot_chunk.
    return mandelbrot_chunk(*args)

def mandelbrot_parallel(N, x_min, x_max, y_min, y_max, max_iter, n_workers=4):
    
    chunk_size = max(1, N // n_workers) # Determine the number of rows each worker will process
    chunks, row = [], 0
    while row < N:
        row_end = min(row + chunk_size, N) # Calculate the end row for the current chunk
        chunks.append((row, row_end, N, x_min, x_max, y_min, y_max, max_iter)) # Append the arguments for the worker
        row = row_end # Move to the next chunk

    with mp.Pool(processes=n_workers) as pool:
        pool.map(_worker, chunks) # Warmup run to compile the numba functions
        parts = pool.map(_worker, chunks) # Actual parallel computation

    return np.vstack(parts) # Combine the results from all workers into a single array


if __name__ == "__main__":
    N = 1024 # Image resolution (N x N)
    x_min, x_max = -2.0, 1.0 # Range of x values in the complex plane
    y_min, y_max = -1.5, 1.5 # Range of y values in the complex plane
    max_iter = 100 # Maximum iterations for Mandelbrot computation

    # Serial computation
    start_time = time.time()
    mandelbrot_set_serial = mandelbrot_serial(N, x_min, x_max, y_min, y_max, max_iter)
    serial_time = time.time() - start_time
    print(f"Serial execution time: {serial_time:.4f} seconds")

    # Parallel computation
    start_time = time.time()
    mandelbrot_set_parallel = mandelbrot_parallel(N, x_min, x_max, y_min, y_max, max_iter)
    parallel_time = time.time() - start_time
    print(f"Parallel execution time: {parallel_time:.4f} seconds")
