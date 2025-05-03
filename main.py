import os
from dotenv import load_dotenv
from scripts.load_teams import load_teams_from_excel
from scripts.fetch_puuid import fetch_puuid
from scripts.fetch_matches import fetch_tournament_matches, save_matches_to_json
from scripts.fetch_match_details import fetch_match_details, save_match_details_to_json
from scripts.analyze_match_stats import analyze_match_stats, save_team_stats_to_json
from scripts.get_general_stats import get_general_stats
from scripts.get_additional_stats import get_additional_stats
from scripts.create_excel import create_tournament_sheet
from scripts.save_json import save_to_json, load_from_json
from datetime import datetime
import json
import openpyxl

def main():
    # Charger les variables d'environnement
    load_dotenv()
    api_key = os.getenv("API_KEY")
    base_url = "https://europe.api.riotgames.com"

    # Chemins des fichiers
    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, "data")
    output_dir = os.path.join(current_dir, "output")

    # Créer les dossiers s'ils n'existent pas
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # Définir tous les chemins de fichiers
    excel_file_path = os.path.join(data_dir, "pseudosOccilan#6.xlsx")
    teams_json_path = os.path.join(data_dir, "teams.json")
    teams_with_puuid_json_path = os.path.join(data_dir, "teams_with_puuid.json")
    matches_output_path = os.path.join(data_dir, "tournament_matches.json")
    match_details_output_path = os.path.join(data_dir, "match_details.json")
    team_stats_output_path = os.path.join(data_dir, "team_stats.json")
    general_stats_path = os.path.join(data_dir, "general_stats.json")
    additional_stats_path = os.path.join(data_dir, "additional_stats.json")
    excel_output_path = os.path.join(output_dir, "OccilanStats.xlsx")

    try:
        # Étape 1 : Charger les équipes depuis le fichier Excel
        print("\nÉtape 1 : Chargement des équipes depuis le fichier Excel...")
        teams = load_teams_from_excel(excel_file_path)
        save_to_json(teams, teams_json_path)
        print(f"Les équipes ont été enregistrées dans {teams_json_path}")

        # Étape 2 : Récupérer les puuid pour chaque joueur
        print("\nÉtape 2 : Récupération des puuid pour chaque joueur...")
        teams_with_puuid = fetch_puuid(teams, api_key, base_url)
        save_to_json(teams_with_puuid, teams_with_puuid_json_path)
        print(f"Les équipes avec les puuid ont été enregistrées dans {teams_with_puuid_json_path}")

        # Étape 3 : Récupérer les matchs de type tournoi
        print("\nÉtape 3 : Récupération des matchs de type tournoi...")
        start_date = datetime(2025, 4, 25)
        end_date = datetime(2025, 4, 27, 23, 59, 59)
        tournament_matches = fetch_tournament_matches(teams_with_puuid, start_date, end_date)
        save_matches_to_json(tournament_matches, matches_output_path)
        print(f"Les matchs de type tournoi ont été enregistrés dans {matches_output_path}")

        # Étape 4 : Récupérer les détails des matchs
        print("\nÉtape 4 : Récupération des détails des matchs...")
        all_match_ids = set()
        for team_matches in tournament_matches.values():
            all_match_ids.update(team_matches)
        match_details = fetch_match_details(all_match_ids)
        save_match_details_to_json(match_details, match_details_output_path)
        print(f"Les détails des matchs ont été enregistrés dans {match_details_output_path}")

        # Étape 5 : Analyser les statistiques des matchs
        print("\nÉtape 5 : Analyse des statistiques des matchs...")
        team_stats = analyze_match_stats(match_details, teams_with_puuid)
        save_team_stats_to_json(team_stats, team_stats_output_path)
        print(f"Les statistiques des équipes ont été enregistrées dans {team_stats_output_path}")

        # Étape 6 : Générer les statistiques générales
        print("\nÉtape 6 : Génération des statistiques générales...")
        general_stats = get_general_stats(team_stats)
        save_to_json(general_stats, general_stats_path)
        print(f"Les statistiques générales ont été enregistrées dans {general_stats_path}")

        # Étape 7 : Générer les statistiques additionnelles
        print("\nÉtape 7 : Génération des statistiques additionnelles...")
        additional_stats = get_additional_stats(match_details)
        save_to_json(additional_stats, additional_stats_path)
        print(f"Les statistiques additionnelles ont été enregistrées dans {additional_stats_path}")

        # Étape 8 : Générer le fichier Excel
        print("\nÉtape 8 : Génération du fichier Excel...")
        wb = openpyxl.Workbook()
        create_tournament_sheet(wb, general_stats, additional_stats)
        wb.save(excel_output_path)
        print(f"Le fichier Excel a été enregistré dans {excel_output_path}")

        print("\nTraitement terminé avec succès!")

    except Exception as e:
        print(f"\nUne erreur s'est produite : {str(e)}")
        raise

if __name__ == "__main__":
    main()