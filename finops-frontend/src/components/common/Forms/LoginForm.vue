<template>
    <div class="w-100 d-flex align-center justify-center">
      <v-card flat>
        <div class="d-flex justify-center align-center mb-15">
          <img src="/src/assets/images/banner-logo.jpeg" class="logo" />
        </div>
  
        <v-card-text class="no-padding">
          <v-form @submit.prevent="login()">
          <v-text-field
              variant="underlined"
              v-model="userName"
              placeholder="Username"
              label="Username"
              type="text"
            ></v-text-field>
          </v-form>
          <!-- <v-text-field
              variant="underlined"
              v-model="finOpsID"
              label="FinOps ID"
              placeholder="············"
              :type="isPasswordVisible ? 'text' : 'password'"
              :append-inner-icon="isPasswordVisible ? 'mdi-eye-off' : 'mdi-eye'"
              @click:append-inner="isPasswordVisible = !isPasswordVisible"
              :rules="finOpsIDRules"
              class="mb-5"
              autocomplete="off"
            ></v-text-field> -->
  
          <ButtonComponent buttonName="Login" :loading="isLoading" @click="login()" />
  
          <v-col cols="12" class="d-flex align-center">
            <v-divider class="ms-3" />
            <span class="mx-4 w-100 divider-content">Are you a new user? </span>
            <v-divider />
          </v-col>
          <!-- </v-form> -->
        </v-card-text>
  
        <v-row class="mt-5">
          <v-col cols="12" class="text-center">
            <ButtonOutlineComponent buttonName="Sign Up" @click="register()" />
          </v-col>
        </v-row>
        <v-col cols="12" class="d-flex align-center justify-center mt-5">
          <v-card-subtitle class="right-panel-conetent d-flex align-center justify-center"
            >Curious about how FinX can help it’s users -
            <v-btn variant="text" to="/Learnmore" class="learn">Learn More</v-btn>
          </v-card-subtitle>
        </v-col>
      </v-card>
  
      <!-- <Snackbar ref="snackbarRef" /> -->
      <!-- 
      <v-alert
        v-model="alert"
        border="start"
        variant="tonal"
        closable
        close-label="Close Alert"
        color="#C51162"
        title="Something went wrong"
        class="alert"
        density="compact"
       
      >
      </v-alert> -->
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref, watch, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import ButtonComponent from '../Buttons/Button.vue'
  import ButtonOutlineComponent from '../Buttons/ButtonOutline.vue'
  import axios from 'axios'
  import * as apis from '../../../utils/_api'
  
  const router = useRouter()
  const isLoading = ref(false)
  const isPasswordVisible = ref<boolean>(false)
  const snackbarRef = ref<any>(null)
  const userName = ref()
  
//   onMounted(() => {
//     introspect()
//   })
  
//   const introspect = async () => {
//     const response = await apis.introspect()
//     const status = response.status
//     if (status === 200) {
//       const payload = response.data
//       console.log('payload', payload)
  
//       if (payload.user_id != undefined) {
//         let page = localStorage.getItem('page')
//         localStorage.setItem('Username', payload.user_id)
//         if (page != undefined) {
//           if (page == 'Service') {
//             router.push('/Service')
//           }
//           if (page == 'register') {
//             router.push('/Register')
//           }
//         } else {
//           router.push('/Service')
//         }
//       }
//     } else {
//       console.log('Errrrrorrrrrrrrr')
//     }
//   }
  
  const showSnackbar = (message: string, color: string) => {
    // Call the showSnackbar method of the Snackbar component
    snackbarRef.value.snackbar.show = true
    snackbarRef.value.snackbar.message = message
    snackbarRef.value.snackbar.color = color
  }
  
  const login = async () => {
    try{
    const response = await fetch('http://localhost:8000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body:  JSON.stringify({
      email: userName.value
    }),
    });
  
    const data = await response.json();
    if (response.ok) {
      // Save token locally (in localStorage)
      localStorage.setItem('Username',userName.value)
      localStorage.setItem('token', data.token);
    router.push('/Service')
    } else {
      alert('Login failed');
    }}
  catch (error) {
    console.error('Login error:', error);
  }



//      const response = await apis.login(userName.value)
// console.log(response)
  //   const data1 = await axios.get("http://localhost:8000/azure/underutilizedresources?subscription_id=e20e19c1-c6dd-4b34-a7c1-0c01aa3f0292", {
  //   headers: { "Content-Type": "application/json" },
  //   withCredentials: true
  // })

  // console.log("Response Data:1", data1);
  }
  
  const register = async () => {
    localStorage.setItem('page', 'register')
    router.push('/Register')
    
  }
  </script>
  
  <style scoped>
  .width {
    width: 85%;
  }
  
  .logo {
    width: auto;
    height: auto;
  }
  
  .no-padding {
    padding: 0;
  }
  
  .right-panel-conetent {
    color: var(--grey-grey-35, #5c5c5c);
    font-family: MB Corpo S Text WEB;
    font-size: 14px;
    font-style: normal;
    font-weight: 400;
    line-height: 20px; /* 166.667% */
    opacity: unset !important;
  }
  
  .right-panel-conetent button {
    color: var(--blue-blue-50, #008dfc);
    font-family: MB Corpo S Text WEB;
    font-size: 14px;
    font-style: normal;
    font-weight: 700;
    line-height: 20px;
    text-decoration-line: underline;
    letter-spacing: 0px;
  }
  
  .divider-content {
    color: var(--test-text-grey-12, #4c4b4b);
    text-align: center;
    font-family: MB Corpo S Text WEB;
    font-size: 12px;
    font-style: normal;
    font-weight: 400;
    line-height: 20px;
  }
  
  .learn {
    color: var(--blue-blue-50, #008dfc);
    font-family: MB Corpo S Text WEB;
    font-size: 12px;
    font-style: normal;
    font-weight: 700;
    line-height: 20px;
    text-decoration-line: underline;
    text-transform: capitalize;
    padding: 0;
  }
  
  /* .alert {
    position: absolute;
      bottom: 55px;
      width: 35%;
      right: 0;
  } */
  </style>