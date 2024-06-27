<template>
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
  <div v-if="url"> 
    <object :data="url" width="800px" height="600px" style="overflow:auto;border:5px ridge blue">
    </object>
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
#graph-container {
  width: 100%;
  height: 600px; /* Définir une hauteur fixe pour tester */
}
</style>