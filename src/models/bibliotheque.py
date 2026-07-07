"""
Module définissant la classe Bibliotheque (conteneur principal).
"""

import logging

logger = logging.getLogger(__name__)


class Bibliotheque:
    """
    Représente la bibliothèque, conteneur principal du catalogue.

    Bibliotheque reçoit des objets Document créés en dehors d'elle
    (relation d'agrégation) : les documents peuvent exister
    indépendamment de la bibliothèque qui les référence.
    """

    def __init__(self, nom: str) -> None:
        self._nom = nom
        self._documents: list = []  # agrégation
        self._adherents: dict = {}  # identifiant -> Adherent

    @property
    def nom(self) -> str:
        return self._nom

    def ajouter_document(self, document) -> None:
        """Ajoute un document déjà créé au catalogue."""
        self._documents.append(document)
        logger.info("Document ajouté au catalogue: %s", document.titre)

    def ajouter_adherent(self, adherent) -> None:
        """Enregistre un adhérent dans la bibliothèque."""
        self._adherents[adherent.identifiant] = adherent
        logger.info("Adhérent enregistré: %s", adherent.nom)

    def rechercher_par_titre(self, titre: str) -> list:
        """Recherche des documents par titre (insensible à la casse)."""
        titre_lower = titre.lower()
        return [d for d in self._documents if titre_lower in d.titre.lower()]

    def documents_disponibles(self) -> list:
        """Retourne la liste des documents actuellement disponibles."""
        from src.models.enums import StatutDocument
        return [d for d in self._documents if d.statut == StatutDocument.DISPONIBLE]

    @property
    def documents(self) -> list:
        return list(self._documents)

    @property
    def adherents(self) -> list:
        return list(self._adherents.values())

    def __str__(self) -> str:
        return (
            f"Bibliotheque '{self._nom}' — {len(self._documents)} document(s), "
            f"{len(self._adherents)} adhérent(s)"
        )
