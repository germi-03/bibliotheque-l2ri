"""
Module de gestion de la persistance JSON du catalogue.
"""

import json
import logging
from src.models.livre import Livre
from src.models.revue import Revue
from src.models.dvd import DVD
from src.models.memoire import Memoire
from src.models.enums import StatutDocument

logger = logging.getLogger(__name__)

# Association type_document -> classe, pour la reconstruction lors du chargement
TYPES_DOCUMENTS = {
    "Livre": Livre,
    "Revue": Revue,
    "DVD": DVD,
    "Memoire": Memoire,
}


def exporter_catalogue(documents: list, filepath: str) -> None:
    """
    Exporte une liste de documents vers un fichier JSON.

    :param documents: Liste d'objets Document (Livre, Revue, DVD, Memoire).
    :param filepath: Chemin du fichier JSON de destination.
    """
    data = []
    for doc in documents:
        entry = {"type": type(doc).__name__, "titre": doc.titre,
                 "reference": doc.reference, "statut": doc.statut.name}

        if isinstance(doc, Livre):
            entry.update({"auteur": doc.auteur, "nb_pages": doc.nb_pages})
        elif isinstance(doc, Revue):
            entry.update({"numero": doc.numero, "periodicite": doc.periodicite})
        elif isinstance(doc, DVD):
            entry.update({"duree_minutes": doc.duree_minutes, "realisateur": doc.realisateur})
        elif isinstance(doc, Memoire):
            entry.update({"auteur_etudiant": doc.auteur_etudiant, "annee_soutenance": doc.annee_soutenance})

        data.append(entry)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info("Catalogue exporté vers %s (%d documents).", filepath, len(data))


def importer_catalogue(filepath: str) -> list:
    """
    Recharge un catalogue de documents depuis un fichier JSON.

    :param filepath: Chemin du fichier JSON source.
    :return: Liste d'objets Document reconstruits.
    :raises FileNotFoundError: Si le fichier n'existe pas.
    :raises ValueError: Si un type de document est inconnu.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = []
    for entry in data:
        type_doc = entry["type"]
        if type_doc not in TYPES_DOCUMENTS:
            raise ValueError(f"Type de document inconnu: {type_doc}")

        if type_doc == "Livre":
            doc = Livre(entry["titre"], entry["reference"], entry["auteur"], entry["nb_pages"])
        elif type_doc == "Revue":
            doc = Revue(entry["titre"], entry["reference"], entry["numero"], entry["periodicite"])
        elif type_doc == "DVD":
            doc = DVD(entry["titre"], entry["reference"], entry["duree_minutes"], entry["realisateur"])
        else:  # Memoire
            doc = Memoire(entry["titre"], entry["reference"], entry["auteur_etudiant"], entry["annee_soutenance"])

        doc.statut = StatutDocument[entry["statut"]]
        documents.append(doc)

    logger.info("Catalogue importé depuis %s (%d documents).", filepath, len(documents))
    return documents