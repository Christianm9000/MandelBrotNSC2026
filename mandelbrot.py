"""
Mandelbrot Set Generator
Author : Christian Mariager
Course : Numerical Scientific Computing 2026
"""

import numpy as np

def mandelbrot_point(complex_input: complex, max_iterations: int = 1000):
    """
    Docstring for mandelbrot_point

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

def compute_mandelbrot(x_space, y_space, resolution):
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

    complex_grid = X + 1j * Y

    # Initialize a 2D array to store the iteration counts
    iteration_counts = np.zeros(complex_grid.shape, dtype=int)

    for i in range(resolution):
        for j in range(resolution):
            complex_input = complex_grid[i, j]
            iteration_count = mandelbrot_point(complex_input)

            # Store the iteration count in a 2D array
            iteration_counts[i, j] = iteration_count

    return iteration_counts


if __name__ == "__main__":
    x_space = [-2.0, 1.0] # Real axis range
    y_space = [-1.5, 1.5] # Imaginary axis range
    resolution = 5 # Number of points along each axis
    max_iterations = 1000 # Maximum number of iterations to determine if a point escapes

    test_number = 1.5 + -0.2j # Example complex number for testing
    print(f"Iteration count for {test_number}: {mandelbrot_point(test_number)}")

    print(compute_mandelbrot(x_space, y_space, resolution))