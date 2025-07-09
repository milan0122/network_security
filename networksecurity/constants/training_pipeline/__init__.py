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
SCHEMA_FILE_PATH :str = os.path.join("data_schema","schema.yaml")

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