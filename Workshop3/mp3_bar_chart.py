import matplotlib.pyplot as plt


if __name__ == "__main__":
    implementations1024 = ["Naïve", "Vectorized",  "NJIT", "Multiprocessing", "Dask Local", "Dask Distributed", "OpenCL float32"]
    runtime1024 = [4.0889, 0.9811, 0.0620, 0.0145, 0.0780, 0.0765, 0.0037]

    bar = plt.bar(implementations1024, runtime1024)
    plt.title("Performance Comparison")
    plt.xlabel("Implementations")
    plt.ylabel("Logarithmic runtime [s]")
    plt.yscale("log")
    plt.bar_label(bar, fmt='%.4f')
    plt.show()