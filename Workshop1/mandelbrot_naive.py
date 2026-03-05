"""
Mandelbrot Set Generator
Author : Christian Mariager
Course : Numerical Scientific Computing 2026
"""

from line_profiler import profile
import statistics
import numpy as np
import time
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

@profile
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
        if abs(z_0) > 2:
            return iteration
        z_0 = z_0**2 + complex_input

    # Return the max iteartion count if the point does not escape
    return max_iterations

@profile
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
    X, Y = np.meshgrid(x, y)

    complex_grid = X + 1j * Y # Create a grid of complex numbers from [0,0] to [resolution-1,resolution-1]

    # Initialize a 2D array to store the iteration counts
    iteration_counts = np.zeros(complex_grid.shape, dtype=int)

    for i in range(resolution):
        for j in range(resolution):
            complex_input = complex_grid[i, j]
            iteration_count = mandelbrot_point(complex_input, max_iterations)

            # Store the iteration count in a 2D array
            iteration_counts[i, j] = iteration_count

    return iteration_counts

def visualize_mandelbrot(iteration_counts, x_space, y_space):
    """
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

if __name__ == "__main__":
    x_space = [-2.0, 1.0] # Real axis range
    y_space = [-1.5, 1.5] # Imaginary axis range
    resolution = 1024 # Number of points along each axis
    max_iterations = 100 # Maximum number of iterations to determine if a point escapes

    #test_number = 1.5 + -0.2j # Example complex number for testing
    #print(f"Iteration count for {test_number}: {mandelbrot_point(test_number, max_iterations)}")

    #start_time = time.time()
    iteration_counts = compute_mandelbrot_naive(x_space, y_space, resolution, max_iterations)
    #print(f"Iteration counts array {iteration_counts}")
    #end_time = time.time()
    #print(f"Computation time: {end_time - start_time} seconds")

    # Visualize the Mandelbrot set
    #visualize_mandelbrot(iteration_counts, x_space, y_space)