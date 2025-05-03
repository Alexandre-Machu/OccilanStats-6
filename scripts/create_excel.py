import openpyxl
from openpyxl.styles import Font, Alignment
from openpyxl.utils import get_column_letter
import json
import os

def create_tournament_sheet(wb, general_stats, additional_stats):
    """
    Crée la feuille "Tournoi" avec les statistiques générales et additionnelles.
    """
    sheet = wb.active
    sheet.title = "Tournoi"

    # Titre
    sheet.merge_cells("A1:E1")
    sheet["A1"] = "Résumé des statistiques globales du tournoi"
    sheet["A1"].font = Font(bold=True, size=14)
    sheet["A1"].alignment = Alignment(horizontal="center")

    # Ajouter les statistiques générales
    sheet.append(["Statistique", "Joueur/Partie/Champion", "Équipe", "Valeur"])

    # Parcourir les statistiques générales
    for stat, data in general_stats.items():
        sheet.append([
            stat.replace("_", " ").capitalize(),  # Remplacer les underscores par des espaces
            data["player"],
            data["team"],
            data["value"]
        ])

    # Ajouter les statistiques additionnelles
    sheet.append([])  # Ligne vide pour séparer les sections
    sheet.append(["Statistique", "Détail", "Valeur"])

    for stat, data in additional_stats.items():
        sheet.append([
            stat.replace("_", " ").capitalize(),
            data["detail"],
            data["value"]
        ])

    # Ajuster la largeur des colonnes
    for col in range(1, 5):
        sheet.column_dimensions[get_column_letter(col)].width = 30

if __name__ == "__main__":
    # Définir les chemins des fichiers
    current_dir = os.path.dirname(__file__)
    data_dir = os.path.join(current_dir, "../data")
    general_stats_path = os.path.join(data_dir, "general_stats.json")
    additional_stats_path = os.path.join(data_dir, "additional_stats.json")
    excel_output_path = os.path.join(current_dir, "../output/OccilanStats.xlsx")

    # Charger les statistiques générales
    print("Chargement des statistiques générales...")
    with open(general_stats_path, "r", encoding="utf-8") as json_file:
        general_stats = json.load(json_file)

    # Charger les statistiques additionnelles
    print("Chargement des statistiques additionnelles...")
    with open(additional_stats_path, "r", encoding="utf-8") as json_file:
        additional_stats = json.load(json_file)

    # Créer le fichier Excel
    print("Génération du fichier Excel...")
    wb = openpyxl.Workbook()
    create_tournament_sheet(wb, general_stats, additional_stats)

    # Sauvegarder le fichier Excel
    wb.save(excel_output_path)
    print(f"Le fichier Excel a été enregistré dans {excel_output_path}.")