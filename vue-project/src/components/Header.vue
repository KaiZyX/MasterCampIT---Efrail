<template>
    <header>
      <nav>
        <div class="logo">
          <img src="@/assets/logo.png" height="90px" alt="Logo"  />
        </div>
        <ul>
          <li><a href="#">Accueil</a></li>
          <li><a href="#">À propos</a></li>
          <li><a href="#">Contact</a></li>
        </ul>
      </nav>
    </header>
  </template>
  
  <script>
 
  </script>
  

  <style scoped>

  .logo{
    position: absolute;
    left : 40px;
    top: 10px
  }
  header {
    background-color: green;
    color: white;
    height: 110px;
    width: 100%;
    
  }

  
  header nav ul {
    list-style-type: none;
    padding: 0;
    margin: 0; /* Enlevez la marge par défaut pour les listes */
  }
  
  header nav ul li {
    display: inline;
    margin-right: 10px;
    position : center;
  }
  
  header nav ul li a {
    color: white;
    text-decoration: none;
  }
  
  header nav ul li a:hover {
    text-decoration: underline;
  }
  </style>
  