<template>
    <div>
      <LoaderComponent :isLoading="isLoading" />
      <TopPanel
        :topPanelValue="topPanelValue"
        :items="breadcrumbItem"
        v-if="showDataTable == false"
      />
  
      <HorizontalCard
        width="600"
        height="250"
        fromselect="notstory"
        class="mt-16 d-flex align-center justify-center"
        v-if="showDataTable == false && cloudProvider == 'AZURE'"
      >
        <v-col cols="12" class="d-flex flex-column justify-center align-center">
          <p class="title text-center mb-5">
            Please select your Azure Subscription to view resources:
          </p>
          <div class="text-center w-75">
            <SelectComponent
              :items="subscriptionList"
              labelName="--Select your Azure Subscription--"
              @itemSelected="onSelectedAzureSubscription"
            />
            <template v-if="errorMessage !== ''">
              {{ errorMessage }}
            </template>
          </div>
        </v-col>
      </HorizontalCard>
  
      
      <v-col cols="12" v-if="showDataTable == true">
        <BreadCrumbs :items="breadcrumbItem" />
        <v-btn variant="text" class="back-btn" @click="backToOrphanResources()">
          <v-icon start icon="mdi-chevron-left" color="#036DC1" size="x-large"></v-icon>
          Underutilized Resources
        </v-btn>
        <v-col cols="3" v-if="cloudProvider === 'AZURE'">
          <SelectComponent
            :items="subscriptionList"
            :labelName="selectedItem"
            @itemSelected="onSelectedAzureSubscription"
          />
        </v-col>
        <SimpleTableWithFilter :items="tableItems" :headers="headers" />
      </v-col>
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, onMounted, computed } from 'vue'
  import { useStore } from 'vuex'
  import LoaderComponent from '../../components/common/Loader/Loader.vue'
  import TopPanel from '../../components/common/TopPanel.vue'
  import HorizontalCard from '../../components/common/Cards/HorizontalCard.vue'
  import SelectComponent from '../../components/common/Selects/Select.vue'
  import BreadCrumbs from '../../components/common/BreadCrumbs.vue'
  import SimpleTableWithFilter from '../../components/common/Tables/SimpleTableWithFilter.vue'
  import * as underutilizedResources from '../../utils/_api'
  import type { breadcrumbIteam } from '../../utils/customInterface'
  
  const store = useStore()
  const selectedService = computed(() => store.state.selectedService)
  let cloudProvider = ref<string>('')  
  let topPanelValue = ref('Underutilized Resources')
  let tableItems = ref<any>([])
  let showDataTable = ref<boolean>(false)
  const selectedItem = ref<string>('')
  let errorMessage = ref<string>('')
  let isLoading = ref(false)
  let subscriptionList = ref<any>([])
  let finOpsID = localStorage.getItem('finOpsID')
  let getSubscribersLists = ref<any>([])
  let selectedsubscriptionId = ref<string>('')
  
  const headers = ref<any>([])
  let breadcrumbItem = ref<Array<breadcrumbIteam>>([])
  breadcrumbItem.value = [
    {
      title: 'Services',
      disabled: false
    },
    {
      title: 'Underutilized Resources - Choose Subscription',
      disabled: true
    }
  ]
  
  onMounted(() => {
    cloudProvider.value = localStorage.getItem('Service')!
    console.log(cloudProvider.value)
    getActiveSubscribersList()
    
  })
  
  const getActiveSubscribersList = async () => {
    const data = {
      integration_name: selectedService.value
    }
    const response = await underutilizedResources.getSubscribersList(data)
    if (response.status === 200) {
      const payload = response.data
      subscriptionList.value = payload
      getSubscribersLists.value = payload
    } else {
      let message = 'Failed'
    }
  }
  type DataApiResponse = {
    location: string
    utilization: number
    resource_group: string | null
    name: string
    type: string
  }
  type DataRecord = {
    location: string
    monthly_utilization_value: number
    resource_name: string
    resource_type: string
  }
  

  const onSelectedAzureSubscription = async (item: any) => {
    if (localStorage.getItem('Service') == 'AZURE') {
      headers.value = [
        {
          title: 'Type',
          align: 'start',
          key: 'resource_type'
        },
        { title: 'Name', align: 'start', key: 'resource_name' },
        { title: 'Resource Group', align: 'start', key: 'resource_group' },
        { title: 'Location', align: 'start', key: 'location' },
        { title: 'Monthly Utilization (%)', align: 'start', key: 'monthly_utilization_value' }
      ]
      isLoading.value = true
      selectedsubscriptionId = item.value.subscription_id
      const selectedName = item.value.name
      if (selectedsubscriptionId.value !== '' && selectedsubscriptionId !== undefined) {
        selectedItem.value = selectedName
        breadcrumbItem.value = [
          {
            title: 'Services',
            disabled: false
          },
          {
            title: 'Underutilized Resources',
            disabled: false
          },
          {
            title: selectedItem.value,
            disabled: true
          }
        ]
        const data = {
          subscription_id: selectedsubscriptionId,
          integration_name: selectedService.value
        }
        const response = await underutilizedResources.getUtilizedResources(data)
        if (response.status === 200) {
          const payload = response.data
          if (payload.length !== 0) {
            console.log('payload', payload)
  
            tableItems.value = payload
            showDataTable.value = true
            errorMessage.value = ''
            isLoading.value = false
          } else {
            showDataTable.value = false
            errorMessage.value = 'No under utilized resources found.'
            isLoading.value = false
          }
        } else {
          let message = 'Failed'
          isLoading.value = false
        }
      }
    }
    
  }
  const backToOrphanResources = () => {
    showDataTable.value = false
    breadcrumbItem.value = [
      {
        title: 'Services',
        disabled: false
      },
      {
        title: 'Underutilized Resources - Choose Subscription',
        disabled: false
      }
    ]
    subscriptionList.value = getSubscribersLists.value
  }
  </script>
  
  <style scoped>
  .title {
    color: var(--grey-grey-20, #333);
    font-family: MB Corpo S Text WEB;
    font-size: 16px;
    font-style: normal;
    font-weight: 400;
    line-height: 24px;
  }
  .card {
    border-radius: 12px;
    border: 1px solid var(--blue-blue-90, #cce8ff);
    box-shadow: 2px 5px 6px 0px rgba(0, 0, 0, 0.1);
  }
  
  .back-btn {
    text-transform: capitalize;
  }
  </style>