"""Mandelbrot set implementations accelerated with Numba.

Author: Christian Mariager
Course: Numerical Scientific Computing 2026
"""

from __future__ import annotations

from typing import Sequence

import matplotlib.pyplot as plt
import numpy as np
from numba import njit, prange


@njit()
def mandelbrot_point(complex_input: complex, max_iterations: int = 1000) -> int:
    """Compute the Mandelbrot escape iteration count for one complex point.

    Parameters
    ----------
    complex_input : complex
        Complex coordinate ``c`` in the recurrence ``z[n+1] = z[n]**2 + c``.
    max_iterations : int, default=1000
        Maximum number of iterations to evaluate before treating the point as
        non-escaping within the iteration budget.

    Returns
    -------
    int
        Iteration index at which the orbit first satisfies ``|z| > 2``.
        Returns ``max_iterations`` if the point does not escape within the
        allotted iterations.
    """
    z_0 = 0.0 + 0.0j

    for iteration in range(max_iterations):
        if z_0.real**2 + z_0.imag**2 > 4.0:
            return iteration
        z_0 = z_0**2 + complex_input

    return max_iterations


@njit(parallel=True, fastmath=True)
def compute_mandelbrot_naive(
    x_space: Sequence[float],
    y_space: Sequence[float],
    resolution: int,
    max_iterations: int,
    prec_type,
) -> np.ndarray:
    """Compute a Mandelbrot escape-count grid using Numba-parallel loops.

    Parameters
    ----------
    x_space : Sequence[float]
        Two-element sequence ``[x_min, x_max]`` defining the real-axis span.
    y_space : Sequence[float]
        Two-element sequence ``[y_min, y_max]`` defining the imaginary-axis
        span.
    resolution : int
        Number of sample points along each axis. The returned array has shape
        ``(resolution, resolution)``.
    max_iterations : int
        Maximum number of iterations used for each point.
    prec_type : type
        NumPy floating-point dtype used when constructing the coordinate axes,
        for example ``np.float32`` or ``np.float64``.

    Returns
    -------
    numpy.ndarray
        Two-dimensional integer array of escape iteration counts for the sampled
        complex grid.
    """
    x = np.linspace(x_space[0], x_space[1], resolution).astype(prec_type)
    y = np.linspace(y_space[0], y_space[1], resolution).astype(prec_type)

    iteration_counts = np.zeros((resolution, resolution), dtype=np.int32)

    for i in prange(resolution):
        yi = y[i]
        for j in prange(resolution):
            complex_input = x[j] + 1j * yi
            iteration_count = mandelbrot_point(complex_input, max_iterations)
            iteration_counts[i, j] = iteration_count

    return iteration_counts


def visualize_mandelbrot_side_by_side(
    iteration_counts: list[np.ndarray],
    x_space: Sequence[float],
    y_space: Sequence[float],
) -> None:
    """Display multiple Mandelbrot escape-count grids side by side.

    Parameters
    ----------
    iteration_counts : list[numpy.ndarray]
        List of two-dimensional escape-count arrays to visualize.
    x_space : Sequence[float]
        Two-element sequence ``[x_min, x_max]`` used for the horizontal plot
        extent.
    y_space : Sequence[float]
        Two-element sequence ``[y_min, y_max]`` used for the vertical plot
        extent.

    Returns
    -------
    None
        This function shows a Matplotlib figure and does not return a value.
    """
    for i, counts in enumerate(iteration_counts):
        plt.subplot(1, len(iteration_counts), i + 1)
        plt.imshow(
            counts,
            extent=(x_space[0], x_space[1], y_space[0], y_space[1]),
            cmap="hot",
        )
        plt.colorbar()
        if i == 0:
            plt.title("Mandelbrot Set (float32)")
        else:
            plt.title("Mandelbrot Set (float64)")
    plt.show()


if __name__ == "__main__":
    x_space = [-2.0, 1.0]
    y_space = [-1.5, 1.5]
    resolution = 1024
    max_iterations = 100
    prec = np.float32

    _ = compute_mandelbrot_naive(
        x_space,
        y_space,
        resolution,
        max_iterations,
        prec_type=prec,
    )

    iteration_list: list[np.ndarray] = []

    for prec in [np.float32, np.float64]:
        print(f"Running with precision: {prec}")
        if prec == np.float64:
            _ = compute_mandelbrot_naive(
                x_space,
                y_space,
                resolution,
                max_iterations,
                prec_type=prec,
            )

        iteration_counts = compute_mandelbrot_naive(
            x_space,
            y_space,
            resolution,
            max_iterations,
            prec_type=prec,
        )
        iteration_list.append(iteration_counts)

    visualize_mandelbrot_side_by_side(iteration_list, x_space, y_space)
