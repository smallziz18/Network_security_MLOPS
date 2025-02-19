from datetime import datetime
import os
from network_security.constants import training_pipeline

class TrainingPipelineConfig:
    """
    Configuration du pipeline d'entraînement.

    Cette classe définit les chemins et noms utilisés pour stocker les artefacts
    et suivre l'évolution du pipeline.
    """

    def __init__(self, timestamp: str = None):
        """
        Initialise la configuration du pipeline.

        :param timestamp: (optionnel) Timestamp unique pour identifier l'exécution.
        """
        self.timestamp = timestamp if timestamp else datetime.now().strftime("%d%m%Y%H%M%S")
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name, self.timestamp)


class DataIngestionConfig:
    """
    Configuration du module d'ingestion des données.

    Cette classe définit les chemins des fichiers utilisés lors de la récupération
    et du stockage des données pour l'entraînement et les tests.
    """

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        """
        Initialise la configuration d'ingestion des données.

        :param training_pipeline_config: Instance de TrainingPipelineConfig.
        """
        self.data_ingestion_dir = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_INGESTION_DIR_NAME,
        )

        self.feature_store_file_path = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR,
            training_pipeline.FILE_NAME
        )

        self.training_file_path = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTED_DIR_NAME,
            training_pipeline.TRAIN_FILE_NAME
        )

        self.test_file_path = os.path.join(
            self.data_ingestion_dir,
            training_pipeline.DATA_INGESTED_DIR_NAME,
            training_pipeline.TEST_FILE_NAME
        )

        self.train_test_split_ratio = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name = training_pipeline.DATA_INGESTION_DATABASE_NAME


class DataValidationConfig:
    """
    Classe de configuration pour la validation des données dans un pipeline d'entraînement.

    Cette classe gère les chemins des répertoires et fichiers nécessaires à la validation des données
    dans le cadre d'un pipeline d'entraînement de machine learning. Elle prend une instance de
    `TrainingPipelineConfig` pour définir les répertoires liés à la validation des données.

    Attributs:
        data_validation_dir (str): Répertoire principal pour la validation des données.
        valid_data_dir (str): Répertoire contenant les données valides.
        invalid_data_dir (str): Répertoire contenant les données invalides.
        valid_train_file_path (str): Chemin du fichier d'entraînement valide.
        valid_test_file_path (str): Chemin du fichier de test valide.
        invalid_train_file_path (str): Chemin du fichier d'entraînement invalide.
        invalid_test_file_path (str): Chemin du fichier de test invalide.
        drift_report_file_path (str): Chemin du fichier de rapport de dérive des données.
    """

    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        """
        Initialiser les chemins des répertoires et fichiers de validation des données.

        Args:
            training_pipeline_config (TrainingPipelineConfig): Une instance de `TrainingPipelineConfig`
            qui fournit les chemins des répertoires et fichiers nécessaires pour l'entraînement.

        """
        self.data_validation_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,
            training_pipeline.DATA_VALIDATION_DIR_NAME
        )
        self.valid_data_dir: str = os.path.join(self.data_validation_dir, training_pipeline.DATA_VALIDATION_VALID_DIR)
        self.invalid_data_dir: str = os.path.join(self.data_validation_dir,
                                                  training_pipeline.DATA_VALIDATION_INVALID_DIR)
        self.valid_train_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path: str = os.path.join(self.valid_data_dir, training_pipeline.TEST_FILE_NAME)
        self.invalid_train_file_path: str = os.path.join(self.invalid_data_dir, training_pipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path: str = os.path.join(self.invalid_data_dir, training_pipeline.TEST_FILE_NAME)
        self.drift_report_file_path: str = os.path.join(
            self.data_validation_dir,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_DIR,
            training_pipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME,
        )
