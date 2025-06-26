import logging
import os
from datetime import datetime 
import sys

# creat the file if not exist
logs_dir = os.path.join(os.getcwd(),"logs")
os.makedirs(logs_dir,exist_ok=True)
#this will be name of file of each log generated
LOG_FILE = f"{datetime.now().strftime('%d_%m_%y_%H_%M_%S')}.logs"
# get the current directory and created logs file if not exist
logs_file_path = os.path.join(logs_dir,LOG_FILE)


#configuring basic info to console and file
logging.basicConfig(
    level=logging.INFO,
    format = '[%(asctime)s %(lineno)s %(name)s %(message)s]',
    handlers=[
        logging.FileHandler(logs_file_path),
        logging.StreamHandler(sys.stdout)
    ]

)