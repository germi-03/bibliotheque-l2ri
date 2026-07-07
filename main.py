"""
Point d'entrée principal du projet Bibliothèque Universitaire.
Démonstration des fonctionnalités principales : création du catalogue,
gestion des emprunts, persistance JSON/CSV/SQLite, génération de rapports.
"""

import logging
from datetime import date, timedelta

from src.models.bibliotheque import Bibliotheque
from src.models.adherent import Adherent
from src.models.emprunt import Emprunt
from src.models.enums import CategorieAdherent
from src.models.livre import Livre
from src.models.revue import Revue
from src.models.dvd import DVD
from src.models.memoire import Memoire

from src.services.gestion_emprunts import GestionEmprunts
from src.services.rapports import generer_rapport_emprunts_en_cours, generer_rapport_retards

from src.persistence.json_manager import exporter_catalogue, importer_catalogue
from src.persistence.csv_manager import exporter_emprunts_retard
from src.persistence.db_manager import DBManager

from src.exceptions.exceptions_biblio import DocumentIndisponibleError


def configurer_logging() -> None:
    """Configure le logging pour toute l'application."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )


def creer_catalogue_demo() -> Bibliotheque:
    """Crée une bibliothèque avec un catalogue mixte de démonstration."""
    bib = Bibliotheque("Bibliothèque Universitaire ISI Dakar")

    documents = [
        Livre("Le Petit Prince", "ISBN001", "Saint-Exupéry", 96),
        Livre("Clean Code", "ISBN002", "Robert C. Martin", 464),
        Revue("National Geographic", "REV001", 245, "Mensuelle"),
        Revue("Science et Vie", "REV002", 1120, "Mensuelle"),
        DVD("Inception", "DVD001", 148, "Christopher Nolan"),
        DVD("Interstellar", "DVD002", 169, "Christopher Nolan"),
        Memoire("Étude sur la POO", "MEM001", "Aissatou Ba", 2025),
        Memoire("Systèmes distribués", "MEM002", "Ibrahima Fall", 2024),
    ]
    for doc in documents:
        bib.ajouter_document(doc)

    adherents = [
        Adherent("AD001", "Germaine", CategorieAdherent.ETUDIANT),
        Adherent("AD002", "Fatoumata", CategorieAdherent.ETUDIANT),
        Adherent("AD003", "Monique", CategorieAdherent.ENSEIGNANT),
    ]
    for adh in adherents:
        bib.ajouter_adherent(adh)

    return bib


def demo_emprunts(bib: Bibliotheque) -> None:
    """Démontre le cycle complet emprunt/retour avec gestion d'erreurs."""
    gestion = GestionEmprunts(bib)

    gestion.effectuer_emprunt("AD001", "ISBN001", 21)
    gestion.effectuer_emprunt("AD002", "DVD001", 5)

    # Emprunt avec date passée pour simuler un retard
    adherent_monique = next(a for a in bib.adherents if a.identifiant == "AD003")
    document_revue = next(d for d in bib.documents if d.reference == "REV001")
    document_revue.emprunter()
    emprunt_retard = Emprunt(document_revue, 7, date.today() - timedelta(days=15))
    adherent_monique._emprunts.append(emprunt_retard)

    # Tentative sur un document déjà emprunté -> exception
    try:
        gestion.effectuer_emprunt("AD002", "ISBN001", 21)
    except DocumentIndisponibleError as e:
        print(f"[Attendu] {e}")

    # Retour d'un document
    amende = gestion.effectuer_retour("AD001", "ISBN001")
    print(f"Amende pour le retour de Germaine: {amende} FCFA")


def demo_rapports(bib: Bibliotheque) -> None:
    """Affiche les rapports d'emprunts en cours et de retards."""
    print("\n--- Rapport: emprunts en cours ---")
    for nom, titre, date_prevue in generer_rapport_emprunts_en_cours(bib):
        print(f"{nom} — {titre} (retour prévu: {date_prevue})")

    print("\n--- Rapport: retards ---")
    for nom, titre, jours in generer_rapport_retards(bib):
        print(f"{nom} — {titre} — {jours} jour(s) de retard")


def demo_persistance(bib: Bibliotheque) -> None:
    """Démontre l'export/import JSON, l'export CSV, et l'insertion SQLite."""
    exporter_catalogue(bib.documents, "data/catalogue.json")
    documents_recharges = importer_catalogue("data/catalogue.json")
    print(f"\nCatalogue JSON exporté puis rechargé: {len(documents_recharges)} document(s).")

    nb_lignes = exporter_emprunts_retard(bib, "data/emprunts_retard.csv")
    print(f"Export CSV des retards: {nb_lignes} ligne(s).")

    db = DBManager()
    for doc in bib.documents:
        db.inserer_document(doc.reference, doc.titre, type(doc).__name__, doc.statut.name)
    print("Documents insérés en base SQLite.")

    print("\n--- Requête: documents disponibles ---")
    for titre, type_doc in db.documents_par_statut("DISPONIBLE"):
        print(f"{titre} ({type_doc})")


def main() -> None:
    configurer_logging()
    bib = creer_catalogue_demo()
    demo_emprunts(bib)
    demo_rapports(bib)
    demo_persistance(bib)
    print(f"\n{bib}")


if __name__ == "__main__":
    main()
