<template>
    <div>
      <!-- Header Component -->
      <HeaderComponent />
  
      <!-- Login Page Content Component-->
      <v-col cols="12" class="top-panel mt-16">
        <BreadCrumbs :items="breadcrumbItem" />
  
        <div class="w-100 d-flex align-center justify-center top-panel-conent">
          <span>{{ topPanelValue }}</span>
        </div>
      </v-col>
  
      <v-col cols="12" class="d-flex align-center justify-center mt-5">
        <v-col cols="6">
          <p class="conetnt">Which path would you like to take ?</p>
          <v-row>
            <v-col
              cols="6"
              class="mt-5"
              @click="selectedService(1, 'AZURE')"
              :class="{ active: activeCard === 1 }"
            >
              <v-card
                variant="outlined"
                class="d-flex align-center justify-center card"
                height="200px"
              >
                <img width="200" src="/src/assets/images/azure.jpeg" />
              </v-card>
            </v-col>
           
          </v-row>
        </v-col>
      </v-col>
  
      <FooterComponent />
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useStore } from 'vuex'
  import HeaderComponent from '../components/common/Header.vue'
  import FooterComponent from '../components/common/Footer.vue'
  import BreadCrumbs from '../components/common/BreadCrumbs.vue'
  import * as apis from '../utils/_api'
  
  const router = useRouter();
  const store = useStore();
  
  
  
  let topPanelValue = ref<string>('Choose Your Cloud Platform')
  let breadcrumbItem = ref([
    {
      title: 'Choose Platform',
      disabled: false
    },
  ])
  
  const activeCard = ref(0)
  const selectedService = async (cardNumber: number, serviceName: string) => {
    activeCard.value = activeCard.value === cardNumber ? 0 : cardNumber
   
    const response = await apis.serviceList(serviceName)
    const status = response.status
    if (status === 200) {
      const payload = response.data
      localStorage.setItem('Service', serviceName)
      router.push('/Dashboard')
      store.commit('setServiceList', payload);
    } else {
      console.log('Errrrrorrrrrrrrr')
    }
  }
  
  
  </script>
  
  <style scoped>
  .top-panel {
    background: var(--blue-blue-95, #e6f5ff);
    width: 100%;
    height: 160px;
    flex-shrink: 0;
    position: relative;
  }
  
  .breadcrumbs {
    color: var(--wb-grey-20, #333);
    font-family: MB Corpo S Text WEB;
    font-size: 12px;
    font-style: normal;
    font-weight: 400;
    line-height: 16px;
    letter-spacing: 0.2px;
  }
  
  .top-panel-conent {
    color: #000;
    text-align: center;
    font-family: MB Corpo A Text Cond WEB;
    font-size: 40px;
    font-style: normal;
    font-weight: 400;
    line-height: 48px;
    position: absolute;
    top: 0;
    bottom: 0;
  }
  
  .conetnt {
    color: var(--grey-grey-20, #333);
    font-family: MB Corpo S Text WEB;
    font-size: 24px;
    font-style: normal;
    font-weight: 400;
    line-height: 24px; /* 100% */
  }
  
  .card {
    transition: filter 0.5s ease;
  }
  
  .active {
    opacity: 0.5;
  }
  
  .card:not(.active) .card {
    opacity: unset;
  }
  
  .sign-card {
    border-radius: 12px;
    border: 1px solid var(--blue-blue-90, #cce8ff);
    box-shadow: 2px 5px 6px 0px rgba(0, 0, 0, 0.1);
  }
  
  .bottom-panel {
    border-radius: 4px;
    border: 1px solid var(--info-light, #3393de);
  }
  
  .bottom-panel p {
    color: var(--blue-blue-40, #036dc1);
    font-family: MB Corpo S Text WEB;
    font-size: 14px;
    font-style: normal;
    font-weight: 400;
    line-height: 20px;
  }
  
  .bottom-panel span {
    color: var(--blue-blue-50, #008dfc);
    font-family: MB Corpo S Text WEB;
    font-size: 14px;
    font-style: normal;
    font-weight: 700;
    line-height: 20px;
    text-decoration-line: underline;
  }
  
  
  
  </style>