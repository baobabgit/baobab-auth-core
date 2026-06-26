"""Exception de base de baobab-auth-core.

:spec: BL-010-005
"""


class BaobabAuthCoreError(Exception):
    """Exception racine de toutes les erreurs métier de baobab-auth-core.

    Toutes les exceptions métier héritent de cette classe afin de permettre
    un traitement générique par les consommateurs de la librairie.

    :param message: Description de l'erreur, sans secret.
    """

    def __init__(self, message: str = "") -> None:
        """Initialise l'exception avec un message sans secret.

        :param message: Description de l'erreur.
        """
        super().__init__(message)
        self.message = message
