<template>
    <v-breadcrumbs :items="items" class="breadcrumbs">
      <template v-slot:divider>
        <v-icon icon="mdi-chevron-right"></v-icon>
      </template>
    </v-breadcrumbs>
  </template>
  
  <script setup lang="ts">
  import type { breadcrumbIteam } from '../../utils/customInterface'
  const props = defineProps({
    items: Array<breadcrumbIteam>
  })
  </script>
  
  <style scoped>
  .breadcrumbs {
    color: var(--wb-grey-20, #333);
    font-family: MB Corpo S Text WEB;
    font-size: 12px;
    font-style: normal;
    font-weight: 400;
    line-height: 16px;
    letter-spacing: 0.2px;
  }
  </style>