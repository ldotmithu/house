from house.pipeline.pipeline import DataIngestionpipeline,DataTransfomationPipeline,Model_Train_Pipeline,ModelEvaluationPipelien
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


try:
    logging.info(">>>> Model_Train Stage>>>>>>>>>>")
    model_train = Model_Train_Pipeline()
    model_train.Main()
    logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
except Exception as e:
    raise e 


try:
    logging.info(">>>> Model_Evaluation Stage>>>>>>>>>>")
    model_evaluation = ModelEvaluationPipelien()
    model_evaluation.Mian()
    logging.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
except Exception as e:
    raise e 