<template>
    <v-select
      v-model="selected"
      clearable
      :label="labelName"
      :items="items"
      item-title="name"
      :return-object="true"
      variant="underlined"
      @update:modelValue="emitItemSelected"
      class="w-100"
    ></v-select>
  </template>
  
  <script setup lang="ts">
  import { ref, defineEmits } from 'vue'
  
  const props = defineProps({
    items: Array,
    labelName: String
  })
  
  const emit = defineEmits(['itemSelected'])
  
  let selected = ref<any>(null)
  
  const emitItemSelected = () => {
    emit('itemSelected', selected)
  }
  </script>