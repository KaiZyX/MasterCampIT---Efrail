from flask import Flask, jsonify, request, send_file, current_app
import pymysql
import matplotlib.pyplot as plt
import io
from flask import send_from_directory
import os
import pymysql.cursors

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
                    B.pointx AS x2, B.pointy AS y2
                FROM 
                    Aretes C
                    JOIN Pospoints A ON FIND_IN_SET(C.num_sommet1, A.station_ids)
                    JOIN Pospoints B ON FIND_IN_SET(C.num_sommet2, B.station_ids);
            ''')
            connections = cursor.fetchall()

        # Dessin des points et des connexions
        fig, ax = plt.subplots()
        fig.patch.set_facecolor('black')
        ax.set_facecolor('black')

        x_points = [point[0] for point in points]  # Supposons que 'pointx' est la première colonne
        y_points = [point[1] for point in points]  # Supposons que 'pointy' est la deuxième colonne

        for connection in connections:
            ax.plot([connection[0], connection[2]], [connection[1], connection[3]], color='white')  # Ajustez les indices selon l'ordre des colonnes

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


if __name__ == '__main__':
    app.run(debug=True)

