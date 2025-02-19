from network_security.entity.artifact_entity import DataIngestArtifact
from network_security.entity.config_entity import DataValidationConfig
from network_security.exceptions.exception import NetworkSecurityException
from network_security.logging.logger import logging
from network_security.entity.artifact_entity import DataValidationArtifact
from scipy.stats import ks_2samp
import os, sys, pandas as pd
from network_security.constants.training_pipeline import SCHEMA_FILE_PATH
from network_security.utils.main_utils.utils import write_yaml_file, read_yaml


class DataValidation:
    """
    Classe responsable de la validation des données dans le pipeline de traitement.

    Cette classe effectue plusieurs tâches essentielles :
    - Chargement des données d'entraînement et de test.
    - Validation du nombre de colonnes en fonction du schéma attendu.
    - Détection de la dérive des données entre l'ensemble d'entraînement et l'ensemble de test.
    - Sauvegarde des fichiers validés et génération d'un rapport de dérive.

    Attributs :
        data_ingestion_artifact (DataIngestArtifact) : Objet contenant les chemins des fichiers d'entraînement et de test.
        data_validation_config (DataValidationConfig) : Objet contenant les chemins de stockage des fichiers validés et du rapport.
        _schema_config (dict) : Schéma des données chargé depuis un fichier YAML.
    """

    def __init__(self, data_ingestion_artifact: DataIngestArtifact,
                 data_validation_config: DataValidationConfig):
        """
        Initialise la classe avec les configurations et charge le schéma des données.

        Args:
            data_ingestion_artifact (DataIngestArtifact) : Objet contenant les fichiers d'entraînement et de test.
            data_validation_config (DataValidationConfig) : Objet contenant les répertoires de stockage des fichiers validés.
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        """
        Charge un fichier CSV en un DataFrame Pandas.

        Args:
            file_path (str) : Chemin du fichier CSV.

        Returns:
            pd.DataFrame : Données chargées sous forme de DataFrame.

        Raises:
            NetworkSecurityException : En cas d'erreur de lecture du fichier.
        """
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        """
        Vérifie si le nombre de colonnes correspond au schéma attendu.

        Args:
            dataframe (pd.DataFrame) : Données à valider.

        Returns:
            bool : True si le nombre de colonnes est correct, sinon False.

        Raises:
            NetworkSecurityException : En cas d'erreur de validation.
        """
        try:
            expected_columns = len(self._schema_config["columns"])
            actual_columns = len(dataframe.columns)
            logging.info(f"Nombre de colonnes requis : {expected_columns}")
            logging.info(f"Nombre de colonnes dans le fichier : {actual_columns}")
            return expected_columns == actual_columns
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def detect_dataset_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold=0.05) -> bool:
        """
        Détecte la dérive des données entre deux ensembles à l'aide du test de Kolmogorov-Smirnov.

        Args:
            base_df (pd.DataFrame) : Données de référence (ex: train).
            current_df (pd.DataFrame) : Données actuelles à comparer (ex: test).
            threshold (float, optionnel) : Seuil de p-value pour détecter une dérive (défaut : 0.05).

        Returns:
            bool : True si aucune dérive n'est détectée, False sinon.

        Raises:
            NetworkSecurityException : En cas d'erreur lors du calcul.
        """
        try:
            status = True
            report = {}

            for column in base_df.columns:
                d1 = base_df[column].dropna()
                d2 = current_df[column].dropna()

                if d1.empty or d2.empty:
                    logging.warning(f"Colonne {column} vide dans l'un des ensembles. Ignorée.")
                    continue

                ks_test = ks_2samp(d1, d2)
                drift_detected = ks_test.pvalue < threshold

                report[column] = {
                    "p_value": float(ks_test.pvalue),
                    "drift_detected": drift_detected
                }

                if drift_detected:
                    status = False

            drift_report_file_path = self.data_validation_config.drift_report_file_path
            os.makedirs(os.path.dirname(drift_report_file_path), exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path, content=report)

            return status
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        """
        Exécute l'ensemble du processus de validation des données.

        - Charge les fichiers train et test.
        - Valide le nombre de colonnes.
        - Détecte la dérive des données.
        - Sauvegarde les fichiers validés.

        Returns:
            DataValidationArtifact : Résultat de la validation des données.

        Raises:
            NetworkSecurityException : En cas d'erreur dans le processus.
        """
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            train_df = self.read_data(train_file_path)
            test_df = self.read_data(test_file_path)

            # Validation du nombre de colonnes
            if not self.validate_number_of_columns(train_df):
                logging.info("Le fichier d'entraînement n'a pas le bon nombre de colonnes.", sys)
            if not self.validate_number_of_columns(test_df):
              logging.info("Le fichier de test n'a pas le bon nombre de colonnes.", sys)

            # Détection de la dérive des données
            validation_status = self.detect_dataset_drift(base_df=train_df, current_df=test_df)

            # Création des répertoires pour stocker les fichiers validés
            os.makedirs(os.path.dirname(self.data_validation_config.valid_train_file_path), exist_ok=True)

            train_df.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            test_df.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)

            # Création de l'objet DataValidationArtifact
            return DataValidationArtifact(
                validation_status=validation_status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys)
