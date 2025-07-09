from datetime import datetime 
import os 
from networksecurity.constants import training_pipeline

class TrainingPipelineConfig:
    def __init__(self,timestamp = datetime.now()):
        timestamp = timestamp.strftime('%m_%d_%Y_%H_%M_%S')
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name,timestamp)
        self.timestamp :str = timestamp
class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        # asign the data_ingestion_dir as combination of training_pipeline_config artifacts and constant data_ingestion_dir
        self.data_ingestion_dir : str = os.path.join(
            training_pipeline_config.artifact_dir,training_pipeline.Data_Ingestion_Dir_Name
        )
        self.feature_store_file_path : str = os.path.join(
            self.data_ingestion_dir,training_pipeline.Data_Ingestion_Feature_Store_Dir,training_pipeline.FILE_NAME
        )
        self.training_file_path :str = os.path.join(
            self.data_ingestion_dir,training_pipeline.Data_Ingestion_Ingested_Dir,training_pipeline.TRAIN_FILE_NAME
        )
        self.testing_file_path :str = os.path.join(
            self.data_ingestion_dir,training_pipeline.Data_Ingestion_Ingested_Dir,training_pipeline.TEST_FILE_NAME
        )
        self.train_test_split_ratio :float = training_pipeline.Data_Ingestion_Train_Test_split_Ratio
        self.collection_name :str = training_pipeline.Data_Ingestion_Collection
        self.database_name:str = training_pipeline.Data_Ingestion_Database

class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir :str = os.path.join(training_pipeline_config.artifact_dir,training_pipeline.DATA_VALIDATION_DIR_NAME)
        self.valid_data_dir :str = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir :str = os.path.join(self.data_validation_dir,training_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path :str = os.path.join(self.valid_data_dir,training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path : str = os.path.join(self.valid_data_dir,training_pipeline.TEST_FILE_NAME)
        self.invalid_train_file_path :str = os.path.join(self.invalid_data_dir,training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path : str = os.path.join(self.invalid_data_dir,training_pipeline.TEST_FILE_NAME)
        self.drift_report_file_path:str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_FILE_NAME
        )