from flask import Flask, jsonify, request, send_file, current_app, send_from_directory
from flask_cors import CORS 

import pymysql, pymysql.cursors

import networkx as nx

from plotly.io import to_html as go
import plotly.graph_objects as go


app = Flask(__name__)
CORS(app) 
@app.route('/')
def home():
    return "Welcome to the API. Use /api/stations or /api/connections to access data."


def get_db_connection():
    return pymysql.connect(host='localhost', user='root', password='louka', db='metro', cursorclass=pymysql.cursors.DictCursor)

def get_db_connection2(): 
    return pymysql.connect(host='localhost', user='root', password='louka', db='metro')# sans cursorclass=pymysql.cursors.DictCursor pour l'api map et line

@app.route('/api/stations', methods=['GET'])
def get_stations():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM Stations')
        stations = cursor.fetchall()
    connection.close()
    return jsonify(stations)




# Affiche le graphique de toutes les lignes de metro
@app.route('/api/map', methods=['GET'])
def get_map():
    db_connection = None
    try:
        db_connection = get_db_connection2()
        with db_connection.cursor() as cursor:
            cursor.execute("SELECT pointx, pointy, station_name FROM Pospoints")
            points = cursor.fetchall()

            cursor.execute('''
                SELECT 
                    A.pointx AS x1, A.pointy AS y1, 
                    B.pointx AS x2, B.pointy AS y2,
                    A.lignes_ids AS lignes_ids1, B.lignes_ids AS lignes_ids2
                FROM 
                    Aretes C
                    JOIN Pospoints A ON FIND_IN_SET(C.num_sommet1, A.station_ids)
                    JOIN Pospoints B ON FIND_IN_SET(C.num_sommet2, B.station_ids);
            ''')
            connections = cursor.fetchall()

        fig = go.Figure()

        
        for point in points:
            fig.add_trace(go.Scatter(x=[point[0]], y=[-point[1]], mode='markers', marker=dict(color='black', size=8), hovertext=[point[2]], hoverinfo='text'))

        for connection in connections:
            lignes_ids = connection[4].split(',')  
            if lignes_ids: 
                line_color = couleur_ligne(lignes_ids[0])  
                fig.add_trace(go.Scatter(x=[connection[0], connection[2]], y=[-connection[1], -connection[3]], mode='lines', line=dict(color=line_color, width=2)))
            else:
                fig.add_trace(go.Scatter(x=[connection[0], connection[2]], y=[connection[1], connection[3]], mode='lines', line=dict(color='grey', width=2)))

        fig.update_layout(
            showlegend=False, 
            plot_bgcolor='white', 
            xaxis=dict(
                showgrid=False, 
                zeroline=False, 
                visible=False,
                scaleanchor='y',
                scaleratio=1
            ),
            yaxis=dict(
                showgrid=False, 
                zeroline=False, 
                visible=False
            ),
            autosize=True
        )
        graph_html = fig.to_html(full_html=False)

        return graph_html

    finally:
        if db_connection:
            db_connection.close()


# Affiche le graphique de la ligne spécifiée
@app.route('/api/line_map', methods=['GET'])
def get_line_map():
    line_id = request.args.get('line_id')  
    color = couleur_ligne(line_id) 

    db_connection = get_db_connection2()
    with db_connection.cursor() as cursor:
        cursor.execute('''
            SELECT pointx, pointy, station_name FROM Pospoints
            WHERE FIND_IN_SET(%s, lignes_ids);
        ''', (line_id,))
        points = cursor.fetchall()

        cursor.execute('''
            SELECT 
                A.pointx AS x1, A.pointy AS y1, 
                B.pointx AS x2, B.pointy AS y2
            FROM 
                Aretes C
                JOIN Pospoints A ON FIND_IN_SET(C.num_sommet1, A.station_ids) AND FIND_IN_SET(%s, A.lignes_ids)
                JOIN Pospoints B ON FIND_IN_SET(C.num_sommet2, B.station_ids) AND FIND_IN_SET(%s, B.lignes_ids);
        ''', (line_id, line_id))
        connections = cursor.fetchall()

    fig = go.Figure()

    for point in points:
        fig.add_trace(go.Scatter(x=[point[0]], y=[-point[1]], mode='markers+text', marker=dict(color='black', size=8),
                                 text=[point[2]], textposition="bottom center", hoverinfo='text'))

    for conn in connections:
        fig.add_trace(go.Scatter(x=[conn[0], conn[2]], y=[-conn[1], -conn[3]], mode='lines', line=dict(color=color, width=2)))

    fig.update_layout(
            showlegend=False, 
            plot_bgcolor='white', 
            xaxis=dict(
                showgrid=False, 
                zeroline=False, 
                visible=False,
                scaleanchor='y',
                scaleratio=1
            ),
            yaxis=dict(
                showgrid=False, 
                zeroline=False, 
                visible=False
            ),
            autosize=True
    )
    graph_html = fig.to_html(full_html=False)

    return graph_html

# dictionnaire des couleurs des lignes de metro
couleurs_metro = {
    "1": "#FFCE00",
    "2": "#0064B0",
    "3": "#9F9825",
    "3bis": "#98D4E2",
    "4": "#C04191",
    "5": "#F28E42",
    "6": "#83C491",
    "7": "#F3A4BA",
    "7bis": "#83C491",
    "8": "#CEADD2",
    "9": "#D5C900",
    "10": "#E3B32A",
    "11": "#8D5E2A",
    "12": "#00814F",
    "13": "#98D4E2",
    "14": "#662483"
}

def couleur_ligne(ligne_id):
    return couleurs_metro.get(ligne_id, "#FFFFFF")  


# Affiche les informations de la station spécifiée grace a leurs station_id
@app.route('/api/station_info', methods=['GET'])
def get_station_info():
    station_id = request.args.get('station_id')
    if not station_id:
        return jsonify({"error": "station_id parameter is required"}), 400

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM Pospoints WHERE FIND_IN_SET(%s, station_ids)', (station_id,))
            station_info = cursor.fetchall()

        if not station_info:
            return jsonify({"error": "Station not found"}), 404

        return jsonify(station_info)

    finally:
        connection.close()


# Fonction pour récupérer les informations de la station spécifiée par son ID
def get_station_info_by_id(station_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM Pospoints WHERE FIND_IN_SET(%s, station_ids)', (station_id,))
            station_info = cursor.fetchall()

        if not station_info:
            return {"error": "Station not found"}, 404

        return station_info

    except pymysql.MySQLError as e:
        print(f"Erreur MySQL lors de la récupération des informations de la station : {e}")
        return {"error": "Internal Server Error"}, 500

    finally:
        connection.close()

# Créer le graph avec toutes les arretes et les sommets
def build_graph():
    connection = get_db_connection()
    graph = nx.Graph()

    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT num_sommet1, num_sommet2, temps_en_secondes FROM Aretes')
            aretes = cursor.fetchall()

            for arete in aretes:
                num_sommet1 = arete['num_sommet1']
                num_sommet2 = arete['num_sommet2']
                temps_en_secondes = int(arete['temps_en_secondes'])

                graph.add_edge(num_sommet1, num_sommet2, weight=temps_en_secondes)

    finally:
        connection.close()

    return graph

# Nouvelle fonction pour obtenir le chemin le plus court entre deux stations
def find_shortest_path(start_station, end_station):
    graph = build_graph()
    try:
        path = nx.shortest_path(graph, source=start_station, target=end_station, weight='weight')
        duration = nx.shortest_path_length(graph, source=start_station, target=end_station, weight='weight')
        return {"path": path, "duration": duration}
    except nx.NetworkXNoPath:
        return {"error": "No path found between the specified stations"}


# Récupère les informations de la station spécifiée grace a leurs nom
def get_station_id(station_name):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Requête SQL pour récupérer l'identifiant de la station à partir de son nom
            sql = """
            SELECT num_sommet FROM Stations
            WHERE SOUNDEX(nom_sommet) = SOUNDEX(%s)
            OR LEVENSHTEIN(nom_sommet, %s) <= 2  # Admet une différence de jusqu'à 2 caractères
            ORDER BY LEVENSHTEIN(nom_sommet, %s), LENGTH(nom_sommet)
            LIMIT 1
            """
            
            cursor.execute(sql, (station_name, station_name, station_name))
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

# Route API pour obtenir le chemin le plus court avec les informations détaillées
@app.route('/api/shortest_path_info', methods=['GET'])
def get_shortest_path_info():
    start_station_name = request.args.get('start_station_name')
    end_station_name = request.args.get('end_station_name')

    print("Start Station Name:", start_station_name)# afficher le nom de la station de départ et d'arrivée
    print("End Station Name:", end_station_name)# afficher le nom de la station de départ et d'arrivée

    if not start_station_name or not end_station_name:
        return jsonify({"error": "Les noms des stations de départ et d'arrivée sont requis"}), 400

    start_station_id = get_station_id(start_station_name)
    print("Start Station ID:", start_station_id)# afficher l'identifiant de la station

    end_station_id = get_station_id(end_station_name)
    print("End Station ID:", end_station_id)# afficher l'identifiant de la station

    if not start_station_id:
        return jsonify({"error": f"Aucune station trouvée avec le nom '{start_station_name}'"}), 404
    if not end_station_id:
        return jsonify({"error": f"Aucune station trouvée avec le nom '{end_station_name}'"}), 404
    


    path_and_duration = find_shortest_path(start_station_id, end_station_id)

    if "error" in path_and_duration:
        return jsonify({"error": "Aucun chemin trouvé entre les stations spécifiées"}), 404

    path = path_and_duration["path"]
    duration = path_and_duration["duration"]


    print("Chemin le plus court:", path)# afficher le chemin le plus court
    print("Durée:", duration)# afficher la durée

    stations_info = []
    for station_id in path:
        info = get_station_info_by_id(station_id)
        if info:
            stations_info.append(info)


    # Supprimer la première station si elle est identique à la deuxième
    if len(stations_info) > 1 and stations_info[0][0]['station_name'] == stations_info[1][0]['station_name']:
        stations_info.pop(0)
        
    # Supprimer la dernière station si elle est identique à l'avant-dernière
    if len(stations_info) > 1 and stations_info[-1][0]['station_name'] == stations_info[-2][0]['station_name']:
        stations_info.pop()

    print("Informations des stations sur le chemin:")# afficher les informations des stations sur le chemin
    for station in stations_info:
        print(station)



    print("--------------------------")
    print(stations_info[0])#affiche informations de la première station
    print(stations_info[len(stations_info) - 1])#afficher informations de la dernière station
    print("--------------------------")
    print(stations_info[0])
    print(stations_info)


    print("--------------------------")
    # Boucle à travers stations_info pour accéder aux informations de chaque station
    for station_list in stations_info:
        if len(station_list) > 0:  # Vérifiez si la liste de station contient au moins un élément
            station_info = station_list[0]  # Accédez au premier élément de la liste (qui est un dictionnaire)
            station_name = station_info['station_name']
            pointx = station_info['pointx']
            pointy = station_info['pointy']
            lignes_ids = station_info['lignes_ids']  # Ajout de lignes_ids

        print(f"Station Name: {station_name}, PointX: {pointx}, PointY: {pointy}, Lignes IDs: {lignes_ids}")
    else:
        print("Empty station list")

    # Exemple spécifique d'accès à la première station
    first_station_info = stations_info[0][0]
    first_station_name = first_station_info['station_name']
    first_station_pointx = first_station_info['pointx']
    first_station_pointy = first_station_info['pointy']
    first_station_ligneid = first_station_info['lignes_ids']

    print(f"First Station Name: {first_station_name}, PointX: {first_station_pointx}, PointY: {first_station_pointy}, Ligneids: {first_station_ligneid}")
    print("--------------------------")

    # Création du graphe Plotly
    fig = go.Figure()

    # Ajout des points (stations) au graphe
    for station_list in stations_info:
        if len(station_list) > 0:  # Vérifiez si la liste de station contient au moins un élément
            station_info = station_list[0]  # Accédez au premier élément de la liste (qui est un dictionnaire)
            station_name = station_info['station_name']
            pointx = station_info['pointx']
            pointy = station_info['pointy']
            

            fig.add_trace(go.Scatter(x=[pointx], y=[-pointy], mode='markers+text', marker=dict(color='black', size=8),
                                    text=[station_name], textposition="bottom center", hoverinfo='text'))


    # Ajout des connexions entre les stations
    for i in range(len(stations_info) - 1):
        station1_info = stations_info[i][0]
        station2_info = stations_info[i + 1][0]
        station1_pointx = station1_info['pointx']
        station1_pointy = station1_info['pointy']
        station2_pointx = station2_info['pointx']
        station2_pointy = station2_info['pointy']

        lignes_ids1 = station1_info['lignes_ids']
        lignes_ids2 = station2_info['lignes_ids']
        station_name1 = station1_info['station_name']
        station_name2 = station2_info['station_name']
        
        color1 = couleur_ligne(lignes_ids1)
        color2 = couleur_ligne(lignes_ids2)
        if(station_name1 == station_name2):
            color='black'
        if(color1 == color2):
            color=color1
        print(color1)
        print(color2)
        

        fig.add_trace(go.Scatter(x=[station1_pointx, station2_pointx], y=[-station1_pointy, -station2_pointy],
                                mode='lines', line=dict(color=color, width=2)))

    # Mise à jour du layout du graphe
    fig.update_layout(
            showlegend=False, 
            plot_bgcolor='white', 
            xaxis=dict(
                showgrid=False, 
                zeroline=False, 
                visible=False,
                scaleanchor='y',
                scaleratio=1
            ),
            yaxis=dict(
                showgrid=False, 
                zeroline=False, 
                visible=False
            ),
            autosize=True
        )
    
    graph_html = fig.to_html(full_html=False)
    
    return graph_html



if __name__ == '__main__':
    app.run(debug=True)
