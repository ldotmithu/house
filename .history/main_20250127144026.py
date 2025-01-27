from house.pipeline.pipeline import DataIngestionpipeline,DataTransfomationPipeline,Model_Train_Pipeline
from house import logging

try:
    logging.info(">>>> DataIngestion Stage>>>>>>>>>>")
    data_ingestion = DataIngestionpipeline()
    data_ingestion.Main()
    logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
except Exception as e:
    raise e 


try:
    logging.info(">>>> DataTransfomation Stage>>>>>>>>>>")
    data_transfomation = DataTransfomationPipeline()
    data_transfomation.Main()
    logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
except Exception as e:
    raise e 