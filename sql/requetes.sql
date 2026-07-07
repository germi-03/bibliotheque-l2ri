SELECT d.titre, e.adherent_nom, e.date_retour_prevue
FROM emprunts e JOIN documents d ON e.document_id = d.id
WHERE e.date_retour_effective IS NULL AND e.date_retour_prevue < '2026-07-10';

-- Requête 2: top documents les plus empruntés
SELECT d.titre, COUNT(e.id) as nb_emprunts
FROM emprunts e JOIN documents d ON e.document_id = d.id
GROUP BY d.id ORDER BY nb_emprunts DESC LIMIT 5;

-- Requête 3: historique des emprunts d'un adhérent donné
SELECT d.titre, e.date_emprunt, e.date_retour_prevue, e.date_retour_effective
FROM emprunts e JOIN documents d ON e.document_id = d.id
WHERE e.adherent_id = 'AD001' ORDER BY e.date_emprunt DESC;

-- Requête 4: documents ayant un statut donné
SELECT titre, type_document FROM documents WHERE statut = 'DISPONIBLE';