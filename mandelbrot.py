"""
Mandelbrot Set Generator
Author : Christian Mariager
Course : Numerical Scientific Computing 2026
"""

import numpy as np

def mandelbrot_point(complex_input: complex):
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

def compute_mandelbrot():
    pass

if __name__ == "__main__":
    x_space = [-2.0, 1.0] # Real axis range
    y_space = [-1.5, 1.5] # Imaginary axis range
    resolution = 1000 # Number of points along each axis
    max_iterations = 1000 # Maximum number of iterations to determine if a point escapes

    test_number = 1.5 + -0.2j # Example complex number for testing
    print(f"Iteration count for {test_number}: {mandelbrot_point(test_number)}")