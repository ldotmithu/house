from house.entity import *
import os 
from urllib.request import urlretrieve
from house import logging
from house.entity.config_entity import DataIngestionConfig
from house.utility.coman import create_folder
import zipfile

class DataIngestion:
    def __init__(self):
        self.data_ingestion = DataIngestionConfig()
        
        create_folder(self.data_ingestion.root_dir)
        
    def dowmload_file(self):
            if not os.path.exists(self.data_ingestion.local_data_path):
                urlretrieve(self.data_ingestion.URL,self.data_ingestion.local_data_path)
                logging.info("Download Zip file ")
                
            else:
                logging.info("File Already Exists")        
        
    def unzip_operation(self):
        try: 
            with zipfile.ZipFile(self.data_ingestion.local_data_path) as f :
                f.extractall(self.data_ingestion.unzip_dir)
                logging.info("Unzip_operation Done")
        
        except Exception as e:
            raise e    
                
        