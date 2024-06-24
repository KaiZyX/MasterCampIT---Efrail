from flask import Flask, jsonify, request, send_file, current_app, send_from_directory
import pymysql
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import os
import pymysql.cursors
import networkx as nx
from plotly.io import to_html
import plotly.graph_objects as go
from flask import Flask, jsonify
import plotly.graph_objects as go


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


app = Flask(__name__)

# Affiche le graphique de toutes les lignes de metro
@app.route('/api/map', methods=['GET'])
def get_map():
    db_connection = None
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

    db_connection = get_db_connection()
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

if __name__ == '__main__':
    app.run(debug=True)
 