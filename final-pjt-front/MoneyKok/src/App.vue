<template>
  <header>
    <HeaderNav/>
  </header>
  
  

  <main>
    <RouterView/>
  </main>



  <footer>
    <FooterNav/>
  </footer>
</template>

<script setup>
import '@/assets/main.css';
import { RouterLink, RouterView } from 'vue-router';
import HeaderNav from './components/common/HeaderNav.vue';
import FooterNav from './components/common/FooterNav.vue';
import HomeView from './views/HomeView.vue';



</script>


<style scoped>
@import 'bootstrap-icons/font/bootstrap-icons.css';
</style>
