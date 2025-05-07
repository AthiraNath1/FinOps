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
              @itemSelected="onSelected"
            />
            <template v-if="errorMessage !== ''">
              {{ errorMessage }}
            </template>
          </div>
        </v-col>
      </HorizontalCard>
  
  
      <v-col cols="12" v-if="showDataTable == true">
        <BreadCrumbs :items="breadcrumbItem" />
        <v-btn variant="text" class="back-btn" @click="backToUntaggedResources()">
          <v-icon start icon="mdi-chevron-left" color="#036DC1" size="x-large"></v-icon>
          Untagged Resources
        </v-btn>
        <v-col cols="3" v-if="cloudProvider == 'AZURE'">
          <SelectComponent
            :items="subscriptionList"
            :labelName="selectedName"
            @itemSelected="onSelected"
          />
        </v-col>
        <DataTableForTags
          :items="tableItems"
          :headers="headers"
          :current-region="selectedRegion"
          :int="selectedService"
          :displaySuccessDialog="successDialog"
          :displaySuccessMessage="successMesssage"
          @taggingResources="tagResources"
          @updateLoading="manageLoading"
          @successDialog="closeSuccessDialog"
        />
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
  import * as UntaggedResources from '../../utils/_api'
  import type { breadcrumbIteam } from '../../utils/customInterface'
  import DataTableForTags from '../../components/common/Tables/DataTableForTags.vue'
  
  const store = useStore()
  
  const selectedService = computed(() => store.state.selectedService)
  
  let isLoading = ref(false)
  let subscriptionList = ref<any>([])
  let finOpsID = localStorage.getItem('finOpsID')
  let getSubscribersLists = ref<any>([])
  let selectedsubscriptionId = ref<string>('')
  let selectedName = ref<string>('')
  let cloudProvider = ref<string>('')
  let selectedRegion = ref<string>('')
  let headers = ref<any>([])
  let azureData = ref<string>('')
  let tableItems = ref<any>([])
  let showDataTable = ref<boolean>(false)
  let tempRegion = ref<string>('')
  let errorMessage = ref<string>('')
  const successDialog = ref(false)
  const successMesssage = ref(null)
  
  onMounted(() => {
    cloudProvider.value = localStorage.getItem('Service')!
    console.log(cloudProvider.value)
    getActiveSubscribersList()
  
  })
  
  const closeSuccessDialog = (value: boolean) => {
    successDialog.value = value
  }
  const getActiveSubscribersList = async () => {
    const data = {
      integration_name: selectedService.value
    }
    const response = await UntaggedResources.getSubscribersList(data)
    if (response.status === 200) {
      const payload = response.data
      subscriptionList.value = payload
      getSubscribersLists.value = payload
    } else {
      let message = 'Failed'
    }
  }
  
  
  
  let topPanelValue = ref('Untagged Resources')
  let breadcrumbItem = ref<Array<breadcrumbIteam>>([])
  breadcrumbItem.value = [
    {
      title: 'Services',
      disabled: false
    },
    {
      title: 'Untagged Resources',
      disabled: true
    }
  ]
  
  const backToUntaggedResources = () => {
    if (localStorage.getItem('Service') == 'AZURE') {
      showDataTable.value = false
      breadcrumbItem.value = [
        {
          title: 'Services',
          disabled: false
        },
        {
          title: 'Orphan Resources',
          disabled: false
        }
      ]
      subscriptionList.value = getSubscribersLists.value
    }
    
  }
  
  const getUntaggedResources = async (item: any) => {
    if (localStorage.getItem('Service') == 'AZURE') {
      azureData.value = item.value
      console.log('hiiii', item.value)
      headers.value = [
        { title: 'Resource Name	', align: 'start', key: 'resource_name_or_id' },
        { title: 'Resource Type', align: 'start', key: 'resource_type' },
        { title: 'Resource ARN', align: 'start', key: 'resource_arn' }
      ]
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
            title: 'Untagged Resources',
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
        const response = await UntaggedResources.getAzureUntaggedResources(data)
        if (response.status === 200) {
          const payload = response.data
          if (payload.length !== 0) {
            tableItems.value = [...payload]
            console.log('tableItems', tableItems.value)
            showDataTable.value = true
            errorMessage.value = ''
            isLoading.value = false
          } else {
            showDataTable.value = false
            errorMessage.value = 'No Untagged resources found.'
            isLoading.value = false
          }
        } else {
          let message = 'Failed'
          isLoading.value = false
        }
      }
    }
  }
  
  const onSelected = async (item: any) => {
    //Azure Implementation to fetch the orphan resources
    await getUntaggedResources(item)
  }
  
  const tagResources = async (value: any) => {
   
    if (localStorage.getItem('Service') == 'AZURE') {
      isLoading.value = true
  
      try {
        const data = {
          subscription_id: selectedsubscriptionId,
          integration_name: selectedService.value,
          resource_id: value[1].resource_arn
        }
        const response = await UntaggedResources.postTagsToAzureResources(data, value[0])
        if (response.status === 201) {
          const payload = response.data
          successDialog.value = true
          successMesssage.value = payload.message
          setTimeout(() => {
            isLoading.value = false
            showDataTable.value = false
            getUntaggedResources(azureData)
          }, 12000)
        }
      } catch (error: any) {
        isLoading.value = false
        const payload = error.response.data
        console.log(payload)
        // successDialog.value = true
        // successMesssage.value = payload.detail
        alert(payload.detail)
        console.log(successMesssage.value)
        setTimeout(() => {
          // successDialog.value = false
          // showDataTable.value = false
          getUntaggedResources(azureData)
        }, 12000)
      }
    }
  }
  const manageLoading = (value: boolean) => {
    isLoading.value = value
  }
  </script>