UNMAP
======

Extracts arrays of values from colormapped figures.

### Usage

#### From Command Line
    unmap [FILE]
* click ends of color bar

#### From Python
    import unmap as um
    img = um.imread('figure.png')
    arr = um.unmap(img)
