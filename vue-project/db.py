import pymysql
import re

# Connexion à la base de données
db = pymysql.connect(
    host="localhost",
    user="root",
    password="Florian1!",
    database="metro",
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with db.cursor() as cursor:
        with open('../Version1/metro.txt', 'r', encoding='utf-8') as file:
            for line in file:
                if line.startswith('V '):
                    
                    if line.startswith('V 0000'):  # Cas spécifique pour le numéro de sommet "0000"
                        line = 'V 0' + line[6:]
                    else:
                        line = line[:2] + line[2:].lstrip('0')  # Comportement existant pour les autres lignes

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

                    cursor.execute(
                        "INSERT INTO Pospoints (pointx, pointy, station_name) VALUES (%s, %s, %s)",
                        (pointx, pointy, station_name)
                    )
                else:
                    print(f"Skipping line due to unexpected format: {line}")
        db.commit()

        # Récupérer tous les noms de stations uniques dans Pospoints
        cursor.execute("SELECT DISTINCT station_name FROM Pospoints")
        pospoints_station_names = cursor.fetchall()

        for pospoint_station_name in pospoints_station_names:
            # Récupérer tous les Pospoints pour ce nom de station
            cursor.execute("SELECT id, station_name FROM Pospoints WHERE station_name = %s", (pospoint_station_name['station_name'],))
            pospoints = cursor.fetchall()
            
            # Récupérer tous les station_id correspondant à ce nom de station
            cursor.execute("SELECT num_sommet FROM Stations WHERE nom_sommet = %s", (pospoint_station_name['station_name'],))
            station_ids = [row['num_sommet'] for row in cursor.fetchall()]
            
            
            assigned_station_ids = set()

            # Associer chaque Pospoint à un station_id unique, dans la mesure du possible
            for pospoint in pospoints:
                station_id_to_assign = None
                for station_id in station_ids:
                    if station_id not in assigned_station_ids:
                        station_id_to_assign = station_id
                        break
                
                if station_id_to_assign is not None:

                    # Si un station_id non assigné est trouvé, l'assigner et le marquer comme assigné
                    assigned_station_ids.add(station_id_to_assign)
                    cursor.execute("UPDATE Pospoints SET station_ids = %s WHERE id = %s", (station_id_to_assign, pospoint['id']))
                
        db.commit()

        cursor.execute("DELETE FROM Pospoints WHERE station_ids IS NULL")
        db.commit()

        for pospoint_station_name in pospoints_station_names:
            # Récupérer tous les Pospoints pour ce nom de station
            cursor.execute("SELECT id, station_name FROM Pospoints WHERE station_name = %s", (pospoint_station_name['station_name'],))
            pospoints = cursor.fetchall()
            
            # Récupérer tous les numero_ligne correspondant à ce nom de station
            cursor.execute("SELECT numero_ligne FROM Stations WHERE nom_sommet = %s", (pospoint_station_name['station_name'],))
            lignes_ids = [row['numero_ligne'] for row in cursor.fetchall()]
            
            # Créer un ensemble pour suivre les lignes_ids déjà assignés
            assigned_lignes_ids = set()

            # Associer chaque Pospoint à un lignes_id unique, dans la mesure du possible
            for pospoint in pospoints:
                lignes_id_to_assign = None
                for lignes_id in lignes_ids:
                    if lignes_id not in assigned_lignes_ids:
                        lignes_id_to_assign = lignes_id
                        break
                
                if lignes_id_to_assign is not None:
                    # Si un lignes_id non assigné est trouvé, l'assigner et le marquer comme assigné
                    assigned_lignes_ids.add(lignes_id_to_assign)
                    cursor.execute("UPDATE Pospoints SET lignes_ids = %s WHERE id = %s", (lignes_id_to_assign, pospoint['id']))
        db.commit()

        # Ajouter des arêtes entre chaque quai de la même station s'ils n'existent pas déjà
        for pospoint_station_name in pospoints_station_names:
            
            # Récupérer tous les station_ids pour ce nom de station
            cursor.execute("SELECT station_ids FROM Pospoints WHERE station_name = %s", (pospoint_station_name['station_name'],))
            station_ids = [row['station_ids'] for row in cursor.fetchall()]

            # Ajouter des arêtes entre chaque station_id de la même station
            for i in range(len(station_ids)):
                for j in range(i + 1, len(station_ids)):
                    # Vérifier si l'arête existe déjà
                    cursor.execute(
                        "SELECT COUNT(*) as count FROM Aretes WHERE (num_sommet1 = %s AND num_sommet2 = %s) OR (num_sommet1 = %s AND num_sommet2 = %s)",
                        (station_ids[i], station_ids[j], station_ids[j], station_ids[i])
                    )
                    result = cursor.fetchone()
                    if result['count'] == 0:
                        cursor.execute(
                            "INSERT INTO Aretes (num_sommet1, num_sommet2, temps_en_secondes) VALUES (%s, %s, %s)",
                            (station_ids[i], station_ids[j], 0)
                        )
        db.commit()

finally:
    db.close()