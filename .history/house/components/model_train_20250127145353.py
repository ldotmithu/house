import os
import pandas as pd
from xgboost import XGBRegressor
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import PowerTransformer, StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split
import joblib  # For saving the model and preprocessing pipeline
from house import logging
from house.entity.config_entity import *
from house.utility.coman import create_folder


def clean_sqft(col):
    """
    Cleans and processes the `total_sqft` column.
    Handles ranges (e.g., '1000-1200') and non-numeric values.
    """
    try:
        tokens = col.split("-")
        if len(tokens) == 2:
            return (float(tokens[0]) + float(tokens[-1])) / 2
        return float(col)
    except ValueError:
        logging.warning(f"Non-numeric value encountered in 'total_sqft': {col}")
        return None


class Model_Train:
    def __init__(self):
        # Configuration for model training
        self.model_train = ModelTrainConfig()
        create_folder(self.model_train.root_dir)

    def preprocess_and_train(self):
        try:
            logging.info("Loading training data...")
            data = pd.read_csv(self.model_train.train_data_path)

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

            logging.info("Applying preprocessing...")
            # Apply preprocessing to the features
            X_preprocessed = preprocess.fit_transform(X)

            # Split data into training and testing sets
            logging.info("Splitting data into training and test sets...")
            X_train, X_test, y_train, y_test = train_test_split(
                X_preprocessed, y, test_size=0.2, random_state=42
            )

            # Train the model
            logging.info("Training the model...")
            xgb = XGBRegressor()
            xgb.fit(X_train, y_train)

            # Save the preprocessing pipeline
            preprocess_path = os.path.join(
                self.model_train.root_dir, self.model_train.preprocess_name
            )
            joblib.dump(preprocess, preprocess_path)
            logging.info(f"Preprocessing pipeline saved at {preprocess_path}")

            # Save the trained model
            model_path = os.path.join(
                self.model_train.root_dir, self.model_train.model_name
            )
            joblib.dump(xgb, model_path)
            logging.info(f"Model saved at {model_path}")

        except Exception as e:
            logging.error(f"Error during preprocessing and training: {e}")
            raise e
