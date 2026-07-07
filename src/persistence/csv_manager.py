"""
Module de gestion de l'export CSV des emprunts en retard.
"""

import csv
import logging
from datetime import date

logger = logging.getLogger(__name__)


def exporter_emprunts_retard(bibliotheque, filepath: str, date_reference: date = None) -> int:
    """
    Exporte vers un fichier CSV la liste des emprunts en retard,
    tous adhérents confondus, à une date de référence donnée.

    :param bibliotheque: Instance de Bibliotheque contenant les adhérents.
    :param filepath: Chemin du fichier CSV de destination.
    :param date_reference: Date de référence (aujourd'hui par défaut).
    :return: Nombre de lignes exportées.
    """
    date_reference = date_reference or date.today()
    lignes = []

    for adherent in bibliotheque.adherents:
        for emprunt in adherent.emprunts:
            if emprunt.est_en_retard(date_reference):
                jours_retard = emprunt.jours_de_retard(date_reference)
                amende = emprunt.document.calculer_amende(jours_retard)
                lignes.append({
                    "adherent": adherent.nom,
                    "document": emprunt.document.titre,
                    "date_emprunt": emprunt.date_emprunt.isoformat(),
                    "date_retour_prevue": emprunt.date_retour_prevue.isoformat(),
                    "jours_retard": jours_retard,
                    "amende": amende,
                })

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "adherent", "document", "date_emprunt",
                "date_retour_prevue", "jours_retard", "amende",
            ],
        )
        writer.writeheader()
        writer.writerows(lignes)

    logger.info("Export CSV des retards effectué: %s (%d ligne(s)).", filepath, len(lignes))
    return len(lignes)
