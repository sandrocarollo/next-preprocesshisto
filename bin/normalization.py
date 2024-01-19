#!/usr/bin/env python

import argparse
import cv2
import os
from pathlib import Path
from PIL import Image
import norm_Macenko

def Normalization(inputPath: Path, sampleImagePath: Path) -> None:
    
    # Fitting of the normalizer to the target image 
    target = cv2.imread(sampleImagePath)
    target = cv2.cvtColor(target, cv2.COLOR_BGR2RGB)    
    normalizer = norm_Macenko.Normalizer()
    normalizer.fit(target)

    # ----- Normalization & Saving Process -----
    for patch in inputPath:
        img = cv2.imread(str(patch))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Patches' normalization 
        nor_img = normalizer.transform(img)
        nor_img = cv2.cvtColor(nor_img, cv2.COLOR_RGB2BGR)

        # Extracting name for main directory 
        extracted_text = patch.name[:(str(patch).find('('))]

        # Main directory 
        outPath = './normalized_patches'
        main_directory = os.path.join(outPath, extracted_text)
        os.makedirs(main_directory, exist_ok=True)

        # Saving 
        nor_img = Image.fromarray(nor_img)
        nor_img.save(os.path.join(main_directory,patch))    

if __name__ == '__main__':
    # Parsing all arguments from the command line
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", "--inputPath", help="Input path of the to-be-normalised tiles", nargs='+', type=Path, required=True)
    parser.add_argument("-si", "--sampleImagePath", help="Image used to determine the colour distribution, uses GitHub one by default", type=Path)
    args = parser.parse_args()

    # Calling the Normalization function with defined parameters
    Normalization(  args.inputPath,
                    args.sampleImagePath if args.sampleImagePath != None else './bin/normalization_template.jpg')