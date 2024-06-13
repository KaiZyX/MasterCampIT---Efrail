<template>
    <footer>
      <div class="container">
        <div class="row">
          <div class="footer-column">
            <h4 class="title">About us</h4>
            <ul class="ulFooter">
              <li class="li-footer"><a class="linkFooter" href="#">Nous sommes passionée de train !</a></li>
            </ul>
          </div>
          <div class="footer-column localisation">
            <h4 class="title">Our Localisation</h4>
            <ul class="ulFooter">
              <li class="li-footer"><a class="linkFooter" href="#">France, 4 rue Karl Marx</a></li>
            </ul>
          </div>
          <div class="footer-column">
            <h4 class="title">Contact us</h4>
            <ul class="ulFooter">
              <li class="li-footer"><a class="linkFooter" href="#">Efrail@gmail.com</a></li>
            </ul>
          </div>
          <div class="footer-column">
            <h4 class="title">Follow us</h4>
            <div class="Social-networks">
              <a class="Social-icon" href="#"><i class="fab fa-facebook-f"></i></a>
              <a class="Social-icon" href="#"><i class="fab fa-instagram"></i></a>
              <a class="Social-icon" href="#"><i class="fab fa-snapchat"></i></a>
              <a class="Social-icon" href="#"><i class="fab fa-tiktok"></i></a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  </template>
  
  <script setup>
  </script>
  
  <style scoped>
  li {
    list-style: none;
  }
  
  footer {
    background-color: #333;
    padding-top: 3%;
  }
  
  .container {
    max-width: 100%;
  }
  
  .row {
    display: flex;
  }
  
  .footer-column {
    width: 25%;
    padding: 0 5%;
  }
  
  .title {
    width: 100%;
    font-size: 12px;
    color: #F5F7F8;
    text-transform: capitalize;
    margin-bottom: 15%;
    font-weight: 500;
    position: relative;
  }
  
  .footer-column h4::before {
    content: '';
    position: absolute;
    left: 0;
    bottom: -10px;
    background-color: red;
    height: 2px;
    width: 40px;
    box-sizing: border-box;
  }
  
  body {
    line-height: 1.2;
    font-family: 'Poppins', sans-serif;
    font-size: 12px;
  }
  
  .li-footer {
    width: 100%;
    font-size: 12px;
    margin-top: 5px;
    margin-left: -3px;
  }
  
  .ulFooter {
    width: 100%;
  }
  
  .Social-networks {
    width: 100%;
  }
  
  .Social-icon {
    display: inline-block;
    border-radius: 50%;
    background-color: red;
    height: 24px;
    width: 24px;
    margin-right: 8px;
    margin-top: 5px;
    color: #F5F7F8;
    text-align: center;
    line-height: 22px;
  }
  
  .fab {
    font-size: 12px;
  }
  
  .Social-icon:hover {
    color: #333;
  }
  
  .linkFooter {
    text-decoration: none;
    color: grey;
    transition: all 0.4s ease;
  }
  
  .linkFooter:hover {
    padding-left: 10px;
    color: red;
  }
  
  @media (min-width: 768px) {
    .row {
      display: flex;
      flex-wrap: wrap;
    }
  
    .li-footer {
      font-size: 19px;
    }
  
    .title {
      width: 100%;
      font-size: 20px;
      color: #F5F7F8;
      text-transform: capitalize;
      margin-bottom: 15%;
      font-weight: 500;
      position: relative;
    }
  
    .Social-networks {
      width: 100%;
    }
  
    .Social-icon {
      display: inline-block;
      border-radius: 50%;
      background-color: red;
      height: 40px;
      width: 40px;
      margin-right: 8px;
      margin-top: -6px;
      margin-bottom: 10px;
      color: white;
      text-align: center;
      line-height: 45px;
    }
  
    .fab {
      font-size: 20px;
    }
  
    .footer-column h4::before {
      content: '';
      position: absolute;
      left: 0;
      bottom: -10px;
      background-color: red;
      width: 60px;
      box-sizing: border-box;
    }
  }
  </style>
  