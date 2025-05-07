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
          Resources Open to Public
        </v-btn>
        <v-col cols="3">
          <SelectComponent
            :items="subscriptionList"
            :labelName="selectedName"
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
  import SimpleTableWithFilter from '../../components/common/Tables/SimpleTableWithFilter.vue'
  import BreadCrumbs from '../../components/common/BreadCrumbs.vue'
  import { getSubscribersList, getPublicResources } from '../../utils/_api'
  import type { breadcrumbIteam } from '../../utils/customInterface'
  
  const store = useStore()
  
  const selectedService = computed(() => store.state.selectedService)
  let cloudProvider = ref<string>('')
  
  let isLoading = ref(false)
  let subscriptionList = ref<any>([])
  let finOpsID = localStorage.getItem('finOpsID')
  let getSubscribersLists = ref<any>([])
  let selectedsubscriptionId = ref<string>('')
  let selectedName = ref<string>('')
  
  let headers = ref<any>([
    { title: 'Type', align: 'start', key: 'resource_type' },
    { title: 'Name', align: 'start', key: 'resource_name' },
    { title: 'Resource Group', align: 'start', key: 'resource_group_name' }
  ])
  
  onMounted(() => {
    cloudProvider.value = localStorage.getItem('Service')!
    console.log(cloudProvider.value)
    getActiveSubscribersList()
 
  })
  
  
  const getActiveSubscribersList = async () => {
    const data = {
      integration_name: selectedService.value
    }
    
    const response = await getSubscribersList(data)
    if (response.status === 200) {
      const payload = response.data
      subscriptionList.value = payload
      getSubscribersLists.value = payload
    } else {
      let message = 'Failed'
    }
  }
  
  let topPanelValue = ref('Resources Open to Public')
  let breadcrumbItem = ref<Array<breadcrumbIteam>>([])
  breadcrumbItem.value = [
    {
      title: 'Services',
      disabled: false
    },
    {
      title: 'Resources Open to Public - Choose Subscription',
      disabled: true
    }
  ]
  //  to: '/Dashboard',
  
  let tableItems = ref<any>([])
  let showDataTable = ref<boolean>(false)
  
  let errorMessage = ref<string>('')
  
  let mockData = [
    {
      enabled_to_public: true,
      resource_group_name: 'pheonix',
      resource_name: 'pheonix-backend',
      resource_type: 'Microsoft.Web/sites',
      subscription_id: '6a63f658-6370-48a4-b854-b94a807a705c'
    }
  ]
  
  const onSelectedAzureSubscription = async (item: any) => {
    if (localStorage.getItem('Service') == 'AZURE') {
      isLoading.value = true
      selectedsubscriptionId = item.value.subscription_id
      selectedName = item.value.name
      if (selectedsubscriptionId.value !== '' && selectedsubscriptionId !== undefined) {
        breadcrumbItem.value = [
          {
            title: 'Services',
            disabled: false
          },
          {
            title: 'Resources Open to Public',
            disabled: false
          },
          {
            title: item.value.name,
            disabled: true
          }
        ]
        const data = {
          subscription_id: selectedsubscriptionId,
          integration_name: selectedService.value
        }


        const response = await getPublicResources(data)
        if (response.status === 200) {
          const payload = response.data
          let truePublicResource: any = []
          if (payload.length !== 0) {
            payload.map((element: { enabled_to_public: boolean }) => {
              if (element.enabled_to_public === true) {
                truePublicResource.push(element)
              }
            })
            tableItems.value = truePublicResource
            showDataTable.value = true
            errorMessage.value = ''
            isLoading.value = false
          } else {
            showDataTable.value = false
            errorMessage.value = 'No public resources found.'
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
        title: 'Resources Open to Public - Choose Subscription',
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