import os
import pandas as pd
from xgboost import XGBRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import PowerTransformer, StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
from house import logging
from house.entity.config_entity import *
from house.utility.coman import *
    

def clean_sqft(col):
    tokens = col.split("-")
    if len(tokens) == 2:
        return (float(tokens[0]) + float(tokens[-1])) / 2
    try:
        return float(col)
    except:
        return None


class Model_Train:
    def __init__(self):
        self.model_train = ModelTrainConfig()
        create_folder(self.model_train.root_dir)

    def preprocess_and_train(self):
        try:
            # Load data
            logging.info("Loading training data...")
            data = pd.read_csv(self.model_train.train_data_path)

            # Data cleaning
            logging.info("Cleaning data...")
            data.dropna(inplace=True)
            data.drop_duplicates(inplace=True)
            data['size'] = data['size'].apply(lambda x: x.split(" ")[0]).astype(int)
            data['location'] = data['location'].apply(clean_sqft)
            
            location_status = data['location'].value_counts()
            location_less_20 = location_status[location_status < 20]
            data['location'] = data['location'].apply(
                lambda x: 'others' if x in location_less_20 else x
            )

            # Drop rows where 'location' could not be cleaned
            data.dropna(subset=['location'], inplace=True)

            # Define numerical and categorical columns
            num_columns = ['size', 'total_sqft', 'bath']
            cat_columns = ['location']

            # Create pipelines for numerical and categorical transformations
            logging.info("Creating preprocessing pipelines...")
            num_pipeline = Pipeline([
                ('power', PowerTransformer(method='yeo-johnson')),
                ('scaler', StandardScaler())
            ])
            cat_pipeline = OneHotEncoder(handle_unknown='ignore')

            preprocess = ColumnTransformer([
                ('num', num_pipeline, num_columns),
                ('cat', cat_pipeline, cat_columns)
            ])

            # Split data into features and target
            X = data.drop(columns='price', axis=1)
            y = data['price']

            # Apply preprocessing to the features
            logging.info("Preprocessing data...")
            X_preprocessed = preprocess.fit_transform(X)

            # Split into training and test sets
            logging.info("Splitting data into train and test sets...")
            X_train, X_test, y_train, y_test = train_test_split(
                X_preprocessed, y, test_size=0.2, random_state=42
            )

            # Train the XGBRegressor
            logging.info("Training the XGBRegressor model...")
            xgb = XGBRegressor()
            xgb.fit(X_train, y_train)

            # Evaluate the model
            logging.info("Evaluating the model...")
            y_pred = xgb.predict(X_test)
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            logging.info(f"Model evaluation completed: MSE = {mse:.2f}, R^2 = {r2:.2f}")

            # Save the preprocessing pipeline
            preprocess_path = os.path.join(
                self.model_train.root_dir, self.model_train.preprocess_name
            )
            logging.info(f"Saving preprocessing pipeline to {preprocess_path}...")
            joblib.dump(preprocess, preprocess_path)

            # Save the trained model
            model_path = joblib.dump(os.path.join(self.model_train.root_dir, self.model_train.model_name))
            logging.info(f"Saving trained model to {model_path}...")
            joblib.dump(xgb, model_path)

        except FileNotFoundError as fnf_error:
            logging.error(f"File not found: {fnf_error}")
        except ValueError as val_error:
            logging.error(f"Value processing error: {val_error}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise e
