"""
Module de gestion de la base de données SQLite pour la bibliothèque.
"""

import sqlite3
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class DBManager:
    """
    Gère la connexion et les opérations sur la base de données
    SQLite de la bibliothèque.
    """

    def __init__(self, db_path: str = "data/bibliotheque.db") -> None:
        self._db_path = db_path
        self._init_schema()

    def _init_schema(self) -> None:
        """Crée les tables si elles n'existent pas, à partir de schema.sql."""
        schema_path = Path("sql/schema.sql")
        with sqlite3.connect(self._db_path) as conn:
            with open(schema_path, "r", encoding="utf-8") as f:
                conn.executescript(f.read())
        logger.info("Schéma de base de données initialisé.")

    def inserer_document(self, reference: str, titre: str, type_document: str, statut: str) -> None:
        """Insère un document dans la base de données."""
        with sqlite3.connect(self._db_path) as conn:
            conn.execute(
                "INSERT OR IGNORE INTO documents (reference, titre, type_document, statut) "
                "VALUES (?, ?, ?, ?)",
                (reference, titre, type_document, statut),
            )
        logger.info("Document inséré en base: %s", titre)

    def inserer_emprunt(
        self, reference_document: str, adherent_id: str, adherent_nom: str,
        date_emprunt: str, date_retour_prevue: str, date_retour_effective: str = None
    ) -> None:
        """Insère un emprunt lié à un document existant (clé étrangère)."""
        with sqlite3.connect(self._db_path) as conn:
            cur = conn.execute(
                "SELECT id FROM documents WHERE reference = ?", (reference_document,)
            )
            row = cur.fetchone()
            if row is None:
                raise ValueError(f"Document {reference_document} introuvable en base.")
            document_id = row[0]

            conn.execute(
                "INSERT INTO emprunts "
                "(document_id, adherent_id, adherent_nom, date_emprunt, "
                "date_retour_prevue, date_retour_effective) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (document_id, adherent_id, adherent_nom, date_emprunt,
                 date_retour_prevue, date_retour_effective),
            )
        logger.info("Emprunt inséré en base pour: %s", reference_document)

    # --- Les 4 requêtes métier exigées par le sujet ---

    def retards_actifs(self, date_reference: str) -> list:
        """Requête 1: emprunts en retard non encore rendus à une date donnée."""
        with sqlite3.connect(self._db_path) as conn:
            cur = conn.execute(
                "SELECT d.titre, e.adherent_nom, e.date_retour_prevue "
                "FROM emprunts e JOIN documents d ON e.document_id = d.id "
                "WHERE e.date_retour_effective IS NULL AND e.date_retour_prevue < ?",
                (date_reference,),
            )
            return cur.fetchall()

    def top_documents_empruntes(self, limite: int = 5) -> list:
        """Requête 2: documents les plus empruntés."""
        with sqlite3.connect(self._db_path) as conn:
            cur = conn.execute(
                "SELECT d.titre, COUNT(e.id) as nb_emprunts "
                "FROM emprunts e JOIN documents d ON e.document_id = d.id "
                "GROUP BY d.id ORDER BY nb_emprunts DESC LIMIT ?",
                (limite,),
            )
            return cur.fetchall()

    def historique_par_adherent(self, adherent_id: str) -> list:
        """Requête 3: historique complet des emprunts d'un adhérent."""
        with sqlite3.connect(self._db_path) as conn:
            cur = conn.execute(
                "SELECT d.titre, e.date_emprunt, e.date_retour_prevue, e.date_retour_effective "
                "FROM emprunts e JOIN documents d ON e.document_id = d.id "
                "WHERE e.adherent_id = ? ORDER BY e.date_emprunt DESC",
                (adherent_id,),
            )
            return cur.fetchall()

    def documents_par_statut(self, statut: str) -> list:
        """Requête 4: liste des documents ayant un statut donné."""
        with sqlite3.connect(self._db_path) as conn:
            cur = conn.execute(
                "SELECT titre, type_document FROM documents WHERE statut = ?",
                (statut,),
            )
            return cur.fetchall()
