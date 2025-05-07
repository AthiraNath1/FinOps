<template>
    <div>
      <LoaderComponent :isLoading="isLoading" />
  
      <TopPanel :topPanelValue="topPanelValue" :items="breadcrumbItem" />
      <v-col col="12">
        <p class="heading mb-2">Choice of Integration</p>
        <p>Please select your Integration option to view resources:</p>
      </v-col>
  
      <v-col cols="8" class="d-flex justify-center">
        <v-row>
          <v-col cols="6">
            <SelectComponent :items="serviceLisItems" :labelName="selectedItem" @itemSelected="onSelectedServiceListn" />
          </v-col>
        </v-row>
      </v-col>
  
      <v-col col="12" v-if="isServiceListSelected">
        <p class="heading">Services</p>
      </v-col>
  
      <v-col col="12" v-if="isServiceListSelected && serviceProvider === 'AZURE'">
        <v-row align="start" justify="start">
          <v-col v-for="(service, i) in Services" :key="i" cols="auto">
            <v-card class="mx-auto card" width="350" height="370" variant="elevated">
              <v-col col="12" class="d-flex justify-end pa-0">
                <v-tooltip location="end center" v-if="service.serviceList != undefined">
                  <template v-slot:activator="{ props }">
                    <v-btn v-bind="props" class="buttonHover">
                      <v-icon icon="mdi-playlist-check" color="#003156"></v-icon>
                    </v-btn>
                  </template>
                  <span>
                    <TooltipText :text="service.serviceList" />
                  </span>
                </v-tooltip>
              </v-col>
              <v-col col="12" class="d-flex align-center justify-center pa-0">
                <img :src="service.src" />
              </v-col>
              <v-col col="12" class="d-flex align-center justify-center pb-0">
                <v-card-title class="title">{{ service.title }}</v-card-title>
              </v-col>
  
              <v-col col="12" class="text-center">
                <p class="subtitle" v-text="service.subtitle"></p>
              </v-col>
              <v-card-actions>
                <ButtonComponent buttonName="Explore" :to="service.link" />
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-col>
  
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted, computed } from 'vue'
  import { useStore } from 'vuex'
  import TopPanel from '../components/common/TopPanel.vue'
  import ButtonComponent from '../components/common/Buttons/Button.vue'
  import SelectComponent from '../components/common/Selects/Select.vue'
  import type { breadcrumbIteam } from '../utils/customInterface'
//   import * as dashboardResources from '@/utils/_api'
  import orphan from '../assets/images/orphan.jpeg'
  import underutilized from '../assets/images/costanalysis.jpeg'
  import advisory from '../assets/images/advisory.jpeg'
//   import aks from '@images/aks.png'
//   import finXRecommend from '@images/FinXRecommend.png'
  import publicimage from '../assets/images/public.jpeg'
  import untaggedImage from '../assets/images/untagged.jpeg'
  import TooltipText from '../components/common/TooltipText.vue'
  
  const store = useStore()
  const topPanelValue = ref<any>('')
  let isLoading = ref(false)
  const serviceProvider = ref<string>('')
  const icon = ref(true)
  let projectsList = ref<any>([])
    let serviceList = ref<any>([])

  let selectedIntegration = ref<string>('')
  onMounted(() => {
    serviceProvider.value = localStorage.getItem('Service')!
 serviceList.value = computed(() => store.state.serviceList)

  })
  
 serviceList.value = computed(() => store.state.serviceList)
  
  let serviceLisItems = serviceList.value.value.map((item: any) => item.integration_name)
  
  console.log('serviceList----->', serviceList.value.value)
  
  const selectedItem = ref<string>('--- Select Integration ---')
  const isServiceListSelected = ref<Boolean>(false)
  
  let breadcrumbItem = ref<Array<breadcrumbIteam>>([])
  breadcrumbItem.value = [
    {
      title: 'Back to Selection',
      disabled: false
    }
  ]
  
  // advisory
  const Services = [
    {
      title: 'Orphan Resources',
      src: orphan,
      subtitle: 'Identify and manage orphaned resources to reduce cost',
      link: '/OrphanResources',
      serviceList: [
        'Public IP',
        'Azure Disk',
        'Network Security Groups',
        'Route Tables',
        'Network security rule'
      ]
    },
    {
      title: 'Underutilized Resources',
      src: underutilized,
      subtitle: 'Deep dive into your expenses and understand areas of saving',
      link: '/UnderutilizedResources',
      serviceList: ['Sql database', 'Webapps', 'Virtual Machine']
    },
    {
      title: 'Resources Open to Public',
      src: publicimage,
      subtitle: 'Public can access these resources',
      link: '/PublicResources',
      serviceList: [
        'Sql servers',
        'Webapps',
        'Virtual Machine',
        'Managed disks',
        'Azure container registery',
        'Databricks workspaces',
        'Eventhub',
        'Key-vaults',
        'Data-factories'
      ]
    },
    {
      title: 'Untagged Resources',
      src: untaggedImage,
      subtitle: 'Public can access these resources',
      link: '/UntaggedResources',
      serviceList: ['ALL']
    },
    
    {
      title: 'Advisor Recommendation',
      src: advisory,
      subtitle: 'Tailored Suggestions to optimize your financial performance',
      link: '/AdvisorRecommendation'
    },

  ]
  
  
  
  const onSelectedServiceListn = async (item: any) => {
    selectedIntegration.value = item.value
    if (item.value !== null) {
      isServiceListSelected.value = true
      store.commit('setSelectedService', item.value)
    } else {
      isServiceListSelected.value = false
    }
  }
  
 
  </script>
  
  <style scoped>
  .heading {
    color: var(--blue-blue-20, #013c6b);
    text-align: left;
    font-family: MB Corpo S Title WEB;
    font-size: 32px;
    font-style: normal;
    font-weight: 400;
    line-height: 40px;
  }
  
  .card {
    border-radius: 12px;
    border: 1px solid var(--blue-blue-90, #cce8ff);
    box-shadow: 2px 5px 6px 0px rgba(0, 0, 0, 0.1);
    padding: 25px;
  }
  
  .tooltip {
    justify-content: end;
  }
  
  .title {
    color: #000;
    text-align: center;
    font-family: MB Corpo S Text WEB;
    font-size: 20px;
    font-style: normal;
    font-weight: 400;
    line-height: 28px;
  }
  
  .mdi-playlist-check.mdi.v-icon.notranslate.v-theme--light.v-icon--size-default {
    padding: 0 20px !important;
  }
  
  .buttonHover {
    border-radius: 20px;
    padding: 0 !important;
    min-width: fit-content;
    background-color: #f4f4f4;
    box-shadow: none;
  }
  
  .v-btn__content {
    padding: 0 12px !important;
  }
  
  .subtitle {
    color: var(--grey-grey-35, #5c5c5c);
    text-align: center;
    font-family: MB Corpo S Text WEB;
    font-size: 16px;
    font-style: normal;
    font-weight: 400;
    line-height: 20px;
  }
  
  .service-image {
    width: 25%;
  }
  </style>