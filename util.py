# <Your name>
# COMP 776, Fall 2017
# Assignment: Dolly Zoom

import numpy as np

from scipy.io import loadmat
from scipy.ndimage.filters import maximum_filter

from camera import PinholeCamera

#-------------------------------------------------------------------------------

# loads scene data from a .mat file
# returns:
# - camera: a PinholeCamera object
# - viewport: used for rendering; this defines a crop of the pixel space in
#     the form (top, left, height, width)
# - points3D: Nx3 array of (x, y, z) point coordinates
# - rgb: Nx3 array (r, g, b) color values for the 3D points
def load_data(data_file):
    data = loadmat(data_file)

    # 3x3 intrinsic camera matrix; converts normalized camera coordinates into
    # pixel coordinates
    K = data["K"]

    # the viewport defines the pixel space for our sensor
    viewport = data["crop_region"].flat # top, left, height, width
    viewport[0] -= 1 # the original file used Matlab's 1-based indexing
    viewport[1] -= 1

    # note, foreground statue is placed closer to the camera by a factor of two
    fg = data["ForegroundPointCloudRGB"].T
    bg = data["BackgroundPointCloudRGB"].T
    points3D = np.row_stack((fg[:,:3], bg[:,:3])) # Nx3
    rgb = np.row_stack((fg[:,3:], bg[:,3:])) # Nx3, [0,1]^3

    camera = PinholeCamera(K)

    return camera, viewport, points3D, rgb

#-------------------------------------------------------------------------------

# renders a 3D point cloud given a PinholeCamera object
# inputs:
# - camera: PinholeCamera
# - points3D: 3D point positions; Nx3
# - rgb: point colors \in [0,1]^3; Nx3
# returns: the rendered image as an HxWx3 numpy array
def render(camera, viewport, points3D, rgb):
    # project the points into the current view; use nearest neighbor
    # interpolation for determining which pixel the point projects into
    points2D = camera.points3D_to_pixel_coordinates(points3D).astype(np.int)

    #
    # filter out points that project outside of the sensor
    #

    left, top = viewport[1], viewport[0]
    width, height = viewport[3], viewport[2]
    mask = np.all(
        (points2D >= (left, top)) & (points2D < (left + width, top + height)),
        axis=-1)

    points2D = points2D[mask]
    rgb = rgb[mask]
    z = points3D[mask,2] # we'll use these below

    #
    # now, we'll compute which 2D points occupy which pixel, and for each pixel,
    # we'll keep the point closest to the camera
    #

    # first, convert (x,y) integer pixel coordinates into a flat index
    points2D_idx = points2D[:,1] * width + points2D[:,0]

    # indirectly sort first by this flat index, and then by point depth
    order = np.lexsort((points2D_idx, z))

    # apply the sort
    points2D = points2D[order]
    points2D_idx = points2D_idx[order]
    rgb = rgb[order]
    
    # the 2D points are now ordered by pixel index, and then by depth; the first
    # occurrence of each pixel index in points2D_idx therefore references the
    # point closest to the camera for that pixel
    _, indices = np.unique(points2D_idx, return_index=True)

    points2D = points2D[indices]
    rgb = rgb[indices]

    #
    # finally, create our image; missing values are black
    #

    image = np.zeros((height, width, 3))
    image[points2D[:,1] - viewport[0], points2D[:,0] - viewport[1]] = rgb

    # apply a 5x5 max filter for each channel

    image[:,:,0] = maximum_filter(image[:,:,0], (5, 5))
    image[:,:,1] = maximum_filter(image[:,:,1], (5, 5))
    image[:,:,2] = maximum_filter(image[:,:,2], (5, 5))

    return image
