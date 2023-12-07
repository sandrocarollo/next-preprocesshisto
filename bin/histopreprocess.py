#!/usr/bin/env python

import argparse
import cv2  
import numpy as np  
import openslide
import os
from PIL import Image


def main():
    # Import slide
    slide = openslide.OpenSlide(file_path)

    # ----- Scaling -----
    # patch size in pixel 
    patch_size_px = 512
    # size thumbnail
    thumb_size = (np.array(slide.dimensions)/patch_size_px).astype(int)
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
    coords = np.flip(np.transpose(mask.nonzero()), 1) * patch_size_px

    # Dictionaries to store the patches with coordinates as keys, bboth saved and discareded patches 
    patches_saved = {}
    patches_discarded = {}

    for c in coords:
        c = c.astype(int)
        # Patch creation
        patch = slide.read_region(c, 0, (int(patch_size_px),)*2)
        # Converting patch to gray scale 
        patch_greyscale = patch.convert('L')
        patch_gray_array = np.array(patch_greyscale)
        
        # ----- CANNY EDGE DETECTION -----
        edge = cv2.Canny(patch_gray_array, CannyRange[0], CannyRange[1])
        
        # Normalization of edge
        edge = (edge / np.max(edge) if np.max(edge) != 0 else 0)
        # Calculation of the edge's percentage
        edge = ((np.sum(np.sum(edge)) / (patch_size_px * patch_size_px)) * 100) 
        
        # Conversion patch
        patch = patch.convert('RGB')
        c_tuple = tuple(c)
        
        # Removal of useless patches 
        if(edge < 2.):
            patches_discarded[c_tuple] = patch
            continue
        # Saving of useful patches     
        patches_saved[c_tuple] = patch

    # Process to delete patches with too less tissue 
    white_threshold = 0.9  # Threshold for proportion of whitish pixels
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
    #last_slash_index = file_path.rfind('/')
    #if last_slash_index != -1:
    #    extracted_text = file_path[last_slash_index + 1:last_slash_index + 13]
    #else:
    #    print("No '/' found in the path. Path could be not valid")
    extracted_text = file_path[0:12]

    # Main directory 
    outPath = './'
    main_directory = os.path.join(outPath, extracted_text)
    os.makedirs(main_directory, exist_ok=True)

    # Subdirectories
    subdirectories = ['patches']
    if full_saving:
        subdirectories.extend(['discard', 'reconstruction'])

    # Creation subdirectories
    for folder in subdirectories:
        subdirectory_path = os.path.join(main_directory, folder)
        os.makedirs(subdirectory_path, exist_ok=True)

    # Save patches in the patches folder
    for position, patch in patches_saved.items():
        filename = "{}_{}".format(extracted_text, position)
        patch.save(os.path.join(main_directory, 'patches', filename + ".jpg"))


    # Save discarded patches in the discard folder 
    if full_saving:
        for position, patch in patches_discarded.items():
            filename = "{}_{}".format(extracted_text, position)
            patch.save(os.path.join(main_directory, 'discard', filename + ".jpg"))


        # Save the reconstructed image in the reconstruction folder 
        reconstructed_image = Image.fromarray(reconstructed_image)
        reconstructed_image.save(os.path.join(main_directory, 'reconstruction', "reconstructed_" + extracted_text + ".jpg"))


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Histo Pre-processing',
                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("-1", "--inputimage", 
                    help="Path of the input image file",
                    default="/data/datasets/gdc/diagnostic_slides/COAD/70012428-8df8-4eb2-8d28-7d0b2a88d1d7/TCGA-A6-3810-01Z-00-DX1.2940ca70-013a-4bc3-ad6a-cf4d9ffa77ce.svs",
                    required=False)
  parser.add_argument("-2", "--inputCannyValues", nargs=2, type=int,
                     help="Values for Canny edge detection",
                     default=[40, 100],
                     required=False)
  parser.add_argument("-3", "--inputCleaningThreshold", type=float,
                     help="Threshold for deleting patches with too mach whitish pixels",
                     default=0.9,
                     required=False)
  parser.add_argument("-4", "--inputPatchPixelSize", type=int,
                     help="Patch size in pixels",
                     default=512,
                     required=False)
  parser.add_argument("-5","--full_saving", action='store_true',
                     help="Activate the full saving process",
                     required=False)
  #parser.add_argument("-3", "--outputfoldername",
  #                  help="Name of the output result folder",
  #                  default="image",
  #                  required=False)
  args = parser.parse_args()
  file_path = args.inputimage
  CannyRange = args.inputCannyValues
  white_threshold = args.inputCleaningThreshold
  patch_size_px = args.inputPatchPixelSize
  full_saving = args.full_saving
  #mainfoldername = args.outputfoldername
  main()