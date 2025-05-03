# OccilanStats

## Description
OccilanStats est un outil d'analyse de statistiques pour les tournois League of Legends de l'Occilan. Il collecte, analyse et présente les statistiques des matchs dans un fichier Excel détaillé.

## Prérequis
- Python 3.10+
- Une clé API Riot Games
- Les dépendances listées dans `requirements.txt`

## Installation
1. Clonez le repository
2. Installez les dépendances :
```bash
pip install -r requirements.txt
```
3. Créez un fichier `.env` à la racine du projet avec votre clé API Riot Games :
```env
API_KEY=RGAPI-your-api-key-here
```

## Structure du projet
```
OccilanStats/
├── data/                           # Dossier contenant les données JSON
│   ├── pseudosOccilan#6.xlsx      # Fichier Excel avec les équipes
│   └── *.json                     # Fichiers JSON générés
├── output/                        # Dossier contenant les fichiers générés
│   └── OccilanStats.xlsx         # Rapport final
├── scripts/                       # Scripts Python
└── main.py                       # Point d'entrée principal
```

## Flux des données et fichiers JSON

### 1. Chargement des équipes
- **Script** : `load_teams.py`
- **Entrée** : `data/pseudosOccilan#6.xlsx`
- **Sortie** : `data/teams.json`
- **Format** : Liste des équipes et leurs joueurs

### 2. Récupération des PUUIDs
- **Script** : `fetch_puuid.py`
- **Entrée** : `data/teams.json`
- **Sortie** : `data/teams_with_puuid.json`
- **Format** : Équipes avec PUUIDs des joueurs

### 3. Récupération des matchs
- **Script** : `fetch_matches.py`
- **Entrée** : `data/teams_with_puuid.json`
- **Sortie** : `data/tournament_matches.json`
- **Format** : Liste des IDs de match par équipe

### 4. Détails des matchs
- **Script** : `fetch_match_details.py`
- **Entrée** : `data/tournament_matches.json`
- **Sortie** : `data/match_details.json`
- **Format** : Détails complets des matchs

### 5. Statistiques des équipes
- **Script** : `analyze_match_stats.py`
- **Entrée** : `data/match_details.json`, `data/teams_with_puuid.json`
- **Sortie** : `data/team_stats.json`
- **Format** : Statistiques par équipe et par joueur

### 6. Statistiques générales
- **Script** : `get_general_stats.py`
- **Entrée** : `data/team_stats.json`
- **Sortie** : `data/general_stats.json`
- **Format** : Meilleures performances par catégorie

### 7. Statistiques additionnelles
- **Script** : `get_additional_stats.py`
- **Entrée** : `data/match_details.json`
- **Sortie** : `data/additional_stats.json`
- **Format** : Statistiques globales du tournoi

### 8. Génération Excel
- **Script** : `create_excel.py`
- **Entrée** : `data/general_stats.json`, `data/additional_stats.json`
- **Sortie** : `output/OccilanStats.xlsx`
- **Format** : Rapport Excel final

## Utilisation
1. Placez votre fichier Excel `pseudosOccilan#6.xlsx` dans le dossier `data/`
2. Exécutez le script principal :
```bash
python main.py
```

## Statistiques calculées
- Kills, morts et assistances moyens
- CS par minute
- Score de vision
- Champions les plus joués/bannis
- Durée des parties
- Et plus encore...

## Contribution
Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.

## Licence
[MIT](LICENSE)