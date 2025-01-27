from house.entity import *
import os 
from urllib.request import urlretrieve
from house import logging
from house.entity.config_entity import DataIngestionConfig

class DataIngestion:
    def __init__(self):
        self.data_ingestion = 