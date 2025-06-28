from networksecurity.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
from networksecurity.components.data_ingestion import DataIngestion
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
     except Exception as e:
          raise CustomException(e,sys)