#!/usr/bin/env python

import argparse
import cv2
from multiprocessing.dummy import Pool as ThreadPool
import numpy as np
import openslide
from openslide import OpenSlide, PROPERTY_NAME_MPP_X
import os
from PIL import Image


def main(file_path):
    # Import slide
    slide = openslide.OpenSlide(file_path)

    # ----- Scaling -----
    tile_size_px = 256/float(slide.properties[PROPERTY_NAME_MPP_X])
    # size thumbnail
    thumb_size = (np.array(slide.dimensions)/tile_size_px).astype(int)
    # creating thumbnail of the image
    image_thumb = slide.get_thumbnail(thumb_size)

    # ----- RGB Thresholding -----
    # Conversion of the image
    image = np.array(image_thumb)
    image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

    # Separation on the image in three color channels
    blue_channel = image[:, :, 0]
    green_channel = image[:, :, 1]
    red_channel = image[:, :, 2]

    # Calculate histograms for each color channel
    hist_blue = cv2.calcHist([blue_channel], [0], None, [256], [0, 256])
    hist_green = cv2.calcHist([green_channel], [0], None, [256], [0, 256])
    hist_red = cv2.calcHist([red_channel], [0], None, [256], [0, 256])

    # Find the most common values in the histograms
    peak_blue = hist_blue.argmax()
    peak_green = hist_green.argmax()
    peak_red = hist_red.argmax()

    # Mask creation and application of it
    lower_threshold = np.array([20, 50, 20], dtype=np.uint8)
    upper_threshold = np.array([peak_red-8, peak_green-8, peak_blue-8], dtype=np.uint8)

    mask = cv2.inRange(np.array(image_thumb), lower_threshold, upper_threshold)

    # ----- Tassellation & Cleaning -----
    # Coordinates of the patches: the dimension is amount of patches * (x,y) coords of tiles
    coords = np.flip(np.transpose(mask.nonzero()), 1) * tile_size_px

    # Dictionaries to store the patches with coordinates as keys, bboth saved and discareded patches
    patches_saved = {}
    patches_discarded = {}

    for c in coords:
        c = c.astype(int)
        # Patch creation
        patch = slide.read_region(c, 0, (int(tile_size_px),)*2)
        # Converting patch to gray scale
        patch_greyscale = patch.convert('L')
        patch_gray_array = np.array(patch_greyscale)

        # ----- CANNY EDGE DETECTION -----
        edge = cv2.Canny(patch_gray_array, CannyRange[0], CannyRange[1])

        # Normalization of edge
        edge = (edge / np.max(edge) if np.max(edge) != 0 else 0)
        # Calculation of the edge's percentage
        edge = ((np.sum(np.sum(edge)) / (patch_gray_array.shape[0] * patch_gray_array.shape[1])) * 100) 

        # Conversion patch
        patch = patch.convert('RGB').resize((patch_size_px,)*2)
        c_tuple = tuple(c)

        # Removal of useless patches
        if(edge < 2.):
            patches_discarded[c_tuple] = patch
            continue
        # Saving of useful patches
        patches_saved[c_tuple] = patch

    # Process to delete patches with too less tissue
    keys_to_delete = []

    for position, patch in patches_saved.items():
        # Convert patch
        patch_gray = patch.convert('L')
        patch_gray_array = np.array(patch_gray)

        # Proportion of whitish pixels
        white_pixels = np.sum(patch_gray_array > 200)
        total_pixels = patch_size_px * patch_size_px
        proportion_white = white_pixels / total_pixels

        # Check fase
        if proportion_white > white_threshold:
            patches_discarded[position] = patch
            keys_to_delete.append(position)  # Add key for deletion later

    # Remove patches
    for key in keys_to_delete:
        del patches_saved[key]

    # ----- Reconstruction -----
    # Find the maximum x and y coordinates to determine canvas size
    max_x = max(coord[0] for coord in patches_saved.keys())
    max_y = max(coord[1] for coord in patches_saved.keys())

    # Empty canvas to reconstruct the image
    reconstructed_image = np.zeros((max_y + patch_size_px, max_x + patch_size_px, 3), dtype=np.uint8)

    # Iterate through saved patches and place them on the canvas
    for coord, patch in patches_saved.items():
        x_coord, y_coord = coord
        reconstructed_image[y_coord:y_coord + patch_size_px, x_coord:x_coord + patch_size_px] = np.array(patch)

    # ----- Saving Process -----
    # Extracting name for main directory
    extracted_text = file_path[:file_path.rfind('.')]

    # Main directory
    outPath = './tiles'
    main_directory = os.path.join(outPath, extracted_text)
    os.makedirs(main_directory, exist_ok=True)

    # Subdirectories
    if full_saving:
        subdirectories = ['discard', 'reconstruction']
        for folder in subdirectories:
            subdirectory_path = os.path.join(main_directory, folder)
            os.makedirs(subdirectory_path, exist_ok=True)

    # Save patches
    for position, patch in patches_saved.items():
        x_coord, y_coord = position
        filename = "{}_({},{})".format(extracted_text, x_coord, y_coord)
        patch.save(os.path.join(main_directory, filename + ".jpg"))


    # Save discarded patches in the discard folder
    if full_saving:
        for position, patch in patches_discarded.items():
            x_coord, y_coord = position
            filename = "{}_({},{})".format(extracted_text, x_coord, y_coord)
            patch.save(os.path.join(main_directory, 'discard', filename + ".jpg"))


        # Save the reconstructed image in the reconstruction folder
        reconstructed_image = Image.fromarray(reconstructed_image)
        reconstructed_image.save(os.path.join(main_directory, 'reconstruction', extracted_text + ".jpg"))


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Histo Pre-processing',
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("-1", "--input_image", nargs='*',
                     help="Path of the input image file",
                     default="/data/datasets/gdc/diagnostic_slides/COAD/70012428-8df8-4eb2-8d28-7d0b2a88d1d7/TCGA-A6-3810-01Z-00-DX1.2940ca70-013a-4bc3-ad6a-cf4d9ffa77ce.svs",
                     required=False)
  parser.add_argument("-2", "--CannyValues", nargs=2, type=int,
                     help="Values for Canny edge detection",
                     default=[40, 100],
                     required=False)
  parser.add_argument("-3", "--CleaningThreshold", type=float,
                     help="Threshold for deleting patches with too mach whitish pixels",
                     default=0.9,
                     required=False)
  parser.add_argument("-4", "--PatchPixelSize", type=int,
                     help="Patch size in pixels",
                     default=512,
                     required=False)
  parser.add_argument("-5","--apply_FullSaving",  action='store_true',
                     help="Activate the full saving process",
                     required=False)
  parser.add_argument("-6", "--threads", type=int,
                      help="Number of threads used for processing, 2 by default",
                      default=2,
                      required=False)
  args = parser.parse_args()
  folder_path = args.input_image
  CannyRange = args.CannyValues
  white_threshold = args.CleaningThreshold
  patch_size_px = args.PatchPixelSize
  full_saving = args.apply_FullSaving
  num_threads = args.threads

pool = ThreadPool(num_threads)
pool.map(main, folder_path)
pool.close()
pool.join()
