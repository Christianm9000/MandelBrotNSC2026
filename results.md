# cProfile Measurements
## cProfile Naive Solution
Thu Feb 26 14:15:34 2026    naive_profile.prof

         23877158 function calls in 7.985 seconds

   Ordered by: cumulative time
   List reduced from 40 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    7.985    7.985 {built-in method builtins.exec}
        1    0.002    0.002    7.985    7.985 <string>:1(<module>)
        1    0.496    0.496    7.983    7.983 C:\Users\chris\Documents\AVS\8sem\NumericalScientificComputing\Mandelbrot\mandelbrot_naive.py:42(compute_mandelbrot_naive)
  1048576    6.290    0.000    7.485    0.000 C:\Users\chris\Documents\AVS\8sem\NumericalScientificComputing\Mandelbrot\mandelbrot_naive.py:24(mandelbrot_point)
 22828510    1.194    0.000    1.194    0.000 {built-in method builtins.abs}
        1    0.000    0.000    0.003    0.003 C:\Users\chris\miniforge3\envs\nsc2026\Lib\site-packages\numpy\lib\_function_base_impl.py:5134(meshgrid)
        3    0.000    0.000    0.003    0.001 C:\Users\chris\miniforge3\envs\nsc2026\Lib\site-packages\numpy\lib\_function_base_impl.py:5280(<genexpr>)
        2    0.003    0.001    0.003    0.001 {method 'copy' of 'numpy.ndarray' objects}
        2    0.000    0.000    0.000    0.000 C:\Users\chris\miniforge3\envs\nsc2026\Lib\site-packages\numpy\_core\function_base.py:26(linspace)
        1    0.000    0.000    0.000    0.000 C:\Users\chris\miniforge3\envs\nsc2026\Lib\site-packages\numpy\lib\_stride_tricks_impl.py:481(broadcast_arrays)

## cProfile Vectorized Solution
Thu Feb 26 14:15:35 2026    vectorized_profile.prof

         77 function calls in 0.983 seconds
   Ordered by: cumulative time
   List reduced from 42 to 10 due to restriction <10>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.983    0.983 {built-in method builtins.exec}
        1    0.002    0.002    0.983    0.983 <string>:1(<module>)
        1    0.975    0.975    0.981    0.981 C:\Users\chris\Documents\AVS\8sem\NumericalScientificComputing\Mandelbrot\mandelbrot_vectorized.py:24(compute_mandelbrot_vectorized)
        1    0.003    0.003    0.003    0.003 C:\Users\chris\miniforge3\envs\nsc2026\Lib\site-packages\numpy\_core\numeric.py:98(zeros_like)
        1    0.000    0.000    0.003    0.003 C:\Users\chris\miniforge3\envs\nsc2026\Lib\site-packages\numpy\lib\_function_base_impl.py:5134(meshgrid)
        3    0.000    0.000    0.003    0.001 C:\Users\chris\miniforge3\envs\nsc2026\Lib\site-packages\numpy\lib\_function_base_impl.py:5280(<genexpr>)
        2    0.002    0.001    0.002    0.001 {method 'copy' of 'numpy.ndarray' objects}
        2    0.000    0.000    0.000    0.000 C:\Users\chris\miniforge3\envs\nsc2026\Lib\site-packages\numpy\_core\function_base.py:26(linspace)
        1    0.000    0.000    0.000    0.000 C:\Users\chris\miniforge3\envs\nsc2026\Lib\site-packages\numpy\lib\_stride_tricks_impl.py:481(broadcast_arrays)
        1    0.000    0.000    0.000    0.000 C:\Users\chris\miniforge3\envs\nsc2026\Lib\site-packages\numpy\lib\_stride_tricks_impl.py:546(<listcomp>)

## Questions regarding cProfile
**Which function takes most total time:**
For the naive method, the 2 functions that dominated in terms of time was the builtin.abs function when evaluating each point at for the threshold (1.194s), and the 'mandelbrot_point' computing function, which dominated with 6.290s.

In the vectorized/Numpy implementation, it was pretty much only the vectorized computations that contributed to the total time, specifically 'compute_mandelbrot_vectorized' with 0.975s out of the 0.983s.

**Are there functions called surprisingly many times:**
There weren't any suprising results for the vectorized/numpy implementation, most calls were not in the top 10 time contributors. However, the naive implementation had significantly many more calls; the mandelbrot_point function was called 1048576 times, and the builtin.abs function was called 22828510 times.

**How does the Numpy compare to the naive:**
The Numpy implementation is way faster than the naive one, and performs way less function calls which probably also eliminates some overhead.