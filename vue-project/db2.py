import pandas as pd
from datetime import datetime
import pymysql
from collections import defaultdict

# Chargement des fichiers txt
stops = pd.read_csv('../Version2-3/stops.txt')
routes = pd.read_csv('../Version2-3/routes.txt')
trips = pd.read_csv('../Version2-3/trips.txt')
stop_times = pd.read_csv('../Version2-3/stop_times.txt')
transfers = pd.read_csv('../Version2-3/transfers.txt')

# Établir la connexion à la base de données MySQL
db = pymysql.connect(
    host="localhost",
    user="root",
    password="Florian1!",
    database="metrogtfs",
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)
cursor = db.cursor()

# Fonction pour ajuster les heures supérieures ou égales à 24:00:00
def adjust_hour(hour_str):
    hour, minute, second = map(int, hour_str.split(':'))
    if hour >= 24:
        hour -= 24
    return f"{hour:02}:{minute:02}:{second:02}"

# Fonction pour insérer les données dans la table Aretes
def insert_into_aretes(num_sommet1, num_sommet2, temps_en_secondes, numero_ligne):
    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO Aretes (num_sommet1, num_sommet2, temps_en_secondes, numero_ligne) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (num_sommet1, num_sommet2, temps_en_secondes, numero_ligne))
        db.commit()
    except Exception as e:
        print(f"Erreur lors de l'insertion dans la table Aretes : {e}")
        db.rollback()

# Insérer les données dans la table Stations
for index, row in stops.iterrows():
    num_sommet = row['stop_id']
    nom_sommet = row['stop_name']
    longitude = row['stop_lon']
    latitude = row['stop_lat']
    wheelchair_boarding = row['wheelchair_boarding']

    # Trouver la colonne numero_ligne
    stop_times_filtered = stop_times[stop_times['stop_id'] == num_sommet]
    if not stop_times_filtered.empty:
        trip_id = stop_times_filtered.iloc[0]['trip_id']
        route_id = trips[trips['trip_id'] == trip_id].iloc[0]['route_id']
        numero_ligne = routes[routes['route_id'] == route_id].iloc[0]['route_short_name']
    else:
        numero_ligne = None

    # Insérer les données dans la table Stations
    insert_station_query = """
    INSERT INTO Stations (num_sommet, nom_sommet, longitude, latitude, wheelchair_boarding, numero_ligne)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_station_query, (num_sommet, nom_sommet, longitude, latitude, wheelchair_boarding, numero_ligne))

# Insérer les données dans la table Transfers 
for index, row in transfers.iterrows():
    num_sommet1 = row['from_stop_id']
    num_sommet2 = row['to_stop_id']
    min_transfer_time = row['min_transfer_time']

    insert_transfer_query = """
    INSERT INTO Transfers (num_sommet1, num_sommet2, min_transfer_time)
    VALUES (%s, %s, %s)
    """
    cursor.execute(insert_transfer_query, (num_sommet1, num_sommet2, min_transfer_time))

# Dictionnaire pour stocker les arêtes entre les sommets
edges = defaultdict(list)

# Ensemble pour suivre les arêtes déjà ajoutées
added_edges = set()

# Récupérer tous les route_short_name distincts
route_short_names = routes['route_short_name'].unique()

# Boucler sur chaque route_short_name
for route_short_name in route_short_names:
    # Filtrer les lignes correspondant à la ligne actuelle dans routes.txt
    current_route = routes[routes['route_short_name'] == route_short_name]

    # Filtrer les trajets associés à la ligne actuelle dans trips.txt
    current_trips = trips[trips['route_id'].isin(current_route['route_id'])]

    # Parcourir chaque trajet de la ligne actuelle
    for index, trip_row in current_trips.iterrows():
        # Filtrer les lignes de stop_times.txt pour ce trip_id
        trip_id = trip_row['trip_id']
        filtered_stop_times = stop_times[stop_times['trip_id'] == trip_id]
        
        # Initialiser les variables pour la première ligne
        previous_stop_id = None
        previous_arrival_time = None
        
        # Récupérer le numéro de ligne (route_short_name)
        numero_ligne = route_short_name
        
        # Parcourir les lignes de stop_times.txt pour ce trip_id
        for st_index, st_row in filtered_stop_times.iterrows():
            stop_id = st_row['stop_id']
            arrival_time_str = st_row['arrival_time']
            
            # Ajuster l'heure si nécessaire
            arrival_time_str = adjust_hour(arrival_time_str)
            
            # Convertir l'heure d'arrivée en objet datetime
            arrival_time = datetime.strptime(arrival_time_str, '%H:%M:%S').time()
            
            # Si c'est la première ligne pour ce trajet, simplement enregistrer le stop_id et l'heure d'arrivée
            if previous_stop_id is None:
                previous_stop_id = stop_id
                previous_arrival_time = arrival_time
                continue
            
            # Vérifier si cette arête a déjà été ajoutée
            edge_key = (previous_stop_id, stop_id)
            if edge_key in added_edges:
                # Si oui, passer à la ligne suivante
                previous_stop_id = stop_id
                previous_arrival_time = arrival_time
                continue
            
            # Calculer le temps moyen si cette arête est présente dans plusieurs trajets
            existing_edges = edges[edge_key]
            if existing_edges:
                existing_times = [edge['time'] for edge in existing_edges]
                existing_mean = sum(existing_times) / len(existing_times)
            else:
                existing_mean = 0
            
            # Calculer le temps pour cette arête
            time_diff = (arrival_time.hour * 3600 + arrival_time.minute * 60 + arrival_time.second) - \
                        (previous_arrival_time.hour * 3600 + previous_arrival_time.minute * 60 + previous_arrival_time.second)
            
            # Si existing_mean est différent de 0, calculer la moyenne, sinon utiliser time_diff
            if existing_mean != 0:
                new_time = (existing_mean + time_diff) / 2
            else:
                new_time = time_diff

            # Ajouter cette arête avec son temps moyen
            edges[edge_key].append({'time': new_time, 'stop_id': stop_id})
            added_edges.add(edge_key)
        
            # Insérer les données dans la table Aretes avec le numero_ligne
            insert_into_aretes(previous_stop_id, stop_id, new_time, numero_ligne)
            
            # Mettre à jour les variables pour l'itération suivante
            previous_stop_id = stop_id
            previous_arrival_time = arrival_time

# Commit les transactions
db.commit()

# Fermer la connexion
cursor.close()
db.close()
