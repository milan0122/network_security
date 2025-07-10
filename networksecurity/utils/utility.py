import yaml 
from networksecurity.Exception_handling.exception import CustomException
from networksecurity.Logging.logger import logging
import os, sys
import numpy as np 
import dill #commonly used for object serialization and deserialization
import pickle

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

def save_object(file_path:str,obj:object)-> None:
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'wb') as file_obj:
            pickle.dump(obj,file_obj)
    except Exception as e:
        raise CustomException(e,sys) from e