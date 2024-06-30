<template>
  <div class="container">
    <div class="search-form-container">
      <div class="search-form-header">
        On va où ?
      </div>
      <div class="search-form">
        <input
          type="text"
          id="from"
          v-model="from"
          placeholder="Start"
          @input="getSuggestions('from')"
        />
        <ul v-if="fromSuggestions.length" class="suggestions-list">
          <li
            v-for="suggestion in fromSuggestions"
            :key="suggestion"
            @click="selectSuggestion('from', suggestion)"
          >
            {{ suggestion }}
          </li>
        </ul>
        <input
          type="text"
          id="to"
          v-model="to"
          placeholder="End"
          @input="getSuggestions('to')"
        />
        <ul v-if="toSuggestions.length" class="suggestions-list">
          <li
            v-for="suggestion in toSuggestions"
            :key="suggestion"
            @click="selectSuggestion('to', suggestion)"
          >
            {{ suggestion }}
          </li>
        </ul>
        <div class="redirection_map">
          <button class="Bouton" @click="fetchShortestPath">Go</button>
        </div>
      </div>
    </div>
    <div v-if="url" class="map-output">
      <object :data="url" width="800px" height="600px" style="overflow:auto;border:5px ridge lightblue">
      </object>
    </div>
  </div>
</template>

<script>
// Importez Axios si vous l'avez installé
import axios from 'axios';

export default {
  data() {
    return {
      from: '',
      to: '',
      url: '',
      fromSuggestions: [],
      toSuggestions: []
    };
  },
  methods: {
    fetchShortestPath() {
      const startStation = encodeURIComponent(this.from);
      const endStation = encodeURIComponent(this.to);
      this.url = `http://127.0.0.1:8000/api/shortest_path_info?start_station_name=${this.from}&end_station_name=${this.to}`;
    },
    async getSuggestions(inputId) {
      const inputVal = this[inputId];
      if (inputVal.length >= 3) {
        try {
          const response = await fetch(`http://127.0.0.1:8000/api/stations?query=${inputVal}`);
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
          const data = await response.json();
          if (inputId === 'from') {
            this.fromSuggestions = data;
          } else {
            this.toSuggestions = data;
          }
        } catch (error) {
          console.error('Error fetching suggestions:', error);
          if (inputId === 'from') {
            this.fromSuggestions = [];
          } else {
            this.toSuggestions = [];
          }
        }
      } else {
        if (inputId === 'from') {
          this.fromSuggestions = [];
        } else {
          this.toSuggestions = [];
        }
      }
    },
    selectSuggestion(inputId, suggestion) {
      this[inputId] = suggestion;
      if (inputId === 'from') {
        this.fromSuggestions = [];
      } else {
        this.toSuggestions = [];
      }
    }
  }
};
</script>


<style scoped>
  .suggestions-list {
    list-style-type: none;
    padding: 0;
    margin: 0;
    border: 1px solid #ddd;
    max-height: 150px;
    overflow-y: auto;
    background-color: #fff;
    position: absolute;
    z-index: 1000;
    width: calc(100% - 22px); /* Ajustement pour compenser le padding des champs de saisie */
    max-width: 300px; /* Limitez la largeur des suggestions à celle des champs de saisie */
  }

  .suggestions-list li {
    padding: 8px;
    cursor: pointer;
  }

  .suggestions-list li:hover {
    background-color: #f0f0f0;
  }

  .container {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }

  .search-form-container {
    display: flex;
    flex-direction: column;
    padding-right: 20px; /* Ajustez selon vos besoins */
    padding: 20px;
    background-color: #c9e4fe;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    max-width: 350px; /* Limitez la largeur du conteneur */
    margin: 20px auto; /* Centre le conteneur horizontalement */
  }

  .search-form-header {
    background-color: #647fa9; /* Bleu plus foncé */
    color: white;
    padding: 10px;
    width: 100%;
    text-align: center;
    border-radius: 10px 10px 0 0;
    margin-top: 0; /* Assurez-vous qu'il n'y a pas d'espace au-dessus du header */
    margin-bottom: 20px; /* Ajoutez un espace entre le header et le formulaire si nécessaire */
  }

  .search-form {
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: #c9e4fe;
    padding: 20px;
    border-radius: 0 0 10px 10px;
  }

  .search-form input {
    margin: 5px;
    padding: 10px;
    width: 300px;
  }

  .redirection_map {
    margin: 10px;
  }

  .Bouton {
    padding: 10px 20px;
    background-color: #ff7f50;
    color: white;
    text-decoration: none;
    border-radius: 5px;
    cursor: pointer;
  }

  .Bouton:hover {
    background-color: #7dbac8;
  }

  .map-output {
    margin-bottom: 40px; /* Ajoute de l'espace après la carte */
  }

  .Global {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .Bouton {
    text-align: center;
    background-color: #f5f5f5;
    color: black;
    padding: 6px 12px;
    border-radius: 5px;
  }

  .text {
    font-size: 18px;
    text-align: center;
  }

  .carousel-control-prev {
    background-color: #a7c7e7;
  }

  .carousel-control-prev-icon {
    background-color: #a7c7e7;
  }

  .carousel-control-next-icon {
    background-color: #a7c7e7;
  }

  .carousel-control-next {
    background-color: #a7c7e7;
  }

  .carousel-inner {
    max-width: 500px;
    margin: 0 auto;
  }

  .ok {
    margin-top: 100px;
    background-color: rgb(187, 145, 145);
    font-size: 25px;
  }

  .fond {
    background-color: rgb(255, 255, 255);
  }

  .table {
    width: 80%; /* Ajustez la largeur du tableau */
    margin: 20px auto; /* Centrer le tableau et ajouter de l'espace autour */
    border-collapse: collapse; /* Supprime les espaces entre les cellules */
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1); /* Ajoute une ombre pour un effet de profondeur */
  }

  .table th,
  .table td {
    padding: 15px; /* Ajustez l'espacement à l'intérieur des cellules */
    text-align: left; /* Alignement du texte */
    border-bottom: 1px solid #ddd; /* Ligne de séparation */
  }

  .table th {
    background-color: #9bcdff; /* Couleur de fond pour les en-têtes */
    color: white; /* Couleur du texte pour les en-têtes */
  }

  .table tr:nth-child(even) {
    background-color: #f2f2f2; /* Couleur de fond pour les lignes paires */
  }

  .table tr:hover {
    background-color: #ddd; /* Couleur de fond au survol */
  }

  .table td {
    color: #333; /* Couleur du texte pour les cellules */
  }

  /* Ajoutez cette classe si elle n'existe pas déjà */
  .coll1,
  .table th:not(.coll1),
  .table td {
    background-color: #fff; /* Couleur de fond uniforme pour toutes les cellules */
  }
</style>
