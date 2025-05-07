<template>
    <v-btn
      :disabled="loading"
      :loading="loading"
      block
      class="text-none mb-4 button"
      size="x-large"
      variant="flat"
      type="submit"
    >
      {{ buttonName }}
    </v-btn>
  </template>
  
  <script setup lang="ts">
  const props = defineProps({
    buttonName: String,
    loading: Boolean
  })
  </script>
  
  <style scoped>
  .button {
    background: var(--blue-blue-50, #008dfc);
    overflow: hidden;
    color: var(--blue-blue-95, #e6f5ff);
    text-align: center;
    text-overflow: ellipsis;
    font-family: MB Corpo S Text WEB;
    font-size: 16px;
    font-style: normal;
    font-weight: 700;
    line-height: 28px; /* 200% */
    border-radius: 0px;
  }
  </style>