from networksecurity.constants.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
from networksecurity.Exception_handling.exception import CustomException
from networksecurity.Logging.logger import logging
import sys
import os 
class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model 
        except Exception as e:
            raise CustomException
        
    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise CustomException(e,sys)