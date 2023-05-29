#! /usr/bin/env python3

"""
Module to read fruit descriptions from text files and send them to a remote server 
via HTTP POST requests.

This module uses the glob and requests libraries to find all text files with a ".txt" 
extension in the "supplier-data/descriptions" directory, parse their contents into 
JSON objects, and send them to a remote server via HTTP POST requests.

Usage:
1. Set the IP address of the remote server in the "IP" variable.
2. Set the "PATH_TO_TXT" constant to the directory containing the text files to upload.
3. Set the "POST_PATH" constant to the URL of the server's API endpoint.
4. Run the module to upload the text files to the server.

Requirements:
- Python 3.6 or later
- The glob and requests libraries

Note: The server must be configured to accept HTTP POST requests with JSON payloads 
containing keys "name", "weight", "description", and "image_name".

Author: Andrey Pomortsev
"""

import glob
import requests

IP = ""
PATH_TO_TXT = "supplier-data/descriptions/*.txt"
POST_PATH = f"http://{IP}/fruits/"

reviews = glob.glob(PATH_TO_TXT)
dict_keys = ["name", "weight", "description"]


def read_txt(txt_file: str, send: bool = True):
    """
    Reads a text file containing data about a fruit, including its name, weight,
    and description. Returns a formatted string with the fruit name and weight.

    Args:
        txt_file (str): The name of the text file to read.
        send (bool, optional): A flag to indicate whether to send the data to a server
            using the requests library. Defaults to True.

    Returns:
        str: A formatted string with the fruit name and weight, in the following format:
            "name: {fruit_name}\nweight: {fruit_weight} lbs".
    """
    with open(txt_file, "r", encoding="UTF-8") as file:
        data = {
            key: value.strip("\nlbs") for key, value in zip(dict_keys, file.readlines())
        }
        data |= {"image_name": txt_file}
        data["weight"] = int(data["weight"])
        if send:
            response = requests.post(POST_PATH, json=data, timeout=2)
            print(response.status_code)
        return f"name: {data['name']}\nweight: {data['weight']} lbs"


for review in reviews:
    read_txt(review)
