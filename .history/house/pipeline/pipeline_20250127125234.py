from house.components.data_ingestion import DataIngestion
from house import logging


class DataIngestionpipeline:
    def __init__(self):
        pass
    
    def Main(self):
        data_ingestion = DataIngestion()
        data_ingestion.dowmload_file()
        data_ingestion.unzip_operation()
        