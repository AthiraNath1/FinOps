<template>
    <div>
      <v-row justify="center">
        <v-dialog :model-value="dialog" persistent width="800" height="550px">
          <v-card>
            <v-row justify="center" class="modal-header pa-5">
              <v-col cols="4" class="d-flex justify-center align-center">
                <p class="modal-ptag heading">
                  Tag Untagged Resouces ({{ fields?.length }})
                </p>
              </v-col>
              <v-col cols="4" class="d-flex start align-center">

                <v-btn elevation="0" rounded="xs" variant="outlined" class="ma-2 outlineButton" @click="addField">
                  <v-icon class="mr-2" style="color: #008DFC73;">mdi-plus</v-icon> <!-- Plus icon -->
                  Add Field
                </v-btn>
              </v-col>  
              <v-col cols="4" class="d-flex justify-end align-center">
                <v-col cols="4" class="d-flex end align-center">
                  <v-icon end icon="mdi-close" color="#003156" size="large" class="d-flex end align-center" @click="closeDialog"></v-icon>
                </v-col>
              </v-col>
            </v-row>
            <v-card-text>
              <v-container>
                <v-row v-for="(field, index) in fields" :key="index">
                  <v-col cols="5" class="d-flex align-center">
                    <p class="mr-5">Key </p>
                    <v-text-field v-model="field.key" :label="('key')" required></v-text-field>
                  </v-col>
                  <v-col cols="5" class="d-flex align-center">
                    <p class="mr-5">Value </p>
                    <v-text-field v-model="field.value" :label="('value')" required></v-text-field>
                  </v-col>
                  <v-col cols="2">
                    <v-btn icon small @click="removeField(index)">
                      <v-icon color="#008DFC73" size="large">mdi-delete</v-icon>
                    </v-btn>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
            <!-- <v-card-actions> -->
              <v-spacer></v-spacer>
              <v-row class="pa-5">
                <v-col cols="4">
                    <ButtonComponent buttonName="Tag Resources" @click="confirmTagging" />
                </v-col>
                <v-col cols="4">
                  <ButtonOutlineComponent buttonName="Clear" @click="clear" />
                </v-col>
              </v-row>
            <!-- </v-card-actions> -->
          </v-card>
        </v-dialog>
      </v-row>
    </div>
  </template>
  
  <script lang="ts" setup>
  import { ref, defineProps, defineEmits } from 'vue'
  import ButtonComponent from '../Buttons/Button.vue'
  import ButtonOutlineComponent from '../Buttons/ButtonOutline.vue'
  
  const { resourcesName, dialog } = defineProps(['resourcesName', 'dialog']);
  const emit = defineEmits()
  const fields = ref([
      { key: '', value: '' },
    ]);
  
  const closeDialog = () => {
    console.log('close dialog')
    emit('closeDialog', false)
    fields.value = [{ key: '', value: '' }]
  }
  
  const confirmTagging = () => {
    if(fields.value.every(field => field.key != null && field.value != null && field.key.length>0 && field.value.length>0)){
      const keyValuePairs = fields.value.map((field) => ({
        key: field.key,
        value: field.value,
      }));
      emit('updateDialog', keyValuePairs)
      fields.value = [{ key: '', value: '' }]
    }
  }

  const addField = () =>{
    fields.value.push({ key: '', value: '' });
  }

  const clear = () =>{
    for( let field of fields.value){
      field.key = '';
      field.value = '';
    }
  }

  const removeField = (index : number) =>{
    if(fields.value.length > 1){
      fields.value.splice(index, 1);
    }
  }
  </script>
  
  <style scoped>
    .modal-header{
      /* background: var(--blue-blue-95, #E6F5FF); */
    }

    .heading{
      font-family: MB Corpo S Text WEB;
      font-size: 16px;
      font-style: normal;
      font-weight: 700;
      line-height: 20px;
      color: #014880;
    }
  
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
    .outlineButton{
      color: #008DFC;
      border: 1px solid #008DFC;

    }
  
  </style>