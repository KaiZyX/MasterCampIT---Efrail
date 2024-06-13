<template>
  <header>
      <nav>
          <div class="logo">
              <img src="@/assets/logo.png" height="90px" alt="Logo" />
              
          </div>
          <ul>
              <div class = "nom">EFREISH</div>
              <li><a href="#">Accueil</a></li>
              <li><a href="#">À propos</a></li>
              <li><a href="#">Contact</a></li>
            
              <li><a href="#">Découvrir</a></li>
          </ul>
      </nav>
  </header>
</template>

<script>
export default {
  // Votre script ici
}
</script>

<style scoped>
/* Vos styles CSS ici */
header {
  background-color: #333; 
  padding: 20px 0;
  font-size: 20px; 
}

.logo img {
  height: 70px;
  padding-left: 10px; 
}

nav {
  display: flex;
  justify-content: space-between; /* Aligner le logo à gauche et les liens à droite */
  align-items: center;
}

nav ul {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
}

nav ul li {
  margin-right: 20px;
}

nav ul li:last-child {
  margin-right: 0; /* Supprimer la marge du dernier élément */
}

nav ul li a {
  color: white;
  text-decoration: none;
  transition: color 0.3s; /* Ajouter une transition pour les liens */
}




nav ul li a:hover {
  color: red; /* Changer la couleur au survol */
}

nav ul li:last-child a {
  background-color: #4CAF50;
  padding: 10px 20px;
  border-radius: 5px;
}

nav ul li:last-child a:hover {
  background-color: #f2f3f4;
}

.nom{

  color: white;
  text-decoration: none;
  margin-right: 650px;
          
  
}

.nom:hover {
  color: red; /* Changer la couleur au survol */
}
         
  


</style>
