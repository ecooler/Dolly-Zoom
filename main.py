# <Your name>
# COMP 776, Fall 2017
# Assignment: Dolly Zoom

import matplotlib.pyplot as plt
import os

import util

#-------------------------------------------------------------------------------

def main(data_file, output_folder):
    # first, load the data
    # camera: a PinholeCamera object
    # viewport: used for rendering; this defines a crop of the pixel space in
    #   the form (top, left, height, width)
    # points3D: Nx3 array of (x, y, z) point coordinates
    # rgb: Nx3 array (r, g, b) color values for the 3D points
    camera, viewport, points3D, rgb = util.load_data(data_file)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # TODO: this code demonstrates how to call the render function; you should
    # change it to modify the camera's intrinsic and extrinsic parameters, in
    # order to recreate the dolly zoom effect

    image = util.render(camera, viewport, points3D, rgb)

    out_file = os.path.join(output_folder, "example.png")
    plt.imsave(out_file, image)

    first_image = image
    last_image = image

    #
    # for quick verification, also show the first image of the sequence, but
    # with the red channel replaced by the red channel of the last image of the
    # sequence
    #

    image = first_image.copy()
    image[:,:,0] = last_image[:,:,0]
    out_file = os.path.join(output_folder, "dolly_zoom_change.png")
    plt.imsave(out_file, image)

#-------------------------------------------------------------------------------

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("--data_file", type=str, default="data.mat")
    parser.add_argument("--output_folder", type=str, default="images")

    args = parser.parse_args()

    main(args.data_file, args.output_folder)
