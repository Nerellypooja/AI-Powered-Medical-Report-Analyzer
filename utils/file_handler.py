# utils/file_handler.py

import os

TEMP_DIR = "temp"

def save_uploaded_file(uploaded_file):
    """
    Saves uploaded file to a temporary directory
    """
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    file_path = os.path.join(TEMP_DIR, uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    return file_path
