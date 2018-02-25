#!/usr/local/bin/env python

from pylab import *
import sys
import scipy.ndimage, Tkinter, tkSimpleDialog

coords = []
cbarvals = []

def onclick(event):
    global ix, iy
    ix, iy = event.xdata, event.ydata
    global coords
    coords.append((ix,iy))
    scatter([ix], [iy], c=img[int(iy),int(ix),:]/256.0)
    fig.canvas.draw()
    global cbarvals
    root = Tkinter.Tk()
    cbarvals.append(float(tkSimpleDialog.askstring("Value", "Enter start value")))
    root.destroy()
    if len(coords) == 2:
        fig.canvas.mpl_disconnect(cid)
        close()
    return coords

def unmap(img, rgb):
    """ img is an image of shape [n, m, 3], and rgb is a colormap of shape [k, 3]. """
    A = img[np.newaxis, ...].astype(float)
    B = rgb[:, np.newaxis, np.newaxis, :].astype(float)
    norm = np.linalg.norm(A-B, axis=-1)
    i = np.argmin(norm, axis=0)
    return i / float(rgb.shape[0] - 1)

if __name__ == '__main__':
    # Load original image
    img = imread(sys.argv[1])[:,:,:3]

    # Display image, and wait for user input
    fig = figure(1)
    ax1 = fig.add_subplot(111)
    ax1.imshow(img)
    title('Click to select the ends of the colorbar')
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    show(1)

    print('\nProcessing...')

    r = sqrt((coords[0][0]-coords[1][0])**2 + (coords[0][1] - coords[1][1])**2)
    xs = linspace(coords[0][0], coords[1][0], r)
    ys = linspace(coords[0][1], coords[1][1], r)

    R = scipy.ndimage.map_coordinates(img[:,:,0], np.vstack((ys, xs)))
    G = scipy.ndimage.map_coordinates(img[:,:,1], np.vstack((ys, xs)))
    B = scipy.ndimage.map_coordinates(img[:,:,2], np.vstack((ys, xs)))

    rgb = array((R,G,B)).T

    values = unmap(img, rgb)

    minv, maxv = cbarvals
    values *= (maxv-minv)
    values += minv

    figure(2)
    imshow(values)
    colorbar()

    figure(3)
    imshow(img)

    #figure()
    #xx = linspace(0,1,rgb.shape[0])
    #plot(xx, rgb[:,0]/float(rgb.ptp()), 'r', linewidth=2)
    #plot(xx, rgb[:,1]/float(rgb.ptp()), 'g', linewidth=2)
    #plot(xx, rgb[:,2]/float(rgb.ptp()), 'b', linewidth=2)
    #xlim((-0.01, 1.01))
    #ylim((-0.01, 1.01))
    #title('Jet color map')
    #ylabel('Intensity')
    #xlabel('Value')

    show()
