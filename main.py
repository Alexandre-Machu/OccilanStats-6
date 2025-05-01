import os
from dotenv import load_dotenv
from load_teams import load_teams_from_excel
from fetch_puuid import fetch_puuid
from fetch_matches import fetch_tournament_matches, save_matches_to_json
from fetch_match_details import fetch_match_details, save_match_details_to_json
from analyze_match_stats import analyze_match_stats, save_team_stats_to_json
from save_json import save_to_json, load_from_json
from datetime import datetime
import json

# Charger les variables d'environnement
load_dotenv()
api_key = os.getenv("API_KEY")
base_url = "https://europe.api.riotgames.com"

# Chemins des fichiers
current_dir = os.path.dirname(__file__)
excel_file_path = os.path.join(current_dir, "pseudosOccilan#6.xlsx")
teams_json_path = os.path.join(current_dir, "teams.json")
teams_with_puuid_json_path = os.path.join(current_dir, "teams_with_puuid.json")
matches_output_path = os.path.join(current_dir, "tournament_matches.json")
match_details_output_path = os.path.join(current_dir, "match_details.json")
team_stats_output_path = os.path.join(current_dir, "team_stats.json")

# Étape 1 : Charger les équipes depuis le fichier Excel
print("Étape 1 : Chargement des équipes depuis le fichier Excel...")
teams = load_teams_from_excel(excel_file_path)
save_to_json(teams, teams_json_path)
print(f"Les équipes ont été enregistrées dans {teams_json_path}.\n")

# Étape 2 : Charger les équipes depuis le fichier JSON
print("Étape 2 : Chargement des équipes depuis le fichier JSON...")
teams = load_from_json(teams_json_path)
print("Les équipes ont été chargées avec succès.\n")

# Étape 3 : Récupérer les puuid pour chaque joueur
print("Étape 3 : Récupération des puuid pour chaque joueur...")
teams_with_puuid = fetch_puuid(teams, api_key, base_url)
save_to_json(teams_with_puuid, teams_with_puuid_json_path)
print(f"Les équipes avec les puuid ont été enregistrées dans {teams_with_puuid_json_path}.\n")

# Étape 4 : Récupérer les matchs de type tournoi
print("Étape 4 : Récupération des matchs de type tournoi...")
start_date = datetime(2025, 4, 25)
end_date = datetime(2025, 4, 27, 23, 59, 59)

# Charger les équipes avec les puuid
teams_with_puuid = load_from_json(teams_with_puuid_json_path)

# Récupérer les matchs
tournament_matches = fetch_tournament_matches(teams_with_puuid, start_date, end_date)

# Enregistrer les matchs dans un fichier JSON
save_matches_to_json(tournament_matches, matches_output_path)
print(f"Les matchs de type tournoi ont été enregistrés dans {matches_output_path}.\n")

# Étape 5 : Récupérer les détails des matchs
print("Étape 5 : Récupération des détails des matchs...")
with open(matches_output_path, "r", encoding="utf-8") as json_file:
    tournament_matches = json.load(json_file)

# Récupérer tous les match IDs uniques
all_match_ids = set()
for team_matches in tournament_matches.values():
    all_match_ids.update(team_matches)

# Récupérer les détails des matchs
match_details = fetch_match_details(all_match_ids)

# Enregistrer les détails des matchs dans un fichier JSON
save_match_details_to_json(match_details, match_details_output_path)
print(f"Les détails des matchs ont été enregistrés dans {match_details_output_path}.\n")

# Étape 6 : Analyser les statistiques des matchs
print("Étape 6 : Analyse des statistiques des matchs...")
with open(match_details_output_path, "r", encoding="utf-8") as json_file:
    match_details = json.load(json_file)

# Charger les équipes avec les puuid
teams_with_puuid = load_from_json(teams_with_puuid_json_path)

# Analyser les statistiques des matchs
team_stats = analyze_match_stats(match_details, teams_with_puuid)

# Enregistrer les statistiques dans un fichier JSON
save_team_stats_to_json(team_stats, team_stats_output_path)
print(f"Les statistiques des équipes ont été enregistrées dans {team_stats_output_path}.\n")

