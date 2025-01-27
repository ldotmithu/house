from house.components.data_ingestion import DataIngestion
from house import logging
from house.components.data_transfomation import DataTransfomation
from house.components.model_train import Model_Train
from house.components.model_evaluation import ModelEvaluation

class DataIngestionpipeline:
    def __init__(self):
        pass
    
    def Main(self):
        data_ingestion = DataIngestion()
        data_ingestion.dowmload_file()
        data_ingestion.unzip_operation()
        
class DataTransfomationPipeline:
    def __init__(self):
        pass
    
    def Main(self):
        data_transfomation = DataTransfomation()
        data_transfomation.split_data()  
        
class Model_Train_Pipeline:
    def __init__(self):
        pass
    def Main(self):
        model_train = Model_Train()
        model_train.preprocess_and_train()
                  
        