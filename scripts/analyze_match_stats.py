import json
import os

def calculate_kda(kills, deaths, assists):
    """
    Calcule le KDA d'un joueur.
    """
    return (kills + assists) / deaths if deaths > 0 else "PERFECT"

def analyze_match_stats(match_details, teams):
    """
    Analyse les statistiques des matchs et les organise par équipe et par joueur.
    """
    team_stats = {team_name: {} for team_name in teams.keys()}

    for match_id, match_data in match_details.items():
        participants = match_data["info"]["participants"]
        game_duration_minutes = match_data["info"]["gameDuration"] / 60  # Durée du match en minutes

        for participant in participants:
            puuid = participant["puuid"]
            team_id = participant["teamId"]
            kills = participant["kills"]
            deaths = participant["deaths"]
            assists = participant["assists"]
            cs = participant["totalMinionsKilled"] + participant["neutralMinionsKilled"]
            vision_score = participant["visionScore"]
            champion_name = participant["championName"]  # Nom du champion joué
            win = participant["win"]

            # Trouver l'équipe et le joueur correspondant
            for team_name, players in teams.items():
                for player in players:
                    if player["puuid"] == puuid:
                        player_name = player["player_name"]

                        # Initialiser les statistiques du joueur si nécessaire
                        if player_name not in team_stats[team_name]:
                            team_stats[team_name][player_name] = {
                                "total_kills": 0,
                                "total_deaths": 0,
                                "total_assists": 0,
                                "total_cs": 0,
                                "total_vision_score": 0,
                                "total_games": 0,
                                "total_game_duration": 0,  # Durée totale des parties jouées
                                "wins": 0,
                                "champions_played": set()  # Ensemble des champions joués
                            }

                        # Ajouter les statistiques du match
                        stats = team_stats[team_name][player_name]
                        stats["total_kills"] += kills
                        stats["total_deaths"] += deaths
                        stats["total_assists"] += assists
                        stats["total_cs"] += cs
                        stats["total_vision_score"] += vision_score
                        stats["total_games"] += 1
                        stats["total_game_duration"] += game_duration_minutes
                        stats["wins"] += 1 if win else 0
                        stats["champions_played"].add(champion_name)  # Ajouter le champion joué

    # Calculer les moyennes pour chaque joueur
    for team_name, players in team_stats.items():
        for player_name, stats in players.items():
            stats["average_kda"] = calculate_kda(
                stats["total_kills"],
                stats["total_deaths"],
                stats["total_assists"]
            )
            stats["average_kills"] = round(stats["total_kills"] / stats["total_games"], 1) if stats["total_games"] > 0 else 0
            stats["average_deaths"] = round(stats["total_deaths"] / stats["total_games"], 1) if stats["total_games"] > 0 else 0
            stats["average_assists"] = round(stats["total_assists"] / stats["total_games"], 1) if stats["total_games"] > 0 else 0
            stats["average_cs_per_game"] = round(stats["total_cs"] / stats["total_games"], 1) if stats["total_games"] > 0 else 0
            stats["average_vision_score"] = round(stats["total_vision_score"] / stats["total_games"], 1) if stats["total_games"] > 0 else 0
            stats["average_cs_per_minute"] = round(stats["total_cs"] / stats["total_game_duration"], 1) if stats["total_game_duration"] > 0 else 0
            stats["unique_champions_played"] = len(stats["champions_played"])  # Nombre de champions différents joués
            del stats["champions_played"]  # Supprimer l'ensemble pour ne garder que le nombre

    return team_stats

def save_team_stats_to_json(team_stats, output_path):
    """
    Enregistre les statistiques des équipes dans un fichier JSON.
    """
    with open(output_path, "w", encoding="utf-8") as json_file:
        json.dump(team_stats, json_file, indent=4, ensure_ascii=False)
        print(f"Les statistiques des équipes ont été enregistrées dans {output_path}")

if __name__ == "__main__":
    # Charger les fichiers nécessaires
    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, "../data")
    match_details_path = os.path.join(data_dir, "match_details.json")
    teams_with_puuid_path = os.path.join(data_dir, "teams_with_puuid.json")
    team_stats_output_path = os.path.join(data_dir, "team_stats.json")

    # Charger les détails des matchs
    with open(match_details_path, "r", encoding="utf-8") as json_file:
        match_details = json.load(json_file)

    # Charger les équipes avec leurs PUUIDs
    with open(teams_with_puuid_path, "r", encoding="utf-8") as json_file:
        teams = json.load(json_file)

    # Analyser les statistiques des matchs
    team_stats = analyze_match_stats(match_details, teams)

    # Enregistrer les statistiques dans un fichier JSON
    save_team_stats_to_json(team_stats, team_stats_output_path)