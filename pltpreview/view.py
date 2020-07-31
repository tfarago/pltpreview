"""Convenience functions for matplotlib plotting and image viewing."""
import collections
import numpy as np
from matplotlib import pyplot as plt


def show(image, block=False, title='', **kwargs):
    """Show *image*. If *block* is False the call is nonblocking. *title* is the image title.
    *kwargs* are passed to matplotlib's ``imshow`` function. This command always creates a new
    figure. Returns matplotlib's ``AxesImage``.
    *image* can have physical units in which case it must contain attribute *magnitude* and *units*.
    If it does, image is stripped off units and passed to matplotlib and units are shown as x label.
    You can specify a keyword argument *clim* which can be either 'auto', a number or a tuple. If it
    is 'auto' then the first and last 0.1 percent of the values are trimmed from the displayed
    image, which is useful when the object of interest has narrow dynamic range in comparison to the
    overall image. If it is a number you specify the percentile yourself. It it is a tuple it means
    you specify the minimum and maximum yourself.
    """
    xlabel = ''
    if hasattr(image, 'magnitude'):
        xlabel = str(image.units)
        image = image.magnitude
    clim = kwargs.pop('clim', None)
    if not (clim is None or isinstance(clim, tuple)):
        # Use 0.1 % for *auto* mode
        percentile = clim if clim != 'auto' else .1
        hist, bins = np.histogram(image, bins=256)
        cumsum = np.cumsum(hist) / float(np.sum(hist)) * 100
        valid = bins[np.where((cumsum > percentile) & (cumsum < 100 - percentile))]
        clim = (valid[0], valid[-1])
    kwargs['clim'] = clim

    plt.figure()
    mpl_image = plt.imshow(image, **kwargs)
    mpl_image.axes.format_coord = _FormatCoord(image)
    mn = np.nanmin(image)
    mx = np.nanmax(image)
    if mx - mn > np.finfo(np.float).eps:
        orientation = 'horizontal' if image.shape[1] / 2 > image.shape[0] else 'vertical'
        plt.colorbar(ticks=np.linspace(mn, mx, 8), orientation=orientation)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.show(block)

    return mpl_image


def plot(*args, **kwargs):
    """Plot using matplotlib's ``plot`` function. Pass it *args* and *kwargs*.  *kwargs* are
    infected with *block* and if False or not specified, the call is nonblocking. *title* is alowed
    to be in *kwargs* which sets the figure title. *grid* can be in kwargs which is a boolean
    turning the grid on or off. *xlabel* and *ylabel* define the x and y axes labels if specified in
    *kwargs*. This command always creates a new figure. Returns a list of ``Line2D`` instances.
    """
    block = kwargs.pop('block', False)
    title = kwargs.pop('title', '')
    xlabel = kwargs.pop('xlabel', '')
    ylabel = kwargs.pop('ylabel', '')
    grid = kwargs.pop('grid', True)

    plt.figure()
    lines = plt.plot(*args, **kwargs)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(grid)
    plt.show(block)

    return lines


class _FormatCoord(object):
    """Coordinates formatter."""
    def __init__(self, image):
        self.image = image
        self.shape = self.image.shape
        self.value_fmt = determine_intensity_format(self.image[0, 0])

    def __call__(self, x, y):
        """Overrides matplotlib's default behavior on mouse motion,
        *x* and *y* are planar coordinates.
        """
        col = int(x + 0.5)
        row = int(y + 0.5)

        if (col >= 0 and col < self.image.shape[1] and
                row >= 0 and row < self.image.shape[0]):
            # The formatting doesn't like np.float32
            if self.image.ndim == 2:
                value = (float(self.image[row, col]),)
            else:
                value = self.image[row, col]
            value_str = self.value_fmt.format(*value)
            return 'x={:<12.2f}y={:<12.2f}{}'.format(x, y, value_str)
        else:
            return 'x={:<12.2f}y={:<12.2f}'.format(x, y)


def determine_intensity_format(number):
    """Get format string based on *number*'s data type."""
    if isinstance(number, collections.Iterable):
        fmt = 'RGB={:>03},{:>03},{:>03}'
    elif isinstance(number, (float, np.float, np.float16, np.float32,
                             np.float64, np.float128)):
        fmt = 'I={:<12.5f}'
    else:
        fmt = 'I={:<12}'

    return fmt
