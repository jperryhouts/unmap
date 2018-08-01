#!/usr/bin/env python

'''
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import matplotlib.pyplot as plt
import numpy as np
try:
    # Python 2.x
    import Tkinter as tk
    from tkSimpleDialog import askfloat as tkaskfloat
except:
    # Python 3.x
    import tkinter as tk
    from tkinter.simpledialog import askfloat as tkaskfloat

def getFloat(prompt, title, default=None):
    # Simple tkinter dialog, returns a float.
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

def interp2D(img, x, y):
    '''
    Linear interpolate from regularly spaced grid.
    '''
    v0 = img[int(y),  int(x)]
    v1 = img[int(y),  int(x)+1]
    v2 = img[int(y)+1,int(x)]
    v3 = img[int(y)+1,int(x)+1]
    x0 = x-int(x)
    y0 = y-int(y)
    shp0 = (1.0-x0)*(1.0-y0)
    shp1 = (x0)*(1.0-y0)
    shp2 = (1.0-x0)*(y0)
    shp3 = (x0)*(y0)
    return sum([v0*shp0, v1*shp1, v2*shp2, v3*shp3])

def get_rgb(img):
    # Interactively choose colorbar, extract color profile from image
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

    R = [interp2D(img[:,:,0],x,y) for x,y in zip(xs,ys)]
    G = [interp2D(img[:,:,1],x,y) for x,y in zip(xs,ys)]
    B = [interp2D(img[:,:,2],x,y) for x,y in zip(xs,ys)]

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
