"""
setup.py est un fichier utilisé pour empaqueter et distribuer un projet Python.
Il définit les métadonnées du package et ses dépendances pour faciliter son installation.
"""

from setuptools import setup, find_packages
from typing import List


def get_requirements(filename: str = "requirements.txt") -> List[str]:
    """
    Lit le fichier des dépendances et retourne une liste des packages requis.

    :param filename: Nom du fichier contenant les dépendances.
    :return: Liste des dépendances filtrées.
    """
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip() and line.strip() != "-e ."]
    except FileNotFoundError:
        print(f"⚠️ Fichier {filename} introuvable. Aucune dépendance installée.")
        return []


# Définition du package
setup(
    name="MLOPS Network Security System",  # Nom du projet
    version="0.0.1",  # Version du package
    packages=find_packages(),  # Recherche automatique des packages
    author="smallziz",  # Nom de l'auteur
    author_email="abdoulazizdiouf221@gmail.com",  # Email de l'auteur
    install_requires=get_requirements(),  # Dépendances à installer
    classifiers=[  # Catégories pour PyPI
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Version minimale requise de Python
)
