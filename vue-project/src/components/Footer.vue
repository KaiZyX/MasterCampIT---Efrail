<template>
  <div class="base">  
    <footer>
      <div class="container">
        <div class="row">
          <div class="col-md-3 footer-column">
            <h4 class="title">A propos de nous</h4>
            <ul class="ulFooter">
              <li class="li-footer"><a class="linkFooter" href="#">Nous sommes passionnés de trains !</a></li>
            </ul>
          </div>
          <div class="col-md-3 footer-column">
            <h4 class="title">Notre location</h4>
            <ul class="ulFooter">
              <li class="li-footer"><a class="linkFooter" href="#">France, 4 rue Karl Marx</a></li>
            </ul>
          </div>
          <div class="col-md-3 footer-column">
            <h4 class="title">Contacter nous ;) !!</h4>
            <ul class="ulFooter">
              <li class="li-footer"><a class="linkFooter" href="#">Efrail@gmail.com</a></li>
            </ul>
          </div>
          <div class="col-md-3 footer-column">
            <h4 class="title">Follow us</h4>
            <div class="Social-networks">
              <a class="Social-icon" href="#"><font-awesome-icon :icon="['fab', 'facebook-f']" /></a>
              <a class="Social-icon" href="#"><font-awesome-icon :icon="['fab', 'instagram']" /></a>
              <a class="Social-icon" href="#"><font-awesome-icon :icon="['fab', 'snapchat']" /></a>
              <a class="Social-icon" href="#"><font-awesome-icon :icon="['fab', 'tiktok']" /></a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  </div>  
</template>

<script setup>
</script>

<style scoped>
  /* Reset des listes et styles de base */
  li {
    list-style: none;
    margin: 0;
    padding: 0;
  }

  footer {
    background-color: #333;
    padding: 25px 0;
    color: #fff;
    font-family: 'Poppins', sans-serif;
  }

  .container {
    width: 90%;
    margin: 0 auto;
  }

  .row {
    display: flex;
    flex-wrap: wrap;
    gap: 15px; /* Espacement entre les colonnes */
  }

  .footer-column {
    flex: 1;
    padding: 0 15px;
    display: flex;
    flex-direction: column;
    align-items: center; /* Centre les éléments horizontalement */
    text-align: center; /* Centre le texte */
  }

  .title {
    font-size: 14px;
    font-weight: bold;
    position: relative;
    margin-bottom: 15px;
  }

  .title::before {
    content: '';
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    bottom: -5px;
    width: 30px;
    height: 2px;
    background-color: #A7C7E7; /* Ligne sous le titre */
  }

  .ulFooter {
    margin-top: 10px;
    padding: 0; /* Remet à zéro le padding pour éviter des décalages */
  }

  .li-footer {
    font-size: 13px;
    margin-bottom: 5px;
  }

  .linkFooter {
    color: #fff;
    text-decoration: none;
    transition: color 0.3s;
  }

  .linkFooter:hover {
    color: #A7C7E7;
  }

  .Social-networks {
    display: flex;
    gap: 10px;
    justify-content: center; /* Centre les icônes */
    margin-top: 30px;
  }

  .Social-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #A7C7E7;
    color: #fff;
    font-size: 20px;
    transition: background-color 0.3s, color 0.3s;
    text-decoration: none;
  }

  .Social-icon:hover {
    background-color: #fff;
    color: #A7C7E7;
  }

  @media (max-width: 768px) {
    .footer-column {
      flex: 1 1 100%;
      margin-bottom: 20px;
      align-items: center;
    }
  }
</style>
