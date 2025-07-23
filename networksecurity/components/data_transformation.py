from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.artifact_entity import (Data_Transformation_Artifact,Data_Validation_Artifact)
import sys
import os 
import numpy as np 
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.constants.training_pipeline import TARGET_COLUMN,DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.Logging.logger import logging
from networksecurity.Exception_handling.exception import CustomException
from networksecurity.utils.utility import save_numpy_array_data,save_object

class DataTransformation:
    def __init__(self,data_validation_artifact:Data_Validation_Artifact,
                 data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise CustomException (e,sys)
        
    def get_data_transformer_object(cls)->Pipeline:
        '''
        It initialize a KNNImputer object with the parameters specified in the training Pipeline
        and return a pipeline object with the KNNImputer object as the first step.
        '''
        logging.info("Entered get_data_transformer_object method of Transformation class")
        try:
            imputer =  KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Initialize the KNN Imputer with parms {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            processor:Pipeline = Pipeline([
                ("imputer",imputer)
            ])
            return processor
        except Exception as e:
            raise CustomException (e,sys)
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException (e,sys)
    def initate_data_transformation(self)-> Data_Transformation_Artifact:
        logging.info("Entered initiate data transformation method of DataTransformation class")
        try:
            logging.info("Starting data transformation")
            #reading data from data validation 
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            # training dataFrame
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)
             # test dataFrame
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            # applying transformation on train and test data
            preprocessor = self.get_data_transformer_object()
            preprocessor_obj = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_obj.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor.transform(input_feature_test_df)
           
            train_arr = np.c_[transformed_input_train_feature,np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature,np.array(target_feature_test_df)]

            # save numpy array data 
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,array=train_arr,)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,array=test_arr,)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_obj)
            logging.info("test_arr,train_arr and preprocessor are saved")
            # preparing artifacts

            # saving the preprocessing file into final_model
            save_object("final_model/preprocessor.pkl",preprocessor_obj,)
            data_transformation_artifact=Data_Transformation_Artifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )
            return data_transformation_artifact
        except Exception as e:
            raise CustomException (e,sys)