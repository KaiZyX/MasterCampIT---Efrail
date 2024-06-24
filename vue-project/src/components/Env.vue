<template>
    <br>
    <strong><div class='oui'>Les émissions de CO2 dues au transport de personnes en Europe : </div></strong>
    <br>
    <div>
      <canvas id="co2Chart" width="600" height="110"></canvas>
    </div>
  </template>
  
  <script>
  import { Chart, registerables } from 'chart.js';
  
  Chart.register(...registerables);
  
  export default {
    name: 'CO2Chart',
    mounted() {
      this.renderChart();
    },
    methods: {
      renderChart() {
        var ctx = document.getElementById('co2Chart').getContext('2d');
        new Chart(ctx, {
          type: 'bar',
          data: {
            labels: ['Avion', 'Voiture', 'Bus' , 'Train', 'Vélo', 'Marche'],
            datasets: [{
              label: 'Gramme de CO2 emis par personne et par kilomètre parcouru',
              

              data: [285, 158, 68, 14, 0, 0],
              backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 206, 86, 0.2)'
              ],
              borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(255, 206, 86, 1)'
              ],
              borderWidth: 1
            }]
          },
          options: {
            scales: {
              y: {
                beginAtZero: true
              }
            },
            plugins: {
              legend: {
                display: true,
                position: 'top'
              },
              tooltip: {
                enabled: true
              }
            }
          }
        });
      }
    }
  }
  </script>
  
  <style scoped>

  .oui{
    align-items: center;
    justify-content: center;
    display: flex;
    font-size: 18px;
  }
  /* Ajoutez des styles ici si nécessaire */
  </style>
  