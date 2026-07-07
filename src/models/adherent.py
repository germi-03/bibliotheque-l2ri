"""
Module définissant la classe Adherent.
"""

from src.models.enums import CategorieAdherent
from src.models.emprunt import Emprunt
from src.exceptions.exceptions_biblio import AdherentInvalideError, RetardNonAutoriseError


class Adherent:
    """
    Représente un adhérent de la bibliothèque.

    Un Adherent crée et possède son propre historique d'Emprunt
    (relation de composition) : les emprunts n'existent pas
    indépendamment de l'adhérent qui les a effectués.
    """

    QUOTA_EMPRUNTS_SIMULTANES = 5

    def __init__(self, identifiant: str, nom: str, categorie: CategorieAdherent) -> None:
        """
        Initialise un adhérent.

        :param identifiant: Identifiant unique de l'adhérent.
        :param nom: Nom complet de l'adhérent.
        :param categorie: Catégorie de l'adhérent (Enum CategorieAdherent).
        :raises AdherentInvalideError: Si l'identifiant ou le nom est vide,
            ou si la catégorie n'est pas valide.
        """
        if not identifiant or not identifiant.strip():
            raise AdherentInvalideError(identifiant or "inconnu", "identifiant vide")
        if not nom or not nom.strip():
            raise AdherentInvalideError(identifiant, "nom vide")
        if not isinstance(categorie, CategorieAdherent):
            raise AdherentInvalideError(identifiant, "catégorie invalide")

        self._identifiant = identifiant.strip()
        self._nom = nom.strip()
        self._categorie = categorie
        self._emprunts: list[Emprunt] = []  # composition

    @property
    def identifiant(self) -> str:
        return self._identifiant

    @property
    def nom(self) -> str:
        return self._nom

    @property
    def categorie(self) -> CategorieAdherent:
        return self._categorie

    @property
    def emprunts(self) -> list:
        return list(self._emprunts)  # copie défensive

    def nb_retards_actifs(self) -> int:
        """Retourne le nombre d'emprunts actuellement en retard."""
        return sum(1 for e in self._emprunts if e.est_en_retard())

    def emprunter_document(self, document, duree_jours: int) -> Emprunt:
        """
        Crée un nouvel emprunt pour ce document et l'ajoute à
        l'historique de l'adhérent.

        :param document: Le document à emprunter.
        :param duree_jours: Durée d'emprunt autorisée en jours.
        :raises RetardNonAutoriseError: Si l'adhérent a des retards non régularisés.
        """
        if self.nb_retards_actifs() > 0:
            raise RetardNonAutoriseError(self._identifiant, self.nb_retards_actifs())

        document.emprunter()
        emprunt = Emprunt(document, duree_jours)
        self._emprunts.append(emprunt)
        return emprunt

    def __str__(self) -> str:
        return f"{self._nom} ({self._categorie}) — {len(self._emprunts)} emprunt(s)"
