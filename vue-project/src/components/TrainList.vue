import bootstrap from 'bootstrap'

<template>
  <p> </p>
  <div class = "fond">
  <div class = "text">


  <strong>Efrail vous propose de nombreux avantages détaillé si dessous</strong> 

</div>
  <p></p>
  



<div id="carouselExampleCaptions" class="carousel slide">
  <div class="carousel-indicators">
    <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
    <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="1" aria-label="Slide 2"></button>
    <button type="button" data-bs-target="#carouselExampleCaptions" data-bs-slide-to="2" aria-label="Slide 3"></button>
  </div>
  <div class="carousel-inner">
    <div class="carousel-item active">
      <img src="@/assets/train1.png"  class="d-block w-100" alt="...">
      <div class="carousel-caption d-none d-md-block">
        <h5></h5>
        <p>Some representative placeholder content for the first slide.</p>
      </div>
    </div>
    <div class="carousel-item">
      <img src="@/assets/train1.png"  class="d-block w-100" alt="...">
      <div class="carousel-caption d-none d-md-block">
        <h5>Second slide label</h5>
        <p>Some representative placeholder content for the second slide.</p>
      </div>
    </div>
    <div class="carousel-item">
      <img src="@/assets/train1.png"  class="d-block w-100" alt="...">
      <div class="carousel-caption d-none d-md-block">
        <h5>Third slide label</h5>
        <p>Some representative placeholder content for the third slide.</p>
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
  <p>
  </p>
  <div class="home">
    <h1>Welcome to the Home Page</h1>
    <button @click="navigateToMap">Go to Map</button>
  </div>
  
</div>  
</div>



</template>

<style>
.text{
  font-size: 25px;
}
.carousel-control-prev{
  background-color: #A7C7E7;
  
}

.carousel-control-prev-icon{
  background-color:  #A7C7E7;
}
.carousel-control-next-icon{
  background-color:  #A7C7E7;

}
.carousel-control-next{
  background-color:#A7C7E7;
}
.carousel-inner {
    max-width: 500px; /* Ajustez la largeur selon vos besoins */
    margin: 0 auto; /* Centre le carrousel horizontalement */
}

.ok{
  margin-top: 100px;
  background-color: white;
  font-size: 25px;
}

.fond{
  background-color: white;
}
</style>

<script>

export default {
  name: 'TrainList',
  methods: {
    navigateToMap() {
      this.$router.push({ name: 'Map' });
    }
  }
}
</script>