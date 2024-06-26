<template>
  <div class="Global">
    <p> </p>
    <div class="fond">
      <div class="search-form-container">
        <div class="search-form-header">
          On va où ?
        </div>
        <div class="search-form">
          <input type="text" v-model="from" placeholder="Start" />
          <input type="text" v-model="to" placeholder="End" />
          <div class="redirection_map">
            <a  class = "Bouton" href="/map">Go</a>
          </div>
        </div>
      </div>
      <div class="text">
        <strong>Efrail vous offre une multitude d'avantages, soigneusement détaillés ci-dessous.</strong>
        <br>
        <br>
      </div>
      <table class="table">
        <thead>
          <tr>
            <th class="coll1" scope="col">Réduction du temps de trajet</th>
            <th scope="col">Diminution des émissions de CO2</th>
            <th classe="coll1" scope="col">Amélioration de l'expérience utilisateur</th>
          </tr>
        </thead>
        <tbody class="table-group-divider">
          <tr>
            <td>Permet de réduire considérablement le temps de trajet en proposant les itinéraires les plus rapides et les moins encombrés.</td>
            <td>Contribue à la diminution des émissions de CO2 en incitant les utilisateurs à privilégier les transports en commun plutôt que les véhicules individuels.</td>
            <td>Améliore l'expérience utilisateur en fournissant des itinéraires clairs, rapides et personnalisés, rendant les déplacements plus simples et agréables.</td>
          </tr>
        </tbody>
      </table>
      <p></p>
      <br>
      <div id="carouselExampleCaptions" class="carousel slide">
        <div class="carousel-indicators">
          <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
          <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="1" aria-label="Slide 2"></button>
          <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="2" aria-label="Slide 3"></button>
        </div>
        <div class="carousel-inner">
          <div class="carousel-item active">
            <img src="@/assets/train1.avif" class="img1" alt="...">
            <div class="carousel-caption d-none d-md-block">
              <p></p>
            </div>
          </div>
          <div class="carousel-item">
            <img src="@/assets/train3.jpg" class="img3" alt="...">
            <div class="carousel-caption d-none d-md-block">
              <p></p>
            </div>
          </div>
          <div class="carousel-item">
            <img src="@/assets/train2.jpg" class="img2" alt="...">
            <div class="carousel-caption d-none d-md-block">
              <p></p>
            </div>
          </div>
        </div>
        <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide="prev">
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide="next">
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Next</span>
        </button>
        <p></p>
      </div>
      
    </div>
    <p></p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      from: '',
      to: ''
    };
  },
  methods: {
    go() {
      this.$router.push({ name: 'Results', params: { from: this.from, to: this.to } });
    }
  }
};
</script>

<style>
.search-form-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: auto;
  padding: 20px;
  background-color: #A7C7E7;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 350px; /* Limitez la largeur du conteneur */
  margin: 20px auto; /* Centre le conteneur horizontalement */
}

.search-form-header {
  background-color: #34568B; /* Bleu plus foncé */
  color: white;
  padding: 10px;
  width: 100%;
  text-align: center;
  border-radius: 10px 10px 0 0;
}

.search-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #A7C7E7;
  padding: 20px;
  border-radius: 0 0 10px 10px;
}

.search-form input {
  margin: 5px;
  padding: 10px;
  width: 300px;
}

.redirection_map {
  margin: 10px;
}

.Bouton {
  padding: 10px 20px;
  background-color: #ff7f50;
  color: white;
  text-decoration: none;
  border-radius: 5px;
  cursor: pointer;
}

.Bouton:hover {
  background-color: #ff6347;
}

.img1 {
  width: 500px;
  height: 400px;
}

.img3 {
  width: 500px;
  height: 400px;
}

.h55 {
  color: black;
}

.img2 {
  width: 1000px;
  height: 400px;
}

.coll1 {
  background-color: #A7C7E7;
}

.redirection_map {
  align-items: center;
  justify-content: center;
  display: flex;
}

.Global {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.Bouton {
  text-align: center;
  background-color: #f5f5f5;
  color: black;
  padding: 6px 12px;
  border-radius: 5px;
}

.text {
  font-size: 18px;
  text-align: center;
}

.carousel-control-prev {
  background-color: #A7C7E7;
}

.carousel-control-prev-icon {
  background-color: #A7C7E7;
}

.carousel-control-next-icon {
  background-color: #A7C7E7;
}

.carousel-control-next {
  background-color: #A7C7E7;
}

.carousel-inner {
  max-width: 500px;
  margin: 0 auto;
}

.ok {
  margin-top: 100px;
  background-color: white;
  font-size: 25px;
}

.fond {
  background-color: white;
}
</style>
