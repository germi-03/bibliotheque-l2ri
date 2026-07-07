"""
Module définissant la classe DVD, héritant de DocumentBase.
"""

from src.models.document_base import DocumentBase
from src.models.enums import StatutDocument
from src.exceptions.exceptions_biblio import DocumentIndisponibleError


class DVD(DocumentBase):
    """
    Représente un DVD du catalogue de la bibliothèque.

    Un DVD a une durée d'emprunt courte (5 jours) et une amende
    de retard élevée, car ce sont des supports très demandés.
    """

    DUREE_EMPRUNT_JOURS = 5
    TARIF_AMENDE_JOUR = 200  # en FCFA

    def __init__(self, titre: str, reference: str, duree_minutes: int, realisateur: str) -> None:
        """
        Initialise un DVD.

        :param titre: Titre du film.
        :param reference: Référence unique.
        :param duree_minutes: Durée du film en minutes (doit être > 0).
        :param realisateur: Nom du réalisateur.
        :raises ValueError: Si la durée est invalide ou le réalisateur vide.
        """
        super().__init__(titre, reference)

        if duree_minutes <= 0:
            raise ValueError("La durée du DVD doit être supérieure à 0.")
        if not realisateur or not realisateur.strip():
            raise ValueError("Le réalisateur ne peut pas être vide.")

        self._duree_minutes = duree_minutes
        self._realisateur = realisateur.strip()

    @property
    def duree_minutes(self) -> int:
        return self._duree_minutes

    @property
    def realisateur(self) -> str:
        return self._realisateur

    def emprunter(self) -> None:
        """
        Marque le DVD comme emprunté.

        :raises ValueError: Si le DVD n'est pas disponible.
        """
        if self.statut != StatutDocument.DISPONIBLE:
            raise DocumentIndisponibleError(self.titre, str(self.statut))
        self.statut = StatutDocument.EMPRUNTE

    def calculer_amende(self, jours_retard: int) -> float:
        """
        Calcule l'amende de retard pour un DVD.

        :param jours_retard: Nombre de jours de retard.
        :return: Montant de l'amende en FCFA.
        :raises ValueError: Si jours_retard est négatif.
        """
        if jours_retard < 0:
            raise ValueError("Le nombre de jours de retard ne peut pas être négatif.")
        return jours_retard * self.TARIF_AMENDE_JOUR

    def __str__(self) -> str:
        return (
            f"DVD: {self.titre} réalisé par {self.realisateur} "
            f"({self.duree_minutes} min) — {self.statut}"
        )
