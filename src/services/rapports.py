"""
Module de génération de rapports sur les emprunts et retards.
"""

import logging
from datetime import date

logger = logging.getLogger(__name__)


def generer_rapport_emprunts_en_cours(bibliotheque) -> list:
    """
    Génère la liste de tous les emprunts actuellement en cours
    (non encore rendus), tous adhérents confondus.

    :return: Liste de tuples (nom_adherent, titre_document, date_retour_prevue).
    """
    rapport = []
    for adherent in bibliotheque.adherents:
        for emprunt in adherent.emprunts:
            if emprunt.date_retour_effective is None:
                rapport.append((adherent.nom, emprunt.document.titre, emprunt.date_retour_prevue))
    logger.info("Rapport emprunts en cours généré: %d entrée(s).", len(rapport))
    return rapport


def generer_rapport_retards(bibliotheque, date_reference: date = None) -> list:
    """
    Génère la liste des emprunts actuellement en retard.

    :param date_reference: Date de référence (aujourd'hui par défaut).
    :return: Liste de tuples (nom_adherent, titre_document, jours_retard).
    """
    date_reference = date_reference or date.today()
    rapport = []
    for adherent in bibliotheque.adherents:
        for emprunt in adherent.emprunts:
            if emprunt.est_en_retard(date_reference):
                jours = emprunt.jours_de_retard(date_reference)
                rapport.append((adherent.nom, emprunt.document.titre, jours))
    logger.info("Rapport retards généré: %d entrée(s).", len(rapport))
    return rapport
