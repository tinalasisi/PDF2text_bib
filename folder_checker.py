# folder_checker.py

import os

def check_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"{folder_name} folder created")
    else:
        print(f"{folder_name} folder exists")
