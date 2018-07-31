#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import scipy.ndimage
try:
    import Tkinter as tk
    from tkSimpleDialog import askfloat as tkaskfloat
except:
    import tkinter as tk
    from tkinter.simpledialog import askfloat as tkaskfloat

def getFloat(prompt, title, default=None):
    root = tk.Tk()
    root.withdraw()
    ret = tkaskfloat(title, prompt, parent=root, initialvalue=default)
    root.destroy()
    return ret

def onclick(event):
    global _coords, _cbarvals, _fig, _cid
    ix, iy = event.xdata, event.ydata
    _coords.append((ix,iy))
    plt.scatter([ix], [iy], c=img[int(iy),int(ix),:]/256.0)
    _fig.canvas.draw()
    val = getFloat('Value', 'Enter value', float(len(_cbarvals)))
    _cbarvals.append(val)
    if len(_coords) == 2:
        _fig.canvas.mpl_disconnect(_cid)
        plt.close(_fig)
    return _coords

def get_rgb(img):
    # Interactively choose ends of colorbar
    global _coords, _cbarvals, _fig, _cid
    _coords = []
    _cbarvals = []
    _fig = plt.figure(1)
    ax1 = _fig.add_subplot(111)
    ax1.imshow(img)
    plt.title('Click to select the ends of the colorbar')
    _cid = _fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show(1)

    # Make transect of interpolation points from pt1 to pt2
    pt1, pt2 = _coords
    r = np.sqrt((pt1[0]-pt2[0])**2 + (pt1[1] - pt2[1])**2)
    xs = np.linspace(pt1[0], pt2[0], r)
    ys = np.linspace(pt1[1], pt2[1], r)

    R = scipy.ndimage.map_coordinates(img[:,:,0], np.stack((ys, xs)))
    G = scipy.ndimage.map_coordinates(img[:,:,1], np.stack((ys, xs)))
    B = scipy.ndimage.map_coordinates(img[:,:,2], np.stack((ys, xs)))

    return np.array((R,G,B)).T, _cbarvals[0], _cbarvals[1]

def unmap(img, rgb=None, minv=None, maxv=None):
    '''
        img is an image of shape [n, m, 3], and rgb is a colormap of shape [k, 3].
            Note: If rgb is omitted, then the user will be prompted to pick the ends of the colorbar
            in the figure.
        minv and maxv are the values of the ends of the colormap (default: [0, 1])
    '''
    if rgb is None:
        rgb, minv, maxv = get_rgb(img)
    elif not minv or not maxv:
        minv = 0.0
        maxv = 1.0

    # Load image with additional axis for euclidian distance
    A = img[np.newaxis, ...].astype(float)
    # Reshape colormap to match A
    B = rgb[:, np.newaxis, np.newaxis, :].astype(float)
    # Calculate Euclidian distance from each pixel to each cmap value
    norm = np.linalg.norm(A-B, axis=-1)
    # Normalize
    values = np.argmin(norm, axis=0) / float(rgb.shape[0] - 1.0)
    
    return values*(maxv-minv)+minv

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Convert a colormapped figure to its raw values.')
    parser.add_argument('-o', '--outfile', type=argparse.FileType('w'), help='Write xyz values to file.')
    parser.add_argument('infile', help='Image to process.')
    args = parser.parse_args()

    img = plt.imread(args.infile)[:,:,:3]
    values = unmap(img)

    if args.outfile:
        np.savetxt(args.outfile, values)

    plt.figure()
    plt.imshow(values)
    plt.colorbar()

    plt.figure()
    plt.imshow(img)

    #plt.figure()
    #xx = np.linspace(0,1,rgb.shape[0])
    #plt.plot(xx, rgb[:,0]/float(rgb.ptp()), 'r', linewidth=2)
    #plt.plot(xx, rgb[:,1]/float(rgb.ptp()), 'g', linewidth=2)
    #plt.plot(xx, rgb[:,2]/float(rgb.ptp()), 'b', linewidth=2)
    #plt.xlim((-0.01, 1.01))
    #plt.ylim((-0.01, 1.01))
    #plt.title('Color map')
    #plt.ylabel('Intensity')
    #plt.xlabel('Value')

    plt.show()
