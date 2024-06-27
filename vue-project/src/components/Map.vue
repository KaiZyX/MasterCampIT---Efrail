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
    <div id="graph-container"></div>   
</template>

<script>
export default {
  data() {
    return {
      from: '',
      to: ''
    }
  },
  methods: {
    async fetchShortestPath() {
      try {
        const response = await fetch(`/api/shortest_path_info?start_station_name=${this.from}&end_station_name=${this.to}`);
        const graphHtml = await response.text();
        document.getElementById('graph-container').innerHTML = graphHtml;
      } catch (error) {
        
      }
    }
  }
}
</script>
