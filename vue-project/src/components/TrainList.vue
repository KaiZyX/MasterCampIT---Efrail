import bootstrap from 'bootstrap'

<template>

  <div class="Global">
  <p> </p>
  <div class = "fond">
  <div class = "text  ">


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
      <img src="@/assets/train1.avif"  class="img1" alt="...">
      <div class="carousel-caption d-none d-md-block">
        <h5 class ="h55">Réduction du temps de trajet</h5>
        <p></p>
      </div>
    </div>
    <div class="carousel-item">
      <img src="@/assets/train3.jpg"  class="img3" alt="...">
      <div class="carousel-caption d-none d-md-block">
        
        <h5 class ="h55">Diminution de CO2</h5>
        <p></p>
      </div>
    </div>
    <div class="carousel-item">
      <img src="@/assets/train2.jpg"  class="img2" alt="...">
      <div class="carousel-caption d-none d-md-block">
        <h5 >	Amélioration de l'expérience utilisateur</h5>
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
  <p>
  </p>
 
   
   

  
</div>  
  <div class = "redirection_map">
    <a  class = "Bouton" href="/map">Découvrir</a>
  </div>

</div>
<p></p>
</div>



</template>

<style>

.Bouton{

  
}

.img1{
  width: 500px;  
  height: 400px
}

.img3{
  width: 500px;  
  height: 400px

}
.h55{ 
  color: black;
}

.img2{
  width: 1000px;  
  height: 400px
  
}
.coll1{
  background-color:  #A7C7E7;

}

.redirection_map{
  align-items: center;
  justify-content: center;
  display: flex;
}

.Global{

  display: flex ;
  flex-direction: column;
  align-items: center ;
  justify-content: center;
} 
.Bouton{

  text-align: center;
  background-color:  #A7C7E7;
  color: black;
  
  padding: 6px 12px;
  border-radius: 5px;

}

.text{
  font-size: 18px;
  text-align: center;
 
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


</script>