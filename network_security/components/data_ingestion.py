import os
import sys
import pymongo
import pandas as pd
import numpy as np
from typing import List, Tuple
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv

from network_security.exceptions.exception import NetworkSecurityException
from network_security.logging import logger
from network_security.entity.config_entity import DataIngestionConfig
from network_security.entity.artifact_entity import DataIngestArtifact

# Chargement des variables d'environnement
load_dotenv()

MONGO_URI = os.getenv("MONGO_DB_URL")


class DataIngestion:
    """
    Classe responsable de l'ingestion des données depuis MongoDB,
    du stockage des features et du split en jeu d'entraînement et de test.
    """

    def __init__(self, data_ingestion_config: DataIngestionConfig):
        """
        Initialise la configuration de l'ingestion.

        :param data_ingestion_config: Instance de DataIngestionConfig contenant les chemins de stockage.
        """
        self.data_ingestion_config = data_ingestion_config
        self.mongo_client = None

    def export_collection_as_dataframe(self)->pd.DataFrame :
        """
        Exporte une collection MongoDB en DataFrame pandas.

        :return: DataFrame contenant les données extraites.
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name

            self.mongo_client = pymongo.MongoClient(MONGO_URI)
            collection = self.mongo_client[database_name][collection_name]

            data = list(collection.find({}))
            if not data:
                raise ValueError("La collection est vide ou inaccessible.")

            df = pd.DataFrame(data)
            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)

            df.replace('na', np.nan, inplace=True)

            logger.logging.info(f"✅ Données extraites de {database_name}.{collection_name}, shape: {df.shape}")

            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def export_data_to_feature_store(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Sauvegarde le DataFrame dans un fichier CSV en tant que Feature Store.

        :param dataframe: DataFrame contenant les données à stocker.
        :return: DataFrame enregistré.
        """
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            os.makedirs(os.path.dirname(feature_store_file_path), exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)

            logger.logging.info(f"✅ Données sauvegardées dans le Feature Store: {feature_store_file_path}")

            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def split_data_as_train_test(self, dataframe: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Sépare les données en jeu d'entraînement et de test.

        :param dataframe: DataFrame complet à diviser.
        :return: Tuple (train_set, test_set)
        """
        try:
            train_set, test_set = train_test_split(
                dataframe,
                test_size=self.data_ingestion_config.train_test_split_ratio,
                random_state=42  # Fixer la seed pour la reproductibilité
            )

            logger.logging.info(f"📊 Taille du Train Set: {len(train_set)}, Test Set: {len(test_set)}")

            # Sauvegarde des fichiers
            os.makedirs(os.path.dirname(self.data_ingestion_config.training_file_path), exist_ok=True)
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.test_file_path, index=False, header=True)

            logger.logging.info("✅ Jeux d'entraînement et de test sauvegardés avec succès.")

            return train_set, test_set

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def ingest_data(self):
        """
        Exécute l'ingestion complète des données :
        - Récupération depuis MongoDB
        - Sauvegarde dans le Feature Store
        - Séparation en jeu d'entraînement et de test
        """
        try:
            logger.logging.info("🚀 Début du processus d'ingestion des données...")

            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_to_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)

            data_ingestion_artifact = DataIngestArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                         test_file_path=self.data_ingestion_config.test_file_path)


            logger.logging.info("🎯 Ingestion des données terminée avec succès.")
            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
