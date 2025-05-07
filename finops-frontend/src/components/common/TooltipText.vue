<template>
    <div class="list">
      <ul>
        <p v-for="item in text" :key="item">
          {{ item }}
        </p>
      </ul>
    </div>
  </template>
  
  <script setup lang="ts">
  const props = defineProps({
    text: Array<string>
  })
  </script>
  
  <style scoped>
  .list {
    padding: 5px;
  }
  </style>