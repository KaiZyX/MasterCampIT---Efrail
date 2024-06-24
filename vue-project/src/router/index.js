// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import TrainList from '@/components/TrainList.vue';
import Map from '@/components/Map.vue';
import Afflu from '@/components/Afflu.vue' ;
import Default from '@/components/Default.vue';
import Env from '@/components/Env.vue';
import Cons from '@/components/Cons.vue'
import { compile } from 'vue';

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
  },
  {
    path : '/Afflu',
    name:'Afflu',
    component : Afflu
  },

  {
  path : '/Env',
  name : 'Env',
  component: Env
  },
  {
  path : '/Cons',
  name : 'Cons',
  component : Cons},
  ]

  }
 
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
