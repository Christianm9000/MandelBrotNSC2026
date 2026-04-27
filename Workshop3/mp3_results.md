# MP3
## M1: Mandelbrot Set Trajectory Divergence
**What fraction of pixels diverge before max_iter?**
Fraction of pixels diverged before max_iter (1000), tau=0.01: 1.0000

**Observations**
It seems that the trajectories diverge early in the regions where the escape-count map shows lower escape counts. This usually happens in the non-structured regions of the Mandelbrot set, where the points are closer to the boundary of the set. The divergence map highlights these areas, showing that the trajectories diverge more quickly in these regions compared to areas with higher escape counts.

## M2: Mandelbrot Sensitivity Map
**Obserations**


## L09: M1: Test Suite Results
**Test Results**
```bash
(nsc2026) C:\Users\chris\Documents\AVS\8sem\NumericalScientificComputing\Mandelbrot>pytest -v
================================================================= test session starts ==================================================================
platform win32 -- Python 3.11.14, pytest-9.0.2, pluggy-1.6.0 -- C:\Users\chris\miniforge3\envs\nsc2026\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\chris\Documents\AVS\8sem\NumericalScientificComputing\Mandelbrot
plugins: cov-7.1.0
collected 11 items                                                                                                                                      

test_mandelbrot.py::test_naive_point_known_values[origin_stays_bounded] PASSED                                                                    [  9%]
test_mandelbrot.py::test_naive_point_known_values[far_outside_right_escapes_immediately] PASSED                                                   [ 18%]
test_mandelbrot.py::test_naive_point_known_values[far_outside_left_escapes_immediately] PASSED                                                    [ 27%]
test_mandelbrot.py::test_naive_point_known_values[hits_radius_two_then_escapes_next_step] PASSED                                                  [ 36%]
test_mandelbrot.py::test_numba_point_known_values[origin_stays_bounded] PASSED                                                                    [ 45%]
test_mandelbrot.py::test_numba_point_known_values[far_outside_right_escapes_immediately] PASSED                                                   [ 54%]
test_mandelbrot.py::test_numba_point_known_values[far_outside_left_escapes_immediately] PASSED                                                    [ 63%]
test_mandelbrot.py::test_numba_point_known_values[hits_radius_two_then_escapes_next_step] PASSED                                                  [ 72%]
test_mandelbrot.py::test_numba_grid_matches_naive_on_small_float64_grid PASSED                                                                    [ 81%]
test_mandelbrot.py::test_multiprocessing_parallel_matches_serial_on_small_grid PASSED                                                             [ 90%]
test_mandelbrot.py::test_build_chunks_covers_all_rows_once PASSED                                                                                 [100%]

================================================================== 11 passed in 9.98s ==================================================================
```

```bash
(nsc2026) C:\Users\chris\Documents\AVS\8sem\NumericalScientificComputing\Mandelbrot>pytest --cov=. -v
================================================================================= test session starts ==================================================================================
platform win32 -- Python 3.11.14, pytest-9.0.2, pluggy-1.6.0 -- C:\Users\chris\miniforge3\envs\nsc2026\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\chris\Documents\AVS\8sem\NumericalScientificComputing\Mandelbrot
plugins: cov-7.1.0
collected 11 items                                                                                                                                                                      

test_mandelbrot.py::test_naive_point_known_values[origin_stays_bounded] PASSED                                                                                                    [  9%]
test_mandelbrot.py::test_naive_point_known_values[far_outside_right_escapes_immediately] PASSED                                                                                   [ 18%]
test_mandelbrot.py::test_naive_point_known_values[far_outside_left_escapes_immediately] PASSED                                                                                    [ 27%]
test_mandelbrot.py::test_naive_point_known_values[hits_radius_two_then_escapes_next_step] PASSED                                                                                  [ 36%]
test_mandelbrot.py::test_numba_point_known_values[origin_stays_bounded] PASSED                                                                                                    [ 45%]
test_mandelbrot.py::test_numba_point_known_values[far_outside_right_escapes_immediately] PASSED                                                                                   [ 54%]
test_mandelbrot.py::test_numba_point_known_values[far_outside_left_escapes_immediately] PASSED                                                                                    [ 63%]
test_mandelbrot.py::test_numba_point_known_values[hits_radius_two_then_escapes_next_step] PASSED                                                                                  [ 72%]
test_mandelbrot.py::test_numba_grid_matches_naive_on_small_float64_grid PASSED                                                                                                    [ 81%]
test_mandelbrot.py::test_multiprocessing_parallel_matches_serial_on_small_grid PASSED                                                                                             [ 90%]
test_mandelbrot.py::test_build_chunks_covers_all_rows_once PASSED                                                                                                                 [100%]

========================================================================== tests coverage ==========================================================================
___________________________________________________________________ coverage: platform win32, python 3.11.14-final-0 ___________________________________________________________________

Name                       Stmts   Miss  Cover
----------------------------------------------
Workshop1\test_script.py      12      0   100%
Workshop2\test_dask.py         9      6    33%
conftest.py                   17      3    82%
mandelbrot_mp.py              90     58    36%
mandelbrot_naive.py           48     19    60%
mandelbrot_numba.py           51     41    20%
test_mandelbrot.py            34      0   100%
----------------------------------------------
TOTAL                        261    127    51%
==================================================================== 11 passed in 8.10s =================================================================
```

## L10: M1: Mandelbrot GPU Implementation
**Timing Results**
```bash
GPU 1024x1024: 3.7 ms
GPU 2048x2048: 6.3 ms
```

A corresponding mandelbrot_gpu_m1.png image is saved.