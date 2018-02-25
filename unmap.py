#!/usr/bin/env python

from pylab import *
import scipy.ndimage, Tkinter, tkSimpleDialog

def onclick(event):
    global ix, iy, coords, cbarvals
    ix, iy = event.xdata, event.ydata
    coords.append((ix,iy))
    scatter([ix], [iy], c=img[int(iy),int(ix),:]/256.0)
    fig.canvas.draw()
    root = Tkinter.Tk()
    cbarvals.append(float(tkSimpleDialog.askstring("Value", "Enter start value")))
    root.destroy()
    if len(coords) == 2:
        fig.canvas.mpl_disconnect(cid)
        close()
    return coords

def get_rgb(img):
    # Display image, and wait for user input
    global coords, cbarvals, fig, cid
    coords = []
    cbarvals = []
    fig = figure(1)
    ax1 = fig.add_subplot(111)
    ax1.imshow(img)
    title('Click to select the ends of the colorbar')
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    show(1)

    # Make transect of interpolation points from pt1 to pt2
    pt1, pt2 = coords
    r = sqrt((pt1[0]-pt2[0])**2 + (pt1[1] - pt2[1])**2)
    xs = linspace(pt1[0], pt2[0], r)
    ys = linspace(pt1[1], pt2[1], r)

    R = scipy.ndimage.map_coordinates(img[:,:,0], np.vstack((ys, xs)))
    G = scipy.ndimage.map_coordinates(img[:,:,1], np.vstack((ys, xs)))
    B = scipy.ndimage.map_coordinates(img[:,:,2], np.vstack((ys, xs)))

    return array((R,G,B)).T, cbarvals[0], cbarvals[1]

def unmap(img, rgb=None, minv=None, maxv=None):
    '''
        img is an image of shape [n, m, 3], and rgb is a colormap of shape [k, 3].
            Note: If rgb is omitted, then the user will be prompted to pick the ends of the colorbar
            in the figure.
        minv and maxv are the values of the ends of the colormap (default: [0, 1])
    '''
    if not rgb:
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
    import sys
    img = imread(sys.argv[1])[:,:,:3]

    values = unmap(img)

    figure()
    imshow(values)
    colorbar()

    figure()
    imshow(img)

    #figure()
    #xx = linspace(0,1,rgb.shape[0])
    #plot(xx, rgb[:,0]/float(rgb.ptp()), 'r', linewidth=2)
    #plot(xx, rgb[:,1]/float(rgb.ptp()), 'g', linewidth=2)
    #plot(xx, rgb[:,2]/float(rgb.ptp()), 'b', linewidth=2)
    #xlim((-0.01, 1.01))
    #ylim((-0.01, 1.01))
    #title('Color map')
    #ylabel('Intensity')
    #xlabel('Value')

    show()
