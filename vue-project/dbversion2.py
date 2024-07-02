import pandas as pd
import pymysql

# Charger les fichiers GTFS nettoyés
stops = pd.read_csv('../Version2-3/stops.txt')
routes = pd.read_csv('../Version2-3/routes.txt')
transfers = pd.read_csv('../Version2-3/transfers.txt')

# Connexion à la base de données MySQL
db = pymysql.connect(
    host="localhost",
    user="root",
    password="louka",
    database="metro2",
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

# Créer un curseur pour exécuter les requêtes SQL
cursor = db.cursor()

# Mapper les données de stops.txt vers la table Stations
for index, row in stops.iterrows():
    sql = """
    INSERT INTO Stations (num_sommet, nom_sommet, numero_ligne, si_terminus, branchement)
    VALUES (%s, %s, %s, %s, %s)
    """
    # Remplacez les valeurs par celles correspondant aux colonnes de stops.txt
    values = (row['stop_id'], row['stop_name'], '', False, 0)  # À adapter selon les données GTFS disponibles
    cursor.execute(sql, values)

# Mapper les données de transfers.txt vers la table Aretes
for index, row in transfers.iterrows():
    sql = """
    INSERT INTO Aretes (num_sommet1, num_sommet2, temps_en_secondes)
    VALUES (%s, %s, %s)
    """
    # Remplacez les valeurs par celles correspondant aux colonnes de transfers.txt
    values = (row['from_stop_id'], row['to_stop_id'], row['min_transfer_time'])
    cursor.execute(sql, values)

# Mapper les données de stops.txt vers la table Pospoints
for index, row in stops.iterrows():
    sql = """
    INSERT INTO Pospoints (pointx, pointy, station_name, station_ids, lignes_ids)
    VALUES (%s, %s, %s, %s, %s)
    """
    # Remplacez les valeurs par celles correspondant aux colonnes de stops.txt et routes.txt
    values = (row['stop_lon'], row['stop_lat'], row['stop_name'], row['stop_id'], '')  # À adapter selon les données GTFS disponibles
    cursor.execute(sql, values)

# Commit des modifications et fermeture de la connexion
db.commit()
db.close()
