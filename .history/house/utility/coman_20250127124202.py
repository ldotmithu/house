import os 
from pathlib import Path
from house import logging

def create_folder(path):
    os.makedirs(path,exist_ok=True)
    logging.info(f"{path} Folder create sucessfully")
    