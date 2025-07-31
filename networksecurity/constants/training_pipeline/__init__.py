import os 
import sys 
import numpy as np 
import pandas as pd 
"""
defining comman constant variable for training pipeline
"""
TARGET_COLUMN = "Result"
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACT_DIR : str = "Artifacts"
FILE_NAME : str = "PhisingData.csv"

TRAIN_FILE_NAME : str = "train.csv"
TEST_FILE_NAME : str = "test.csv"

PREPROCESSING_OBJECT_FILE_NAME:str = "preprocessing.pkl"
SCHEMA_FILE_PATH :str = os.path.join("data_schema","schema.yaml")
SAVED_MODEL_DIR = os.path.join("saved_models")
MODEL_FILE_NAME = "model.pkl"
TRAINING_BUCKET_NAME = "milannetworksecurity"
"""
Data Ingestion related constant start with Data_Ingestion var
"""
Data_Ingestion_Collection: str = "NetworkData"
Data_Ingestion_Database : str = "MilanAI"
Data_Ingestion_Dir_Name: str = "data_ingestion"
Data_Ingestion_Feature_Store_Dir: str = "feature_store"
Data_Ingestion_Ingested_Dir: str = "ingested"
Data_Ingestion_Train_Test_split_Ratio: float = 0.2

"""
Data Validation related constant start with DATA_VALIDATION VAR Name
"""
DATA_VALIDATION_DIR_NAME:str= "data_validation"
DATA_VALIDATION_VALID_DIR:str = "validated"
DATA_VALIDATION_INVALID_DIR :str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR :str = "drift_report"
DATA_VALIDATION_DRIFT_FILE_NAME:str = "report.yaml"
"""
Data Transformation related constant and params
"""
DATA_TRANSFORMATION_DIR_NAME:str= "data_transformation"
DATA_TRASNFORMATION_TRANSFORMED_DATA_DIR:str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str = "transformed_object"
DATA_TRANSFORMATION_IMPUTER_PARAMS:dict = {
    "missing_values":np.nan,
    "n_neighbors":3,
    "weights":"uniform"
}
DATA_TRANSFORMATION_TRAIN_FILE_PATH: str = "train.npy"
DATA_TRANSFORMATION_TEST_FILE_PATH: str = "test.npy"

"""
Model Trainer related constants
"""
MODEL_TRINER_DIR_NAME:str = "model_trainer"
MODEL_TRINER_TRAINED_DIR_NAME:str = "trained_model"
MODEL_TRINER_TRAINED_FILE_NAME:str = "network_model.pkl"
MODEL_TRAINER_EXCEPTED_SCORE:float = 0.7

MODEL_TRAINER_OVER_FITING_UNDER_FITING_THRESHOLD:float = 0.05