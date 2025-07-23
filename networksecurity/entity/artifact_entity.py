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


@dataclass
class Data_Transformation_Artifact:
    transformed_object_file_path:str
    transformed_train_file_path:str
    transformed_test_file_path:str

@dataclass
class ClassificationMetricArtifact:
    f1_score:float
    precision_score:float
    recall_score:float



    
@dataclass
class ModelTrainingArtifact:
    trained_model_file_path:str
    train_metric_artifact:ClassificationMetricArtifact
    test_metric_artifact:ClassificationMetricArtifact