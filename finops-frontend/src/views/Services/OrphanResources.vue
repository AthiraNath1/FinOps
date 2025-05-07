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
  
      <!-- v-if="showDataTable == true" -->
      <v-col cols="12" v-if="showDataTable == true">
        <BreadCrumbs :items="breadcrumbItem" />
        <v-btn variant="text" class="back-btn" @click="backToOrphanResources()">
          <v-icon start icon="mdi-chevron-left" color="#036DC1" size="x-large"></v-icon>
          Orphan Resources
        </v-btn>
        <v-col cols="3" v-if="cloudProvider == 'AZURE'">
          <SelectComponent
            :items="subscriptionList"
            :labelName="selectedName"
            @itemSelected="onSelectedAzureSubscription"
          />
        </v-col>
  
        <DataTableWithCheckboxs
          :items="tableItems"
          :headers="headers"
          :current-region="selectedRegion"
          :int="selectedService"
          @orphanResources="deleteorphanResources"
          @updateLoading="manageLoading"
          v-if="showDataTable"
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
  import DataTableWithCheckboxs from '../../components/common/Tables/DataTableWithCheckboxs.vue'
  import BreadCrumbs from '../../components/common/BreadCrumbs.vue'
  import * as orphanResources from '../../utils/_api'
  import type { breadcrumbIteam } from '../../utils/customInterface'
  
  const store = useStore()
  
  const selectedService = computed(() => store.state.selectedService)
  console.log(selectedService.value)
  
  let isLoading = ref(false)
  let subscriptionList = ref<any>([])
  let finOpsID = localStorage.getItem('finOpsID')
  let getSubscribersLists = ref<any>([])
  let selectedsubscriptionId = ref<string>('')
  let selectedName = ref<string>('')
  let cloudProvider = ref<string>('')
  let selectedRegion = ref<string>('')
  
  onMounted(() => {
    cloudProvider.value = localStorage.getItem('Service')!
    console.log(cloudProvider.value)
    getActiveSubscribersList()
  })
  
  const getActiveSubscribersList = async () => {
    const data = {
      integration_name: selectedService.value
    }
    const response = await orphanResources.getSubscribersList(data)
    if (response.status === 200) {
      const payload = response.data
      subscriptionList.value = payload
      getSubscribersLists.value = payload
    } else {
      let message = 'Failed'
    }
  }
  
  let topPanelValue = ref('Orphan Resources')
  let breadcrumbItem = ref<Array<breadcrumbIteam>>([])
  breadcrumbItem.value = [
    {
      title: 'Services',
      disabled: false
    },
    {
      title: 'Orphan Resources',
      disabled: true
    }
  ]
  
  const headers = ref<any>([])
  
  let tableItems = ref<any>([])
  let showDataTable = ref<boolean>(false)
  
  let errorMessage = ref<string>('')
  
  const onSelectedAzureSubscription = async (item: any) => {
    //Azure Implementation to fetch the orphan resources
    if (localStorage.getItem('Service') == 'AZURE') {
      headers.value = [
        { title: 'Resource Name	', align: 'start', key: 'resource_name' },
        { title: 'Resource Type', align: 'start', key: 'resource_type' },
        { title: 'Resource Group', align: 'start', key: 'resource_group' },
        { title: 'Cost', align: 'start', key: 'cost' }
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
            title: 'Orphan Resources',
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
        const response = await orphanResources.getOrphanResources(data)
        if (response.status === 200) {
          const payload = response.data
          if (payload.length !== 0) {
            tableItems.value = payload
            showDataTable.value = true
            errorMessage.value = ''
            isLoading.value = false
          } else {
            showDataTable.value = false
            errorMessage.value = 'No orphan resources found.'
            isLoading.value = false
          }
        } 
        else {
          let message = 'Failed'
          isLoading.value = false
        }
      }
    }
  
  }
  
  const backToOrphanResources = () => {
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
  const jiraIntegration = computed(() => store.state.jiraIntegration)
  
  const deleteorphanResources = async (item: any) => {
    const user = localStorage.getItem('Username')
  
    if (localStorage.getItem('Service') == 'AZURE') {
      isLoading.value = true
      let data = {
        resource_id: item,
        subscription_id: selectedsubscriptionId,
        integration_name: selectedService.value
      }
      const response = await orphanResources.deleteOrphanResources(data)
      if (response.status === 200) {
        isLoading.value = false
        const payload = response.data
        let items = {
          value: {
            subscription_id: selectedsubscriptionId,
            name: selectedName
          }
        }
        if (jiraIntegration.value.length > 0) {
          const jiraData = {
            integration_name: selectedService.value,
            project_name: jiraIntegration.value[0].project_name,
            project_key: jiraIntegration.value[0].project_key,
            issue_type: 'Bug',
            description: `${item} resource has been deleted`,
            summary: ` Orphan resource - ${item} has been deleted`,
            assignee: `${user}`
          }
          await orphanResources.createClientJiraIssue(jiraData)
        }
        await onSelectedAzureSubscription(items)
      } else {
        isLoading.value = false
      }
    }
  
  
  }
  
  const manageLoading = (value: boolean) => {
    isLoading.value = value
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