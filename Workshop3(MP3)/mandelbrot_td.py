import numpy as np
import matplotlib.pyplot as plt


def mandelbrot_trajectory_divergence(n=512, max_iter=1000, tau=0.01, x_min=-0.7530, x_max=-0.7490, y_min=0.0990, y_max=0.1030):
    """
    Compute the first iteration where float32 and float64 Mandelbrot
    trajectories diverge by more than tau.

    Parameters
    ----------
    n : int
        Grid resolution in each dimension.
    max_iter : int
        Maximum number of iterations.
    tau : float
        Divergence threshold.
    x_min, x_max, y_min, y_max : float
        Complex plane region bounds.

    Returns
    -------
    diverge_iter : np.ndarray
        2D array of shape (n, n), containing the first divergence iteration
        for each pixel. Pixels that never diverge keep the value max_iter.
    extent : list
        Plot extent for imshow.
    """
    # Build grid in float64 / complex128 first
    x = np.linspace(x_min, x_max, n, dtype=np.float64)
    y = np.linspace(y_min, y_max, n, dtype=np.float64)

    c64 = (x[np.newaxis, :] + 1j * y[:, np.newaxis]).astype(np.complex128)
    c32 = c64.astype(np.complex64)

    z64 = np.zeros_like(c64, dtype=np.complex128)
    z32 = np.zeros_like(c32, dtype=np.complex64)

    # Store first divergence iteration; default = max_iter if never diverged
    diverge_iter = np.full((n, n), max_iter, dtype=np.int32)

    # Track pixels that have not diverged yet
    active = np.ones((n, n), dtype=bool)

    for k in range(max_iter):
        if not active.any():
            break

        # Iterate only still-active pixels
        z32[active] = z32[active] * z32[active] + c32[active]
        z64[active] = z64[active] * z64[active] + c64[active]

        # Compare trajectories in float64 precision
        diff = (np.abs(z32.real.astype(np.float64) - z64.real) + np.abs(z32.imag.astype(np.float64) - z64.imag))

        newly_diverged = active & (diff > tau)
        diverge_iter[newly_diverged] = k
        active[newly_diverged] = False

    extent = [x_min, x_max, y_min, y_max]
    return diverge_iter, extent


def escape_count(c, max_iter=1000):
    """
    Standard Mandelbrot escape count for comparison plotting.
    """
    z = np.zeros_like(c, dtype=np.complex128)
    counts = np.full(c.shape, max_iter, dtype=np.int32)
    escaped = np.zeros(c.shape, dtype=bool)

    for k in range(max_iter):
        z[~escaped] = z[~escaped] * z[~escaped] + c[~escaped]
        newly_escaped = (~escaped) & (np.abs(z) > 2.0)
        counts[newly_escaped] = k
        escaped[newly_escaped] = True

    return counts


if __name__ == "__main__":
    N = 512
    MAX_ITER = 1000
    TAU = 0.01

    X_MIN, X_MAX = -0.7530, -0.7490
    Y_MIN, Y_MAX = 0.0990, 0.1030

    # Compute divergence map
    diverge_map, extent = mandelbrot_trajectory_divergence(n=N, max_iter=MAX_ITER, tau=TAU, x_min=X_MIN, x_max=X_MAX, y_min=Y_MIN, y_max=Y_MAX)

    # Optional: compute escape-count map for visual comparison
    x = np.linspace(X_MIN, X_MAX, N, dtype=np.float64)
    y = np.linspace(Y_MIN, Y_MAX, N, dtype=np.float64)
    c = (x[np.newaxis, :] + 1j * y[:, np.newaxis]).astype(np.complex128)
    escape_map = escape_count(c, MAX_ITER)

    # Fraction of pixels that diverged before max_iter
    diverged_fraction = np.mean(diverge_map < MAX_ITER)
    print(f"Fraction of pixels diverged before max_iter: {diverged_fraction:.4f}")

    # Plot divergence map
    plt.figure(figsize=(8, 6))
    plt.imshow(diverge_map, cmap="plasma", origin="lower", extent=extent)
    plt.colorbar(label="First divergence iteration")
    plt.title(f"Trajectory divergence (tau={TAU})")
    plt.xlabel("Re(c)")
    plt.ylabel("Im(c)")
    plt.tight_layout()
    plt.show()

    # Optional comparison: escape-count map
    plt.figure(figsize=(8, 6))
    plt.imshow(escape_map, cmap="magma", origin="lower", extent=extent)
    plt.colorbar(label="Escape iteration")
    plt.title("Escape-count map")
    plt.xlabel("Re(c)")
    plt.ylabel("Im(c)")
    plt.tight_layout()
    plt.show()