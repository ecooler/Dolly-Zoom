# <Your name>
# COMP 776, Fall 2017
# Assignment: Dolly Zoom

import numpy as np

#-------------------------------------------------------------------------------

# stores camera intrinsics and extrinsics, and provides functionality for
# projecting 3D points into the camera
class PinholeCamera:
    # 
    def __init__(self, K):
        # store the intrinsic camera matrix (you can also store the focal
        # length, etc. separately)
        self.K = K

        # create a default camera pose
        self.R = np.eye(3)
        self.t = np.zeros(3)

    #---------------------------------------------------------------------------

    # this function should project a set of 3D points in world coordinates
    # into pixel coordinates, according to the camera extrinsics and intrinsics
    # inputs:
    # - points3D: Nx3 array of (x, y, z) point coordinates
    # returns:
    # - points2D: Nx2 array (x, y) pixel locations
    def points3D_to_pixel_coordinates(self, points3D):
        # TODO: implement this function!
        return np.empty((len(points3D), 2))
