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
                      <li class="nav-item"><a class="nav-link" href="/">À propos</a></li>
                      <li class="nav-item"><a class="nav-link" href="/">Contact</a></li>
                      <li class="nav-item"><a class="nav-link btn btn-light" href="/map">Découvrir</a></li>
                  </ul>
              </div>
          </div>
      </nav>
  </header>
</template>

<style scoped>

.container{
  background-color: #A7C7E7;

}



.navbar-brand {
  display: flex;
  align-items: center;

}

.navbar-brand img {
  margin-right: 30px;
}

.nav-link {
  color: black;
  transition: color 0.3s;
}

.nav-link:hover {
  color: white;
}
  

.btn-light {
  background-color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 20px;
}

.btn-light:hover {
  background-color: white;
  color: black;
}
</style>
