from networksecurity.entity.artifact_entity import Data_Ingestion_Artifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.Exception_handling.exception import CustomException
from networksecurity.Logging.logger import logging
from networksecurity.entity.artifact_entity import Data_Validation_Artifact
from scipy.stats import ks_2samp
import pandas as pd
import os,sys
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.utility import read_yaml_file,write_yaml_file
class DataValidation:
    def __init__(self,data_ingestion_artifact :Data_Ingestion_Artifact,
                 data_validation_config : DataValidationConfig) :
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e,sys)
    def validate_name_of_columns(self,df:pd.DataFrame)->bool:
        try:
            no_cols = len(self._schema_config)
            logging.info(f"Required number of columns:{no_cols}")
            logging.info(f"Data frame has columns:{len(df.columns)}")
            if len(df.columns) == no_cols:
                return True 
            else:
                return False
        except Exception as e:
            raise CustomException(e,sys)
        
    """
      this func used to check drift in the distribution of the data.
      Meaning that , whether there are some changes in whole dataset or not
      It is not actually like outlier checking, it check flow(pattern) the sample data  against another sample data
      """
    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)-> bool:
        try:
            status = True
            #defining dict
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                # checking whether the two distribution are same or not using Kolmogorov-Smironv Test
                is_sample_dist = ks_2samp(d1,d2)
                #condition
                if threshold <= is_sample_dist.pvalue:
                    #set to false
                    is_found = False
                else:
                    is_found = True
                    status = False
                # report updated
                report.update({
                    column:{
                        "pvalue":float(is_sample_dist.pvalue),
                        "drift_status":is_found
                    }
                })
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            # create directory 
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            #calling function and update the content into yaml file 
            write_yaml_file(file_path=drift_report_file_path,content=report)
        except Exception as e:
            raise CustomException(e,sys)   




    @staticmethod 
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e,sys)
        
        
    def initiate_data_validation(self)->Data_Validation_Artifact:
        try:
            #getting path of train and test
            train_file_path= self.data_ingestion_artifact.train_file_path
            test_file_path= self.data_ingestion_artifact.test_file_path

            #read the data from train and test
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)

            #validate no. of columns
            status = self.validate_name_of_columns(df = train_df)
            if not status:
                error_message = "Train dataframe does not contain all columns\n"
            status = self.validate_name_of_columns(df = test_df)
            if not status:
                error_message = "Test dataframe does not contain all columns\n"


            status = self.detect_dataset_drift(base_df=train_df,current_df=test_df)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)
            train_df.to_csv(
                self.data_validation_config.valid_train_file_path,index=False,header=True
            )
            test_df.to_csv(
                self.data_validation_config.valid_test_file_path,index=False,header=True
            )
            data_validation_artifact = Data_Validation_Artifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.train_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact
        except Exception as e:
            raise CustomException(e,sys)
        