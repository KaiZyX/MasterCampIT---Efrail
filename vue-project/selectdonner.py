from flask import Flask, jsonify, send_file, request
import pymysql
import pandas as pd
import folium
import os
import networkx as nx


app = Flask(__name__)

# Fonction pour se connecter à la base de données
def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Florian1!",
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

    # Créer une carte centrée sur Paris
    m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

    # Ajouter des marqueurs pour chaque station
    for index, row in stations_df.iterrows():
        folium.Marker(
            location=[float(row['latitude']), float(row['longitude'])],
            popup=row['nom_sommet']
        ).add_to(m)

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

    # Fermer la connexion à la base de données
    db.close()

    # Créer une carte centrée sur Paris
    m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

    # Dictionnaire des couleurs par numéro de ligne
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
                folium.Marker(
                    location=[float(station['latitude']), float(station['longitude'])],
                    popup=station['nom_sommet']
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

    # Enregistrer la carte dans un fichier HTML
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

    # Requête SQL pour récupérer les stations
    connection = connect_db()  # Supposons que connect_db() soit une fonction de connexion à la base de données
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

    if 'error' in result:
        return result, 404

    # Créer une carte centrée sur Paris
    m = folium.Map(location=[48.8566, 2.3522], zoom_start=12)

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
                        folium.Marker(
                            location=[float(station['latitude']), float(station['longitude'])],
                            popup=station['nom_sommet']
                        ).add_to(m)
                        added_stations.add(sommet)

            except pymysql.MySQLError as e:
                print(f"Erreur MySQL lors de la récupération des informations de la station : {e}")
            finally:
                connection.close()

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
                    color = colors_by_line.get(arete['numero_ligne'], 'blue')  # Utilisation de 'blue' par défaut si la ligne n'est pas trouvée
                    folium.PolyLine(
                        locations=[
                            [float(station1['latitude']), float(station1['longitude'])],
                            [float(station2['latitude']), float(station2['longitude'])]
                        ],
                        color=color,
                        tooltip=f"Temps: {arete['temps_en_secondes']}s"
                    ).add_to(m)

        except pymysql.MySQLError as e:
            print(f"Erreur MySQL lors de la récupération des arêtes entre les stations : {e}")
        finally:
            connection.close()

    # Enregistrer la carte dans un fichier HTML temporaire
    map_file = 'shortest_path_map.html'
    m.save(map_file)

    # Envoyer le fichier HTML généré en réponse
    return send_file(map_file)





# Démarrer l'application Flask
if __name__ == '__main__':
     app.run(debug=True)
    # station_id = 'IDFM:463200'  # Remplacez par l'ID de la station que vous souhaitez récupérer
    # station_info = get_station_info_by_id(station_id)
    # print(station_info)
    # graph = build_graph()
    # # Exemple : affichage du nombre de sommets et d'arêtes dans le graphe
    # print(f"Nombre de sommets : {graph.number_of_nodes()}")
    # print(f"Nombre d'arêtes : {graph.number_of_edges()}")
    # start_station = 'IDFM:463200'  # Remplacez par l'ID de la station de départ
    # end_station = 'IDFM:22393'  # Remplacez par l'ID de la station d'arrivée
    # shortest_path_info = find_shortest_path(start_station, end_station)
    # print(shortest_path_info)
    # station_name = "Châtelet"  # Remplacez par le nom de la station que vous recherchez
    # station_id = get_station_id(station_name)
    # if station_id:
    #     print(f"L'identifiant de la station '{station_name}' est : {station_id}")
    # else:
    #     print(f"Aucune station trouvée avec le nom '{station_name}'")
