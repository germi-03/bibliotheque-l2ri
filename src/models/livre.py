"""
Module définissant la classe Livre, héritant de DocumentBase.
"""

from src.models.document_base import DocumentBase
from src.models.enums import StatutDocument
from src.exceptions.exceptions_biblio import DocumentIndisponibleError


class Livre(DocumentBase):
    """
    Représente un livre du catalogue de la bibliothèque.

    Un livre peut être emprunté pour une durée standard de 21 jours.
    L'amende de retard est calculée à un tarif fixe par jour.
    """

    DUREE_EMPRUNT_JOURS = 21
    TARIF_AMENDE_JOUR = 100  # en FCFA

    def __init__(self, titre: str, reference: str, auteur: str, nb_pages: int) -> None:
        """
        Initialise un livre.

        :param titre: Titre du livre.
        :param reference: Référence unique (ex: ISBN).
        :param auteur: Auteur du livre.
        :param nb_pages: Nombre de pages (doit être > 0).
        :raises ValueError: Si l'auteur est vide ou le nombre de pages invalide.
        """
        super().__init__(titre, reference)

        if not auteur or not auteur.strip():
            raise ValueError("L'auteur du livre ne peut pas être vide.")
        if nb_pages <= 0:
            raise ValueError("Le nombre de pages doit être supérieur à 0.")

        self._auteur = auteur.strip()
        self._nb_pages = nb_pages

    @property
    def auteur(self) -> str:
        return self._auteur

    @property
    def nb_pages(self) -> int:
        return self._nb_pages

    def emprunter(self) -> None:
        """
        Marque le livre comme emprunté.

        :raises ValueError: Si le livre n'est pas disponible.
        """
        if self.statut != StatutDocument.DISPONIBLE:
            raise DocumentIndisponibleError(self.titre, str(self.statut))
        self.statut = StatutDocument.EMPRUNTE

    def calculer_amende(self, jours_retard: int) -> float:
        """
        Calcule l'amende de retard pour un livre.

        :param jours_retard: Nombre de jours de retard.
        :return: Montant de l'amende en FCFA.
        :raises ValueError: Si jours_retard est négatif.
        """
        if jours_retard < 0:
            raise ValueError("Le nombre de jours de retard ne peut pas être négatif.")
        return jours_retard * self.TARIF_AMENDE_JOUR

    def __str__(self) -> str:
        return f"Livre: {self.titre} par {self.auteur} ({self.nb_pages} pages) — {self.statut}"