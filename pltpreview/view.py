"""Convenience functions for matplotlib plotting and image viewing."""
import numpy as np
from matplotlib import pyplot as plt


def show(image, block=False, title='', **kwargs):
    """Show *image*. If *block* is False the call is nonblocking. *title*
    is the image title.  *kwargs* are passed to matplotlib's ``imshow``
    function. This command always creates a new figure. Returns matplotlib's
    ``AxesImage``.
    """
    plt.figure()
    mpl_image = plt.imshow(image, **kwargs)
    plt.colorbar(ticks=np.linspace(image.min(), image.max(), 8))
    plt.title(title)
    plt.show(block)

    return mpl_image


def plot(*args, **kwargs):
    """Plot using matplotlib's ``plot`` function. Pass it *args* and *kwargs*.
    *kwargs* are infected with *block* and if False or not specified,
    the call is nonblocking. *title* is also alowed to be in *kwargs* which
    sets the figure title. This command always creates a new figure. Returns
    a list of ``Line2D`` instances.
    """
    block = kwargs.pop('block', False)
    title = kwargs.pop('title', '')

    plt.figure()
    lines = plt.plot(*args, **kwargs)
    plt.title(title)
    plt.show(block)

    return lines
