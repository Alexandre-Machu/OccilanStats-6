import json

def getMostStat(team_stats, stat_keys):
    """
    Trouve les joueurs avec les meilleures statistiques pour une liste de métriques.
    
    Args:
        team_stats (dict): Les statistiques des équipes et des joueurs.
        stat_keys (list): Liste des clés des statistiques à analyser.
    
    Returns:
        dict: Un dictionnaire contenant les meilleurs joueurs pour chaque statistique.
    """
    results = {}

    for stat_key in stat_keys:
        max_value = float('-inf')  # Initialiser avec une valeur très basse
        best_player = None
        best_team = None

        # Parcourir toutes les équipes et joueurs
        for team_name, players in team_stats.items():
            for player_name, stats in players.items():
                if stat_key in stats:  # Vérifier si la statistique existe pour ce joueur
                    if stats[stat_key] > max_value:
                        max_value = stats[stat_key]
                        best_player = player_name
                        best_team = team_name

        # Ajouter le résultat pour cette statistique
        results[stat_key] = {
            "team": best_team,
            "player": best_player,
            "value": round(max_value, 1)  # Arrondir à 1 chiffre après la virgule
        }

    return results

if __name__ == "__main__":
    # Charger les données de team_stats.json
    with open("team_stats.json", "r", encoding="utf-8") as file:
        team_stats = json.load(file)

    # Liste des statistiques à analyser
    stats_to_check = [
        "total_kills",
        "total_deaths",
        "total_assists",
        "average_kills",
        "average_deaths",
        "average_assists",
        "average_kda",
        "average_cs_per_minute",
        "unique_champions_played",
        "average_vision_score"
    ]

    # Obtenir les meilleurs joueurs pour chaque statistique
    results = getMostStat(team_stats, stats_to_check)

    # Afficher les résultats formatés
    for stat, result in results.items():
        print(f"Le joueur avec le plus de {stat} est {result['player']} de l'équipe {result['team']} avec {result['value']}.")

    # Enregistrer les résultats dans un fichier JSON
    output_path = "most_stats.json"
    with open(output_path, "w", encoding="utf-8") as output_file:
        json.dump(results, output_file, indent=4, ensure_ascii=False)
    print(f"\nLes résultats ont été enregistrés dans {output_path}.")