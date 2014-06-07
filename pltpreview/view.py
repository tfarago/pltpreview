"""Convenience functions for matplotlib plotting and image viewing."""
import numpy as np
from matplotlib import pyplot as plt


def show(image, blocking=False, **kwargs):
    """Show *image*. If *blocking* is False the call is nonblocking.
    *kwargs* are passed to matplotlib's ``imshow`` function. This command
    always creates a new figure. Returns matplotlib's ``AxesImage``.
    """
    plt.figure()
    mpl_image = plt.imshow(image, **kwargs)
    plt.colorbar(ticks=np.linspace(image.min(), image.max(), 8))
    plt.show(blocking)

    return mpl_image


def plot(*args, **kwargs):
    """Plot using matplotlib's ``plot`` function. Pass it *args* and *kwargs*.
    *kwargs* are infected with *blocking* and if False or not specified,
    the call is nonblocking. This command always creates a new figure. Returns
    a list of ``Line2D`` instances.
    """
    blocking = False if 'blocking' not in kwargs else kwargs.pop('blocking')
    plt.figure()
    lines = plt.plot(*args, **kwargs)
    plt.show(blocking)

    return lines
