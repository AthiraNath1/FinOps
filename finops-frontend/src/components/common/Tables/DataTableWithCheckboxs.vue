<template>
    <div class="mb-15">
      <v-card-title>
        Resources Present ({{ items?.length }})
        <v-spacer></v-spacer>
        <v-col cols="12">
          <v-row>
            
          </v-row>
        </v-col>
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
            <v-col cols="3" v-if="cloudProvider === 'AZURE'">
              <SelectComponent labelName="Resource Type" />
            </v-col>
            <v-col cols="3" v-if="cloudProvider === 'AZURE'">
              <SelectComponent labelName="Resource Group" />
            </v-col>
          </v-row>
        </v-col>
      </v-card-title>
     
      <v-col col="12" v-if="cloudProvider === 'AZURE'">
        <v-data-table
          v-model="tableRowSelected"
          class="elevation-1 datatable"
          :headers="headers"
          :items="localItems"
          item-value="resource_id"
          return-object
          show-select
          select-strategy="all"
          :search="search"
          :items-per-page="10"
        >
        </v-data-table>
      </v-col>
     
      
  
      <v-col cols="12">
        <v-row>
          <v-col cols="1">
            <ButtonComponent
              buttonName="Delete"
              :loading="isLoading"
              @click="DeleteResourcesModal()"
            />
          </v-col>
          <v-col cols="1">
            <ButtonOutlineComponent
              buttonName="clear"
              :loading="isLoading"
              @click="clearSelection()"
            />
          </v-col>
          <v-col cols="2">
            <ButtonComponent buttonName="Select All" :loading="isLoading" @click="selectAllRows()" />
          </v-col>
        </v-row>
      </v-col>
      <DeleteModal
        :dialog="dialogRef"
        :resourcesName="resourcesName"
        @closeDialog="closeDialog"
        @updateDialog="DeleteResources"
      />
    </div>
  </template>
  
  <script lang="ts" setup>
  import { ref, defineEmits, defineProps, computed, onMounted, watch, watchEffect } from 'vue'
  import { useStore } from 'vuex'
  import { VDataTable } from 'vuetify/components'
  import SelectComponent from '../Selects/Select.vue'
  import ButtonComponent from '../Buttons/Button.vue'
  import ButtonOutlineComponent from '../Buttons/ButtonOutline.vue'
  import DeleteModal from '../Modal/DeleteModal.vue'
  import type { orphanResourcesData } from '../../../utils/customInterface'
  let { items, headers, currentRegion, int } = defineProps([
    'items',
    'headers',
    'currentRegion',
    'currentSubs',
    'int'
  ])
  
  let localItems = ref<any>(items)
  const store = useStore()
  const cloudProvider = ref('')
  let azureCost = ref<any>()
  
  onMounted(() => {
    cloudProvider.value = localStorage.getItem('Service') || ''
    
  })
  
  const selectAllRows = () => {
    if (localStorage.getItem('Service') === 'AZURE') {
      tableRowSelected.value = localItems.value.map((item: orphanResourcesData) => item)
    }
  }
  
  const emit = defineEmits(['orphanResources', 'updateLoading'])
  let isLoading = ref(false)
  let search = ref('')
  
  let tableRowSelected = ref<orphanResourcesData[]>([])
  
  const clearSelection = () => {
    if (localStorage.getItem('Service') === 'AZURE') {
      tableRowSelected.value = []
    }
   
  }
  
  const dialogRef = ref(false)
  
  let resourcesName = ref<any>([])
  
  const closeDialog = (newValue: boolean) => {
    dialogRef.value = newValue
  }
  
  const DeleteResourcesModal = async () => {
    if (localStorage.getItem('Service') === 'AZURE') {
      if (tableRowSelected.value.length !== 0) {
        dialogRef.value = true
        resourcesName.value = tableRowSelected.value.map((item) => item.resource_name)
      }
    }
    
  }
  
  const DeleteResources = () => {
    if (localStorage.getItem('Service') === 'AZURE') {
      emit(
        'orphanResources',
        tableRowSelected.value.map((item) => item.resource_id)
      )
      dialogRef.value = false
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
  .text {
    color: green;
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