<template>
    <div>
      <v-row justify="center">
        <v-dialog :model-value="dialog" persistent width="350">
          <v-card>
            <v-col cols="12" class="d-flex justify-end align-center">
              <v-icon start icon="mdi-close" color="#003156" size="large" @click="closeDialog"></v-icon>
            </v-col>
            <v-col cols="12" class="d-flex justify-center align-center pa-0">
              <v-col cols="9" class="d-flex justify-center align-center">
                <img src="../../../assets/images/ignore.jpeg" class="deleteicon w-100" v-if="label == 'Ignore'" />
                <img src="../../../assets/images/active.jpeg" class="deleteicon w-100" v-if="label == 'Active'" />
              </v-col>
            </v-col>
            <v-col cols="12" class="text-center mb-5">
              <p class="modal-ptag">
                Moved <span class="item"> 1 item </span> to {{ label }} tab.
              </p>
              <p class="modal-ptag">
                Check <span class="item"> {{ label }} </span> tab to view it.
              </p>
            </v-col>
          </v-card>
        </v-dialog>
      </v-row>
    </div>
  </template>
  
  <script lang="ts" setup>
  import { defineProps, defineEmits } from 'vue'
  
  const { resourcesName, dialog, label } = defineProps(['resourcesName', 'dialog', 'label']);
  const emit = defineEmits()
  
  const closeDialog = () => {
    emit('closeDialog', false)
  }
  
  const confirmDelete = () => {
    emit('updateDialog', false)
  }
  </script>
  
  <style scoped>
  .message {
    border-radius: 4px;
    background: var(--blue-blue-95, #E6F5FF);
    padding: 0px;
  }
  
  .message p {
    color: #373636;
    font-family: MB Corpo S Text WEB;
    font-size: 16px;
    font-style: normal;
    font-weight: 400;
    line-height: 16px;
  }
  
  .modal-ptag {
    color: #373636;
    font-family: MB Corpo S Text WEB;
    font-size: 1rem;
    font-style: normal;
    font-weight: 400;
    line-height: 1.5rem;
  }
  
  .item {
    color: #373636;
    font-family: MB Corpo S Text WEB;
    font-size: 1rem;
    font-style: normal;
    font-weight: 700;
    line-height: 1.5rem;
  }
  </style>