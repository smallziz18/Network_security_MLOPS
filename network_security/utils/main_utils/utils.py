import yaml
import os
import sys
import numpy as np
import pickle
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

from network_security.logging.logger import logging
from network_security.exceptions.exception import NetworkSecurityException


def read_yaml(file_path: str) -> dict:
    """
    Lit un fichier YAML et retourne son contenu sous forme de dictionnaire.

    Args:
        file_path (str): Chemin du fichier YAML.

    Returns:
        dict: Contenu du fichier YAML.

    Raises:
        NetworkSecurityException: Si la lecture du fichier échoue.
    """
    try:
        with open(file_path, "r") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    """
    Écrit un dictionnaire dans un fichier YAML.

    Args:
        file_path (str): Chemin du fichier YAML.
        content (object): Contenu à écrire dans le fichier.
        replace (bool, optionnel): Remplace le fichier s'il existe déjà (défaut : False).

    Raises:
        NetworkSecurityException: En cas d'erreur d'écriture.
    """
    try:
        if replace and os.path.exists(file_path):
            os.remove(file_path)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)


def save_numpy_array_data(file_path: str, array: np.ndarray):
    """
    Sauvegarde un tableau NumPy dans un fichier.

    Args:
        file_path (str): Chemin du fichier de sauvegarde.
        array (np.ndarray): Tableau NumPy à sauvegarder.

    Raises:
        NetworkSecurityException: En cas d'erreur de sauvegarde.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def load_numpy_array_data(file_path: str) -> np.ndarray:
    """
    Charge un tableau NumPy depuis un fichier.

    Args:
        file_path (str): Chemin du fichier contenant les données.

    Returns:
        np.ndarray: Tableau NumPy chargé.

    Raises:
        NetworkSecurityException: En cas d'erreur de lecture.
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj, allow_pickle=True)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def save_object(file_path: str, obj: object) -> None:
    """
    Sauvegarde un objet Python dans un fichier en utilisant Pickle.

    Args:
        file_path (str): Chemin du fichier de sauvegarde.
        obj (object): Objet à sauvegarder.

    Raises:
        NetworkSecurityException: En cas d'erreur de sauvegarde.
    """
    try:
        logging.info("Sauvegarde de l'objet en cours...")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Objet sauvegardé avec succès.")
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def load_object(file_path: str) -> object:
    """
    Charge un objet Python à partir d'un fichier Pickle.

    Args:
        file_path (str): Chemin du fichier contenant l'objet.

    Returns:
        object: Objet chargé.

    Raises:
        NetworkSecurityException: En cas d'erreur de lecture.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Le fichier {file_path} n'existe pas.")
        with open(file_path, "rb") as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def evaluate_models(X_train, y_train, X_test, y_test, models: dict, param: dict) -> dict:
    """
    Évalue plusieurs modèles en optimisant leurs hyperparamètres avec GridSearchCV.

    Args:
        X_train (np.ndarray): Données d'entraînement.
        y_train (np.ndarray): Cibles d'entraînement.
        X_test (np.ndarray): Données de test.
        y_test (np.ndarray): Cibles de test.
        models (dict): Dictionnaire contenant les modèles à entraîner.
        param (dict): Dictionnaire des hyperparamètres associés aux modèles.

    Returns:
        dict: Scores R² des modèles sur les données de test.

    Raises:
        NetworkSecurityException: En cas d'erreur lors de l'entraînement ou de l'évaluation.
    """
    try:
        report = {}

        for model_name, model in models.items():
            if model_name not in param:
                logging.warning(f"Aucun paramètre d'optimisation trouvé pour {model_name}. Utilisation des paramètres par défaut.")
                gs = None
            else:
                gs = GridSearchCV(model, param[model_name], cv=3)
                gs.fit(X_train, y_train)
                model.set_params(**gs.best_params_)

            model.fit(X_train, y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_score = r2_score(y_train, y_train_pred)
            test_score = r2_score(y_test, y_test_pred)

            logging.info(f"Modèle {model_name} - R² entraînement : {train_score:.4f}, R² test : {test_score:.4f}")

            report[model_name] = test_score

        return report

    except Exception as e:
        raise NetworkSecurityException(e, sys)
