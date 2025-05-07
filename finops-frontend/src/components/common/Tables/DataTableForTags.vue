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
          :search="search"
          :items-per-page="10"
          select-strategy="single"
        >
        </v-data-table>
      </v-col>
  
      <v-col cols="12">
        <v-row>
          <v-col cols="2">
            <ButtonComponent
              :buttonName="`AddTags ${
                 tableRowSelected?.length
              }`"
              :loading="isLoading"
              @click="AddTagsModalOpen()"
            />
          </v-col>
          <v-col cols="2">
            <ButtonOutlineComponent
              buttonName="clear"
              :loading="isLoading"
              @click="clearSelection()"
            />
          </v-col>
        </v-row>
      </v-col>
      <AddTagsModal :dialog="dialogRef" @closeDialog="closeDialog" @updateDialog="TagResources" />
      <TagSuccessModal
        :dialog="displaySuccessDialog"
        :message="displaySuccessMessage"
        label="Tagged"
        @closeDialog="closeSuccessDialog"
      />
    </div>
  </template>
  
  <script lang="ts" setup>
  import { ref, defineEmits, defineProps, computed, onMounted } from 'vue'
  import { useStore } from 'vuex'
  import { VDataTable } from 'vuetify/components'
  import SelectComponent from '../Selects/Select.vue'
  import ButtonComponent from '../Buttons/Button.vue'
  import ButtonOutlineComponent from '../Buttons/ButtonOutline.vue'
  import type {
    orphanResourcesData,
    UntaggedResourceData
  } from '@/utils/customInterface'
//   import * as dataTableResources from '@/utils/_api'
  import AddTagsModal from '../Modal/AddTagsModal.vue'
  import TagSuccessModal from '../Modal/TagSuccessModal.vue'
  
  let {
    items,
    headers,
    currentRegion,
    currentSubs,
    int,
    displaySuccessDialog,
    displaySuccessMessage
  } = defineProps([
    'items',
    'headers',
    'currentRegion',
    'currentSubs',
    'int',
    'displaySuccessDialog',
    'displaySuccessMessage'
  ])
  
  let localItems = ref<any>(items)
  const store = useStore()
  const cloudProvider = ref('')
  onMounted(() => {
    cloudProvider.value = localStorage.getItem('Service') || ''
  })
  
  const emit = defineEmits(['taggingResources', 'updateLoading', 'successDialog'])
  let isLoading = ref(false)
  let search = ref('')
  
  let tableRowSelected = ref<UntaggedResourceData[]>([])
  let itemSelected = ref<UntaggedResourceData>()
  
  const clearSelection = () => {
    if (localStorage.getItem('Service') === 'AZURE') {
      tableRowSelected.value = []
    }
  }
  
  const dialogRef = ref(false)
  const dialog = ref(displaySuccessDialog)
  
  const closeDialog = (newValue: boolean) => {
    dialogRef.value = newValue
  }
  
  const closeSuccessDialog = (newValue: boolean) => {
    dialog.value = newValue
    emit('successDialog', newValue)
  }
  
  const AddTagsModalOpen = () => {
    if (localStorage.getItem('Service') === 'AZURE') {
      console.log('Opening the Tags Modal')
      console.log(tableRowSelected.value[0])
      itemSelected.value = tableRowSelected.value[0]
      isLoading.value = false
      dialogRef.value = true
      isLoading.value = false
    }
   
  }
  
  const TagResources = (value: any) => {
    if (localStorage.getItem('Service') === 'AZURE') {
      const data = [[...value], itemSelected.value]
      emit('taggingResources', data)
      dialogRef.value = false
    }
    console.log('Tagging Resources', value)
    console.log(itemSelected.value)
    
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