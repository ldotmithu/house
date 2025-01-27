from house.pipeline.pipeline import DataIngestionpipeline,DataTransfomationPipeline
from house import logging

try:
    logging.info(">>>> DataIngestion Stage>>>>>>>>>>")
    data_ingestion = DataIngestionpipeline()
    data_ingestion.Main()
except Exception as e:
    raise e 


try:
    logging.info(">>>> DataTransfomation Stage>>>>>>>>>>")
    data_transfomation = DataTransfomationPipeline()
    data_transfomation.Main()
except Exception as e:
    raise e 