import openpyxl

def load_teams_from_excel(file_path):
    # Charger le fichier Excel
    wb = openpyxl.load_workbook(file_path)
    sheet = wb.active  # Utiliser la première feuille

    teams = {}
    for row in sheet.iter_rows(min_row=2, max_col=4, values_only=True):  # Inclure les 4 colonnes
        team_name, role, player_name, player_tag = row
        if team_name not in teams:
            teams[team_name] = []
        teams[team_name].append({
            "role": role,
            "player_name": player_name,
            "player_tag": player_tag
        })

    return teams