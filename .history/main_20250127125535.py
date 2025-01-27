from house.pipeline.pipeline import DataIngestionpipeline
from house import logging

try:
    logging.info(">>>> DataIngestion Stage>>>>>>>>>>")
    data_ingestion = DataIngestionpipeline()
    data_ingestion.Main()
except Exception as e:
    raise e 