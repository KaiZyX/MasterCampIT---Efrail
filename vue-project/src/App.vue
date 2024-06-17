<!-- src/App.vue -->
<template>
  <div id="app">
    <Header /> <!-- Ajout du Header ici -->
    <main>
      
      <TrainList></TrainList>
    </main>
    <Footer></Footer>
  </div>
  
</template>

<script>
import Header from './components/Header.vue'; // Import du composant Header
import TrainList from './components/TrainList.vue';
import Map from './components/Map.vue';
import Footer from './components/Footer.vue';


export default {
  name: 'App',
  components: {
    Header, // Enregistrement du composant Header
    TrainList,
    Map,
    Footer,
    
  },
  data() {
    return 
  },
  methods: {
    
  }
};
</script>

<style>
body {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  margin: 0;
  padding: 0;
}
#app {
  text-align: center;
}

</style>
