"""
Mandelbrot Set Generator
Author : Christian Mariager
Course : Numerical Scientific Computing 2026
"""

import numpy as np
from numba import njit, prange
import time
import matplotlib.pyplot as plt


@njit()
def mandelbrot_point(complex_input: complex, max_iterations: int = 1000) -> int:
    """
    Description:
    - Takes a single complex number c
    - returns iteration count
    - test with known points (e.g., c=0 should be max_iterations)
    """
    # Initialize z to 0
    z_0 = 0 + 0j

    for iteration in prange(max_iterations):
        if z_0.real**2 + z_0.imag**2 > 4: # Check if the magnitude of z exceeds 2
            return iteration
        z_0 = z_0**2 + complex_input

    # Return the max iteartion count if the point does not escape
    return max_iterations

@njit(parallel=True, fastmath=True)
def compute_mandelbrot_naive(x_space, y_space, resolution, max_iterations, prec_type):
    """
    x_space: Describes the range of the real axis (e.g., [-2.0, 1.0])
    y_space: Describes the range of the imaginary axis (e.g., [-1.5, 1.5])
    param resolution: Number of points along each axis (e.g., 1000)

    Description:
    - Creates a grid of complex numbers representing the points in the complex plane
    - For each point in the grid, it calls mandelbrot_point to determine the iteration count
    - Returns a 2D array of iteration counts corresponding to each point in the grid
    """

    # Create a grid of complex numbers representing the points in the complex plane
    x = np.linspace(x_space[0], x_space[1], resolution).astype(prec_type) # Real axis values
    y = np.linspace(y_space[0], y_space[1], resolution).astype(prec_type) # Imaginary axis values
    #X, Y = np.meshgrid(x, y)

    # Initialize a 2D array to store the iteration counts
    iteration_counts = np.zeros((resolution, resolution), dtype=np.int32)

    for i in prange(resolution):
        yi = y[i]
        for j in prange(resolution):
            complex_input = x[j] + 1j * yi
            iteration_count = mandelbrot_point(complex_input, max_iterations)

            # Store the iteration count in a 2D array
            iteration_counts[i, j] = iteration_count

    return iteration_counts


def visualize_mandelbrot_side_by_side(iteration_counts: list[np.ndarray], x_space, y_space):
    """
    Docstring for visualize_mandelbrot_side_by_side

    Description:
    - Takes 2D arrays of iteration counts and visualizes it
    - Displays the resulting image of the Mandelbrot set
    """

    for i, counts in enumerate(iteration_counts):
        plt.subplot(1, len(iteration_counts), i+1)
        plt.imshow(counts, extent=(x_space[0], x_space[1], y_space[0], y_space[1]), cmap='hot')
        plt.colorbar()
        if i == 0:
            plt.title('Mandelbrot Set (float32)')
        else:
            plt.title('Mandelbrot Set (float64)')
    plt.show()

if __name__ == "__main__":
    x_space = [-2.0, 1.0] # Real axis range
    y_space = [-1.5, 1.5] # Imaginary axis range
    resolution = 2048 # Number of points along each axis
    max_iterations = 100 # Maximum number of iterations to determine if a point escapes
    prec = np.float64

    _ = compute_mandelbrot_naive(x_space, y_space, resolution, max_iterations, prec_type=prec)
    
    iteration_list = []

    for prec in [np.float32, np.float64]:
        print(f"Running with precision: {prec}")
        if prec == np.float64:
            # Warm up the JIT compiler for float64 precision
            _ = compute_mandelbrot_naive(x_space, y_space, resolution, max_iterations, prec_type=prec)

        start = time.perf_counter()
        iteration_counts = compute_mandelbrot_naive(x_space, y_space, resolution, max_iterations, prec_type=prec)
        end = time.perf_counter()
        print(f"Execution time: {end - start:.3f} seconds")
        iteration_list.append(iteration_counts)
    visualize_mandelbrot_side_by_side(iteration_list, x_space, y_space)