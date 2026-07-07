"""
Module de gestion du cycle de vie complet des emprunts.
"""

import logging
from datetime import date
from src.exceptions.exceptions_biblio import DocumentIndisponibleError

logger = logging.getLogger(__name__)


class GestionEmprunts:
    """
    Service orchestrant le cycle complet d'un emprunt : création,
    retour, et calcul de l'amende en cas de retard.
    """

    def __init__(self, bibliotheque) -> None:
        self._bibliotheque = bibliotheque

    def effectuer_emprunt(self, adherent_id: str, reference_document: str, duree_jours: int):
        """
        Effectue un emprunt : trouve l'adhérent et le document, puis
        délègue la création de l'emprunt à l'adhérent.

        :raises ValueError: Si l'adhérent ou le document est introuvable.
        :raises DocumentIndisponibleError: Si le document n'est pas disponible.
        """
        adherent = next(
            (a for a in self._bibliotheque.adherents if a.identifiant == adherent_id), None
        )
        if adherent is None:
            raise ValueError(f"Adhérent introuvable: {adherent_id}")

        document = next(
            (d for d in self._bibliotheque.documents if d.reference == reference_document), None
        )
        if document is None:
            raise ValueError(f"Document introuvable: {reference_document}")

        emprunt = adherent.emprunter_document(document, duree_jours)
        logger.info("Emprunt effectué: %s -> %s", adherent.nom, document.titre)
        return emprunt

    def effectuer_retour(self, adherent_id: str, reference_document: str, date_retour: date = None) -> float:
        """
        Enregistre le retour d'un document et calcule l'amende éventuelle.

        :return: Montant de l'amende (0 si aucun retard).
        :raises ValueError: Si l'adhérent, le document ou l'emprunt est introuvable.
        """
        adherent = next(
            (a for a in self._bibliotheque.adherents if a.identifiant == adherent_id), None
        )
        if adherent is None:
            raise ValueError(f"Adhérent introuvable: {adherent_id}")

        emprunt = next(
            (e for e in adherent.emprunts
             if e.document.reference == reference_document and e.date_retour_effective is None),
            None,
        )
        if emprunt is None:
            raise ValueError(f"Aucun emprunt en cours pour ce document: {reference_document}")

        jours_retard = emprunt.jours_de_retard(date_retour or date.today())
        emprunt.retourner(date_retour)
        emprunt.document.statut = emprunt.document.statut.__class__.DISPONIBLE

        amende = emprunt.document.calculer_amende(jours_retard)
        logger.info("Retour enregistré: %s, amende = %s", emprunt.document.titre, amende)
        return amende