from flask import Flask, jsonify, request, send_file
import pymysql
import matplotlib.pyplot as plt
import io
from flask import send_from_directory
import os

app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome to the API. Use /api/stations or /api/connections to access data."


def get_db_connection():
    connection = pymysql.connect(
        host="localhost",
        user="root",
        password="louka",
        database="metro",
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

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
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute('SELECT pointx, pointy, station_name FROM Pospoints')
        points = cursor.fetchall()
    connection.close()

    # Créer une figure avec un fond noir
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    # Ajouter les points
    for point in points:
        ax.plot(point['pointx'], point['pointy'], 'ro')  # 'ro' pour les points rouges

    # Supprimer les axes
    ax.axis('off')

    # Sauvegarder l'image dans un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)

    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)


