# End-to-End Network Security Project

## Overview

This project is an end-to-end solution for detecting malicious network behaviors using machine learning techniques. The project incorporates **data ingestion**, **data validation**, **model training**, and **deployment** via a REST API. It uses multiple **classification algorithms** (Random Forest, Decision Tree, Gradient Boosting, Logistic Regression, and AdaBoost), and it automatically selects the best model after hyperparameter tuning. The solution is fully integrated with **CI/CD pipelines**, **Docker**, **AWS EC2**, and **S3** for efficient deployment and storage.

## Table of Contents

- [Features](#-features)
- [Project Structure](#-project-structure)
- [Technologies Used](#-technologies-used)
- [Setup & Installation](#️-setup--installation)
- [ML Pipeline Stages](#-ml-pipeline-stages)
- [Model Performance](#-model-performance)
- [FastAPI Service](#-fastapi-service)
- [CI/CD with GitHub Actions & AWS EC2](#️-cicd-with-github-actions--aws-ec2)
- [Artifacts & S3 Integration](#-artifacts--s3-integration)
---

##  Features

- Data ingestion from **MongoDB Atlas**.
- Data validation and transformation with **KNN Imputer**.
- Model training with multiple classifiers: **Random Forest**, **Decision Tree**, **Gradient Boosting**, **Logistic Regression**, and **AdaBoost**.
- Automated **hyperparameter tuning** and **model selection**.
- **Model evaluation** using **F1-score**, **Precision**, **Recall**, and **Accuracy**.
- Model deployment using **FastAPI**.
- Dockerized application for easy deployment.
- **S3** integration for storing important files like trained models, logs, and artifacts.
- Continuous **CI/CD pipeline** with **GitHub Actions** and **AWS EC2**.

---

## Project Structure
network_security_project
.
├── Artifacts
├── Network_Data
│   └── phisingData.csv
├── README.md
├── app.py
├── data_schema
│   └── schema.yaml
├── dockerfile
├── final_model
│   ├── model.pkl
│   └── preprocessor.pkl
├── networksecurity
│   ├── Exception_handling
│   ├── Logging
│   ├── __init__.py
│   ├── cloud
│   ├── components
│   │   ├── __init__.py
│   │   ├── data_ingestion.py
│   │   ├── data_transformation.py
│   │   ├── data_validation.py
│   │   └── model_training.py
│   ├── constants
│   ├── entity
│   │   ├── artifact_entity.py
│   │   └── config_entity.py
│   ├── pipeline
│   │   └── training_pipeline.py
│   └── utils
│       ├── ml_utils
│       └── utility.py
├── notebooks
├── push_data.py
├── requirements.txt
├── setup.py
├── templates
│   └── index.html
└── valid_data
    └── test.csv             
---

##  Technologies Used

- **Python 3.10+**
- **FastAPI** for API deployment
- **Scikit-learn** for machine learning
- **Pandas**, **NumPy** for data manipulation
- **MLflow** and **DVC** for model tracking
- **MongoDB Atlas** for data storage
- **Docker** for containerization
- **AWS** (EC2, ECR, S3) for deployment and storage
- **GitHub Actions** for CI/CD pipelines

---

## ⚙️ Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/network_security.git
   cd network_security

2. **Create a virtual environment and activate it**
    ```bash
    python -m venv venv
    source venv/bin/activate   
3. **Install dependencies**
    ```bash
    pip install -r requirements.txt

4. **Configure MongoDB in .env and Setup github secrets:**
    - MONGO_URI=mongodb+srv://<your-atlas-uri>
    - AWS_ACCESS_KEY_ID=AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY=AWS_SECRET_ACCESS_KEY
    - AWS_REGION = your region
    - AWS_ECR_LOGIN_URI = Create ECR repo and you will get and copy URI
    - ECR_REPOSITORY_NAME = networkssecurity
---
## ML Pipeline Stages
The ML pipeline consists of the following stages, all implemented as modular components:
- **Data Ingestion:** Data is ingested from MongoDB Atlas and saved locally for processing.
- **Data Validation**:Ensures data integrity and checks for inconsistencies.
Performs drift detection to spot any issues in the dataset over time.
- **Data Transformation**:Applies KNN Imputer to handle missing values.Transforms data into a format suitable for model training.
- **Model Training and Evaluation**:Trains multiple models using different classifiers: Random Forest, Decision Tree, Gradient Boosting, Logistic Regression, and AdaBoost. Hyperparameter tuning is performed using cross-validation to find the best model.
---
## Model Performance
Quick summary of bestmodel performance 
|Artifact|f1 score| precission score|recall score |
|---|---|---|---|
|Train |0.991| 0.989|0.993|
|Test|0.973|0.967|0.979|
---
## 🌐 FastAPI Service
    You can serve predictions using FastAPI:
    ```bash
        uvicorn app:app --host 0.0.0.0 --port 8080
---
## CI/CD with Github Actions & AWS EC2
### Continuous Integration (CI)
- Automatically pull the latest code from the repository.
- Ensure code follows style guidelines using linting
### Continuous Delivery (CD)
- Configure AWS access using secrets stored in GitHub.
- Login to Amazon Elastic Container Registry (ECR) to push the Docker image.
- Build a Docker image for the app and tag it with latest.
- Push the built Docker image to the Amazon ECR repository.
### Continuous Deployment (CD)
- Pull the latest Docker image from ECR.
- Deploy the Docker image to a self-hosted EC2 instance running on port 8080.
- Remove unused Docker containers and images to save space.
---
## Artifacts & S3 Integration
In addition to local artifact storage, important files (e.g., trained models, logs, and other outputs) are pushed to an S3 bucket for reliable long-term storage and easy access.
Files such as model.pkl, logs/, and evaluation reports are uploaded to your configured S3 bucket during training.

---
Note: Some important command for Docker Setup In EC2 commands to be Executed
```bash
sudo apt-get update -y # optional 
sudo apt-get upgrade #required
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker