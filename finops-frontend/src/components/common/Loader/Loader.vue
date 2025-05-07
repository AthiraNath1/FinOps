<template>
    <div class="text-center" v-if="isLoading">
      <v-overlay :model-value="isLoading" contained class="align-center justify-center">
        <v-progress-circular :size="40" color="#014880" indeterminate></v-progress-circular>
      </v-overlay>
    </div>
  </template>
  
  <script setup lang="ts">
  
  const props = defineProps({
    isLoading: Boolean,
  })
  
  </script>