<template>
    <div class="d-flex align-center justify-center bg-color fullscreen">
      <!-- Login Page Content Component-->
      <v-col cols="12" md="8" sm="12">
        <v-card>
          <v-row>
            <v-col cols="6" class="left-panel">
              <img
                class="mx-auto"
                height="200"
                max-width="500"
                src="/src/assets/images/handshake.jpeg"
              />
              <v-container class="d-flex align-center justify-center">
                <v-col cols="9">
                  <v-card-title class="text-h5 left-panel-heading"> Why Us... </v-card-title>
                  <v-col
                    cols="12"
                    class="d-flex align-center justify-start"
                    v-for="(item, index) in list"
                    :key="index"
                  >
                    <img class="api-icons" src="/src/assets/images/Api.jpeg" />
                    <v-card-subtitle class="left-panel-conetent">{{ item.content }}</v-card-subtitle>
                  </v-col>
                </v-col>
              </v-container>
            </v-col>
  
            <v-col cols="6" class="d-flex align-center justify-center">
              <LoginForm />
            </v-col>
          </v-row>
        </v-card>
      </v-col>
  
      <!-- Footer Component -->
      <FooterComponent />
    </div>
  </template>
  
  <script setup lang="ts">
  // import FooterComponent from '@/components/common/Footer.vue'
  import LoginForm from '../components/common/Forms/LoginForm.vue'
  import { ref } from 'vue'
  
  const list = ref([
    {
      content: 'Get transparency on your Cloud accounts'
    },
    {
      content: 'Expert cloud FinOps consulting'
    },
    {
      content: 'Derive Cost reduction on cloud spend'
    },
    {
      content: 'Technical and Executive Dashboards'
    },
    {
      content: 'Budget and Forecast your Cloud investments'
    }
  ])
  </script>
  
  <style scoped>
  .bg-color {
    background: linear-gradient(180deg, #1681d6 0%, #a3d5fd 100%);
    box-shadow: 0px 4px 4px 0px rgba(0, 0, 0, 0.25);
    height: 100vh;
  }
  
  .left-panel {
    background: var(--blue-blue-95, #e6f5ff);
    box-shadow: 0px 4px 4px 0px rgba(0, 0, 0, 0.25);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }
  
  .handshake {
    width: 343px;
    height: 190px;
    flex-shrink: 0;
  }
  
  .api-icons {
    height: 25px;
    max-width: 25px;
  }
  
  .left-panel-heading {
    color: #000;
    font-family: MB Corpo S Title WEB;
    font-size: 26px;
    font-style: normal;
    font-weight: 400;
    line-height: 32px;
  }
  
  .left-panel-conetent {
    color: var(--grey-grey-20, #333);
    opacity: unset !important;
    font-family: MB Corpo S Text WEB;
    font-size: 14px;
    font-style: normal;
    font-weight: 400;
    line-height: 20px;
  }
  </style>