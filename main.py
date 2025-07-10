from networksecurity.entity.config_entity import (TrainingPipelineConfig, DataIngestionConfig,DataValidationConfig,DataTransformationConfig)
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.Logging.logger import logging
from networksecurity.Exception_handling.exception import CustomException
import sys 
if __name__ == '__main__':
     try:
          trainingpipelineconfig = TrainingPipelineConfig()
          dataingestionconfig = DataIngestionConfig(training_pipeline_config=trainingpipelineconfig)
          obj = DataIngestion(data_ingestion_config=dataingestionconfig)
          logging.info("Initiate the data ingestion config")
          dataingestionartifact =obj.initiate_data_ingestion()
          print(dataingestionartifact)
          logging.info("Data Ingestion Completed")

          data_validation_config =DataValidationConfig(training_pipeline_config=trainingpipelineconfig)
          data_validation = DataValidation(dataingestionartifact,data_validation_config=data_validation_config)
          logging.info("Data Validation Initiated")
          data_validation_artifact=data_validation.initiate_data_validation()
          print(data_validation_artifact)
          logging.info("Data Validation completed")

          data_transformation_config=DataTransformationConfig(trainingpipelineconfig)
          data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,data_transformation_config=data_transformation_config)
          logging.info("Data Transformation initiated")
          data_transformation.initate_data_transformation()
          print(data_transformation)
          logging.info("Data Transformation completed")
          
         
     except Exception as e:
          raise CustomException(e,sys)