"""
Module définissant les exceptions personnalisées pour la gestion
de la bibliothèque universitaire.
"""


class BibliothequeError(Exception):
    """
    Exception de base pour toutes les erreurs métier liées
    à la gestion de la bibliothèque. Permet d'attraper toutes
    les erreurs spécifiques au projet avec un seul except si besoin.
    """
    pass


class DocumentIndisponibleError(BibliothequeError):
    """
    Levée lorsqu'un utilisateur tente d'emprunter un document
    qui n'est pas dans un statut DISPONIBLE (déjà emprunté,
    réservé, ou perdu).
    """

    def __init__(self, titre_document: str, statut_actuel: str) -> None:
        self.titre_document = titre_document
        self.statut_actuel = statut_actuel
        message = (
            f"Impossible d'emprunter '{titre_document}' : "
            f"statut actuel = {statut_actuel}."
        )
        super().__init__(message)


class AdherentInvalideError(BibliothequeError):
    """
    Levée lorsqu'un adhérent tente une action alors qu'il n'est pas
    autorisé (ex: quota d'emprunts atteint, catégorie invalide,
    identifiant inexistant).
    """

    def __init__(self, identifiant_adherent: str, raison: str) -> None:
        self.identifiant_adherent = identifiant_adherent
        self.raison = raison
        message = (
            f"Adhérent invalide (id={identifiant_adherent}) : {raison}"
        )
        super().__init__(message)


class RetardNonAutoriseError(BibliothequeError):
    """
    Levée lorsqu'un adhérent tente d'emprunter un nouveau document
    alors qu'il a déjà un ou plusieurs retards non régularisés.
    """

    def __init__(self, identifiant_adherent: str, nb_retards: int) -> None:
        self.identifiant_adherent = identifiant_adherent
        self.nb_retards = nb_retards
        message = (
            f"L'adhérent {identifiant_adherent} a {nb_retards} retard(s) "
            f"non régularisé(s). Nouvel emprunt refusé."
        )
        super().__init__(message)