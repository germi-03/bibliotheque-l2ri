"""
Module définissant la classe Revue, héritant de DocumentBase.
"""

from src.models.document_base import DocumentBase
from src.models.enums import StatutDocument


class Revue(DocumentBase):
    """
    Représente une revue (magazine périodique) du catalogue de la bibliothèque.

    Une revue a une durée d'emprunt plus courte qu'un livre (7 jours),
    et une amende de retard plus élevée par jour car la rotation
    doit être rapide pour les autres lecteurs.
    """

    DUREE_EMPRUNT_JOURS = 7
    TARIF_AMENDE_JOUR = 150  # en FCFA

    def __init__(self, titre: str, reference: str, numero: int, periodicite: str) -> None:
        """
        Initialise une revue.

        :param titre: Titre de la revue.
        :param reference: Référence unique.
        :param numero: Numéro de parution (doit être > 0).
        :param periodicite: Périodicité (ex: "Mensuelle", "Hebdomadaire").
        :raises ValueError: Si le numéro est invalide ou la périodicité vide.
        """
        super().__init__(titre, reference)

        if numero <= 0:
            raise ValueError("Le numéro de parution doit être supérieur à 0.")
        if not periodicite or not periodicite.strip():
            raise ValueError("La périodicité ne peut pas être vide.")

        self._numero = numero
        self._periodicite = periodicite.strip()

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def periodicite(self) -> str:
        return self._periodicite

    def emprunter(self) -> None:
        """
        Marque la revue comme empruntée.

        :raises ValueError: Si la revue n'est pas disponible.
        """
        if self.statut != StatutDocument.DISPONIBLE:
            raise ValueError(
                f"La revue '{self.titre}' n'est pas disponible (statut actuel : {self.statut})."
            )
        self.statut = StatutDocument.EMPRUNTE

    def calculer_amende(self, jours_retard: int) -> float:
        """
        Calcule l'amende de retard pour une revue.

        :param jours_retard: Nombre de jours de retard.
        :return: Montant de l'amende en FCFA.
        :raises ValueError: Si jours_retard est négatif.
        """
        if jours_retard < 0:
            raise ValueError("Le nombre de jours de retard ne peut pas être négatif.")
        return jours_retard * self.TARIF_AMENDE_JOUR

    def __str__(self) -> str:
        return f"Revue: {self.titre} n°{self.numero} ({self.periodicite}) — {self.statut}"