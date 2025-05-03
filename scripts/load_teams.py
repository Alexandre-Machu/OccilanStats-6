import openpyxl

def load_teams_from_excel(file_path):
    """
    Charge les équipes depuis un fichier Excel.

    Args:
        file_path (str): Chemin du fichier Excel.

    Returns:
        dict: Un dictionnaire contenant les équipes et leurs joueurs.
    """
    try:
        # Charger le fichier Excel
        wb = openpyxl.load_workbook(file_path)
        sheet = wb.active  # Utiliser la première feuille

        teams = {}
        for row in sheet.iter_rows(min_row=2, max_col=4, values_only=True):  # Inclure les 4 colonnes
            team_name, role, player_name, player_tag = row

            # Vérifier que les données nécessaires sont présentes
            if not team_name or not player_name or not player_tag:
                print(f"Ligne ignorée : données manquantes ({row})")
                continue

            if team_name not in teams:
                teams[team_name] = []

            teams[team_name].append({
                "role": role,
                "player_name": player_name,
                "player_tag": player_tag
            })

        return teams

    except FileNotFoundError:
        print(f"Erreur : Le fichier {file_path} est introuvable.")
        return {}
    except Exception as e:
        print(f"Erreur inattendue lors du chargement du fichier Excel : {e}")
        return {}

if __name__ == "__main__":
    # Exemple d'utilisation
    file_path = "../data/pseudosOccilan#6.xlsx"
    print("Chargement des équipes depuis le fichier Excel...")
    teams = load_teams_from_excel(file_path)
    if teams:
        print("Équipes chargées avec succès :")
        for team_name, players in teams.items():
            print(f"Équipe {team_name} :")
            for player in players:
                print(f"  - {player['player_name']}#{player['player_tag']} ({player['role']})")
    else:
        print("Aucune équipe n'a été chargée.")