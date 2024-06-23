<template>
    <br>
    <strong><div class='oui'>Heures d'affluence du lundi au vendredi :</div></strong>
    <br>
    <div class="afflu-container">
      <canvas ref="affluenceChart1"></canvas>
    </div>
    <br>
    <strong><div class='oui'>Heures d'affluence du samedi au dimanche :</div></strong>
    <br>
    <div class="afflu-container">
      <canvas ref="affluenceChart2"></canvas>
    </div>
    <br>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import { Chart, registerables } from 'chart.js';
  
  // Enregistrez tous les composants nécessaires de Chart.js
  Chart.register(...registerables);
  
  export default {
    name: 'Afflu',
    setup() {
      const chart1 = ref(null);
      const chart2 = ref(null);
      const affluenceChart1 = ref(null);
      const affluenceChart2 = ref(null);
  
      onMounted(() => {
        const ctx1 = affluenceChart1.value.getContext('2d');
        chart1.value = new Chart(ctx1, {
          type: 'line',
          data: {
            labels: ['6h','7h','8h', '9h', '10h', '11h', '12h', '13h', '14h', '15h', '16h', '17h', '18h', '19h', '20h'],
            datasets: [{
              label: 'Heures d\'affluence du lundi au vendredi',
              data: [20, 50, 90, 80, 60, 45, 50, 50, 50, 60, 80, 100, 100, 80, 30], // Données fictives d'affluence
              borderColor: 'rgba(75, 192, 192, 1)',
              backgroundColor: 'rgba(75, 192, 192, 0.2)',
              fill: true,
              tension: 0.4
            }]
          },
          options: {
            scales: {
              x: {
                title: {
                  display: true,
                  text: 'Heures de la journée'
                }
              },
              y: {
                title: {
                  display: true,
                  text: 'Affluence'
                },
                beginAtZero: true
              }
            },
            responsive: true,
            plugins: {
              legend: {
                display: true,
                position: 'top'
              }
            }
          }
        });
        
        const ctx2 = affluenceChart2.value.getContext('2d');
        chart2.value = new Chart(ctx2, {
          type: 'line',
          data: {
            labels: ['6h', '7h', '8h', '9h', '10h', '11h', '12h', '13h', '14h', '15h', '16h', '17h', '18h', '19h', '20h','21'],
            datasets: [{
              label: 'Heures d\'affluence du samedi au dimanche',
              data: [10, 20, 30, 40, 50, 70, 90, 95, 95, 100, 100, 100, 90, 80, 60,40], // Données fictives d'affluence
              borderColor: 'rgba(153, 102, 255, 1)',
              backgroundColor: 'rgba(153, 102, 255, 0.2)',
              fill: true,
              tension: 0.4
            }]
          },
          options: {
            scales: {
              x: {
                title: {
                  display: true,
                  text: 'Heures de la journée'
                }
              },
              y: {
                title: {
                  display: true,
                  text: 'Affluence'
                },
                beginAtZero: true
              }
            },
            responsive: true,
            plugins: {
              legend: {
                display: true,
                position: 'top'
              }
            }
          }
        });
      });
  
      return {
        chart1,
        chart2,
        affluenceChart1,
        affluenceChart2
      };
    }
  }
  </script>
  
  <style>
  .oui {
    align-items: center;
    justify-content: center;
    display: flex;
    font-size: 18px;
  }
  .afflu-container {
    width: 100%;
    max-width: 800px;
    margin: 0 auto;
  }
  </style>
  