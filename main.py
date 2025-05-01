import os
from dotenv import load_dotenv
from load_teams import load_teams_from_excel
from fetch_puuid import fetch_puuid
from save_json import save_to_json, load_from_json

# Charger les variables d'environnement
load_dotenv()
api_key = os.getenv("API_KEY")
base_url = "https://europe.api.riotgames.com"

# Chemins des fichiers
current_dir = os.path.dirname(__file__)
excel_file_path = os.path.join(current_dir, "pseudosOccilan#6.xlsx")
teams_json_path = os.path.join(current_dir, "teams.json")
teams_with_puuid_json_path = os.path.join(current_dir, "teams_with_puuid.json")

# Étape 1 : Charger les équipes depuis le fichier Excel
teams = load_teams_from_excel(excel_file_path)
save_to_json(teams, teams_json_path)

# Étape 2 : Charger les équipes depuis le fichier JSON
teams = load_from_json(teams_json_path)

# Étape 3 : Récupérer les puuid pour chaque joueur
teams_with_puuid = fetch_puuid(teams, api_key, base_url)
save_to_json(teams_with_puuid, teams_with_puuid_json_path)