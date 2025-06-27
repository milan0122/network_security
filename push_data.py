
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from urllib.parse import quote_plus
import os
from dotenv import load_dotenv
import json 
import certifi
import pandas as pd 
import numpy as np 
import pymongo
import sys
from networksecurity.Exception_handling.exception import CustomException
load_dotenv()
username = quote_plus(os.getenv("username"))
password = quote_plus(os.getenv("password"))

uri = f"mongodb+srv://{username}:{password}@cluster0.o8bs1oh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

ca = certifi.where()
class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)
        '''
        This func convert csv data into json
        '''
    def cv_to_json(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise CustomException(e,sys)
    def insert_data_to_mongodb(self,records,database,collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records
            self.mongo_client = pymongo.MongoClient(uri)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]

            self.collection.insert_many(self.records)
            return len(self.records)
            
        except Exception as e:
            raise CustomException(e,sys)
if __name__ == '__main__':
    file_path = "Network_Data/phisingData.csv"
    database = "MilanAI"
    collection = "NetworkData"
    networkobj = NetworkDataExtract()
    records = networkobj.cv_to_json(file_path=file_path)
    no_of_records = networkobj.insert_data_to_mongodb(records,database,collection)
    print(no_of_records,"are inserted sucessfully")
