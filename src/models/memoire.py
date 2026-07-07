"""
Module définissant la classe Memoire, héritant de DocumentBase.
"""

from src.models.document_base import DocumentBase
from src.models.enums import StatutDocument


class Memoire(DocumentBase):
    """
    Représente un mémoire universitaire du catalogue de la bibliothèque.

    Un mémoire est un document sensible, souvent en exemplaire unique.
    Son emprunt est très court (3 jours) et l'amende de retard
    est la plus élevée du catalogue pour dissuader les retards.
    """

    DUREE_EMPRUNT_JOURS = 3
    TARIF_AMENDE_JOUR = 300  # en FCFA

    def __init__(self, titre: str, reference: str, auteur_etudiant: str, annee_soutenance: int) -> None:
        """
        Initialise un mémoire.

        :param titre: Titre du mémoire.
        :param reference: Référence unique.
        :param auteur_etudiant: Nom de l'étudiant auteur du mémoire.
        :param annee_soutenance: Année de soutenance (doit être raisonnable).
        :raises ValueError: Si l'auteur est vide ou l'année invalide.
        """
        super().__init__(titre, reference)

        if not auteur_etudiant or not auteur_etudiant.strip():
            raise ValueError("L'auteur du mémoire ne peut pas être vide.")
        if annee_soutenance < 1990 or annee_soutenance > 2100:
            raise ValueError("L'année de soutenance n'est pas valide.")

        self._auteur_etudiant = auteur_etudiant.strip()
        self._annee_soutenance = annee_soutenance

    @property
    def auteur_etudiant(self) -> str:
        return self._auteur_etudiant

    @property
    def annee_soutenance(self) -> int:
        return self._annee_soutenance

    def emprunter(self) -> None:
        """
        Marque le mémoire comme emprunté.

        :raises ValueError: Si le mémoire n'est pas disponible.
        """
        if self.statut != StatutDocument.DISPONIBLE:
            raise ValueError(
                f"Le mémoire '{self.titre}' n'est pas disponible (statut actuel : {self.statut})."
            )
        self.statut = StatutDocument.EMPRUNTE

    def calculer_amende(self, jours_retard: int) -> float:
        """
        Calcule l'amende de retard pour un mémoire.

        :param jours_retard: Nombre de jours de retard.
        :return: Montant de l'amende en FCFA.
        :raises ValueError: Si jours_retard est négatif.
        """
        if jours_retard < 0:
            raise ValueError("Le nombre de jours de retard ne peut pas être négatif.")
        return jours_retard * self.TARIF_AMENDE_JOUR

    def __str__(self) -> str:
        return (
            f"Memoire: {self.titre} par {self.auteur_etudiant} "
            f"({self.annee_soutenance}) — {self.statut}"
        )