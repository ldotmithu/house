from house.entity import *
import os 
from urllib.request import urlretrieve
from house import logging
from house.entity.config_entity import DataIngestionConfig
from house.utility.coman import create_folder

class DataIngestion:
    def __init__(self):
        self.data_ingestion = DataIngestionConfig()
        