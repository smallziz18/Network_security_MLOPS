import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import sys
import json
from dotenv import load_dotenv
import certifi
import pandas as pd
import numpy as np
from network_security.logging import logger
from network_security.exceptions.exception import NetworkSecurityException

# Certificat SSL pour MongoDB Atlas
ca = certifi.where()

# Charger les variables d'environnement
load_dotenv()
MONGO_URI = os.getenv("MONGO_DB_URL")


class DataExtractionAndPusher:
    """
    Classe pour extraire des données CSV et les insérer dans MongoDB.
    """

    def __init__(self, database: str, collection: str, mongo_uri: str = MONGO_URI):
        """
        Initialise la connexion à MongoDB et sélectionne la base de données et la collection.

        :param database: Nom de la base de données MongoDB.
        :param collection: Nom de la collection MongoDB.
        :param mongo_uri: URI de connexion MongoDB (par défaut, récupéré depuis les variables d'environnement).
        """
        self.database_name = database
        self.collection_name = collection
        self.mongo_uri = mongo_uri

        try:
            self.mongo_client = MongoClient(self.mongo_uri, server_api=ServerApi("1"), tlsCAFile=ca)
            self.database = self.mongo_client[self.database_name]
            self.collection = self.database[self.collection_name]
            logger.logging.info(f"Connexion établie avec MongoDB: {self.database_name}.{self.collection_name}")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def csv_to_json_converter(self, filepath: str) -> list:
        """
        Convertit un fichier CSV en liste de dictionnaires JSON.

        :param filepath: Chemin du fichier CSV à convertir.
        :return: Liste des enregistrements convertis.
        """
        try:
            logger.logging.info(f"Conversion du fichier CSV en JSON: {filepath}")
            dataframe = pd.read_csv(filepath)
            dataframe.reset_index(inplace=True, drop=True)
            records = json.loads(dataframe.to_json(orient="records"))
            logger.logging.info(f"Conversion réussie. Nombre d'enregistrements: {len(records)}")
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_dataframe(self, dataframe: pd.DataFrame):
        """
        Insère un DataFrame Pandas dans la collection MongoDB.

        :param dataframe: DataFrame contenant les données à insérer.
        """
        try:
            logger.logging.info(f"Insertion de {len(dataframe)} enregistrements dans MongoDB...")
            records = dataframe.to_dict(orient="records")
            self.collection.insert_many(records)
            logger.logging.info("Insertion réussie dans MongoDB.")
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        finally:
            self.mongo_client.close()  # Fermeture de la connexion MongoDB




if __name__ == "__main__":
    try:
        data_pusher = DataExtractionAndPusher(database="mlops", collection="NetworkData", mongo_uri=MONGO_URI)
        records = data_pusher.csv_to_json_converter("Network_Data/phisingData.csv")
        df = pd.DataFrame(records)
        data_pusher.insert_dataframe(df)
    except NetworkSecurityException as nse:
        logger.logging.info(nse)

