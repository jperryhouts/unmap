UNMAP
======

Extracts arrays of values from colormapped figures.

### Usage

#### Interactive GUI
    unmap [FILE]
* click ends of color bar

#### From Python
    import unmap as um
    img = um.imread('figure.png')
    arr = um.unmap(img)

![Unmapped figure example](unmapped_example.png?raw=true "Unmapped figure")
Adapted from [Gao et al., “Crust and Lithosphere Structure of the Northwestern U.S. with Ambient Noise Tomography.”](https://www.sciencedirect.com/science/article/pii/S0012821X11000598)
