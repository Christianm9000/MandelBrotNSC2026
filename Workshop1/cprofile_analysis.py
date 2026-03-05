import cProfile, pstats
from mandelbrot_naive import compute_mandelbrot_naive
from mandelbrot_vectorized import compute_mandelbrot_vectorized

cProfile.run('compute_mandelbrot_naive([-2.0, 1.0], [-1.5, 1.5], 1024, 100)', 'naive_profile.prof')
cProfile.run('compute_mandelbrot_vectorized([-2.0, 1.0], [-1.5, 1.5], 1024, 100)', 'vectorized_profile.prof')

if __name__ == "__main__":
    x_space = [-2.0, 1.0]
    y_space = [-1.5, 1.5]
    resolution = 1024
    max_iterations = 100 # Maximum number of iterations to determine if a point escapes

    for name in ('naive_profile.prof', 'vectorized_profile.prof'):
        stats = pstats.Stats(name)
        stats.sort_stats('cumulative')
        stats.print_stats(10)