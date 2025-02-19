import os
import sys
import pandas as pd
import numpy as np
from typing import List, Tuple
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from network_security.constants.training_pipeline import TARGET_COLUMN, DATA_TRANSFORMATION_IMPUTER_PARAMS
from network_security.logging.logger import logging
from network_security.components.data_validation import DataValidation
from network_security.constants import *
from network_security.exceptions.exception import NetworkSecurityException
from network_security.logging import logger
from network_security.entity.config_entity import DataTransformationConfig
from network_security.entity.artifact_entity import DataTransformationArtifact, DataValidationArtifact
from network_security.utils.main_utils.utils import save_numpy_array_data, save_object


class DataTransformation:
    """
    Classe responsable de la transformation des données avant l'entraînement des modèles.

    Attributs :
        data_validation_artifact (DataValidationArtifact) : Objet contenant les chemins des fichiers validés.
        data_transformation_config (DataTransformationConfig) : Configuration de la transformation des données.
    """

    def __init__(self, data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        """
        Lit un fichier CSV et retourne un DataFrame pandas.

        Args:
            file_path (str): Chemin du fichier CSV.

        Returns:
            pd.DataFrame: Données chargées.

        Raises:
            NetworkSecurityException: En cas d'échec de lecture du fichier.
        """
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    @staticmethod
    def get_data_transformer_object() -> Pipeline:
        """
        Initialise un Pipeline de transformation des données basé sur un KNNImputer.

        Returns:
            Pipeline: Pipeline de transformation des données.

        Raises:
            NetworkSecurityException: En cas d'erreur lors de l'initialisation du pipeline.
        """
        logging.info("Initialisation du pipeline de transformation des données...")
        try:
            imputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"KNNImputer initialisé avec {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
            return Pipeline([("imputer", imputer)])
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        """
        Exécute la transformation des données et enregistre les résultats.

        Returns:
            DataTransformationArtifact: Objet contenant les chemins des fichiers transformés.

        Raises:
            NetworkSecurityException: En cas d'erreur durant la transformation.
        """
        logging.info("Début de la transformation des données...")

        try:
            # Chargement des données validées
            train_df = self.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = self.read_data(self.data_validation_artifact.valid_test_file_path)

            # Vérification que la colonne cible existe
            if TARGET_COLUMN not in train_df.columns or TARGET_COLUMN not in test_df.columns:
                logging.info(
                    f"La colonne cible '{TARGET_COLUMN}' est absente des données."
                )

            # Séparation des features et de la cible
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN])
            target_feature_train_df = train_df[TARGET_COLUMN].replace(-1, 0)

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN])
            target_feature_test_df = test_df[TARGET_COLUMN].replace(-1, 0)

            # Transformation des données
            preprocessor = self.get_data_transformer_object()
            preprocessor.fit(input_feature_train_df)

            transformed_input_train_feature = preprocessor.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor.transform(input_feature_test_df)

            # Création des tableaux combinés (features + target)
            train_arr = np.c_[transformed_input_train_feature, target_feature_train_df.to_numpy()]
            test_arr = np.c_[transformed_input_test_feature, target_feature_test_df.to_numpy()]

            # Sauvegarde des données transformées
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, test_arr)

            # Sauvegarde du préprocesseur
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
            save_object("final_model/preprocessor.pkl", preprocessor)

            logging.info("Transformation des données terminée avec succès.")

            # Création de l'objet artifact contenant les chemins des fichiers transformés
            return DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

        except Exception as e:
            raise NetworkSecurityException(e, sys)
