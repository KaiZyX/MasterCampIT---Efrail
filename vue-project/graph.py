import requests

# Remplacez cette URL par l'URL de votre API si elle est différente
base_url = "http://127.0.0.1:5000/api"

# Tester l'endpoint /stations
response_stations = requests.get(f"{base_url}/stations")
print("Stations:", response_stations.json())

# Tester l'endpoint /connections
response_connections = requests.get(f"{base_url}/connections")
print("Connections:", response_connections.json())

# Pour /api/map, comme il retourne une image, vous ne pouvez pas simplement afficher le JSON
# Vous devriez sauvegarder le contenu de la réponse dans un fichier image et l'ouvrir
response_map = requests.get(f"{base_url}/map")
with open("map_result.png", "wb") as f:
    f.write(response_map.content)
print("Map image saved as map_result.png.")