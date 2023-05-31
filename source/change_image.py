#!/usr/bin/env python3

"""
Module for bulk image processing.

This module contains a function that opens image files, resizes them to 
600x400 pixels, and saves them to a specified destination folder. 
The function processes all image files in the specified directory.

Example:
    To bulk process a folder of images, call the changer() function:
        changer(img_name)

Author Andrey Pomortsev
"""

import os
import glob
from PIL import Image

DESTINATION = os.path.expanduser("~/supplier-data/images/")

if not os.path.exists(DESTINATION):
    os.makedirs(DESTINATION)


def changer(img_name: str, dest_dir: str | None = None) -> None:
    """Open image file resize it to 600x400
    and save to the DESTINATION folder
    """
    if not dest_dir:
        dest_dir = DESTINATION
    try:
        with Image.open(img_name) as img:
            if img.mode != "RGB":
                img = img.convert("RGB")
            path_to_save = os.path.join(dest_dir, os.path.basename(img_name))
            img.resize((600, 400)).save(path_to_save, "jpeg")
    except Exception as error:
        print(f"Error processing file {img_name}: {error}")


os.chdir(DESTINATION)
images = glob.glob("*")

for image in images:
    changer(image)
