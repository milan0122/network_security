from dataclasses import dataclass

'''
usually this entity used for known what will be our input and output
'''
@dataclass
class Data_Ingestion_Artifact:
    train_file_path:str
    test_file_path:str

@dataclass
class Data_Validation_Artifact:
    validation_status :bool
    valid_train_file_path:str
    valid_test_file_path:str
    invalid_train_file_path:str
    invalid_test_file_path:str
    drift_report_file_path:str
