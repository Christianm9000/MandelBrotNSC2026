# Lecture 2, Milestone 3: Memory Access Patterns

import statistics

import numpy as np
import time

def compute_rows(A):
    """Compute the sum of each row in A."""
    for i in range(n): s = np.sum(A[i, :])

    return s

def compute_cols(A):
    """Compute the sum of each column in A."""
    for j in range(n): s = np.sum(A[:, j])

    return s

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

if __name__ == "__main__":
    #initialize variables
    n = 10000

    #Large Square array
    A = np.random.rand(n, n)

    #Fortran
    A_f = np.asfortranarray(A)

    #Time different access pattenrs
    print("row access (A):")
    benchmark(compute_rows, A)

    print("column access (A):")
    benchmark(compute_cols, A)

    print("row access (A_f):")
    benchmark(compute_rows, A_f)

    print("column access (A_f):")
    benchmark(compute_cols, A_f)


"""
Results:

row access (A):
 Median : 0.1184s ( min =0.1160, max =0.1378)
column access (A):
 Median : 1.1256s ( min =1.0935, max =1.1451)
row access (A_f):
 Median : 1.0866s ( min =1.0839, max =1.1318)
column access (A_f):
 Median : 0.1216s ( min =0.1183, max =0.1333)
"""