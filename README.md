# Bibliothèque Universitaire — Gestion des documents et emprunts

Projet de fin de semestre — L2 RI, ISI Dakar
Module : Programmation Orientée Objet & Persistance des Données
Formateur : M. HAMANE — Année universitaire 2025-2026

## Description

Application de gestion d'une bibliothèque universitaire permettant de gérer un
catalogue de documents (livres, revues, DVD, mémoires), les adhérents, et le
cycle complet des emprunts (emprunt, retour, calcul d'amende en cas de retard).

Le projet met en œuvre :
- Une architecture orientée objet complète (héritage, classe abstraite, Enum,
  agrégation, composition)
- La persistance des données via JSON, CSV et SQLite
- La gestion des exceptions personnalisées et le logging des opérations critiques

## Membres du groupe

- Germaine — @germi-03
- Fatoumata — @[fatima2005bah-ai]
- Monique — @[diagnemonik-pro]

Voir [CONTRIBUTIONS.md](CONTRIBUTIONS.md) pour la répartition détaillée du travail.

## Structure du projet

bibliotheque-l2ri/
├── main.py                  # Point d'entrée — démonstration complète
├── src/
│   ├── models/               # Classes métier (POO)
│   │   ├── document_base.py  # Classe abstraite
│   │   ├── livre.py, revue.py, dvd.py, memoire.py
│   │   ├── adherent.py, emprunt.py, bibliotheque.py
│   │   └── enums.py
│   ├── exceptions/            # Exceptions personnalisées
│   ├── persistence/           # JSON, CSV, SQLite
│   ├── services/               # Logique applicative (emprunts, rapports)
│   └── utils/
├── sql/                        # Schéma et requêtes SQL
├── data/                        # Fichiers générés (JSON, CSV, DB)
└── tests/

## Installation

Le projet n'utilise que des modules standards Python (aucune dépendance externe).

1. Cloner le dépôt :
```bash
   git clone https://github.com/germi-03/bibliotheque-l2ri.git
   cd bibliotheque-l2ri
```
2. Vérifier que Python 3.10+ est installé :
```bash
   python --version
```

## Utilisation

Lancer la démonstration complète du projet :

```bash
python main.py
```

Ce script :
1. Crée un catalogue mixte (8 documents, 3 adhérents)
2. Effectue des emprunts et un retour (avec calcul d'amende)
3. Génère les rapports d'emprunts en cours et de retards
4. Exporte le catalogue en JSON puis le recharge
5. Exporte les retards en CSV
6. Insère les documents en base SQLite et exécute une requête métier

## Fonctionnalités principales

- Gestion d'un catalogue de documents (Livre, Revue, DVD, Mémoire)
- Cycle complet d'emprunt : emprunt, retour, calcul d'amende différencié
  selon le type de document
- Détection automatique des retards
- Export/import JSON du catalogue
- Export CSV des emprunts en retard
- Base de données SQLite avec 4 requêtes métier (retards actifs, top
  documents empruntés, historique par adhérent, documents par statut)
- Gestion des exceptions métier personnalisées
- Logging de toutes les opérations critiques

## Architecture orientée objet

- **Classe abstraite** : `DocumentBase` impose les méthodes `emprunter()` et
  `calculer_amende()`
- **Héritage** : `Livre`, `Revue`, `DVD`, `Memoire` héritent de `DocumentBase`
- **Enum** : `StatutDocument`, `CategorieAdherent`
- **Agrégation** : `Bibliotheque` contient des `Document` créés indépendamment
- **Composition** : `Adherent` crée et possède son historique d'`Emprunt`

## Licence

Projet académique — ISI Dakar, L2 RI, 2025-2026.