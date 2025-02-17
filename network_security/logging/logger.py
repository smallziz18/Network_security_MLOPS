import logging
import os
from datetime import datetime

# Nom du fichier log avec un horodatage
LOG_FILE = f"{datetime.now().strftime('%d%m%Y-%H%M%S')}.log"

# Dossier où stocker les logs
logs_dir = os.path.join(os.getcwd(), 'logs')
os.makedirs(logs_dir, exist_ok=True)  # Création du dossier si inexistant

# Chemin complet du fichier log
LOG_FILE_PATH = os.path.join(logs_dir, LOG_FILE)

# Configuration du logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    level=logging.INFO,
    format="%(asctime)s - Ligne %(lineno)d - %(name)s - %(levelname)s - %(message)s",
)


