CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reference TEXT NOT NULL UNIQUE,
    titre TEXT NOT NULL,
    type_document TEXT NOT NULL,       -- Livre, Revue, DVD, Memoire
    statut TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS emprunts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    adherent_id TEXT NOT NULL,
    adherent_nom TEXT NOT NULL,
    date_emprunt TEXT NOT NULL,
    date_retour_prevue TEXT NOT NULL,
    date_retour_effective TEXT,
    FOREIGN KEY (document_id) REFERENCES documents (id)
);