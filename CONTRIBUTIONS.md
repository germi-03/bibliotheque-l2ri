# Contributions au projet

## Membres du groupe
- Germaine — @germi-03
- Fatoumata — @[pseudo_github_fatoumata]
- Monique — @[pseudo_github_monique]

## Répartition du travail

| Membre | Modules / classes développés | Contribution estimée |
|--------|-------------------------------|----------------------|
| Germaine | enums.py, document_base.py, livre.py, revue.py, dvd.py, memoire.py, exceptions_biblio.py | 33% |
| Fatoumata | emprunt.py, adherent.py, bibliotheque.py, gestion_emprunts.py, rapports.py, README.md | 33% |
| Monique | json_manager.py, csv_manager.py, db_manager.py, schema.sql, requetes.sql, main.py | 33% |

## Répartition par phase

| Phase | Responsable principal |
|-----------------------------------|------------------------|
| Conception (diagramme de classes) | Germaine, Fatoumata, Monique (collectif) |
| Implémentation POO | Germaine |
| Persistance fichiers (JSON/CSV) | Monique |
| Persistance SQL | Monique |
| Tests / gestion des exceptions | Germaine, Fatoumata |
| README / documentation | Fatoumata |

## Difficultés rencontrées et résolution

1. **Problème réseau lors du push (Fatoumata)** : échec temporaire de connexion
   à GitHub lors d'un `git push`. Résolu en réessayant après vérification de
   la connexion internet ; le commit local n'a pas été perdu.

2. **Dossier `data/` manquant après clonage (Monique)** : Git ne conserve pas
   les dossiers vides, causant une erreur SQLite à l'ouverture de la base.
   Résolu en créant manuellement le dossier (`mkdir data`) et en ajoutant un
   fichier `.gitkeep` pour le tracker à l'avenir.

3. **Simulation d'un retard pour les tests (Monique)** : la classe `Emprunt`
   refuse une durée d'emprunt négative (validation stricte). Résolu en
   simulant plutôt une date d'emprunt dans le passé pour obtenir un retard
   réaliste, plutôt que de manipuler la durée.