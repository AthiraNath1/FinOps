<template>
    <div class="mb-15">
      <LoaderComponent :isLoading="isLoadings" />
      <v-card-title>
        <v-col cols="12">
          <v-row>
            <v-col cols="3">
              <v-text-field
                v-model="search"
                prepend-inner-icon="mdi-magnify"
                label="Search"
                single-line
                hide-details
                variant="underlined"
              ></v-text-field>
            </v-col>
            <v-spacer></v-spacer>
            <v-col cols="3">
              <SelectComponent labelName="Resource Type" />
            </v-col>
            <v-col cols="3">
              <SelectComponent labelName="Resource Group" />
            </v-col>
          </v-row>
        </v-col>
      </v-card-title>
      <v-col col="12">
        <v-data-table
          v-model="tableRowSelected"
          class="elevation-1 datatable"
          :headers="headers"
          :items="items"
          item-value="resource_id"
          return-object
          show-select
          :search="search"
          :items-per-page="10"
          select-strategy="single"
        >
          <template v-slot:[`item.impacted_field`]="{ item }">
            {{ shortenString(item.impacted_field, 40) }}
            <!-- {{ shortenString(item.Impacted_Field, 30) }} -->
          </template>
  
          <template v-slot:[`item.actions`]="{ item }">
            <v-icon size="small" class="me-2" @click="advisorModal(item)"> mdi-chevron-right </v-icon>
          </template>
        </v-data-table>
      </v-col>
  
      <v-col cols="12">
        <v-row>
          <v-col cols="2">
            <ButtonComponent
              :buttonName="'Move To ' + tabButtonName"
              :loading="isLoading"
              @click="activeIgnoreResource()"
            />
          </v-col>
          <v-col cols="1">
            <ButtonOutlineComponent
              buttonName="clear"
              :loading="isLoading"
              @click="clearSelection()"
            />
          </v-col>
        </v-row>
      </v-col>
      <AdvisorRecommendationModal
        :dialog="dialogRef"
        :item="advisorRecommendationItem"
        @closeDialog="closeDialog"
        @moveToActiveIgnore="closeAdvisorModal"
        :buttonName="tabButtonName"
      />
  
      <ActiveIgnoreModal :label="tabButtonName" :dialog="dialogDelete" @closeDialog="closeDialog" />
    </div>
  </template>
  
  <script lang="ts" setup>
  import { ref, defineEmits, defineProps, onMounted } from 'vue'
  import LoaderComponent from '../Loader/Loader.vue'
  import { VDataTable } from 'vuetify/components'
  import SelectComponent from '../Selects/Select.vue'
  import ButtonComponent from '../Buttons/Button.vue'
  import ButtonOutlineComponent from '../Buttons/ButtonOutline.vue'
  import AdvisorRecommendationModal from '../Modal/AdvisorRecommendationModal.vue'
  import ActiveIgnoreModal from '../Modal/ActiveIgnoreModal.vue'
  import type { advisorRecommendation } from '@/utils/customInterface'
  import * as AdvisorRecommendation from '../../../utils/_api'
  
  const { items, tabButtonName, finOpsID, subscriptionId, integrationName } = defineProps([
    'items',
    'tabButtonName',
    'finOpsID',
    'subscriptionId',
    'integrationName'
  ])
  const serviceProvider = ref<string>('')
  
  onMounted(() => {
    serviceProvider.value = localStorage.getItem('Service')!
  })
  const headers = ref<any>([])
  headers.value = [
    {
      title: 'Impacted_Field',
      align: 'start',
      key: 'impacted_field'
    },
    { title: 'Resource Group', align: 'start', key: 'resource_group' },
    { title: 'Category', align: 'start', key: 'category' },
    { title: 'Impact', align: 'start', key: 'impact' },
    { title: 'Problem', align: 'start', key: 'problem' },
    { title: 'Recommendation', align: 'start', key: 'recommendation' },
    { title: 'Savings(monthly)', align: 'start', key: 'monthly_cost_savings', width: '50' },
    { title: '', key: 'actions' }
  ]
  
  const shortenString = (str: any, maxLength: any) => {
    if (str !== null) {
      if (str.length <= maxLength) {
        return str
      } else {
        return str.substr(0, maxLength - 3) + '...'
      }
    }
  }
  
  // const emit = defineEmits(['orphanResources'])
  const emit = defineEmits()
  
  let isLoading = ref(false)
  let isLoadings = ref(false)
  let search = ref('')
  
  let tableRowSelected = ref<Array<advisorRecommendation>>([])
  
  const clearSelection = () => {
    tableRowSelected.value = []
  }
  
  const dialogRef = ref(false)
  let advisorRecommendationItem = ref<any>()
  
  const advisorModal = (item: Array<advisorRecommendation>) => {
    dialogRef.value = true
    advisorRecommendationItem.value = item
  }
  
  const closeDialog = (newValue: boolean) => {
    dialogRef.value = newValue
    dialogDelete.value = newValue
  }
  
  const dialogDelete = ref(false)
  const activeIgnoreResource = () => {
    if (tableRowSelected.value.length !== 0) {
      isLoadings.value = true
      let recid = tableRowSelected.value[0].recommendation_id
      if (tabButtonName === 'Ignore') {
        addIgnoreList(recid, integrationName)
      } else {
        addActiveList(recid, integrationName)
      }
    }
  }
  
  const addIgnoreList = async (recid: String, integrationName: string) => {
    console.log('Integration Name from Props', integrationName)
    let data = {
      integration_name: integrationName,
      // finops_id: finOpsID,
      // subscription_id: subscriptionId,
      recommendation_id: recid
    }
    const response = await AdvisorRecommendation.excludeRecommendations(data)
    if (true) {
      const payload = response.data
      isLoadings.value = false
      dialogDelete.value = true
      tableRowSelected.value = []
      serviceProvider.value === 'AZURE' && emit('updateActiveIgnoreList')
  
    } else {
      isLoadings.value = false
    }
  }
  
  const addActiveList = async (recid: String, integrationName: string) => {
    console.log('Integration Name from Props', integrationName)
    let data = {
      integration_name: integrationName,
      // finops_id: finOpsID,
      // subscription_id: subscriptionId,
      recommendation_id: recid
    }
    const response = await AdvisorRecommendation.includeRecommendations(data)
    if (response.status === 200) {
      const payload = response.data
      isLoadings.value = false
      dialogDelete.value = true
      tableRowSelected.value = []
      serviceProvider.value === 'AZURE' && emit('updateActiveIgnoreList')
  
    } else {
      isLoadings.value = false
    }
  }
  
  const closeAdvisorModal = (btn: String) => {
    dialogRef.value = false
    isLoadings.value = true
    let recid: string = advisorRecommendationItem.value['recommendation_id']
    console.log('Recid', recid)
    if (btn === 'Ignore') {
      addIgnoreList(recid, integrationName)
    } else {
      addActiveList(recid, integrationName)
    }
  }
  </script>
  
  <style scoped>
  .datatable {
    padding-bottom: 24px;
  }
  
  .modal-header {
    background: var(--blue-blue-95, #e6f5ff);
    padding: 12px 20px;
  }
  
  .deleteicon {
    width: 3.5rem;
    height: 3.5rem;
  }
  .modal-ptag {
    color: var(--blue-blue-15, #003156);
    font-family: MB Corpo S Text WEB;
    font-size: 1.25rem;
    font-style: normal;
    font-weight: 400;
    line-height: 1.75rem; /* 140% */
  }
  </style>