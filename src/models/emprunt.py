"""
Module définissant la classe Emprunt, représentant un emprunt
effectué par un adhérent sur un document donné.
"""

from datetime import date, timedelta


class Emprunt:
    """
    Représente un emprunt : lien entre un adhérent, un document,
    et les dates associées (emprunt, retour prévu, retour effectif).

    Cette classe est créée et possédée par un Adherent (composition) :
    son cycle de vie est lié à celui de l'adhérent qui l'a effectué.
    """

    def __init__(self, document, duree_jours: int, date_emprunt: date = None) -> None:
        """
        Initialise un emprunt.

        :param document: L'objet document emprunté (Livre, Revue, DVD, Memoire).
        :param duree_jours: Durée d'emprunt autorisée en jours.
        :param date_emprunt: Date de l'emprunt (aujourd'hui par défaut).
        :raises ValueError: Si duree_jours n'est pas positif.
        """
        if duree_jours <= 0:
            raise ValueError("La durée d'emprunt doit être supérieure à 0.")

        self._document = document
        self._date_emprunt = date_emprunt or date.today()
        self._date_retour_prevue = self._date_emprunt + timedelta(days=duree_jours)
        self._date_retour_effective = None

    @property
    def document(self):
        return self._document

    @property
    def date_emprunt(self) -> date:
        return self._date_emprunt

    @property
    def date_retour_prevue(self) -> date:
        return self._date_retour_prevue

    @property
    def date_retour_effective(self):
        return self._date_retour_effective

    def est_en_retard(self, date_reference: date = None) -> bool:
        """
        Indique si l'emprunt est en retard à une date donnée.

        :param date_reference: Date de référence (aujourd'hui par défaut).
        :return: True si en retard et non encore rendu, False sinon.
        """
        date_reference = date_reference or date.today()
        if self._date_retour_effective is not None:
            return False
        return date_reference > self._date_retour_prevue

    def jours_de_retard(self, date_reference: date = None) -> int:
        """
        Calcule le nombre de jours de retard.

        :param date_reference: Date de référence (aujourd'hui par défaut).
        :return: Nombre de jours de retard (0 si aucun retard).
        """
        date_reference = date_reference or date.today()
        reference = self._date_retour_effective or date_reference
        delta = (reference - self._date_retour_prevue).days
        return max(0, delta)

    def retourner(self, date_retour: date = None) -> None:
        """
        Enregistre le retour effectif du document.

        :param date_retour: Date du retour (aujourd'hui par défaut).
        :raises ValueError: Si le document a déjà été retourné.
        """
        if self._date_retour_effective is not None:
            raise ValueError("Ce document a déjà été retourné.")
        self._date_retour_effective = date_retour or date.today()

    def __str__(self) -> str:
        statut = "Rendu" if self._date_retour_effective else "En cours"
        return (
            f"Emprunt: {self._document.titre} — "
            f"prévu le {self._date_retour_prevue} — {statut}"
        )
