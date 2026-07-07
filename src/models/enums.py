"""
Module définissant les énumérations utilisées dans le système
de gestion de la bibliothèque universitaire.
"""

from enum import Enum, auto


class StatutDocument(Enum):
    """
    Représente l'état de disponibilité d'un document dans le catalogue.
    """
    DISPONIBLE = auto()
    EMPRUNTE = auto()
    RESERVE = auto()
    PERDU = auto()

    def __str__(self) -> str:
        return self.name.capitalize()


class CategorieAdherent(Enum):
    """
    Représente la catégorie d'un adhérent, utilisée notamment
    pour déterminer les règles d'emprunt et le calcul des amendes.
    """
    ETUDIANT = auto()
    ENSEIGNANT = auto()
    EXTERNE = auto()

    def __str__(self) -> str:
        return self.name.capitalize()