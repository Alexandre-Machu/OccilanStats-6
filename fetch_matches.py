import requests
import json
import os
import time
from datetime import datetime
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
api_key = os.getenv("API_KEY")
base_url = "https://europe.api.riotgames.com"

def fetch_tournament_matches(teams, start_date, end_date, count=50, match_type="tourney"):
    """
    Récupère les matchs de type tournoi pour tous les joueurs dans les équipes spécifiées.
    Élimine les doublons pour chaque équipe.
    """
    start_time = int(time.mktime(start_date.timetuple()))
    end_time = int(time.mktime(end_date.timetuple()))

    all_matches = {}

    for team_name, players in teams.items():
        print(f"Récupération des matchs pour l'équipe : {team_name}")
        team_matches = set()  # Utiliser un ensemble pour éviter les doublons

        for player in players:
            puuid = player.get("puuid")
            if not puuid:
                print(f"Pas de puuid pour le joueur {player.get('player_name')}, passage au suivant.")
                continue

            # Construire l'URL pour récupérer les IDs des matchs
            endpoint = f"/lol/match/v5/matches/by-puuid/{puuid}/ids"
            api_url = f"{base_url}{endpoint}?count={count}&type={match_type}&startTime={start_time}&endTime={end_time}&api_key={api_key}"

            try:
                response = requests.get(api_url)
                if response.status_code == 200:
                    match_ids = response.json()
                    print(f"Matchs récupérés pour {player.get('player_name')}: {match_ids}")
                    team_matches.update(match_ids)  # Ajouter les matchs à l'ensemble
                else:
                    print(f"Erreur pour {player.get('player_name')}: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Erreur lors de la requête pour {player.get('player_name')}: {e}")

        # Convertir l'ensemble en liste unique et l'ajouter au dictionnaire
        all_matches[team_name] = list(team_matches)

    return all_matches

def save_matches_to_json(matches, output_path):
    """
    Enregistre les matchs dans un fichier JSON.
    """
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(matches, json_file, indent=4, ensure_ascii=False)
        print(f"Les matchs ont été enregistrés dans {output_path}")

if __name__ == "__main__":
    # Charger les équipes depuis le fichier JSON
    current_dir = os.path.dirname(__file__)
    teams_with_puuid_json_path = os.path.join(current_dir, "teams_with_puuid.json")
    matches_output_path = os.path.join(current_dir, "tournament_matches.json")

    with open(teams_with_puuid_json_path, "r", encoding="utf-8") as json_file:
        teams = json.load(json_file)

    # Définir les dates pour récupérer les matchs
    start_date = datetime(2025, 4, 25)
    end_date = datetime(2025, 4, 27, 23, 59, 59)

    # Récupérer les matchs
    tournament_matches = fetch_tournament_matches(teams, start_date, end_date)

    # Enregistrer les matchs dans un fichier JSON
    save_matches_to_json(tournament_matches, matches_output_path)