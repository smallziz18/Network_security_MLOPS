import pandas as pd
from pymongo import MongoClient
import os

from network_security.exceptions.exception import NetworkSecurityException
from network_security.logging import logger
from push_data import DataExtractionAndPusher

# Configuration de MongoDB (locale ou distante)
MONGO_URI = "mongodb://localhost:27017/"

if __name__ == "__main__":
    try:
        # Initialisation de l'extracteur de données
        data_pusher = DataExtractionAndPusher(database="ai", collection="NetworkData", mongo_uri=MONGO_URI)

        # Vérification de l'existence du fichier CSV
        csv_path = "Network_Data/phisingData.csv"
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Le fichier '{csv_path}' est introuvable.")

        logger.logging.info(f"Chargement du fichier: {csv_path}")

        # Conversion du CSV en JSON
        records = data_pusher.csv_to_json_converter(csv_path)
        df = pd.DataFrame(records)

        # Insertion des données dans MongoDB
        data_pusher.insert_dataframe(df)

        logger.logging.info(f"{len(records)} enregistrements insérés avec succès dans MongoDB.")
        print(f"✅ {len(records)} enregistrements insérés avec succès.")

    except NetworkSecurityException as nse:
        logger.logging.info(f"Erreur de sécurité réseau: {nse}")
    except FileNotFoundError as fnf:
        logger.logging.info(fnf)
    except Exception as e:
        logger.logging.info(f"Erreur inattendue: {e}")
