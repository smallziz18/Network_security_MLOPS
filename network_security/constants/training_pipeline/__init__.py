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

SCHEMA_FILE_PATH = os.path.join("data_schema", "schema.yaml")

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