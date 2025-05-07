<template>
    <v-btn
      :disabled="loading"
      :loading="loading"
      block
      class="button-outline"
      size="x-large"
      variant="flat"
      type="submit"
    >
      {{ buttonName }}
    </v-btn>
  </template>
  
  <script setup lang="ts">
//   import jiraIcon from '@images/jira.png'
  
  const props = defineProps({
    buttonName: String,
    loading: Boolean,
    icon: Boolean
  })
  </script>
  <style scoped>
  .button-outline {
    border-radius: 0px;
    background: var(--test-white, #fff);
    border: 1px solid var(--blue-blue-50, #008dfc);
    overflow: hidden;
    color: var(--blue-blue-50, #008dfc);
    text-align: center;
    text-overflow: ellipsis;
    font-family: MB Corpo S Text WEB;
    font-size: 14px;
    font-style: normal;
    font-weight: 700;
    line-height: 28px; /* 200% */
  }
  </style>