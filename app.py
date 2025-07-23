
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
from networksecurity.Logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline


from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,File,UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
import pandas as pd 
from networksecurity.utils.utility import load_object
load_dotenv()
username = quote_plus(os.getenv("username"))
password = quote_plus(os.getenv("password"))

uri = f"mongodb+srv://{username}:{password}@cluster0.o8bs1oh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

ca = certifi.where()
client = pymongo.MongoClient(uri,tlsCAFile=ca)

from networksecurity.constants.training_pipeline import Data_Ingestion_Collection,Data_Ingestion_Database
database = client[Data_Ingestion_Database]
collection = database[Data_Ingestion_Collection]
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        training_pipeline =TrainingPipeline()
        training_pipeline.run_pipeline()
        return Response("Training is sucessfully")
    except Exception as e:
        raise CustomException(e,sys)
if __name__=='__main__':
    app_run(app,host="localhost",port=8000)