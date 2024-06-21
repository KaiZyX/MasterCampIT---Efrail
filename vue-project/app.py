from flask import Flask, jsonify, request, send_file, current_app, send_from_directory
import pymysql
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import os
import pymysql.cursors
import networkx as nx

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the API. Use /api/stations or /api/connections to access data."


def get_db_connection():
    return pymysql.connect(host='localhost', user='root', password='louka', db='metro')

@app.route('/api/stations', methods=['GET'])
def get_stations():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM Stations')
        stations = cursor.fetchall()
    connection.close()
    return jsonify(stations)

@app.route('/api/connections', methods=['GET'])
def get_connections():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM Connections')
        connections = cursor.fetchall()
    connection.close()
    return jsonify(connections)

@app.route('/api/map', methods=['GET'])
def get_map():
    db_connection = None  # Assurez-vous que connection est définie avant le bloc try
    try:
        db_connection = get_db_connection()
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

        for row in connections:
            print(f"x1: {row[0]}, y1: {row[1]}, x2: {row[2]}, y2: {row[3]}, lignes_ids1: {row[4]}, lignes_ids2: {row[5]}")

        # Dessin des points et des connexions
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')

        # Dessin des connexions avec la couleur déterminée
        for connection in connections:
            # Extraire les IDs de ligne sous forme de listes
            lignes_ids1 = connection[4].split(',')
            lignes_ids2 = connection[5].split(',')
            # Trouver les IDs communs
            common_ids = set(lignes_ids1).intersection(lignes_ids2)
            # Pour cet exemple, on prend le premier ID commun pour déterminer la couleur
            if common_ids:
                common_id = next(iter(common_ids))
                color = couleur_ligne(common_id)
                ax.plot([connection[0], connection[2]], [-connection[1], -connection[3]], color=color, linewidth=2)

        # Dessin des points
        x_points = [point[0] for point in points]
        y_points = [-point[1] for point in points]
        ax.scatter(x_points, y_points, color='black', edgecolors='black', s=15)  # s contrôle la taille
       
        ax.axis('off')
    
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close(fig)

        return send_file(buf, mimetype='image/png')
    
    except Exception as e:
        current_app.logger.error("Erreur: %s", e)
        return jsonify({'error': str(e)}), 500
    finally:
        if db_connection:
            db_connection.close()

# def creer_graphe():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     G = nx.Graph()
#     cursor.execute("SELECT id, num_sommet FROM Stations")
#     stations = cursor.fetchall()
#     for station in stations:
#         G.add_node(station[1], id=station[0])
#     cursor.execute("SELECT num_sommet1, num_sommet2, temps_en_secondes FROM Aretes")
#     aretes = cursor.fetchall()
#     for sommet1, sommet2, temps in aretes:
#         G.add_edge(sommet1, sommet2, weight=int(temps))
#     conn.close()
#     return G

def trouver_chemin_et_temps(station_depart, station_arrivee):
    # G = creer_graphe()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT num_sommet FROM Stations WHERE nom_sommet = %s", (station_depart,))
    depart_id = cursor.fetchone()[0]
    cursor.execute("SELECT num_sommet FROM Stations WHERE nom_sommet = %s", (station_arrivee,))
    arrivee_id = cursor.fetchone()[0]
    conn.close()
    chemin = nx.dijkstra_path(G, source=depart_id, target=arrivee_id, weight='weight')
    temps_total = nx.dijkstra_path_length(G, source=depart_id, target=arrivee_id, weight='weight')
    return chemin, temps_total


# def get_path_data(chemin, db_connection):
#     # Récupère les données des points et des connexions pour les IDs de sommets dans 'chemin'
#     points = []
#     connections = []
#     with db_connection.cursor() as cursor:
#         # Récupérer les points
#         placeholders = ','.join(['%s'] * len(chemin))
#         cursor.execute(f"SELECT pointx, pointy, station_name FROM Pospoints WHERE station_ids IN ({placeholders})", chemin)
#         points = cursor.fetchall()

#         # Récupérer les connexions
#         # Note: Cette requête doit être adaptée à votre schéma de base de données et à la manière dont vous stockez les connexions
#         cursor.execute(f'''
#             SELECT 
#                 A.pointx AS x1, A.pointy AS y1, 
#                 B.pointx AS x2, B.pointy AS y2,
#                 A.lignes_ids AS lignes_ids1, B.lignes_ids AS lignes_ids2
#             FROM 
#                 Aretes C
#                 JOIN Pospoints A ON FIND_IN_SET(C.num_sommet1, A.station_ids)
#                 JOIN Pospoints B ON FIND_IN_SET(C.num_sommet2, B.station_ids)
#             WHERE 
#                 C.num_sommet1 IN ({placeholders}) AND
#                 C.num_sommet2 IN ({placeholders})
#         ''', chemin * 2)  # La liste chemin est répétée pour correspondre aux placeholders pour num_sommet1 et num_sommet2
#         connections = cursor.fetchall()

#     return points, connections

app.route('/api/mapPath', methods=['GET'])
def get_map_path():
    station_depart = request.args.get('depart')
    station_arrivee = request.args.get('arrivee')
    if not station_depart or not station_arrivee:
        return jsonify({'error': 'Les paramètres "depart" et "arrivee" sont requis'}), 400

    db_connection = get_db_connection()
    cursor = db_connection.cursor()
    try:
        chemin, temps_total = trouver_chemin_et_temps(station_depart, station_arrivee)
        informations_chemin = []

        for i in range(len(chemin) - 1):
            station_id1 = chemin[i]
            station_id2 = chemin[i + 1]
            cursor.execute('''
                SELECT 
                    A.pointx AS x1, A.pointy AS y1, 
                    B.pointx AS x2, B.pointy AS y2,
                    A.lignes_ids AS lignes_ids1, B.lignes_ids AS lignes_ids2,
                    C.ligne_id
                FROM 
                    Aretes C
                    JOIN Pospoints A ON FIND_IN_SET(C.num_sommet1, A.station_ids)
                    JOIN Pospoints B ON FIND_IN_SET(C.num_sommet2, B.station_ids)
                WHERE
                    A.station_id = %s AND B.station_id = %s;
            ''', (station_id1, station_id2))
            informations_chemin.extend(cursor.fetchall())

        # Dessin des points et des connexions
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('white')
        ax.set_facecolor('white')

        # Dessin des connexions
        for connection in informations_chemin:
            lignes_ids1 = connection[4].split(',')
            lignes_ids2 = connection[5].split(',')
            common_ids = set(lignes_ids1).intersection(lignes_ids2)
            if common_ids:
                common_id = next(iter(common_ids))
                color = couleur_ligne(common_id)
                ax.plot([connection[0], connection[2]], [-connection[1], -connection[3]], color=color, linewidth=2)

        # Dessin des points
        x_points = [point[0] for point in informations_chemin]
        y_points = [-point[1] for point in informations_chemin]
        ax.scatter(x_points, y_points, color='black', edgecolors='black', s=15)

        ax.axis('off')

        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        plt.close(fig)

        return send_file(buf, mimetype='image/png')
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if db_connection:
            db_connection.close()
















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
    return couleurs_metro.get(ligne_id, "#FFFFFF")  # Retourne blanc par défaut si la ligne n'est pas trouvée


if __name__ == '__main__':
    app.run(debug=True)

