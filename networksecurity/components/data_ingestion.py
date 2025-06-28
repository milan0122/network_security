from networksecurity.Exception_handling.exception import CustomException
from networksecurity.Logging.logger import logging

## configuration of the Data Ingestion Config
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import Data_Ingestion_Artifact
from networksecurity.entity.config_entity import TrainingPipelineConfig
import os 
import sys 
import numpy as np 
import pandas as pd 
import pymongo
from typing import List 
from sklearn.model_selection import train_test_split
from urllib.parse import quote_plus
from dotenv import load_dotenv
load_dotenv()
username = quote_plus(os.getenv("username"))
password = quote_plus(os.getenv("password"))

uri = f"mongodb+srv://{username}:{password}@cluster0.o8bs1oh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

class DataIngestion:
    #initiating the value defined in DataIngestionConfig
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e,sys)
        
    """
    This function used to read data from mongodb
    """
    def export_collection_as_dataFrame(self):
        try:
            # getting information about database_name, collection_name from DataIngestionConfig
            database_name = self.data_ingestion_config.database_name
            collection_name  = self.data_ingestion_config.collection_name
            #connecting to database
            self.mongo_client = pymongo.MongoClient(uri)
            #fetching the collection from database
            collection = self.mongo_client[database_name][collection_name]
            #formatting in DataFrame
            df = pd.DataFrame(list(collection.find()))
            # Default, in mongodb there is extra cols name _id, so dropping it
            if "_id" in df.columns.to_list():
                 df.drop(columns=["_id"],axis=1,inplace=True)
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
                raise CustomException(e,sys)
    
    """"- Always calling data from mongodb , it will impact on perfromance
        - So once we call from mongodb, let's keep the information in certain folders name feature store
      """  
    def export_data_to_feature_store(self,dataframe:pd.DataFrame):
        try:
            #getting the feature store file path
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            # return directory path
            dir_path = os.path.dirname(feature_store_file_path)
            # create directory
            os.makedirs(dir_path,exist_ok=True)
            #save df in csv file 
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
                raise CustomException(e,sys)
        
    """
    func to split data into train_test and saving the file into respective locations
    """
    def split_data_as_train_test(self,dataframe:pd.DataFrame):
         try:
              #split into train test data 
              train_set,test_set = train_test_split(
                   dataframe,test_size=self.data_ingestion_config.train_test_split_ratio,random_state=42
              )
              logging.info("Performed train test split on the dataframe")
              # return the directory and create the folder
              dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
              os.makedirs(dir_path,exist_ok=True)
              logging.info("Exporting train and test file path ")
              #saving train_set and test_set as train.csv and test.csv
              train_set.to_csv(self.data_ingestion_config.training_file_path,index=None,header=True)
              test_set.to_csv(self.data_ingestion_config.testing_file_path,index=None,header=True)
              logging.info("Exported train and test file path")
            
         except Exception as e:
              raise CustomException(e,sys)
    def initiate_data_ingestion(self):
        try:
            # getting dataframe file and store in df
            df = self.export_collection_as_dataFrame()
            # save df to feature_store dir for future usage instead of calling from database for training
            df = self.export_data_to_feature_store(df)
            #spliting into train_test and save them into respective file
            self.split_data_as_train_test(dataframe=df)
            dataingestionartifact= Data_Ingestion_Artifact(train_file_path=self.data_ingestion_config.training_file_path,
                                                  test_file_path=self.data_ingestion_config.testing_file_path)
            return dataingestionartifact  
        except Exception as e:
            raise CustomException(e,sys)
        
