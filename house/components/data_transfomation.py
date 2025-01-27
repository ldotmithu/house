from house.entity.config_entity import DataTransfomationConfig
from house import logging
from sklearn.model_selection import train_test_split
import pandas as pd 
from house.utility.coman import *


class DataTransfomation:
    def __init__(self):
        self.data_transfomation = DataTransfomationConfig()
        
        create_folder(self.data_transfomation.root_dir)
        
    def split_data(self):
        data = pd.read_csv(self.data_transfomation.data_path)
        logging.info("read the data through pandas")
        
        train_data , test_data = train_test_split(data,test_size=0.2,random_state=42)
        logging.info("Split the data into train and test ")
        
        train_data.to_csv(os.path.join(self.data_transfomation.root_dir,"train.csv"),index=False)
        
        test_data.to_csv(os.path.join(self.data_transfomation.root_dir,"test.csv"),index=False)
            