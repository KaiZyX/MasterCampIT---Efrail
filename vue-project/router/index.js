// src/router/index.js
import Vue from 'vue';
import Router from 'vue-router';
import TrainList from '@/components/TrainList.vue';
import Navig from '@/components/Navig.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'TrainList',
      component: TrainList
    },
    {
      path: '/navig',
      name: 'Navig',
      component: Navig
    }
  ]
});
