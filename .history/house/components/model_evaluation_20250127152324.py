from house.entity.config_entity import *
from house import logging
import pandas as pd 
from house.utility.coman import *


class ModelEvaluation: 
    def __init__(self):
        self.model_evaluation = ModelEvaluationConfig()
        
        create_folder(self.model_evaluation.root_dir)
        
    def preprocess_test(self):
        logging.info("Loading test data...")
        data = pd.read_csv(self.model_evaluation.test_data_path)

        logging.info("Cleaning data...")
        # Drop rows with missing or duplicate values
        data.dropna(inplace=True)
        data.drop_duplicates(inplace=True)
        # Process `size` column to extract numeric values
        data['size'] = data['size'].apply(lambda x: x.split(" ")[0]).astype(int)
        # Clean and process `total_sqft` column
        data['total_sqft'] = data['total_sqft'].apply(clean_sqft)
        data.dropna(subset=['total_sqft'], inplace=True)
        # Reduce categories in `location` column
        location_status = data['location'].value_counts()
        location_less_20 = location_status[location_status < 20]
        data['location'] = data['location'].apply(
            lambda x: 'others' if x in location_less_20 else x
                                    )                                                            