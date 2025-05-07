<template>
    <div>
      <LoaderComponent :isLoading="isLoading"  />
      <TopPanel
        :topPanelValue="topPanelValue"
        :items="breadcrumbItem"
        v-if="showDataTable == false"
      />
  
      <HorizontalCard width="600" height="250" fromselect="notstory" class="mt-16 d-flex align-center justify-center" v-if="showDataTable == false && cloudProvider==='AZURE'">
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
          Advisor Recommendation
        </v-btn>
        <v-col cols="3" v-if="cloudProvider === 'AZURE'">
          <SelectComponent
            :items="subscriptionList"
            :labelName="selectedItem"
            @itemSelected="onSelectedAzureSubscription"
          />
        </v-col>
  
        <v-col cols="12">
          <v-tabs
            v-model="tab"
            align-tabs="start"
            color="#013C6B"
            class="tabs"
          >
            <v-tab value="Active">
              Active
            </v-tab>
            <v-tab value="Ignore">
              Ignore
            </v-tab>
          </v-tabs>
        </v-col>
          
          <v-window v-model="tab">
            <v-window-item value="Active">
              <DataTableWithModalsAndCheckboxs :items="activeList"  tabButtonName="Ignore" :finOpsID="finOpsID" :subscriptionId="selectedsubscriptionId" :integrationName="integrationName" @updateActiveIgnoreList="getAdvisorActiveList"/>
            </v-window-item>
            <v-window-item value="Ignore">
              <div v-if="errorMessage1.length>0">{{ errorMessage1 }}</div>
              <DataTableWithModalsAndCheckboxs v-else :items="ignoreList" tabButtonName="Active" :finOpsID="finOpsID" :subscriptionId="selectedsubscriptionId" :integrationName="integrationName" @updateActiveIgnoreList="getAdvisorActiveList" />
            </v-window-item>
          </v-window>
          
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
  import DataTableWithModalsAndCheckboxs from '../../components/common/Tables/DataTableWithModalsAndCheckboxs.vue'
  import type { breadcrumbIteam, advisorRecommendation } from '../../utils/customInterface'
  import * as AdvisorRecommendation from '../../utils/_api'
  
    const store = useStore()
  
  
    let topPanelValue = ref('Advisor Recommendation');
    let isLoading = ref(false)
    let subscriptionList = ref<any>([]);
    let finOpsID = localStorage.getItem('finOpsID');
    let getSubscribersLists = ref<any>([]);
    let selectedsubscriptionId = ref<string>('');
    let cloudProvider = ref<string>('');
    let integrationName = ref<string>('');
  
    let breadcrumbItem = ref<Array<breadcrumbIteam>>([]);
    breadcrumbItem.value = [
      {
        title: 'Services',
        disabled: false
      },
      {
        title: 'Advisor Recommendation - Choose Subscription',
        disabled: true
      }
    ];
  
    const tab = ref(null);
  
    onMounted(() => {
      cloudProvider.value = localStorage.getItem('Service')!;
      integrationName.value = computed(() => store.state.selectedService).value;
      console.log("integrationName", integrationName.value)  
      getActiveSubscribersList();
    });
  
    const getActiveSubscribersList = async () => {
      const data = {
        integration_name : integrationName.value
      }
      const response = await AdvisorRecommendation.getSubscribersList(data);
      if(response.status === 200) {
        const payload = response.data
        subscriptionList.value = payload
        getSubscribersLists.value = payload;
        // getAdvisorActiveList();
      }else {
        let message = ('Failed');
      }
    };
  
  
    let activeList = ref<Array<advisorRecommendation>>([]);
    let ignoreList = ref<Array<advisorRecommendation>>([])
    let showDataTable = ref<boolean>(false)
    const selectedItem = ref<string>('')
    let errorMessage = ref<string>('');
      let errorMessage1 = ref<string>('');
    
    const onSelectedAzureSubscription = async (item: any) => {
      if(cloudProvider.value === 'AZURE') {
        console.log("AZURE", "FETCHING DATA")
        isLoading.value = true;
        console.log(item.value.subscription_id)
      selectedsubscriptionId = item.value.subscription_id;
      const selectedName = item.value.name;
      if (selectedsubscriptionId.value !== '' && selectedsubscriptionId !== undefined) {
        selectedItem.value = selectedName
        breadcrumbItem.value = [
          {
            title: 'Services',
            disabled: false
          },
          {
            title: 'Advisor Recommendation',
            disabled: false
          },
          {
            title: selectedItem.value,
            disabled: true
          }
        ];
        const data = {
          subscription_id: selectedsubscriptionId,
           integration_name: integrationName.value
        }
        // const response = await AdvisorRecommendation.getAdvisor(data);
        // console.log(response)
        showDataTable.value = true;

        getAdvisorActiveList();
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
          title: 'Advisor Recommendation - Choose Subscription',
          disabled: false
        }
      ]
      subscriptionList.value = getSubscribersLists.value
    }
  
    const getAdvisorActiveList = async () => {
      const data = {
        subscription_id: selectedsubscriptionId,
        integration_name: integrationName.value
         
        }
      const response = await AdvisorRecommendation.getAdvisor(data);
        if (response.status === 200) {
          const payload = response.data;
          activeList.value = payload;
          isLoading.value = false;
  
        }
        getAdvisorIgnoreList();
    }
  
    const getAdvisorIgnoreList = async () => {
      const data = {
          subscription_id: selectedsubscriptionId,
          integration_name: integrationName.value
        }
        console.log(data)
      const response = await AdvisorRecommendation.getAdvisorIgnoreData(data);
        if (response.status === 200) {
          const payload = response.data;
console.log(payload.length !== 0)
          if (payload.length !== 0) {
            
          ignoreList.value = payload
console.log(ignoreList.value)
errorMessage1.value=''
          } else {
            errorMessage1.value = 'No ignored recommendation found.'
          }
console.log(errorMessage.value)
          
        }
        
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
  .tabs{
    border-bottom: 1px solid #767676;
  }
  </style>