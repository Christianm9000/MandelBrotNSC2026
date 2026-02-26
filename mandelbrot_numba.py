"""
Mandelbrot Set Generator
Author : Christian Mariager
Course : Numerical Scientific Computing 2026
"""

import numpy as np
from numba import njit
import time

@njit
def mandelbrot_point(complex_input: complex, max_iterations: int = 1000):
    """
    Description:
    - Takes a single complex number c
    - returns iteration count
    - test with known points (e.g., c=0 should be max_iterations)
    """
    # Initialize z to 0
    z_0 = 0 + 0j

    for iteration in range(max_iterations):
        if z_0.real**2 + z_0.imag**2 > 4: # Check if the magnitude of z exceeds 2
            return iteration
        z_0 = z_0**2 + complex_input

    # Return the max iteartion count if the point does not escape
    return max_iterations

@njit
def compute_mandelbrot_naive(x_space, y_space, resolution, max_iterations):
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
    x = np.linspace(x_space[0], x_space[1], resolution) # Real axis values
    y = np.linspace(y_space[0], y_space[1], resolution) # Imaginary axis values
    #X, Y = np.meshgrid(x, y)

    # Initialize a 2D array to store the iteration counts
    iteration_counts = np.zeros((resolution, resolution), dtype=np.int32)

    for i in range(resolution):
        yi = y[i]
        for j in range(resolution):
            complex_input = x[j] + 1j * yi
            iteration_count = mandelbrot_point(complex_input, max_iterations)

            # Store the iteration count in a 2D array
            iteration_counts[i, j] = iteration_count

    return iteration_counts

if __name__ == "__main__":
    x_space = [-2.0, 1.0] # Real axis range
    y_space = [-1.5, 1.5] # Imaginary axis range
    resolution = 1024 # Number of points along each axis
    max_iterations = 100 # Maximum number of iterations to determine if a point escapes

    _ = compute_mandelbrot_naive(x_space, y_space, resolution, max_iterations)
    
    start = time.perf_counter()
    iteration_counts = compute_mandelbrot_naive(x_space, y_space, resolution, max_iterations)
    end = time.perf_counter()
    print(f"Execution time: {end - start:.3f} seconds")
