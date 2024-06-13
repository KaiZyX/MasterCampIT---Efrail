import pymysql
import re

# Connexion à la base de données
db = pymysql.connect(
    host="localhost",
    user="root",
    password="louka",
    database="metro",
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with db.cursor() as cursor:
        # Lire le fichier metro.txt
        with open('../Version1/metro.txt', 'r', encoding='utf-8') as file:
            for line in file:
                # Ignorer les lignes non pertinentes
                if line.startswith('V '):
                    # Supprimer le préfixe "V" et les espaces inutiles, puis séparer les composants
                    parts = [part.strip() for part in line[2:].split(';')]
                    if len(parts) == 5:
                        # Extraire les données des stations
                        num_sommet = parts[0]
                        nom_sommet = parts[1]
                        numero_ligne = int(parts[2])
                        si_terminus = parts[3] == 'True'
                        branchement = int(parts[4])

                        # Insérer dans la table Stations
                        cursor.execute("INSERT INTO Stations (num_sommet, nom_sommet, numero_ligne, si_terminus, branchement) VALUES (%s, %s, %s, %s, %s)",
                                    (num_sommet, nom_sommet, numero_ligne, si_terminus, branchement))
                    else:
                        print(f"Skipping line due to unexpected format: {line}")
                elif line.startswith('E '):
                    # Extraire les données des arêtes
                    _, num_sommet1, num_sommet2, temps_en_secondes = line.strip().split()
                    # Insérer dans la table Aretes
                    cursor.execute("INSERT INTO Aretes (num_sommet1, num_sommet2, temps_en_secondes) VALUES (%s, %s, %s)",
                                   (num_sommet1, num_sommet2, temps_en_secondes))

        # Valider les insertions
        db.commit()
finally:
    # Fermer la connexion
    db.close()