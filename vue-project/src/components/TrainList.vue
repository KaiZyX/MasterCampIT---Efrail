<!-- src/components/TrainList.vue -->
<template>
    <div class="train-list">
      <h1>Liste des Trains</h1>
      <ul>
        <li v-for="train in trains" :key="train.id">
          <a @click="selectTrain(train)">{{ train.name }}</a>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  export default {
    name: "TrainList",
    data() {
      return {
        trains: [
          { id: 1, name: "TGV" },
          { id: 2, name: "Eurostar" },
          { id: 3, name: "Thalys" }
        ],
      };
    },
    methods: {
      selectTrain(train) {
        this.$emit('train-selected', train);
      }
    }
  };
  </script>
  
  <style scoped>
  .train-list {
    padding: 20px;
  }
  .train-list ul {
    list-style-type: none;
    padding: 0;
  }
  .train-list li {
    margin: 10px 0;
  }
  .train-list a {
    cursor: pointer;
    color: #42b983;
    text-decoration: none;
  }
  .train-list a:hover {
    text-decoration: underline;
  }
  </style>
