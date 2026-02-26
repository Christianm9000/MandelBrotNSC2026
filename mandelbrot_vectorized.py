"""
Mandelbrot Set Generator
Author : Christian Mariager
Course : Numerical Scientific Computing 2026
"""

import numpy as np
import time, statistics
import matplotlib.pyplot as plt

def benchmark ( func , * args , n_runs =3) :
    """ Time func , return median of n_runs . """
    times = []
    for _ in range(n_runs):
        t0 = time.perf_counter()
        result = func(*args)
        times.append(time.perf_counter() - t0)
    median_t = statistics.median(times)
    
    print(f" Median : {median_t:.4f}s " f"( min ={ min( times ):.4f}, max ={ max( times ):.4f})")
    return median_t, result


def compute_mandelbrot(x_space, y_space, resolution, max_iterations):
    """
    Docstring for compute_mandelbrot
    
    :param x_space: Describes the range of the real axis (e.g., [-2.0, 1.0])
    :param y_space: Describes the range of the imaginary axis (e.g., [-1.5, 1.5])
    :param resolution: Number of points along each axis (e.g., 1000)

    Description:
    - Creates a grid of complex numbers representing the points in the complex plane
    - For each point in the grid, it calls mandelbrot_point to determine the iteration count
    - Returns a 2D array of iteration counts corresponding to each point in the grid
    """

    # Create a grid of complex numbers representing the points in the complex plane
    x = np.linspace(x_space[0], x_space[1], resolution) # Real axis values
    y = np.linspace(y_space[0], y_space[1], resolution) # Imaginary axis values
    X, Y = np.meshgrid(x, y)

    complex_grid = X + 1j * Y # Create a grid of complex numbers from [0,0] to [resolution-1,resolution-1]

    # Initialize a 2D array to store the iteration counts
    iteration_counts = np.zeros(complex_grid.shape, dtype=int)
    Z = np.zeros_like(complex_grid) # Initialize Z to be the same shape as complex_grid

    #replace the nested loops with vectorized operations
    for iteration in range(max_iterations):
        mask = np.abs(Z) <= 2 # create a mask for points that have not escaped. This is a bool mask.
        Z[mask] = Z[mask]**2 + complex_grid[mask] # UPdate Z for points that have not escaped
        iteration_counts[mask] = iteration # update the iteration count for points that have not escaped

    return iteration_counts

def visualize_mandelbrot(iteration_counts, x_space, y_space):
    """
    Docstring for visualize_mandelbrot

    Description:
    - Takes the 2D array of iteration counts and visualizes it
    - Displays the resulting image of the Mandelbrot set
    """

    plt.imshow(iteration_counts, extent=(x_space[0], x_space[1], y_space[0], y_space[1]), cmap='hot')
    plt.colorbar()
    plt.title('Mandelbrot Set')
    plt.xlabel('Real Axis')
    plt.ylabel('Imaginary Axis')
    plt.show()

def runtime_scaling_test(x_space, y_space, max_iterations, test_space):
    """
    Docstring for runtime_scaling_test

    Description:
    - Tests the runtime of the compute_mandelbrot function for different resolutions
    - Plots the runtime against the resolution to analyze scaling behavior
    """

    runtimes = []
    for resolution in test_space:
        t, _ = benchmark(compute_mandelbrot, x_space, y_space, resolution, max_iterations)
        runtimes.append(t)

    #plot runtime against resolution
    plt.plot(test_space, runtimes, marker='o')
    plt.xlabel('Resolution (number of points along each axis)')
    plt.ylabel('Runtime (seconds)')
    plt.title('Runtime Scaling of Mandelbrot Set Computation')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    x_space = [-2.0, 1.0] # Real axis range
    y_space = [-1.5, 1.5] # Imaginary axis range
    resolution = 1024 # Number of points along each axis
    max_iterations = 100 # Maximum number of iterations to determine if a point escapes
    test_number = 1.5 + -0.2j # Example complex number for testing
    test_space = [256, 512, 1024, 2048, 4096] # Different resolutions to test

    #t , iteration_counts = benchmark(compute_mandelbrot, x_space, y_space, resolution, max_iterations)

    #iteration_counts = compute_mandelbrot(x_space, y_space, resolution, max_iterations)
    #print(f"Iteration counts array {iteration_counts}")

    # Visualize the Mandelbrot set
    #visualize_mandelbrot(iteration_counts, x_space, y_space)

    # Test runtime scaling
    runtime_scaling_test(x_space, y_space, max_iterations, test_space)