UNMAP
======

Extracts arrays of values from colormapped figures.

### Usage

#### Interactive GUI
    usage: unmap [-h] [-o OUTFILE] infile

    positional arguments:
      infile                Image to process.

    optional arguments:
      -h, --help            show this help message and exit
      -o, --outfile OUTFILE Write xyz values to file.

    * Select ends of color bar with mouse

#### From Python
    import unmap as um
    img = um.plt.imread('figure.png')
    arr = um.unmap(img)

### Dependencies
    * Python (>= 2.7)
    * Matplotlib
    * Numpy
    * Scipy

![Unmapped figure example](unmapped_example.png?raw=true "Unmapped figure")
Adapted from [Gao et al., “Crust and Lithosphere Structure of the Northwestern U.S. with Ambient Noise Tomography.”](https://www.sciencedirect.com/science/article/pii/S0012821X11000598)
