import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


def escape_count(c, max_iter=1000):
    """
    Compute Mandelbrot escape counts for a complex grid c.

    Parameters
    ----------
    c : np.ndarray
        2D array of complex128 values.
    max_iter : int
        Maximum number of iterations.

    Returns
    -------
    counts : np.ndarray
        2D array of escape iterations. Pixels that do not escape
        before max_iter keep the value max_iter.
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


def mandelbrot_sensitivity_map(n=512, max_iter=1000, x_min=-0.7530, x_max=-0.7490, y_min=0.0990, y_max=0.1030):
    """
    Compute the MP3 M2 sensitivity / condition-number approximation map.

    Returns
    -------
    kappa : np.ndarray
        Condition-number approximation map.
    n_base : np.ndarray
        Escape-count map for the unperturbed grid.
    extent : list
        Plot extent for imshow.
    """
    x = np.linspace(x_min, x_max, n, dtype=np.float64)
    y = np.linspace(y_min, y_max, n, dtype=np.float64)

    c = (x[np.newaxis, :] + 1j * y[:, np.newaxis]).astype(np.complex128)

    eps32 = float(np.finfo(np.float32).eps)

    # Slide 40 example uses delta = max(eps32 * |c|, 1e-10)
    delta = np.maximum(eps32 * np.abs(c), 1e-10)

    n_base = escape_count(c, max_iter).astype(np.float64)
    n_perturb = escape_count(c + delta, max_iter).astype(np.float64)

    dn = np.abs(n_base - n_perturb)

    # Use NaN where n(c) = 0, per slide instructions
    kappa = np.where(n_base > 0, dn / (eps32 * n_base), np.nan)

    extent = [x_min, x_max, y_min, y_max]
    return kappa, n_base, extent


if __name__ == "__main__":
    N = 512
    MAX_ITER = 1000

    X_MIN, X_MAX = -0.7530, -0.7490
    Y_MIN, Y_MAX = 0.0990, 0.1030

    kappa, escape_map, extent = mandelbrot_sensitivity_map(n=N, max_iter=MAX_ITER, x_min=X_MIN, x_max=X_MAX, y_min=Y_MIN, y_max=Y_MAX)

    cmap_k = plt.cm.hot.copy()
    cmap_k.set_bad("0.25")  # grey for NaN, as requested

    vmax = np.nanpercentile(kappa, 99)

    plt.figure(figsize=(8, 6))
    plt.imshow(
        kappa,
        cmap=cmap_k,
        origin="lower",
        extent=extent,
        norm=LogNorm(vmin=1, vmax=vmax),
    )
    plt.colorbar(label=r'$\kappa(c)$ (log scale, $\kappa \geq 1$)')
    plt.title(r'Condition number approx $\kappa(c)=|\Delta n|/(\varepsilon_{32} n(c))$')
    plt.xlabel("Re(c)")
    plt.ylabel("Im(c)")
    plt.tight_layout()
    plt.show()

    # Optional comparison plot: escape-count map
    plt.figure(figsize=(8, 6))
    plt.imshow(escape_map, cmap="magma", origin="lower", extent=extent)
    plt.colorbar(label="Escape iteration")
    plt.title("Escape-count map")
    plt.xlabel("Re(c)")
    plt.ylabel("Im(c)")
    plt.tight_layout()
    plt.show()