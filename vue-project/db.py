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
        with open('../Version1/metro.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith('V '):

                    line = line[2:].replace(';', '') 
                    parts = line.split()  
                    if len(parts) >= 4 :
                        num_sommet = parts[0]
                        nom_sommet = ' '.join(parts[1:-3])  
                        numero_ligne = parts[-3]
                        si_terminus = parts[-2] == 'True'
                        branchement = int(parts[-1])  
                        cursor.execute(
                            "INSERT INTO Stations (num_sommet, nom_sommet, numero_ligne, si_terminus, branchement) VALUES (%s, %s, %s, %s, %s)",
                            (num_sommet, nom_sommet, numero_ligne, si_terminus, branchement)
                        )
                    else:
                        print(f"Skipping line due to unexpected format: {line}")
                elif line.startswith('E '):
                    _, num_sommet1, num_sommet2, temps_en_secondes = line.strip().split()
                    cursor.execute("INSERT INTO Aretes (num_sommet1, num_sommet2, temps_en_secondes) VALUES (%s, %s, %s)",
                                   (num_sommet1, num_sommet2, temps_en_secondes))
        db.commit()

        inserted_stations = set()

        with open('../Version1/pospoints.txt', 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                line = line.replace('@', ' ')
                parts = line.split(';')
                if len(parts) == 3:
                    pointx = int(parts[0])
                    pointy = int(parts[1])
                    station_name = parts[2]

                    # Vérifier si la station a déjà été insérée
                    if station_name not in inserted_stations:
                        cursor.execute(
                            "INSERT INTO Pospoints (pointx, pointy, station_name) VALUES (%s, %s, %s)",
                            (pointx, pointy, station_name)
                        )
                        inserted_stations.add(station_name)
                    else:
                        print(f"Skipping duplicate station: {station_name}")
                else:
                    print(f"Skipping line due to unexpected format: {line}")
        db.commit()

finally:
    db.close()