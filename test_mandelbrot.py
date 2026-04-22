import numpy as np
import pytest

import Workshop2.mandelbrot_mp as mandelbrot_mp
import Workshop1.mandelbrot_naive as mandelbrot_naive
import Workshop1.mandelbrot_numba as mandelbrot_numba


KNOWN_POINT_CASES = [
    pytest.param(0 + 0j, 25, 25, id='origin_stays_bounded'),
    pytest.param(5 + 0j, 25, 1, id='far_outside_right_escapes_immediately'),
    pytest.param(-2.5 + 0j, 25, 1, id='far_outside_left_escapes_immediately'),
    pytest.param(0 + 2j, 25, 2, id='hits_radius_two_then_escapes_next_step'),
]


@pytest.mark.parametrize('c, max_iter, expected', KNOWN_POINT_CASES)
def test_naive_point_known_values(c: complex, max_iter: int, expected: int) -> None:
    assert mandelbrot_naive.mandelbrot_point(c, max_iter) == expected


@pytest.mark.parametrize('c, max_iter, expected', KNOWN_POINT_CASES)
def test_numba_point_known_values(c: complex, max_iter: int, expected: int) -> None:
    assert mandelbrot_numba.mandelbrot_point(c, max_iter) == expected


def test_numba_grid_matches_naive_on_small_float64_grid() -> None:
    x_space = (-2.0, 1.0)
    y_space = (-1.5, 1.5)
    resolution = 16
    max_iter = 25

    naive_grid = mandelbrot_naive.compute_mandelbrot_naive(
        x_space, y_space, resolution, max_iter
    )
    numba_grid = mandelbrot_numba.compute_mandelbrot_naive(
        x_space, y_space, resolution, max_iter, np.float64
    )

    np.testing.assert_array_equal(numba_grid, naive_grid)


def test_multiprocessing_parallel_matches_serial_on_small_grid() -> None:
    resolution = 16
    x_min, x_max = -2.0, 1.0
    y_min, y_max = -1.5, 1.5
    max_iter = 25

    serial_grid = mandelbrot_mp.mandelbrot_serial(
        resolution, x_min, x_max, y_min, y_max, max_iter
    )
    parallel_grid = mandelbrot_mp.mandelbrot_parallel(
        resolution,
        x_min,
        x_max,
        y_min,
        y_max,
        max_iter=max_iter,
        n_workers=2,
        n_chunks=4,
    )

    np.testing.assert_array_equal(parallel_grid, serial_grid)


def test_build_chunks_covers_all_rows_once() -> None:
    chunks = mandelbrot_mp.build_chunks(10, -2.0, 1.0, -1.5, 1.5, 25, n_chunks=3)
    covered_rows = []
    for row_start, row_end, *_ in chunks:
        covered_rows.extend(range(row_start, row_end))

    assert covered_rows == list(range(10))
