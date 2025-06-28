from dataclasses import dataclass

'''
usually this entity used for known what will be our input and output
'''
@dataclass
class Data_Ingestion_Artifact:
    train_file_path:str
    test_file_path:str