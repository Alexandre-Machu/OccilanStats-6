import requests

def fetch_puuid(teams, api_key, base_url):
    for team_name, players in teams.items():
        for player in players:
            player_name = player["player_name"]
            player_tag = player["player_tag"]

            # Endpoint pour récupérer le puuid
            endpoint = f"/riot/account/v1/accounts/by-riot-id/{player_name}/{player_tag}"
            api_url = f"{base_url}{endpoint}?api_key={api_key}"

            try:
                response = requests.get(api_url)
                if response.status_code == 200:
                    player["puuid"] = response.json()["puuid"]
                    print(f"puuid récupéré pour {player_name}#{player_tag}: {player['puuid']}")
                else:
                    print(f"Erreur pour {player_name}#{player_tag}: {response.status_code} - {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Erreur lors de la requête pour {player_name}#{player_tag}: {e}")
    return teams