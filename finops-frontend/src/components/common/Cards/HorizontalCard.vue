<template>
    <v-col col="12">
      <v-row align="center" justify="space-evenly">
        <v-col cols="auto">
          <v-card
            class="mx-auto card"
            :width="width"
            :height="height"
            variant="elevated"
            :class="{
              'd-flex': assignedValue === 'notstory',
              'flex-column': assignedValue === 'notstory',
              'justify-content-center': assignedValue === 'notstory',
              'align-items-center': assignedValue === 'notstory'
            }"
          >
          <!-- :width="600"
            :height="250" -->
            <slot></slot>
          </v-card>
        </v-col>
      </v-row>
    </v-col>
  </template>
  
  
  <script setup lang="ts">
    import { ref } from 'vue'
  const props = defineProps({
    width: String,
    height: String,
    fromselect: String
  })
  
  const assignedValue = ref(props.fromselect);
  
  </script>
  
  <style scoped>
  .card {
    border-radius: 12px;
    border: 1px solid var(--blue-blue-90, #cce8ff);
    box-shadow: 2px 5px 6px 0px rgba(0, 0, 0, 0.1);
  }
  </style>