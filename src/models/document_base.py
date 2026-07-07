"""
Module définissant la classe abstraite DocumentBase, socle commun
à tous les types de documents de la bibliothèque.
"""

from abc import ABC, abstractmethod
from src.models.enums import StatutDocument


class DocumentBase(ABC):
    """
    Classe abstraite représentant un document de la bibliothèque.

    Toute classe concrète héritant de DocumentBase doit implémenter
    les méthodes emprunter() et calculer_amende(), propres aux règles
    spécifiques de chaque type de document.
    """

    def __init__(self, titre: str, reference: str) -> None:
        """
        Initialise un document avec ses attributs communs.

        :param titre: Titre du document.
        :param reference: Référence unique du document (ex: ISBN, code interne).
        :raises ValueError: Si le titre ou la référence est vide.
        """
        if not titre or not titre.strip():
            raise ValueError("Le titre du document ne peut pas être vide.")
        if not reference or not reference.strip():
            raise ValueError("La référence du document ne peut pas être vide.")

        self._titre = titre.strip()
        self._reference = reference.strip()
        self._statut = StatutDocument.DISPONIBLE

    @property
    def titre(self) -> str:
        return self._titre

    @property
    def reference(self) -> str:
        return self._reference

    @property
    def statut(self) -> StatutDocument:
        return self._statut

    @statut.setter
    def statut(self, nouveau_statut: StatutDocument) -> None:
        if not isinstance(nouveau_statut, StatutDocument):
            raise TypeError("Le statut doit être une instance de StatutDocument.")
        self._statut = nouveau_statut

    @abstractmethod
    def emprunter(self) -> None:
        """
        Marque le document comme emprunté selon les règles spécifiques
        du type de document. Doit être implémentée par les classes filles.
        """
        raise NotImplementedError

    @abstractmethod
    def calculer_amende(self, jours_retard: int) -> float:
        """
        Calcule le montant de l'amende en fonction du nombre de jours
        de retard, selon les règles spécifiques du type de document.

        :param jours_retard: Nombre de jours de retard (doit être >= 0).
        :return: Montant de l'amende.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        return f"{self._titre} ({self._reference}) — {self._statut}"