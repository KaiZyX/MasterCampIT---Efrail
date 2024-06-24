<template>
    <br>
    <strong><div class='oui'>Les émissions de CO2 dues au transport de personnes en Europe : </div></strong>
    <br>
    <div>
      <canvas id="co2Chart" width="600" height="110"></canvas>
    </div>
    <br>
    <br>
    <p class = 'oui'> Les transports en commun comme le métro sont rentables pour l'environnement principalement en raison de leur efficacité énergétique, de leur capacité élevée à transporter des passagers, de leur réduction des émissions de gaz à effet de serre, de leur utilisation optimisée de l'espace urbain et de leur impact réduit sur la pollution sonore. Ces systèmes jouent un rôle essentiel dans la promotion de villes durables en réduisant la dépendance à la voiture individuelle et en améliorant la qualité de vie urbaine pour tous.</p>
    <br>

    <br>
    <div class="container">
    <img src="@/assets/env.jpg" class="imge" height="400px" width="500">
    </div>
    <br>
    <br>
  
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
  .container{
    display: flex;
    justify-content: center; /* Centre horizontalement */
    align-items: center; /* Centre verticalement */
    
  }

  .oui{
    align-items: center;
    justify-content: center;
    display: flex;
    font-size: 18px;
  }
  /* Ajoutez des styles ici si nécessaire */
  </style>
  