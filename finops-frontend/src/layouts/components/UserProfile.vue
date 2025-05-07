<template>
    <v-container fluid>
      <v-row justify="center">
        <!-- <span class="loggin-person d-flex align-center">{{ UserName }}</span> -->
        <v-menu min-width="200px" rounded>
          <template v-slot:activator="{ props }">
            <v-btn icon v-bind="props">
              <v-avatar color="brown" size="36px">
                <span class="text-h7">{{ UserName }}</span>
              </v-avatar>
            </v-btn>
          </template>
          <v-card>
            <v-card-text>
              <div class="mx-auto text-center">
                <v-btn variant="text"> Setting </v-btn>
                <v-divider class="my-3"></v-divider>
                <v-btn variant="text" @click="logout()"> Logout </v-btn>
              </div>
            </v-card-text>
          </v-card>
        </v-menu>
      </v-row>
    </v-container>
  </template>
  <script setup lang="ts">
  import { ref, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
//   import * as apis from '@/utils/_api'
  
  let UserName = ref<string>('')
  let initials = ref<string>('')
  let capitalize = ref<string>('')
  
  onMounted(() => {
    capitalize.value = localStorage.getItem('Username') || ''
    UserName.value = capitalize.value.slice(0,2).toUpperCase()
    initials.value = UserName.value.charAt(0).toUpperCase()
  })
  
  const router = useRouter()
  
  const logout = async () => {
    const response = await apis.logout()
    const status = response.status
    if (status === 200) {
      const payload = response.data
      localStorage.clear()
      router.push('/')
    } else {
      console.log('Errrrrorrrrrrrrr')
    }
  }
  </script>
  
  <style scoped>
  .loggin-person {
    color: #fff;
    font-family: MB Corpo S Text WEB;
    font-size: 1rem;
    font-style: normal;
    font-weight: 400;
    line-height: 0.9375rem;
  }
  </style>