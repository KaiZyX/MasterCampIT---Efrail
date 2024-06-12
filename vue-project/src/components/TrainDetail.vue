<!-- src/components/TrainDetail.vue -->
<template>
    <div class="train-detail" v-if="train">
      <h2>Détails du Train : {{ train.name }}</h2>
      <p>ID du Train : {{ train.id }}</p>
    </div>
  </template>
  
  <script>
  export default {
    name: "TrainDetail",
    props: {
      train: Object
    }
  };
  </script>
  
  <style scoped>
  .train-detail {
    padding: 20px;
  }
  </style>
  