from pathlib import Path
import os 
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    root_dir:Path = "artifacts/data_ingestion"
    URL:str = "https://github.com/ldotmithu/Dataset/raw/refs/heads/main/bengaluru_house_prices.zip"
    local_data_path:Path = "artifacts/data_ingestion/data.zip"
    unzip_dir:Path = "artifacts/data_ingestion"
    
    
@dataclass 
class DataTransfomationConfig:
    root_dir:Path = "artifacts/data_transfomation"
    data_path:Path = "artifacts/data_ingestion/bengaluru_house_prices.csv" 
    
@dataclass
class ModelTrainConfig:
    root_dir:Path = "artifacts/model_train"
    train_data_path=Path = "artifacts/data_transfomation/train.csv"
    model_name:str="model.json"
    preprocess_name :str = "preprocess.json"
    
@dataclass
class ModelEvaluationConfig:
    root_dir:Path="artifacts/model_evaluation"
    model_path:Path ="artifacts/model_train/model.json"
    preprocess_path:Path="artifacts/model_train/preprocess.json"
    test_data_path:Path="artifacts/data_transfomation/test.csv"    
          