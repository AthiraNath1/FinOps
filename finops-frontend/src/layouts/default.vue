<template>
    <main :class="['core-view', viewSize]">
      <RouterView />
    </main>
  </template>
  
  <script lang="ts">
  import { defineComponent, type PropType, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  export default defineComponent({
    props: {
      viewSize: {
        type: String as PropType<'open' | 'close'>,
        required: true
      }
    },
    setup() {
      const router = useRouter()
      // onMounted(() => {
      //   let UserName = localStorage.getItem('Username')
      //   let finOpsID = localStorage.getItem('finOpsID')
      //   if (
      //     UserName == undefined ||
      //     (UserName == null && finOpsID == undefined) ||
      //     finOpsID == null
      //   ) {
      //     router.push('/')
      //   } else {
      //     router.push('/Dashboard')
      //   }
      // })
    }
  })
  </script>
  
  <style scoped>
  .core-view {
    transition: all 0.3s;
  }
  
  .open {
    padding: 0px 0px 0px 255px;
  }
  
  .close {
    padding: 0px 0px 0px 55px;
  }
  </style>