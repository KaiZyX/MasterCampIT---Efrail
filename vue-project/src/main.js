// src/main.js
import { createApp } from 'vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { library } from '@fortawesome/fontawesome-svg-core';
import { faFacebookF, faInstagram, faSnapchat, faTiktok } from '@fortawesome/free-brands-svg-icons';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap';

import router from './router';  // Assurez-vous que le chemin est correct
import App from './App.vue';

// Ajouter les icônes que vous souhaitez utiliser à la bibliothèque
library.add(faFacebookF, faInstagram, faSnapchat, faTiktok);

const app = createApp(App);

app.use(router);

// Déclarer FontAwesomeIcon pour pouvoir l'utiliser dans vos composants
app.component('font-awesome-icon', FontAwesomeIcon);

app.mount('#app');
