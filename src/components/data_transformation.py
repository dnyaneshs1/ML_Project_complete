import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer

from src.exception import CustomException
from src.logger import logging

from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_object_file_path=os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.Data_Transformation_Config=DataTransformationConfig()

    def get_data_transformer_object(self):
        """
        This function is for data transformation
        """
        try:

            num_column=['MPG.city','Horsepower','RPM','Rev.per.mile','Fuel.tank.capacity','Passengers','Weight']
            cat_column=['Man.trans.avail']

            num_pipe=Pipeline(steps=[('Imputer',SimpleImputer(strategy='median')),('Scalar',StandardScaler())])
            cat_pipe=Pipeline(steps=[('imputer',SimpleImputer(strategy='most_frequent')),('encoder',OneHotEncoder())])

            logging.info(f'Categorical Column : {cat_column}')
            logging.info(f'Numerical Column:{num_column}')

            preprocessor=ColumnTransformer([('Cat_pipe',cat_pipe,cat_column),('num_pipe',num_pipe,num_column)])

            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def Initiate_data_transformation(self,train_path,test_path):

        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info('Reading of train and test data has been completed')

            logging.info('Obtaining Preprocessor Object')

            preprocessing_object=self.get_data_transformer_object()

            target_column_name='Price'

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info('Applying Preprocessing object on training and testing dataframe')

            input_feature_train_arr=preprocessing_object.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_object.fit_transform(input_feature_test_df)

            train_arr= np.c_[input_feature_train_arr,np.array(input_feature_train_df)]
            test_arr=np.c_[input_feature_test_arr,np.array(input_feature_test_df)]

            logging.info('save preprocessing object')

            save_object(file_path=self.Data_Transformation_Config.preprocessor_object_file_path,
                        obj=preprocessing_object)
            
            return (train_arr,test_arr,self.Data_Transformation_Config.preprocessor_object_file_path)
        
        except Exception as e:
            raise CustomException(e,sys)

            

    


