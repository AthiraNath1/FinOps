<template>
    <div>
      <v-row justify="center">
        <v-dialog :model-value="dialog" persistent width="450">
          <v-card>
            <v-row justify="center" class="modal-header pa-5">
              <v-col cols="2" class="d-flex justify-center align-center">
                <img src="/src/assets/images/delete.jpeg" class="deleteicon w-100" />
              </v-col>
              <v-col cols="9" class="d-flex justify-center align-center">
                <p class="modal-ptag">
                  Are you sure you want to delete the following orphan resources?
                </p>
                <v-col cols="1" class="d-flex justify-center align-center">
                  <v-icon
                    start
                    icon="mdi-close"
                    color="#003156"
                    size="large"
                    @click="closeDialog"
                  ></v-icon>
                </v-col>
              </v-col>
            </v-row>
            <v-col cols="12">
              <li v-for="item in resourcesName" :key="item" style="text-align: center">
                {{ item }}
              </li>
            </v-col>
            <v-col cols="12" class="d-flex justify-center align-center pa-0">
              <v-col cols="9" class="d-flex justify-center align-center message">
                <v-col cols="1" class="d-flex justify-center align-center">
                  <v-icon
                    start
                    icon="mdi-information-outline"
                    color="#1998FC"
                    size="x-large"
                  ></v-icon>
                </v-col>
                <v-col cols="10" class="d-flex justify-center align-center">
                  <p>Please note once deleted, you will not be able to retrieve it.</p>
                </v-col>
              </v-col>
            </v-col>
            <v-row justify="center" class="mt-4">
              <v-col cols="8">
                <v-card-actions>
                  <ButtonComponent buttonName="Confirm Delete" @click="confirmDelete" />
                </v-card-actions>
              </v-col>
            </v-row>
          </v-card>
        </v-dialog>
      </v-row>
    </div>
  </template>
  
  <script lang="ts" setup>
  import { ref, defineProps, defineEmits } from 'vue'
  import ButtonComponent from '../Buttons/Button.vue'
  
  const { resourcesName, dialog } = defineProps(['resourcesName', 'dialog'])
  const emit = defineEmits()
  
  const closeDialog = () => {
    emit('closeDialog', false)
  }
  
  const confirmDelete = () => {
    emit('updateDialog', false)
  }
  </script>
  
  <style scoped>
  .modal-header {
    background: var(--blue-blue-95, #e6f5ff);
  }
  
  .message {
    border-radius: 4px;
    background: var(--blue-blue-95, #e6f5ff);
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
  </style>