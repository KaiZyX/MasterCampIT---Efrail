<template>
    <div>
      <Header/>
      <router-view/>
      <div v-if="isHomePage">
      <TrainList/>

    </div>

      <Footer/>
    </div>
  </template>


<script setup>

import Header from "@/components/Header.vue";
import Footer from "@/components/Footer.vue";
import { computed } from "vue";
import { useRouter } from "vue-router";
import TrainList from "./TrainList.vue";


const router = useRouter();
const isHomePage = computed(() => router.currentRoute.value.path === "/");
</script>
