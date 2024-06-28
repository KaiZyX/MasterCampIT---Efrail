<template>
  <div class="Global">
    <p> </p>
    <div class="fond">
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
      <div class="text">
        <strong>Efrail vous offre une multitude d'avantages, soigneusement détaillés ci-dessous.</strong>
        <br>
        <br>
      </div>
      <table class="table">
        <thead>
          <tr>
            <th class="coll1" scope="col">Réduction du temps de trajet</th>
            <th class="coll1">Diminution des émissions de CO2</th>
            <th class="coll1" scope="col">Amélioration de l'expérience utilisateur</th>
          </tr>
        </thead>
        <tbody class="table-group-divider">
          <tr>
            <td>Permet de réduire considérablement le temps de trajet en proposant les itinéraires les plus rapides et les moins encombrés.</td>
            <td>Contribue à la diminution des émissions de CO2 en incitant les utilisateurs à privilégier les transports en commun plutôt que les véhicules individuels.</td>
            <td>Améliore l'expérience utilisateur en fournissant des itinéraires clairs, rapides et personnalisés, rendant les déplacements plus simples et agréables.</td>
          </tr>
        </tbody>
      </table>
      <p></p>
      <br>
      <div id="carouselExampleCaptions" class="carousel slide">
        <div class="carousel-indicators">
          <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
          <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="1" aria-label="Slide 2"></button>
          <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="2" aria-label="Slide 3"></button>
        </div>
        <div class="carousel-inner">
          <div class="carousel-item active">
            <img src="@/assets/train1.avif" class="img1" alt="...">
            <div class="carousel-caption d-none d-md-block">
              <p></p>
            </div>
          </div>
          <div class="carousel-item">
            <img src="@/assets/train3.jpg" class="img3" alt="...">
            <div class="carousel-caption d-none d-md-block">
              <p></p>
            </div>
          </div>
          <div class="carousel-item">
            <img src="@/assets/train2.jpg" class="img2" alt="...">
            <div class="carousel-caption d-none d-md-block">
              <p></p>
            </div>
          </div>
        </div>
        <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide="prev">
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide="next">
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Next</span>
        </button>
        <p></p>
      </div>
    </div>
    <p></p>
  </div>
</template>

<script>
import $ from 'jquery';

export default {
  data() {
    return {
      from: '',
      to: '',
      fromSuggestions: [],
      toSuggestions: [],
      url: ''
    };
  },
  methods: {
    fetchShortestPath() {
      this.url = `http://127.0.0.1:5000/api/shortest_path_info?start_station_name=${this.from}&end_station_name=${this.to}`;
    },
    getSuggestions(inputId) {
      const inputVal = this[inputId];
      if (inputVal.length >= 3) {
        $.ajax({
          url: `http://127.0.0.1:5000/api/stations?query=${inputVal}`,
          method: 'GET',
          success: (data) => {
            if (inputId === 'from') {
              this.fromSuggestions = data;
            } else {
              this.toSuggestions = data;
            }
          }
        });
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
  width: calc(100% - 20px); /* Ajustez la largeur pour correspondre à vos entrées */
}

.suggestions-list li {
  padding: 8px;
  cursor: pointer;
}

.suggestions-list li:hover {
  background-color: #f0f0f0;
}
</style>
