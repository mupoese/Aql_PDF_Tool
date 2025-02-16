import os
import logging

logging.basicConfig(level=logging.INFO)

def check_folders(input_folder, output_folder):
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
