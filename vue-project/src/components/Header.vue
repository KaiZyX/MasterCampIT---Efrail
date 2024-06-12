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
  background-color: white;
  height: 110px;
  width: 100%;
  display: flex;
  align-items: center;
  padding: 0 200px;
  box-sizing: border-box;
  font-family: 'Arial', sans-serif; /* Changer la police d'écriture */
  font-size: 30px;

}
  
  header nav ul {
    display: flex;
    list-style-type: none;
    padding: 0;
    margin: 0; /* Enlevez la marge par défaut pour les listes */
    gap: 40px
    
  }
  
  header nav ul li {
    display: inline;
    margin-right: 10px;
    position : center;
  }
  
  header nav ul li a {
    color: black;
    text-decoration: none;
  }

  li :hover{
    color: rgb(0, 233, 78);
  }
  
  
  header nav ul li a:hover {
    text-decoration: underline;
  }
  </style>
  