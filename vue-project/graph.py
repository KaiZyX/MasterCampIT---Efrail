import pymysql
import networkx as nx
import matplotlib.pyplot as plt

def get_db_connection():
    return pymysql.connect(host='localhost', user='root', password='louka', db='metro')

def creer_graphe():
    conn = get_db_connection()
    cursor = conn.cursor()
    G = nx.Graph()
    cursor.execute("SELECT id, num_sommet FROM Stations")
    stations = cursor.fetchall()
    for station in stations:
        G.add_node(station[1], id=station[0])
    cursor.execute("SELECT num_sommet1, num_sommet2, temps_en_secondes FROM Aretes")
    aretes = cursor.fetchall()
    for sommet1, sommet2, temps in aretes:
        G.add_edge(sommet1, sommet2, weight=int(temps))
    conn.close()
    return G

def trouver_chemin(station_depart, station_arrivee):
    G = creer_graphe()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT num_sommet FROM Stations WHERE nom_sommet = %s", (station_depart,))
    depart_id = cursor.fetchone()[0]
    cursor.execute("SELECT num_sommet FROM Stations WHERE nom_sommet = %s", (station_arrivee,))
    arrivee_id = cursor.fetchone()[0]
    conn.close()
    chemin = nx.dijkstra_path(G, source=depart_id, target=arrivee_id, weight='weight')
    return chemin

# Exemple d'utilisation
station_depart = input("Entrez la station de départ: ")
station_arrivee = input("Entrez la station d'arrivée: ")
chemin = trouver_chemin(station_depart, station_arrivee)
print("Le chemin le plus rapide est :", chemin)

G = creer_graphe()

nx.draw(G, with_labels=True, font_weight='bold')
plt.show()