// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import TrainList from '@/components/TrainList.vue';
import Map from '@/components/Map.vue';
import Default from '@/components/Default.vue'

const routes = [
  {path: '',
  name : 'Main',
  component: Default,

  children : [

    { path: "/", redirect: "" },
    { path: '/:pathMatch(.*)*', },

     {
    path: '/Accueil',
    name: 'TrainList',
    component: TrainList
  },
  {
    path: '/map',
    name: 'Map',
    component: Map
  }
  ]

  }
 
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
