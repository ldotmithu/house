from house import logging
from house.entity.config_entity import *
from xgboost import XGBRegressor
from house.utility.coman import *
import pandas as pd 
from xgboost import XGBRegressor

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import PowerTransformer, StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split

class MOdel_Train:
    def __init__(self):
        self.model_train = ModelTrainConfig()
        
        create_folder(self.model_train.root_dir)
        
    def preprocess(self):
        try:
            data = pd.read_csv(self.model_train.train_data_path)
            logging.info("read train data")
            
            data.dropna(inplace=True)
            data.drop_duplicates(inplace=True)
            data['size'] = data['size'].apply(lambda x:x.split(" ")[0]).astype(int)
            data['location'] = data['location'].apply(clean_sqft)
            location_status = data['location'].value_counts()
            location_less_20 = location_status[location_status < 20]
            data['location'] = data['location'].apply(lambda x:'others' if x in location_less_20 else x)

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
            X = preprocess.fit_transform(X)

            # Optional: Split into training and test sets
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            xgb = XGBRegressor()
            xgb.fit(X_train,y_train)
            
            
        except Exception as e :
            raise e 

                
                
                        
                        
                    
                
                