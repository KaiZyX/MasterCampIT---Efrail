<template>
  <div class="container">
    <div class="search-form-container">
      <div class="search-form-header">
        On va où ?
      </div>
      <div class="search-form">
        <input type="text" v-model="from" placeholder="Start" />
        <input type="text" v-model="to" placeholder="End" />
        <div class="redirection_map">
          <button class="Bouton" @click="fetchShortestPath">Go</button>
        </div>
      </div>
    </div>
    <div v-if="url" class="map-output"> 
      <object :data="url" width="800px" height="600px" style="overflow:auto;border:5px ridge blue">
      </object>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      from: '',
      to: '',
      url: ''
    };
  },
  methods: {
    fetchShortestPath() {
      this.url = `http://127.0.0.1:5000/api/shortest_path_info?start_station_name=${this.from}&end_station_name=${this.to}`;
    }
  }
};
</script>

<style scoped>
.container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.search-form-container, .map-output {
  flex: 1; /* Permet aux enfants de prendre une largeur égale */
}

/* Ajustez selon vos besoins pour un meilleur rendu */
.search-form-container {
  padding-right: 20px; /* Ajoute un peu d'espace entre les deux colonnes */
}

.map-output {
  padding-left: 20px; /* Ajoute un peu d'espace entre les deux colonnes */
}

.search-form-header {
  margin-top: 0; /* Assurez-vous qu'il n'y a pas d'espace au-dessus du header */
  margin-bottom: 20px; /* Ajoutez un espace entre le header et le formulaire si nécessaire */
}

.search-form-container {
  display: flex;
  flex-direction: column;
  padding-right: 20px; /* Ajustez selon vos besoins */
}
</style>