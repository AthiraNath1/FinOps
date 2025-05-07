<template>
    <VApp>
      <DashboardCoreAppBar />
      <div class="layout-content-wrapper">
        <DashboardCoreDrawer @toggle-view-size="adjustViewSize" @drawer-open="drawerOpen" />
        <DashboardCoreView :viewSize="viewSize" />
      </div>
      <DashboardCoreFooter />
    </VApp>
  </template>
  
  <script setup lang="ts">
  import { defineComponent, ref } from 'vue'
  import DashboardCoreAppBar from '../layouts/components/Header.vue'
  import DashboardCoreDrawer from '../layouts/components/SideBar.vue'
  import DashboardCoreView from '../layouts/default.vue'
  import DashboardCoreFooter from '../layouts/components/Footer.vue'
  
  const viewSize = ref<any>('open')
  const adjustViewSize = () => {
    // Toggle the view size or adjust it based on your requirements
    viewSize.value = viewSize.value === 'open' ? 'close' : 'open'
  }
  
  const drawerOpen = () => {
    viewSize.value = 'open'
  }
  </script>
  
  <style>
  .layout-content-wrapper {
    position: relative;
    margin-top: 4.1rem;
    height: 100%;
  }
  </style>