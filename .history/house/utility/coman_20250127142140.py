import os 
from pathlib import Path
from house import logging

def create_folder(path):
    os.makedirs(path,exist_ok=True)
    logging.info(f"{path} Folder create sucessfully")
    
def clean_sqft(col):
            tokens = col.split("-")
            if len(tokens) == 2:
                return (float(tokens[0]) + float(tokens[-1])) / 2
            try: 
                return float(col)
            except:
                return None    
    