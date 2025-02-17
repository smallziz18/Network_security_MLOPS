import sys
from network_security.logging import logger



class NetworkSecurityException(Exception):
    """
    Exception personnalisée pour la gestion des erreurs liées à la sécurité réseau.

    Cette classe capture automatiquement le fichier et la ligne où l'exception a été levée,
    facilitant ainsi le débogage.
    """

    def __init__(self, error_message: Exception, error_detail: sys):
        """
        Initialise l'exception avec un message d'erreur et des détails supplémentaires.

        :param error_message: Message décrivant l'erreur.
        :param error_detail: Objet sys contenant les détails de l'exception.
        """
        super().__init__(error_message)  # Appelle le constructeur parent

        # Récupération des détails de l'exception en cours
        _, _, exc_tb = error_detail.exc_info()

        # Vérification si l'erreur contient bien un traceback
        if exc_tb is not None:
            self.lineno = exc_tb.tb_lineno  # Numéro de la ligne où l'erreur a été levée
            self.filename = exc_tb.tb_frame.f_code.co_filename  # Nom du fichier source
        else:
            self.lineno = None
            self.filename = "Inconnu"

        # Construction du message d'erreur détaillé
        self.error_message = f"{error_message} (Fichier: {self.filename}, Ligne: {self.lineno})"

    def __str__(self):
        """
        Retourne une représentation textuelle de l'exception.

        :return: Message d'erreur détaillé.
        """
        return self.error_message




















