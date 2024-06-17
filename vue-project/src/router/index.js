// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import TrainList from '@/components/TrainList.vue';
import Map from '@/components/Map.vue';

const routes = [
  {
    path: '/',
    name: 'TrainList',
    component: TrainList
  },
  {
    path: '/map',
    name: 'Map',
    component: Map
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

export default router;
