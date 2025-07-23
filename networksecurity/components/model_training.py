import os 
import sys 
from networksecurity.entity.artifact_entity import ModelTrainingArtifact,Data_Transformation_Artifact
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.Exception_handling.exception import CustomException
from networksecurity.Logging.logger import logging

from networksecurity.utils.utility import save_object,load_object,evaluate_models
from networksecurity.utils.utility import load_numpy_array_data
from networksecurity.utils.ml_utils.classification_metric import get_classification_metric
from networksecurity.utils.ml_utils.model_estimator import NetworkModel
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,

)
from sklearn.model_selection import GridSearchCV
import mlflow
import dagshub
dagshub.init(repo_owner='milan0122', repo_name='network_security', mlflow=True)

class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:Data_Transformation_Artifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)
    def track_mlflow(self,best_model,classification_metric):
            with mlflow.start_run():
                   f1_score = classification_metric.f1_score
                   precision_score = classification_metric.precision_score
                   recall_score = classification_metric.recall_score

                   mlflow.log_metric("f1_score",f1_score)
                   mlflow.log_metric("precision",precision_score)
                   mlflow.log_metric("recall",recall_score)
                   mlflow.sklearn.log_model(best_model,"model")

    def train_model(self,x_train,y_train,x_test,y_test):
        models = {
            "Random Forest":RandomForestClassifier(verbose=1),
            "Decision Tree":DecisionTreeClassifier(),
            "Gradient Boosting":GradientBoostingClassifier(verbose=1),
            "Logistic Regression": LogisticRegression(verbose=1),
            "AdaBoost":AdaBoostClassifier()
        }

        # defining the params
        params = {
            "Decision Tree":{
                'criterion':['gini','entropy','log_loss'],
                'max_features':['sqrt','log2']
            },
            "Random Forest":{
                 'criterion':['gini','entropy','log_loss'],
                 'n_estimators':[4,9,11,25,20]
            },
            "Gradient Boosting":{
                'learning_rate':[.1,.01,.005,.001],
                'subsample':[0.6,0.7,.85],
                'n_estimators':[4,9,11,25,20]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.005],
                'n_estimators':[4,9,11,25,20]
            }
        }

        model_report:dict = evaluate_models(X_train=x_train,X_test=x_test,y_train=y_train,y_test=y_test,models=models,params=params)

    # to get best model score from dict
        best_model_score = max(sorted(model_report.values()))

        # to get best model name from dict
        best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

        best_model = models[best_model_name]
        y_train_pred = best_model.predict(x_train)
        classifcation_train_metric = get_classification_metric(
            y_true=y_train,y_pred=y_train_pred
        )
        # Track the  experiment with mlflow
        self.track_mlflow(best_model,classifcation_train_metric)

        y_test_pred = best_model.predict(x_test)
        classifcation_test_metric = get_classification_metric(
            y_true=y_test,y_pred=y_test_pred
        )

        self.track_mlflow(best_model,classifcation_test_metric)
        #loading the preprocessor file and creating directory 
        preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path,exist_ok=True)

        Network_Model = NetworkModel(preprocessor=preprocessor,model=best_model)
        # saving the object
        save_object(self.model_trainer_config.trained_model_file_path,obj=Network_Model)
        #saving the the best model into final_model
        save_object("final_model/model.pkl",best_model)

        # Model trainer Artifact
        model_trainer_artifact=ModelTrainingArtifact(
            trained_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_metric_artifact=classifcation_train_metric,
            test_metric_artifact=classifcation_test_metric
        )
        logging.info(f"Model trainer artifact:{model_trainer_artifact}")
        return model_trainer_artifact
    def initiate_model_trainer(self)->ModelTrainingArtifact:
        try:
          train_file_path = self.data_transformation_artifact.transformed_train_file_path
          test_file_path = self.data_transformation_artifact.transformed_test_file_path

          #load training array and testing array
          train_arr = load_numpy_array_data(train_file_path)
          test_arr = load_numpy_array_data(test_file_path)
          x_train,y_train,x_test,y_test = (
              train_arr[:,:-1],
              train_arr[:,-1],
              test_arr[:,:-1],
              test_arr[:,-1]
          )
          model_trainer_artifact = self.train_model(x_train,y_train,x_test,y_test)
          return model_trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)