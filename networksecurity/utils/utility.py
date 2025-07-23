import yaml 
from networksecurity.Exception_handling.exception import CustomException
from networksecurity.Logging.logger import logging
import os, sys
import numpy as np 
import dill #commonly used for object serialization and deserialization
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
'''
func to read the yaml file , where the schema of the data define 
'''
def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
        
    except Exception as e:
        raise CustomException(e,sys)
    
'''
func to writing content to yaml file 
    - file_path:str : full path where yaml file will be written
    - content: object: list or dict going to write into yaml file
    - replace :bool : optional argument to check whether the file already exist or not 
'''
def write_yaml_file(file_path:str, content:object,replace:bool=False)-> None:
    try:
        # check the file, if True then delete before overwriting
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w') as file:
            yaml.dump(content,file)
    except Exception as e:
        raise CustomException(e,sys)


def save_numpy_array_data(file_path:str,array:np.array):
    '''
save numpy array data into file
file_path: str location of file to save
array : np.array data to saves
'''
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file:
            np.save(file,array)
    except Exception as e:
        raise CustomException(e,sys) from e 
    
    
def load_numpy_array_data(file_path:str)->np.array:
    try:
        if os.path.exists(file_path):
            with open(file_path,'rb') as file_object:
                return np.load(file_path)
    except Exception as e:
        raise CustomException(e,sys) from e 
    

def save_object(file_path:str,obj:object)-> None:
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as file_obj:
            pickle.dump(obj,file_obj)
    except Exception as e:
        raise CustomException(e,sys) from e
    

def load_object(file_path:str)->object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file :{file_path} does not exists")
        with open(file_path,'rb') as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise CustomException(e,sys) from e
    


# for evaluating the models
def evaluate_models(X_train,y_train,X_test,y_test,models,params):
    try:
        report = {}
        for i in range(len(list(models))):
            model = list(models.values())[i]
            para = params[list(models.keys())[i]]
            logging.info("Hyper tuning the model.......")
            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)
            logging.info("Fitting the model with best params")
            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)
            train_model_score = accuracy_score(y_train,y_train_pred)
            test_model_score = accuracy_score(y_test,y_test_pred)
            report[list(models.keys())[i]] = test_model_score
            return report
    except Exception as e:
        raise CustomException(e,sys)