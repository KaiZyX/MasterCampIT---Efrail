<template>
    <div class="container">
      <p class="description">Voici la liste des stations de Paris</p>
      <div v-if="url" class="map-output">
        <object :data="url" width="800px" height="600px" style="overflow:auto;border:5px ridge lightblue">
        </object>
      </div>
    </div>
  </template>
  
  
  
  <script>
  export default {
    data() {
      return {
        url: '',
      };
    },
    methods: {
      line_stations() {
        this.url = `http://127.0.0.1:5000/generate_map`;
      },
    },
    mounted() {
      this.line_stations();
    },
  };
  </script>
  
  <style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.description {
  font-size: 18px;
  text-align: center;
  margin-bottom: 20px; /* Espace entre le texte et la carte */
}

.map-output {
  margin-bottom: 40px; /* Ajoute de l'espace après la carte */
}

/* Autres styles existants */
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
  width: calc(100% - 22px);
  max-width: 300px;
}

.suggestions-list li {
  padding: 8px;
  cursor: pointer;
}

.suggestions-list li:hover {
  background-color: #f0f0f0;
}

.search-form-container {
  display: flex;
  flex-direction: column;
  padding-right: 20px;
  padding: 20px;
  background-color: #c9e4fe;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 350px;
  margin: 20px auto;
}

.search-form-header {
  background-color: #647fa9;
  color: white;
  padding: 10px;
  width: 100%;
  text-align: center;
  border-radius: 10px 10px 0 0;
  margin-top: 0;
  margin-bottom: 20px;
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

.Global {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
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
  width: 80%;
  margin: 20px auto;
  border-collapse: collapse;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.table th,
.table td {
  padding: 15px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

.table th {
  background-color: #9bcdff;
  color: white;
}

.table tr:nth-child(even) {
  background-color: #f2f2f2;
}

.table tr:hover {
  background-color: #ddd;
}

.table td {
  color: #333;
}

.coll1,
.table th:not(.coll1),
.table td {
  background-color: #fff;
}
</style>
