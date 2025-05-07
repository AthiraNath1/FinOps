<template>
    <v-col cols="12" class="top-panel">
      <BreadCrumbs :items="items" />
      <div class="w-100 top-panel-conent mb-2">
        <v-row>
        <v-col cols="11" class="d-flex align-center justify-center">
          <span class="heading">{{ topPanelValue }}</span>
        </v-col >
        <v-col  cols="1">
  
          <img :src="azure" class="azure" v-if="service == 'AZURE'"/>
        </v-col >
        
      </v-row>
       
     
       
      </div>
    </v-col>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import BreadCrumbs from './Breadcrumbs.vue'
  import type { breadcrumbIteam } from '../../utils/customInterface'
  import azure from '../../assets/images/azure.jpeg'
  
  const props = defineProps({
    topPanelValue: String,
    items: Array<breadcrumbIteam>
  })
  
  const service = ref<string | null>('')
  
  
  onMounted(() => {
    const serviceName = localStorage.getItem('Service');
    service.value = serviceName
  })
  </script>
  
  <style scoped>
  .top-panel {
    background: var(--blue-blue-95, #e6f5ff);
    width: 100%;
    /* height: 160px; */
    flex-shrink: 0;
    position: relative;
  }
  .azure {
    width: 100%;
  }
  
  
  .heading {
    color: #000;
    text-align: center;
    font-family: MB Corpo A Text Cond WEB;
    font-size: 25px;
    font-style: normal;
    font-weight: 400;
    line-height: 48px;
    text-transform: capitalize;
  }
  </style>