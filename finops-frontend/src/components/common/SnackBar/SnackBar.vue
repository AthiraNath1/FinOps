<template>
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" :timeout="snackbar.timeout" top>
      {{ snackbar.message }}
    </v-snackbar>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue';
  
  interface SnackbarState {
    show: boolean;
    message: string;
    color: string;
    timeout: number;
  }
  
  const snackbar = ref<SnackbarState>({
    show: false,
    message: '',
    color: '',
    timeout: 3000,
  });
  </script>