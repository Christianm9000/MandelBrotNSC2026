# Test imports and print versions of various libraries
import numpy
import matplotlib
import scipy
import numba
import pytest
import dask

print("NumPy version:", numpy.__version__)
print("Matplotlib version:", matplotlib.__version__)
print("SciPy version:", scipy.__version__)
print("Numba version:", numba.__version__)
print("Pytest version:", pytest.__version__)
print("Dask version:", dask.__version__)