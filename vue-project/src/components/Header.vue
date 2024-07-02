
<template>
  <header>
      <nav class="navbar navbar-expand-lg navbar-light bg-light">
          <div class="container">
              <a class="navbar-brand" href="#">
                  <img src="@/assets/logo.png" height="50" alt="Logo" />
                  EFRAIL
              </a>
              <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                  <span class="navbar-toggler-icon"></span>
              </button>
              <div class="collapse navbar-collapse" id="navbarNav">
                  <ul class="navbar-nav ml-auto">
                      <li class="nav-item"><a class="nav-link" href="/">Accueil</a></li>
                      <li class="nav-item"><a class="nav-link" href="/Afflu">Heures d'affluences</a></li>
                      <li class="nav-item"><a class="nav-link" href="/Env">Environnement</a></li>
                      <li class="nav-item"><a class="nav-link" href="/Cons">Conseil</a></li>
                      <li class="nav-item"><a class="nav-link" href="/Map">Version 1</a></li>
                      <li class="nav-item"><a class="nav-link" href="/Stat">Les lignes de métros</a></li>
                      <li class="nav-item"><a class="nav-link" href="/Station">Les stations de Paris</a></li>
                      
                      
                  </ul>
              </div>
          </div>
      </nav>
  </header>
</template>

<style scoped>
.container {
  background-color: #f8f9fa; /* Couleur de fond plus douce */
  box-shadow: 0 2px 4px rgba(0,0,0,0.1); /* Ajoute une ombre pour donner de la profondeur */
}

.navbar {
  padding: 0.5rem 1rem; /* Réduit le padding pour un look plus épuré */
}

.navbar-nav {
  display: flex; /* Assure que les éléments sont traités comme des flex items */
  justify-content: space-evenly; /* Espacement équitable entre les éléments */
  width: 100%; /* S'assure que le .navbar-nav utilise toute la largeur disponible */
}
.navbar-brand {
  display: flex;
  align-items: center;
  color: #00b3ff; /* Couleur du texte du logo pour le rendre plus distinct */
  font-family: "Audiowide", sans-serif;
  font-size: x-large;
  font-style: normal;
}

.navbar-brand img {
  margin-right: 15px; /* Ajuste l'espacement autour du logo */
}

.nav-link {
  color: #555; /* Couleur plus douce pour les liens */
  transition: color 0.3s;
  font-weight: 500; /* Rend le texte un peu plus épais */
  border: 2px solid #7cbbff; /* Ajoute une bordure */
  border-radius: 5px; /* Arrondit les coins */
  padding: 5px 10px; /* Ajoute un peu d'espace à l'intérieur */
  margin: 0 5px; /* Ajoute un peu d'espace entre les boutons */
}

.nav-link:hover, .nav-link:focus {
  color: #ffffff; /* Change la couleur du texte au survol */
  background-color: #97caff; /* Change la couleur de fond au survol */
  border-color: #5981ad; /* Assombrit la bordure au survol */
}

.btn-light {
  background-color: #007bff; /* Couleur de fond du bouton */
  color: white; /* Couleur du texte du bouton */
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
  transition: background-color 0.3s, color 0.3s; /* Transition douce pour le survol */
}

.btn-light:hover {
  background-color: #0056b3; /* Couleur de fond du bouton au survol */
  color: #ffffff; /* Couleur du texte du bouton au survol */
}
</style>