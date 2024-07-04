from flask import Flask, jsonify, send_file, request
import pymysql
import pandas as pd
import folium
import branca
import math
import os
import networkx as nx


app = Flask(__name__)

# Fonction pour se connecter à la base de données
def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="louka",
        database="metrogtfs",
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# Route pour générer la carte de toutes les lignes
@app.route('/generate_map', methods=['GET'])
def generate_map():
    db = connect_db()
    cursor = db.cursor()

    # Récupérer les données des arêtes (Aretes)
    cursor.execute("SELECT * FROM Aretes")
    aretes = cursor.fetchall()
    aretes_df = pd.DataFrame(aretes)

    # Récupérer les données des transferts (Transfers)
    cursor.execute("SELECT * FROM Transfers")
    transfers = cursor.fetchall()
    transfers_df = pd.DataFrame(transfers)

    # Récupérer les données des stations
    cursor.execute("SELECT * FROM Stations")
    stations = cursor.fetchall()
    stations_df = pd.DataFrame(stations)

    # Fermer la connexion à la base de données
    db.close()

    # Dictionnaire des couleurs par numéro de ligne
    colors_by_line = {
        "1": "#FFCE00",
        "2": "#0064B0",
        "3": "#9F9825",
        "4": "#C04191",
        "5": "#F28E42",
        "6": "#83C491",
        "7": "#F3A4BA",
        "8": "#CEADD2",
        "9": "#D5C900",
        "10": "#E3B32A",
        "11": "#8D5E2A",
        "12": "#00814F",
        "13": "#98D4E2",
        "14": "#662483",
        "3B": "#6EC4E8",
        "7B": "#6ECA97"
    }

    # Créer une carte centrée sur Paris
    m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

    # Ajouter des marqueurs pour chaque station
    station_count = 0  # Initialisation du compteur de stations
    for index, row in stations_df.iterrows():
        folium.CircleMarker(
            location=[float(row['latitude']), float(row['longitude'])],
            radius=5,  # Définit la taille du point. Ajustez selon les besoins
            popup=row['nom_sommet'],
            color='blue',  # Couleur du bord du cercle
            fill=True,
            fill_color='black'  # Couleur de remplissage du cercle
        ).add_to(m)
        station_count += 1  # Incrémentation du compteur de stations

    # Ajouter des lignes entre les stations à partir des Aretes
    for index, row in aretes_df.iterrows():
        station1 = stations_df[stations_df['num_sommet'] == row['num_sommet1']].iloc[0]
        station2 = stations_df[stations_df['num_sommet'] == row['num_sommet2']].iloc[0]
        color = colors_by_line.get(row['numero_ligne'], 'blue')  # Utilise 'blue' par défaut si la ligne n'est pas trouvée
        folium.PolyLine(
            locations=[
                [float(station1['latitude']), float(station1['longitude'])],
                [float(station2['latitude']), float(station2['longitude'])]
            ],
            color=color,  # Couleur des lignes pour les arêtes
            tooltip=f"Temps: {row['temps_en_secondes']}s"
        ).add_to(m)

    # Ajouter des lignes entre les stations à partir des Transfers
    for index, row in transfers_df.iterrows():
        station1 = stations_df[stations_df['num_sommet'] == row['num_sommet1']].iloc[0]
        station2 = stations_df[stations_df['num_sommet'] == row['num_sommet2']].iloc[0]
        folium.PolyLine(
            locations=[
                [float(station1['latitude']), float(station1['longitude'])],
                [float(station2['latitude']), float(station2['longitude'])]
            ],
            color='black',  # Couleur des lignes pour les transferts
            tooltip=f"Min Transfert Time: {row['min_transfer_time']}s"
        ).add_to(m)

    # Compter le nombre d'arêtes
    num_edges = aretes_df.shape[0]

    # Texte de la légende avec le nombre de stations et d'arêtes
    legend_text = f'''
     <div style="
     position: fixed; 
     bottom: 50px; left: 50px; width: auto; height: auto; 
     background-color: rgba(255, 255, 255, 0.8); 
     border: 2px solid #4CAF50; 
     border-radius: 5px; 
     padding: 10px; 
     box-shadow: 2px 2px 5px rgba(0,0,0,0.3); 
     z-index:9999; 
     font-size: 14px; 
     font-family: Arial, sans-serif;
     color: #333;
     ">
     <b>Carte des stations de métro de Paris</b> <br>
     <b>Nombre de stations:</b> {station_count} <br>
     <b>Nombre d'arêtes:</b> {num_edges}
     </div>
     '''
    m.get_root().html.add_child(branca.element.Element(legend_text))

    # Enregistrer la carte dans un fichier HTML
    map_file = 'metro_stations_map.html'
    m.save(map_file)

    return send_file(map_file)


# Route pour afficher toutes les stations d'une ligne et générer une carte
@app.route('/line_stations/<line_number>', methods=['GET'])
def line_stations(line_number):
    db = connect_db()
    cursor = db.cursor()

    # Récupérer les données des arêtes pour la ligne spécifiée
    cursor.execute("SELECT * FROM Aretes WHERE numero_ligne = %s", (line_number,))
    aretes = cursor.fetchall()
    aretes_df = pd.DataFrame(aretes)

    # Récupérer les données des stations
    cursor.execute("SELECT * FROM Stations")
    stations = cursor.fetchall()
    stations_df = pd.DataFrame(stations)

    db.close()

    m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

    colors_by_line = {
        "1": "##FFCE00",
        "2": "#0064B0",
        "3": "#9F9825",
        "4": "#C04191",
        "5": "#F28E42",
        "6": "#83C491",
        "7": "#F3A4BA",
        "8": "#CEADD2",
        "9": "#D5C900",
        "10": "#E3B32A",
        "11": "#8D5E2A",
        "12": "#00814F",
        "13": "#98D4E2",
        "14": "#662483",
        "3B": "#6EC4E8",
        "7B": "#6ECA97"
    }

    # Ajouter des marqueurs pour chaque station
    added_stations = set()
    for index, row in aretes_df.iterrows():
        for sommet in [row['num_sommet1'], row['num_sommet2']]:
            if sommet not in added_stations:
                station = stations_df[stations_df['num_sommet'] == sommet].iloc[0]
                folium.CircleMarker(
                            location=[float(station['latitude']), float(station['longitude'])],
                            radius=5,  # Définit la taille du point.
                            popup=station['nom_sommet'],
                            color='blue',  # Couleur du bord du cercle
                            fill=True,
                            fill_color='black'  # Couleur de remplissage du cercle
                        ).add_to(m)
                added_stations.add(sommet)

    # Ajouter des lignes entre les stations à partir des Aretes
    for index, row in aretes_df.iterrows():
        station1 = stations_df[stations_df['num_sommet'] == row['num_sommet1']].iloc[0]
        station2 = stations_df[stations_df['num_sommet'] == row['num_sommet2']].iloc[0]
        color = colors_by_line.get(line_number, 'blue')  # Utilise 'blue' par défaut si la ligne n'est pas trouvée
        folium.PolyLine(
            locations=[
                [float(station1['latitude']), float(station1['longitude'])],
                [float(station2['latitude']), float(station2['longitude'])]
            ],
            color=color,  # Couleur des lignes pour les arêtes
            tooltip=f"Temps: {row['temps_en_secondes']}s"
        ).add_to(m)

    map_file = f'metro_line_{line_number}_map.html'
    
    m.save(map_file)

    return send_file(map_file)

# Fonction pour récupérer les informations de la station spécifiée par son ID
def get_station_info_by_id(station_id):
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            # Requête pour récupérer les informations de la station depuis la table Stations
            cursor.execute('SELECT * FROM Stations WHERE num_sommet = %s', (station_id,))
            station_info = cursor.fetchone()

            if not station_info:
                return {"error": "Station not found"}, 404

            # Requête pour récupérer les arêtes (Aretes) liées à cette station
            cursor.execute('SELECT * FROM Aretes WHERE num_sommet1 = %s OR num_sommet2 = %s', (station_id, station_id,))
            aretes_info = cursor.fetchall()
            station_info['aretes'] = aretes_info

            # Requête pour récupérer les transferts (Transfers) liés à cette station
            cursor.execute('SELECT * FROM Transfers WHERE num_sommet1 = %s OR num_sommet2 = %s', (station_id, station_id,))
            transfers_info = cursor.fetchall()
            station_info['transfers'] = transfers_info

            return station_info

    except pymysql.MySQLError as e:
        print(f"Erreur MySQL lors de la récupération des informations de la station : {e}")
        return {"error": "Internal Server Error"}, 500

    finally:
        connection.close()


# Fonction pour récupérer le nom de la station spécifiée par son ID
def get_station_name_by_id(station_id):
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            # Requête pour récupérer le nom de la station depuis la table Stations
            cursor.execute('SELECT nom_sommet FROM Stations WHERE num_sommet = %s', (station_id,))
            station_name = cursor.fetchone()
            
            if not station_name:
                return None  # Retourne None si la station n'est pas trouvée
            
            return station_name['nom_sommet']
    except pymysql.MySQLError as e:
        print(f"Erreur MySQL lors de la récupération du nom de la station : {e}")
        return None
    finally:
        connection.close()


# Fonction pour récupérer l'identifiant de la station à partir de son nom
@app.route('/stations', methods=['GET'])
def get_station_id(station_name):
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            # Requête SQL pour récupérer l'identifiant de la station à partir de son nom
            sql = "SELECT num_sommet FROM Stations WHERE nom_sommet = %s LIMIT 1"
            cursor.execute(sql, (station_name,))
            result = cursor.fetchone()

            if result:
                return result['num_sommet']
            else:
                return None  # Retourne None si aucune station correspondante n'est trouvée

    except pymysql.MySQLError as e:
        print(f"Erreur MySQL lors de la récupération de l'identifiant de la station : {e}")
        return None
    finally:
        if connection:
            connection.close()

# Fonction pour construire le graphe à partir des données de la base de données
def build_graph():
    connection = connect_db()
    graph = nx.Graph()

    try:
        with connection.cursor() as cursor:
            # Récupérer les arêtes (Aretes)
            cursor.execute('SELECT num_sommet1, num_sommet2, temps_en_secondes FROM Aretes')
            aretes = cursor.fetchall()

            for arete in aretes:
                num_sommet1 = arete['num_sommet1']
                num_sommet2 = arete['num_sommet2']
                temps_en_secondes = int(arete['temps_en_secondes'])

                graph.add_edge(num_sommet1, num_sommet2, weight=temps_en_secondes, type='arete')

            # Récupérer les transferts (Transfers)
            cursor.execute('SELECT num_sommet1, num_sommet2, min_transfer_time FROM Transfers')
            transfers = cursor.fetchall()

            for transfer in transfers:
                num_sommet1 = transfer['num_sommet1']
                num_sommet2 = transfer['num_sommet2']
                min_transfer_time = int(transfer['min_transfer_time'])

                graph.add_edge(num_sommet1, num_sommet2, weight=min_transfer_time, type='transfer')

    except pymysql.MySQLError as e:
        print(f"Erreur MySQL lors de la récupération des données pour construire le graphe : {e}")

    finally:
        connection.close()

    return graph

# Fonction pour trouver le chemin le plus court entre deux stations
def find_shortest_path(start_station, end_station):
    graph = build_graph()
    try:
        path = nx.shortest_path(graph, source=start_station, target=end_station, weight='weight')
        duration = nx.shortest_path_length(graph, source=start_station, target=end_station, weight='weight')
        return {"path": path, "duration": duration}
    except nx.NetworkXNoPath:
        return {"error": "No path found between the specified stations"}


# Endpoint pour la suggestion de stations
@app.route('/suggestion', methods=['GET'])
def suggestion():
    query = request.args.get('query')
    if not query or len(query) < 3:
        return jsonify([])  # Retourne une liste vide si la requête est vide ou moins de 3 caractères
    connection = connect_db()  

    try:
        with connection.cursor() as cursor:
            sql = "SELECT nom_sommet FROM Stations WHERE nom_sommet LIKE %s"
            cursor.execute(sql, (f"{query}%",))
            stations = [row['nom_sommet'] for row in cursor.fetchall()]
    except pymysql.MySQLError as e:
        print(f"Erreur MySQL lors de la récupération des stations : {e}")
        return jsonify([]), 500
    finally:
        connection.close()

    return jsonify(stations)


# Valeurs des émissions de CO2 par minute pour chaque type de transport
CO2_PER_MINUTE_METRO = 1.5
CO2_PER_MINUTE_CAR = 132.5
CO2_PER_MINUTE_PLANE = 1350

def add_legend(map_object, duration_seconds, stations_list):
    # Convertir la durée de secondes en minutes
    duration_minutes = duration_seconds / 60
    duration_minutes = math.ceil(duration_minutes)  # Arrondir à l'entier supérieur

    # Calculer les émissions de CO2 pour chaque type de transport
    co2_metro = duration_minutes * CO2_PER_MINUTE_METRO
    co2_car = duration_minutes * CO2_PER_MINUTE_CAR
    co2_plane = duration_minutes * CO2_PER_MINUTE_PLANE

    # Générer stations_text pour afficher les stations et les lignes en une seule ligne
    stations_text = "".join(stations_list)

    # HTML pour la légende
    legend_html = f'''
    <div style="
    position: fixed; 
    bottom: 0; left: 0; width: 100%; height: auto; 
    background-color: rgba(255, 255, 255, 0.8); 
    border-top: 2px solid #4CAF50; 
    padding: 10px; 
    box-shadow: 0px -2px 5px rgba(0,0,0,0.3); 
    z-index:9999; 
    font-size: 14px; 
    font-family: Arial, sans-serif;
    color: #333;
    text-align: center;
    ">
    <b>Chemin le plus court:</b><br>
    <p><b>Durée:</b> {duration_minutes} minute(s) &nbsp;|&nbsp; <b>Émissions de CO₂ :</b> Métro: {co2_metro:.2f} g, Voiture thermique: {co2_car:.2f} g, Avion: {co2_plane:.2f} g</p>
    <b>Stations et lignes:</b><br>
    <div style="font-size: 12px; display: inline-block; text-align: left;">  
    {stations_text}
    </div>
    </div>
    '''
    map_object.get_root().html.add_child(branca.element.Element(legend_html))

# API endpoint pour obtenir le chemin le plus court entre deux stations par leur nom
@app.route('/shortest_path', methods=['GET'])
def shortest_path():
    start_station_name = request.args.get('start_station')
    end_station_name = request.args.get('end_station')

    # Récupérer les identifiants des stations à partir de leur nom
    start_station_id = get_station_id(start_station_name)
    end_station_id = get_station_id(end_station_name)

    if not start_station_id or not end_station_id:
        return {"error": "One or both station names not found in the database"}, 404

    # Trouver le chemin le plus court entre les stations
    result = find_shortest_path(start_station_id, end_station_id)
    duration = result["duration"]

    if 'error' in result:
        return result, 404

    # Créer une carte centrée sur Paris
    m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

    # Liste pour stocker les noms des stations parcourues
    stations_set = set()
    stations_list = []

    print(result['path'])

    if len(result['path']) > 0:
        # Supprimer les doublons initiaux (garder la dernière occurrence)
        for i in range(len(result['path']) - 1, 0, -1):
            if get_station_name_by_id(result['path'][i]) == get_station_name_by_id(result['path'][0]):
                del result['path'][0]
                break

        # Supprimer les doublons finaux (garder la première occurrence)
        for i in range(len(result['path']) - 2, -1, -1):
            if get_station_name_by_id(result['path'][-1]) == get_station_name_by_id(result['path'][i]):
                del result['path'][-1]
                break

    print(result['path'])


    print("-------------")
    print(stations_list)
    # Ajouter des marqueurs pour chaque station du chemin le plus court
    added_stations = set()
    for sommet in result['path']:
        if sommet not in added_stations:
            connection = connect_db()
            try:
                with connection.cursor() as cursor:
                    sql = "SELECT * FROM Stations WHERE num_sommet = %s"
                    cursor.execute(sql, (sommet,))
                    station = cursor.fetchone()
    
                    if station:

                        folium.CircleMarker(
                            location=[float(station['latitude']), float(station['longitude'])],
                            radius=5,  # Définit la taille du point. Ajustez selon les besoins
                            popup=station['nom_sommet'],
                            color='blue',  # Couleur du bord du cercle
                            fill=True,
                            fill_color='black'  # Couleur de remplissage du cercle
                        ).add_to(m)
                        added_stations.add(sommet)

            except pymysql.MySQLError as e:
                print(f"Erreur MySQL lors de la récupération des informations de la station : {e}")
            finally:
                connection.close()

    previous_station_name = None  # Pour vérifier la station précédente
    
    # Ajouter des lignes entre les stations du chemin le plus court
    for index in range(len(result['path']) - 1):
        station1_id = result['path'][index]
        station2_id = result['path'][index + 1]

        station1 = get_station_info_by_id(station1_id)
        station2 = get_station_info_by_id(station2_id)

        connection = connect_db()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM Aretes WHERE (num_sommet1 = %s AND num_sommet2 = %s) OR (num_sommet1 = %s AND num_sommet2 = %s)"
                cursor.execute(sql, (station1_id, station2_id, station2_id, station1_id))
                arete = cursor.fetchone()

                # Dictionnaire des couleurs par numéro de ligne
                colors_by_line = {
                    "1": "#FFCE00",
                    "2": "#0064B0",
                    "3": "#9F9825",
                    "4": "#C04191",
                    "5": "#F28E42",
                    "6": "#83C491",
                    "7": "#F3A4BA",
                    "8": "#CEADD2",
                    "9": "#D5C900",
                    "10": "#E3B32A",
                    "11": "#8D5E2A",
                    "12": "#00814F",
                    "13": "#98D4E2",
                    "14": "#662483",
                    "3B": "#6EC4E8",
                    "7B": "#6ECA97"
                }

                if arete:

                    # Ajouter le texte dans stations_list
                    if station1['nom_sommet'] != previous_station_name:
                        segment_text1 = f"{station1['nom_sommet']}→{arete['numero_ligne']}→"
                    else:
                        segment_text1 = f"→{arete['numero_ligne']}→"
                    segment_text2 = f"{station2['nom_sommet']}"

                    stations_list.append(segment_text1 + segment_text2)

                    color = colors_by_line.get(arete['numero_ligne'], 'blue')  # Utilisation de 'blue' par défaut si la ligne n'est pas trouvée

                    folium.PolyLine(
                        locations=[
                            [float(station1['latitude']), float(station1['longitude'])],
                            [float(station2['latitude']), float(station2['longitude'])]
                        ],
                        color=color,
                        tooltip=f"Temps: {arete['temps_en_secondes']}s"
                    ).add_to(m)

                    # Mettre à jour la station précédente pour stations_list
                    previous_station_name = station2['nom_sommet']

        except pymysql.MySQLError as e:
            print(f"Erreur MySQL lors de la récupération des arêtes entre les stations : {e}")
        finally:
            connection.close()

    print(stations_list)

    # Ajouter la légende avec la durée et la liste des stations parcourues
    add_legend(m, duration, stations_list)

    # Enregistrer la carte dans un fichier HTML temporaire
    map_file = 'shortest_path_map.html'
    m.save(map_file)

    # Envoyer le fichier HTML généré en réponse
    return send_file(map_file)


# Démarrer l'application Flask
if __name__ == '__main__':
     app.run(debug=True)
