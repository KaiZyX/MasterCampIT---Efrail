<!-- src/App.vue -->
<template>
  <div id="app">
    <TrainList @train-selected="trainSelected" />
    <TrainDetail :train="selectedTrain" />
  </div>
</template>

<script>
import TrainList from './components/TrainList.vue';
import TrainDetail from './components/TrainDetail.vue';

export default {
  name: 'App',
  components: {
    TrainList,
    TrainDetail
  },
  data() {
    return {
      selectedTrain: null
    };
  },
  methods: {
    trainSelected(train) {
      this.selectedTrain = train;
    }
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
