import os 
import sys
from networksecurity.Exception_handling.exception import CustomException
from networksecurity.Logging.logger import logging
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.model_training import ModelTrainer
from networksecurity.constants.training_pipeline import TRAINING_BUCKET_NAME
from networksecurity.cloud.s3_syncer import S3Sync

from networksecurity.entity.config_entity import (
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    ModelTrainerConfig
)
from networksecurity.entity.artifact_entity import (
    Data_Ingestion_Artifact,
    Data_Validation_Artifact,
    Data_Transformation_Artifact,
    ModelTrainingArtifact
)


class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.s3_sync = S3Sync()
    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Data Ingestion Started....")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact= data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingestion completed and artifact:{data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e,sys)
    def start_data_validation(self,data_ingestion_artifact:Data_Ingestion_Artifact):
        try:
          data_validation_config =DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
          data_validation = DataValidation(data_ingestion_artifact,data_validation_config=data_validation_config)
          logging.info("Data Validation Initiated")
          data_validation_artifact=data_validation.initiate_data_validation()
          logging.info(f"Data Validation completed and artifacts:{data_validation_artifact}")
          return data_validation_artifact
        except Exception as e:
            raise CustomException(e,sys)
    def start_data_transformation(self,data_validation_artifact:Data_Validation_Artifact):
        try:
          data_transformation_config =DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
          data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,data_transformation_config=data_transformation_config)
          logging.info("Data Transformation Initiated")
          data_transformation_artifact = data_transformation.initate_data_transformation()
          logging.info(f"Data Transformation artifact completed and artifact :{data_transformation_artifact}")
          return data_transformation_artifact

        except Exception as e:
            raise CustomException(e,sys)
        

    def start_model_trainer(self,data_transformation_artifact:Data_Transformation_Artifact)->ModelTrainingArtifact:
        try:
            model_trainer_config = ModelTrainerConfig(self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
            logging.info("Model Training Started.....")
            model_trainer_artifact=model_trainer.initiate_model_trainer()
            print(f"Model Training completed and artifact :{model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)
    # local artifact pushing to s3 bucket
    def sync_artifact_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder=self.training_pipeline_config.artifact_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise CustomException(e,sys)
        # final model pushing to s3 bucket
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder=self.training_pipeline_config.model_dir,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            raise CustomException(e,sys)
    def run_pipeline(self):
        try:
           data_ingestion_artifact = self.start_data_ingestion()
           data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
           data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
           model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)
           self.sync_artifact_dir_to_s3()
           self.sync_saved_model_dir_to_s3()
           return model_trainer_artifact
    
        except Exception as e:
            raise CustomException(e,sys)