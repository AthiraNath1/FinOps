<template>
    <div class="mb-15">
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
              <SelectComponent v-if="cloudProvider === 'AZURE'" labelName="Resource Group" />
            </v-col>
            <v-col cols="3">
              <SelectComponent labelName="Resource Type" />
            </v-col>
          </v-row>
        </v-col>
      </v-card-title>
      <v-col col="12">
        <v-data-table
          class="elevation-1 datatable"
          :headers="headers"
          :items="formattedItems()"
          item-value="resource_id"
          :search="search"
          :items-per-page="10"
          select-strategy="single"
        >
        </v-data-table>
      </v-col>
    </div>
  </template>
  
  <script lang="ts" setup>
  import { ref, defineProps, onMounted } from 'vue'
  import { VDataTable } from 'vuetify/components'
  import SelectComponent from '../Selects/Select.vue'
  
  // const props = defineProps({
  //   items: Array,
  //   headers: Array
  // });
  
  const { items, headers } = defineProps(['items', 'headers'])
  let cloudProvider = ref<string>('')
  let isLoading = ref(false)
  let search = ref('')
  onMounted(() => {
    cloudProvider.value = localStorage.getItem('Service')!
  })
  
  const formattedItems = () => {
    return items.map((item: any) => ({
      ...item,
      cost_savings: item.cost_savings === null ? '--' : item.cost_savings
    }))
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