#!/usr/bin/env python3

"""
Module to upload JPEG images to a server via HTTP POST requests.

This module uses the glob, os, and requests libraries to find all JPEG images
in a given directory, open each image file in binary mode, and send an HTTP POST
request to a server at a specified URL, with the contents of the image file as
the request payload.

Usage:
1. Set the "URL" variable to the desired server URL.
2. Set the current working directory to the directory containing the JPEG images.
3. Run the module to upload all JPEG images to the server.

Example:
$ python3 supplier_image_upload.py

Requirements:
- Python 3.6 or later
- The glob, os, and requests libraries

Note: The server must be configured to accept HTTP POST requests with a "file"
parameter containing binary image data.

Author: Andrey Pomortsev
"""

import glob
import os
import requests

URL = "http://localhost/upload/"
os.chdir(os.path.expanduser("~/supplier-data/images/"))
images = tuple(glob.glob("*.jpeg"))

for image in images:
    with open(image, "rb") as opened:
        request = requests.post(URL, files={"file": opened}, timeout=1)
        print(f"Responce: {request.status_code}")
