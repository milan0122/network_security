'''
This setup.py file is an essential part of packaging and distributing python projects. 
It is used by setuptools to define the configuration of 
your project, such its metadata, dependencies, and more
'''
from setuptools import find_packages,setup
from typing import List 
def get_requirements()-> List[str]:
    requirement_lst:List[str] = []
    try:
        with open ('requirements.txt','r') as obj_file:
            # read lines from the file
            lines = obj_file.readlines()
            #process each line
            for line in lines:
                requirement = line.strip()
                ## ignore empty lines and - e . 
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)
    except: 
        print('requirements.txt file is not found')
    return requirement_lst

__version__="0.0.1"
REPO_Name="network_security"
AUTHOR_USER_NAME="milan0122"
SRC_REPO="network_security"
AUTHOR_EMAIL="dangi.milan46@gmail.com"

setup(
    name = SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    packages = find_packages(),
    install_requires = get_requirements(),
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_Name}",
)
