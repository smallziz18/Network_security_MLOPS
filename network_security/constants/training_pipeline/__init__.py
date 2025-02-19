import os
import pandas as pd
import numpy as np
import sys


"""
definition des  constantes pour le training pipeline
"""
TARGET_COLUMN = "Result"
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME: str = "phisingData.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

SCHEMA_FILE_PATH = 'data_schema/schema.yml'

SAVED_MODEL_DIR =os.path.join("saved_models")
MODEL_FILE_NAME = "model.pkl"

"""
Constantes relative a l ingestion des donnes
"""
DATA_INGESTION_COLLECTION_NAME:str = 'NetworkData'
DATA_INGESTION_DATABASE_NAME:str = 'mlops'
DATA_INGESTION_DIR_NAME:str = 'data_ingestion'
DATA_INGESTION_FEATURE_STORE_DIR:str = 'feature_store'
DATA_INGESTED_DIR_NAME:str = 'data_ingested'
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.25


"""
constantes relative a la validation des donnees
"""
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_VALID_DIR: str = "validated"
DATA_VALIDATION_INVALID_DIR: str = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"

