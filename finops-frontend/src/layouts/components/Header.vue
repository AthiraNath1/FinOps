<template>
    <v-app-bar color="#014880" class="header" height="65" flat app>
      <div class="nav-header d-flex" @click="returnHome()">
        <img src="../../assets/images/logo.jpeg" class="logo d-flex" />
        <span class="brand-name"> FinX </span>
        <!-- <v-icon icon="md:home"></v-icon> -->
      </div>
      <v-spacer></v-spacer>
      <div class="nav-header d-flex">
        <User />
      </div>
    </v-app-bar>
  </template>
  
  <script lang="ts" setup>
    import { defineComponent } from 'vue'
    import { useRouter } from 'vue-router'
    import User from './UserProfile.vue'
  
    const router = useRouter()
    const returnHome = () => {
      router.push('/Dashboard')
    }
  
  </script>
  
  <style scoped>
  .header {
    position: fixed !important;
    top: 0 !important;
    right: 0 !important;
    z-index: 9999 !important;
  }
  
  .nav-header {
    overflow: hidden;
    padding: 1rem 2.2rem;
    margin-inline: 0;
    align-items: center;
    cursor: pointer;
  }
  
  .logo {
    width: 2.5rem;
    height: 2.5rem;
    justify-content: center;
    align-items: center;
    flex-shrink: 0;
  }
  
  .brand-name {
    color: #fff;
    font-family: MB Corpo A Title Cond WEB;
    font-size: 1.2rem;
    font-style: normal;
    font-weight: 400;
    line-height: 1.40625rem;
    margin-left: 0.30919rem;
  }
  </style>