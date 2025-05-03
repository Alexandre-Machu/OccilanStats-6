import json
import os

def get_additional_stats(match_details):
    """
    Calcule les statistiques additionnelles à partir des détails des matchs.
    """
    longest_game = {"detail": None, "value": 0}
    shortest_game = {"detail": None, "value": float("inf")}
    most_kills_in_game = {"detail": None, "value": 0}
    least_kills_in_game = {"detail": None, "value": float("inf")}
    champion_picks = {}
    champion_bans = {}

    # Parcourir les matchs
    for match_id, match_data in match_details.items():
        try:
            # Convertir la durée en minutes et secondes
            game_duration_seconds = float(match_data["info"].get("gameDuration", 0))
            game_duration_minutes = game_duration_seconds / 60
            formatted_duration = f"{int(game_duration_minutes)}:{int(game_duration_seconds % 60):02d}"

            participants = match_data["info"].get("participants", [])
            teams = match_data["info"].get("teams", [])

            # Calculer la durée des parties
            if game_duration_seconds > longest_game["value"]:
                longest_game = {
                    "detail": f"Match {match_id}",
                    "value": formatted_duration
                }
                longest_game["value_for_comparison"] = game_duration_seconds

            if game_duration_seconds < shortest_game["value"]:
                shortest_game = {
                    "detail": f"Match {match_id}",
                    "value": formatted_duration
                }
                shortest_game["value_for_comparison"] = game_duration_seconds

            # Calculer les kills dans la partie
            total_kills = sum(int(p.get("kills", 0)) for p in participants)
            if total_kills > most_kills_in_game["value"]:
                most_kills_in_game = {
                    "detail": f"Match {match_id}",
                    "value": total_kills
                }
            if total_kills < least_kills_in_game["value"]:
                least_kills_in_game = {
                    "detail": f"Match {match_id}",
                    "value": total_kills
                }

            # Compter les champions joués
            for participant in participants:
                champion = participant.get("championName")
                if champion:
                    champion_picks[champion] = champion_picks.get(champion, 0) + 1

            # Compter les champions bannis
            for team in teams:
                for ban in team.get("bans", []):
                    champion = ban.get("championName")
                    if champion:
                        champion_bans[champion] = champion_bans.get(champion, 0) + 1

        except Exception as e:
            print(f"Erreur lors du traitement du match {match_id}: {e}")
            continue

    # Initialiser avec des valeurs par défaut si aucun match n'est trouvé
    if not champion_picks:
        champion_picks["Aucun"] = 0
    if not champion_bans:
        champion_bans["Aucun"] = 0

    # Trouver les champions les plus et moins sélectionnés/bannis
    most_selected = max(champion_picks.items(), key=lambda x: x[1])
    least_selected = min(champion_picks.items(), key=lambda x: x[1])
    most_banned = max(champion_bans.items(), key=lambda x: x[1])
    least_banned = min(champion_bans.items(), key=lambda x: x[1])

    return {
        "longest_game": {
            "detail": longest_game["detail"],
            "value": longest_game["value"]
        },
        "shortest_game": {
            "detail": shortest_game["detail"],
            "value": shortest_game["value"]
        },
        "most_kills_in_game": most_kills_in_game,
        "least_kills_in_game": least_kills_in_game,
        "most_selected_champion": {
            "detail": most_selected[0],
            "value": most_selected[1]
        },
        "least_selected_champion": {
            "detail": least_selected[0],
            "value": least_selected[1]
        },
        "most_banned_champion": {
            "detail": most_banned[0],
            "value": most_banned[1]
        },
        "least_banned_champion": {
            "detail": least_banned[0],
            "value": least_banned[1]
        }
    }

if __name__ == "__main__":
    # Pour tester le script indépendamment
    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, "../data")
    match_details_path = os.path.join(data_dir, "match_details.json")
    additional_stats_path = os.path.join(data_dir, "additional_stats.json")

    # Charger les détails des matchs
    with open(match_details_path, "r", encoding="utf-8") as json_file:
        match_details = json.load(json_file)

    # Calculer les statistiques additionnelles
    additional_stats = get_additional_stats(match_details)

    # Sauvegarder les résultats
    with open(additional_stats_path, "w", encoding="utf-8") as json_file:
        json.dump(additional_stats, json_file, indent=4, ensure_ascii=False)
    print(f"Les statistiques additionnelles ont été enregistrées dans {additional_stats_path}")