Projet de Métro EFRAIL
============================================================================================
Introduction

La solution que nous proposons est une application innovante permettant d’optimiser les temps de trajets dans le transport parisien.
============================================================================================
Fonctionnalités principales
============================================================================================
Utilisation de l’algorithme de Dijkstra pour calculer les itinéraires les plus courts et les plus rapides en fonction des données en temps réel.
Intégration des données d’Ile-de-France Mobilités.
Réduction de l’empreinte carbone en optimisant les trajets et en promouvant l’utilisation des transports en commun.
Application facile à utiliser, permettant à l’utilisateur d’obtenir des itinéraires optimisés.
Versions

Le projet est divisé en deux versions principales :
============================================================================================
Version 1 : Utilise les fichiers metro.txt et pospoints.txt.
Version 2-3 : Utilise les fichiers agency.txt, calendar.txt, calendar_dates.txt, pathways.txt, routes.txt, stops.txt, stop_extensions.txt, stop_times.txt, transfers.txt, trips.txt.
============================================================================================
Prérequis :
============================================================================================
Avant de pouvoir utiliser ce projet, vous devez installer certaines bibliothèques  nécessaires pour le back-end et font-end. Vous pouvez les installer en utilisant les commandes suivantes :
============================================================================================
Pour le back-end :
pip install Flask flask-cors pymysql networkx plotly pandas folium branca

============================================================================================

Cela installera les bibliothèques suivantes pour le back-end:
============================================================================================
Flask
Flask-CORS
PyMySQL
NetworkX
Plotly
Pandas
Folium
Branca
============================================================================================
Front-end
Pour le front-end, exécutez :
============================================================================================
npm install (dépendances présentes dans les fichiers package.json et package-lock.json)
============================================================================================
assurez-vous que toutes les dépendances présentes dans les fichiers package.json et package-lock.json sont installées.
============================================================================================
Structure des Données
============================================================================================
Version 1
============================================================================================
Les fichiers metro.txt et pospoints.txt contiennent les données nécessaires pour la version 1 du projet.

Structure de la Base de Données

Vous devez créer une base de données MySQL avec la structure suivante :

============================================================================================
-- Supprimer les tables si elles existent
DROP TABLE IF EXISTS Pospoints;
DROP TABLE IF EXISTS Aretes;
DROP TABLE IF EXISTS Stations;

-- Supprimer la base de données si elle existe
DROP DATABASE IF EXISTS metro;

-- Créer la nouvelle base de données
CREATE DATABASE metro;

-- Utiliser la nouvelle base de données
USE metro;

-- Créer la table Stations
CREATE TABLE Stations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    num_sommet VARCHAR(255),
    nom_sommet VARCHAR(255),
    numero_ligne VARCHAR(255),
    si_terminus BOOLEAN,
    branchement INT
);

-- Créer la table Aretes
CREATE TABLE Aretes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    num_sommet1 VARCHAR(255),
    num_sommet2 VARCHAR(255),
    temps_en_secondes VARCHAR(255)
);

-- Créer la table Pospoints
CREATE TABLE Pospoints (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pointx INT,
    pointy INT,
    station_name VARCHAR(255),
    station_ids VARCHAR(255),
    lignes_ids VARCHAR(255)
);

============================================================================================
Voici une fonction a mettre dans un autre fichier sql pour la version 1 :

DELIMITER $$
CREATE FUNCTION levenshtein( s1 VARCHAR(255), s2 VARCHAR(255) )
    RETURNS INT
    DETERMINISTIC
    BEGIN
        DECLARE s1_len, s2_len, i, j, c, c_temp, cost INT;
        DECLARE s1_char CHAR;
        -- max strlen=255
        DECLARE cv0, cv1 VARBINARY(256);

        SET s1_len = CHAR_LENGTH(s1), s2_len = CHAR_LENGTH(s2), cv1 = 0x00, j = 1, i = 1, c = 0;

        IF s1 = s2 THEN
            RETURN 0;
        ELSEIF s1_len = 0 THEN
            RETURN s2_len;
        ELSEIF s2_len = 0 THEN
            RETURN s1_len;
        ELSE
            WHILE j <= s2_len DO
                SET cv1 = CONCAT(cv1, UNHEX(HEX(j))), j = j + 1;
            END WHILE;
            WHILE i <= s1_len DO
                SET s1_char = SUBSTRING(s1, i, 1), c = i, cv0 = UNHEX(HEX(i)), j = 1;
                WHILE j <= s2_len DO
                    SET c = c + 1;
                    IF s1_char = SUBSTRING(s2, j, 1) THEN
                        SET cost = 0; ELSE SET cost = 1;
                    END IF;
                    SET c_temp = CONV(HEX(SUBSTRING(cv1, j, 1)), 16, 10) + cost;
                    IF c > c_temp THEN SET c = c_temp; END IF;
                    SET c_temp = CONV(HEX(SUBSTRING(cv1, j+1, 1)), 16, 10) + 1;
                    IF c > c_temp THEN
                        SET c = c_temp;
                    END IF;
                    SET cv0 = CONCAT(cv0, UNHEX(HEX(c))), j = j + 1;
                END WHILE;
                SET cv1 = cv0, i = i + 1;
            END WHILE;
        END IF;
        RETURN c;
    END$$
DELIMITER ;
============================================================================================
Version 2-3
Les fichiers agency.txt, calendar.txt, calendar_dates.txt, pathways.txt, routes.txt, stops.txt, stop_extensions.txt, stop_times.txt, transfers.txt, trips.txt contiennent les données nécessaires pour les versions 2-3 du projet. 
Vous devez les deposer a l'interieur du dossier, je ne peux vous les fournir trop volumineux pour github.   

Structure de la Base de Données
============================================================================================
Vous devez créer une base de données MySQL avec la structure suivante:

============================================================================================
-- Supprimer les tables si elles existent
DROP TABLE IF EXISTS Transfers;
DROP TABLE IF EXISTS Stations;
DROP TABLE IF EXISTS Aretes;

-- Supprimer la base de données si elle existe
DROP DATABASE IF EXISTS metrogtfs;

-- Créer la nouvelle base de données
CREATE DATABASE metrogtfs;

-- Utiliser la nouvelle base de données
USE metrogtfs;

-- Créer la table Stations
CREATE TABLE Stations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    num_sommet VARCHAR(255),
    nom_sommet VARCHAR(255),
    longitude VARCHAR(255),
    latitude VARCHAR(255),
    wheelchair_boarding VARCHAR(255),
    numero_ligne VARCHAR(255)
);

-- Créer la table Transfers
CREATE TABLE Transfers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    num_sommet1 VARCHAR(255),
    num_sommet2 VARCHAR(255),
    min_transfer_time VARCHAR(255)
);

-- Créer la table Aretes
CREATE TABLE Aretes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    num_sommet1 VARCHAR(255),
    num_sommet2 VARCHAR(255),
    temps_en_secondes VARCHAR(255),
    numero_ligne VARCHAR(255)
);
============================================================================================
Instructions d'Utilisation
============================================================================================
Clonez le dépôt du projet sur votre machine locale.
Assurez-vous d'avoir tous les fichiers de données nécessaires dans les bons dossiers (Version1 et Version2-3).
Configurez votre serveur MySQL et créez les bases de données et tables en utilisant les scripts SQL fournis.
Changez les mots de passe MySQL dans les fichiers app.py, app2.py, db.py, et db2.py selon les informations de votre serveur.
Installez les bibliothèques Python nécessaires en utilisant pip (voir les commandes dans la section Prérequis).
============================================================================================
Lancement du Programme
============================================================================================
Version 1
Exécutez db.py pour insérer toutes les données de la version 1 dans MySQL.
Lancez app.py pour démarrer la version 1 de l'application.
============================================================================================
Version 2-3
Ouvrez cleandb-version2-3.ipynb et exécutez les cellules une par une pour bien nettoyer toutes les données.
Exécutez db2.py pour insérer toutes les données de la version 2-3 dans MySQL. Ce processus peut prendre 15-20 minutes.
Lancez app2.py pour démarrer la version 2-3 de l'application.
Lancement de l'Interface Web
============================================================================================
Accédez au dossier vue-projet.
Exécutez la commande npm run dev pour lancer le site web et profiter de toutes les versions de l'application.
============================================================================================
Conclusion
Merci d'avoir choisi le projet de Métro EFRAIL. Nous espérons que notre application vous sera utile pour optimiser vos trajets dans le transport parisien.







