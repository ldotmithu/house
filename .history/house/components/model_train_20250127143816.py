import os
from house import logging
from house.entity.config_entity import *
from xgboost import XGBRegressor
from house.utility.coman import *
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import PowerTransformer, StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
import joblib  # For saving the model and preprocessing pipeline

class Model_Train:
    def __init__(self):
        self.model_train = ModelTrainConfig()
        create_folder(self.model_train.root_dir)

    def preprocess_and_train(self):
        try:
            # Load data
            data = pd.read_csv(self.model_train.train_data_path)
            logging.info("Read train data successfully")

            # Data cleaning
            data.dropna(inplace=True)
            data.drop_duplicates(inplace=True)
            data['size'] = data['size'].apply(lambda x: x.split(" ")[0]).astype(int)
            data['location'] = data['location'].apply(clean_sqft)
            location_status = data['location'].value_counts()
            location_less_20 = location_status[location_status < 20]
            data['location'] = data['location'].apply(lambda x: 'others' if x in location_less_20 else x)

            # Define numerical and categorical columns
            num_columns = ['size', 'total_sqft', 'bath']
            cat_columns = ['location']

            # Create pipelines for numerical and categorical transformations
            num_pipeline = Pipeline([
                ('power', PowerTransformer(method='yeo-johnson')),
                ('scaler', StandardScaler())
            ])
            cat_pipeline = OneHotEncoder(handle_unknown='ignore')

            # Combine transformations into a ColumnTransformer
            preprocess = ColumnTransformer([
                ('num', num_pipeline, num_columns),
                ('cat', cat_pipeline, cat_columns)
            ])

            # Split data into features and target
            X = data.drop(columns='price', axis=1)
            y = data['price']

            # Apply preprocessing to the features
            X_preprocessed = preprocess.fit_transform(X)

            # Split into training and test sets
            X_train, X_test, y_train, y_test = train_test_split(X_preprocessed, y, test_size=0.2, random_state=42)

            # Train the XGBRegressor
            xgb = XGBRegressor()
            xgb.fit(X_train, y_train)
            logging.info("Model training completed")

            # Save the preprocessing pipeline
            joblib.dump(preprocess,os.path.join(self.model_train.root_dir,self.model_train.preprocess_name))
            logging.info(f"Preprocessing pipeline saved at {self.model_train.model_name}")

            # Save the trained model
            joblib.dump(xgb,os.path.join(self.model_train.root_dir,self.model_train.model_name))
            logging.info(f"Model saved at {self.model_train.model_name}")

        except Exception as e:
            logging.error(f"Error during preprocessing and training: {e}")
            raise e
