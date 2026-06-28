"""Exception de base de baobab-auth-core.

:spec: BL-010-005, BL-050-003
"""


class BaobabAuthCoreError(Exception):
    """Exception racine de toutes les erreurs métier de baobab-auth-core.

    Toutes les exceptions métier héritent de cette classe afin de permettre
    un traitement générique par les consommateurs de la librairie.

    Chaque exception publique expose trois attributs de **contrat** (ADR-0013) :

    :cvar error_code: Code d'erreur applicatif stable (ex. ``auth.user.not_found``).
    :cvar http_status: Statut HTTP **recommandé** (entier ; jamais une exception web).
    :cvar safe_message: Message générique sans secret, retournable au client.

    :param message: Description détaillée (logs internes), sans secret. Si vide,
        ``safe_message`` est utilisé.
    """

    error_code: str = "auth.error"
    http_status: int = 400
    safe_message: str = "Une erreur d'authentification est survenue."

    def __init__(self, message: str = "") -> None:
        """Initialise l'exception avec un message sans secret.

        Le message détaillé est indépendant de ``safe_message`` (vue publique).

        :param message: Description de l'erreur (logs internes), ou vide.
        """
        super().__init__(message)
        self.message = message
