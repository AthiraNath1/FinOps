<template>
    <div>
      <!-- Header Component -->
      <HeaderComponent />
  
      <!-- Login Page Content Component-->
      <v-col cols="12" class="top-panel mt-16">
        <BreadCrumbs :items="breadcrumbItem" />
  
        <v-btn variant="text" class="back-btn" v-if="visibleBackBtn == true && selectedAccount" @click="getBack()">
          <v-icon start icon="mdi-chevron-left" color="#036DC1" size="x-large"></v-icon>
          Back
        </v-btn>
  
        <v-btn variant="text" class="back-btn" v-if="visibleBackBtn == true && selectedAccount == false" to='/Service'>
          <v-icon start icon="mdi-chevron-left" color="#036DC1" size="x-large"></v-icon>
          Back
        </v-btn>
  
        <div class="w-100 d-flex align-center justify-center top-panel-conent">
          <span>{{ topPanelValue }}</span>
        </div>
      </v-col>
  
      <v-col cols="12" class="d-flex align-center justify-center mt-5" v-if="selectingAcount == true">
        <v-col cols="6">
          <p class="conetnt">Which Cloud Service Provider would you prefer to sign up for?</p>
          <v-row>
            <v-col
              cols="6"
              class="mt-5"
              @click="selectedCard(2, 'Azure')"
            >
              <v-card
                variant="outlined"
                class="d-flex align-center justify-center card"
                height="200px"
              >
                <img width="200" src="../assets/images/azure.jpeg" />
              </v-card>
            </v-col>
           
          </v-row>
        </v-col>
      </v-col>
  
  
      <!-- Azure Account Signup Form -->
      <div class="d-flex align-center justify-center mt-5" v-if="selectedAccount && selectedAccountType == 'Azure'">
        <v-col cols="12" sm="10" md="8" lg="4">
          <v-card class="sign-card">
            <v-form
              @submit.prevent="comfirmBtn()"
              class="w-100 d-flex align-center justify-center mt-10 mb-10"
            >
              <v-col cols="12" sm="10" md="8" lg="10">
                <v-col cols="12">
                  <v-row>
                    <v-col cols="10">
                      <v-text-field
                        variant="underlined"
                        v-model="clientID"
                        autofocus
                        placeholder="Client ID"
                        label="Client ID"
                        type="text"
                        :rules="clientIDRules"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="2" class="d-flex align-center justify-center">
                      <v-tooltip v-model="clientId">
                        <template v-slot:activator="{ props }">
                          <v-btn icon v-bind="props" variant="text">
                            <v-icon color="grey-lighten-1"> mdi-information-outline </v-icon>
                          </v-btn>
                        </template>
                        <span
                          >Login to Azure portal > Azure Directory >App Registration >Select Your app.
                          <br />
                          Check Client Id from Overview Section
                        </span>
                      </v-tooltip>
                    </v-col>
                  </v-row>
                </v-col>
  
                <v-col cols="12">
                  <v-row>
                    <v-col cols="10">
                      <v-text-field
                        variant="underlined"
                        v-model="tenantID"
                        placeholder="Tenant ID"
                        label="Tenant ID"
                        type="text"
                        :rules="tenantIDRules"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="2" class="d-flex align-center justify-center">
                      <v-tooltip v-model="tenantId">
                        <template v-slot:activator="{ props }">
                          <v-btn icon v-bind="props" variant="text">
                            <v-icon color="grey-lighten-1"> mdi-information-outline </v-icon>
                          </v-btn>
                        </template>
                        <span>
                          Login to Azure portal > Azure Directory > App Registration >Select Your
                          app.<br />
                          Check Tenant Id from Overview Section
                        </span>
                      </v-tooltip>
                    </v-col>
                  </v-row>
                </v-col>
  
                <v-col cols="12">
                  <v-row>
                    <v-col cols="10">
                      <v-text-field
                        variant="underlined"
                        v-model="clientSecretKey"
                        placeholder="Client Secret"
                        label="Client Secret"
                        type="password"
                        :rules="clientSecretKeyRules"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="2" class="d-flex align-center justify-center">
                      <v-tooltip v-model="clientSecret">
                        <template v-slot:activator="{ props }">
                          <v-btn icon v-bind="props" variant="text">
                            <v-icon color="grey-lighten-1"> mdi-information-outline </v-icon>
                          </v-btn>
                        </template>
                        <span>
                          After App Registration > Select your app. <br />
                          Select Ceritificates& Secrets, create a new client secret and copy it
                        </span>
                      </v-tooltip>
                    </v-col>
                  </v-row>
                </v-col>
  
                <v-col cols="12">
                  <v-row>
                    <v-col cols="10">
                      <v-text-field
                        variant="underlined"
                        v-model="clientUsername"
                        placeholder="Username"
                        label="Username"
                        type="text"
                        
                      ></v-text-field>
                    </v-col>
                    <v-col cols="2" class="d-flex align-center justify-center">
                      <v-tooltip v-model="Username">
                        <template v-slot:activator="{ props }">
                          <v-btn icon v-bind="props" variant="text">
                            <v-icon color="grey-lighten-1"> mdi-information-outline </v-icon>
                          </v-btn>
                        </template>
                        <span> Same as your username </span>
                      </v-tooltip>
                    </v-col>
                  </v-row>
                </v-col>
  
                <v-col cols="12">
                  <v-row>
                    <v-col cols="10">
                      <v-text-field
                        variant="underlined"
                        v-model="integrationName"
                        placeholder="Integration Name"
                        label="Integration Name"
                        type="text"
                        :rules="integrationNameRules"
                      ></v-text-field>
                    </v-col>
                    <v-col cols="2" class="d-flex align-center justify-center">
                      <v-tooltip v-model="intName">
                        <template v-slot:activator="{ props }">
                          <v-btn icon v-bind="props" variant="text">
                            <v-icon color="grey-lighten-1"> mdi-information-outline </v-icon>
                          </v-btn>
                        </template>
                        <span> Same as Azure your Cloud Provider Integration Environment Type. </span>
                      </v-tooltip>
                    </v-col>
                  </v-row>
                </v-col>
  
                <ButtonComponent buttonName="Confirm SignUp" :loading="isLoading" />
  
                <v-col cols="12" class="d-flex align-center bottom-panel">
                  <v-row>
                    <v-col cols="1" class="d-flex align-center">
                      <v-icon color="#0078D6" icon="mdi-information-outline"></v-icon>
                    </v-col>
                    <v-col cols="10" class="d-flex align-center">
                      <p>
                        User is required to set up the application in Azure and also create a service
                        principal. <span>Get Help</span>
                      </p>
                    </v-col>
                    <v-col cols="1" class="d-flex align-center">
                      <v-icon icon="mdi-close"></v-icon>
                    </v-col>
                  </v-row>
                </v-col>
              </v-col>
            </v-form>
          </v-card>
        </v-col>
      </div>     
  
      <div class="d-flex align-center justify-center mt-5" v-if="accountCreated">
        <v-col cols="12" sm="10" md="8" lg="4">
          <v-card class="sign-card d-flex align-center justify-center">
            <v-col cols="12" sm="10" md="8" lg="10">
              <v-col cols="12" class="d-flex align-center justify-center mt-5">
                <span class="success">Success</span>
              </v-col>
  
              <v-col cols="12" class="d-flex align-center justify-center">
                <img src="../assets/images/lock.jpeg" alt="" class="w-50" />
              </v-col>
  
  
              <ButtonComponent buttonName="Login" to="/" />
            </v-col>
          </v-card>
        </v-col>
      </div>
      <FooterComponent />
    </div>
  </template>
  
  <script setup lang="ts">
  import { ref } from 'vue'
  import HeaderComponent from '../components/common/Header.vue'
  import FooterComponent from '../components/common/Footer.vue'
  import ButtonComponent from '../components/common/Buttons/Button.vue'
  import BreadCrumbs from '../components/common/BreadCrumbs.vue'
  import * as UserRegistrationInAzure from '../utils/_api'
  
  const isLoading = ref<boolean>(false)
  let topPanelValue = ref<string>('Select Your Preferred Cloud Service Provider to Register')
  const selectingAcount = ref<boolean>(true)
  const selectedAccount = ref<boolean>(false)
  const selectedAccountType = ref<string>('')
  const accountCreated = ref<boolean>(false)
  const clientId = ref<boolean>(false)
  const tenantId = ref<boolean>(false)
  // const subscriptionID = ref<boolean>(false)
  const clientSecret = ref<boolean>(false)
  const Username = ref<boolean>(false)
  const intName = ref<boolean>(false)
  let visibleBackBtn = ref<boolean>(true)
  let finopsID = ref<string>('')
  const clientUsername = ref<string>('')
  
  const copyDoiToClipboard = (finopsID: string) => {
    navigator.clipboard.writeText(finopsID)
  }
  
  const clientID = ref<string>('')
  const clientIDRules = [
    (value: string | any[]) => {
      if (value?.length > 0) return true
      return 'Client ID is required.'
    }
  ]
  
  const tenantID = ref<string>('')
  const tenantIDRules = [
    (value: string | any[]) => {
      if (value?.length > 0) return true
      return 'tenant ID is required.'
    }
  ]
  
  // const subscriptionId = ref<string>('')
  // const subscriptionIdRules = [
  //   (value: string | any[]) => {
  //     if (value?.length > 0) return true
  //     return 'Subscription ID is required.'
  //   }
  // ] 
  
  const clientSecretKey = ref<string>('')
  const clientSecretKeyRules = [
    (value: string | any[]) => {
      if (value?.length > 0) return true
      return 'Client Secret is required.'
    }
  ]
  
  const accessToken = ref<string>('')
  const accessTokenRules = [
    (value: string | any[]) => {
      if (value?.length > 0) return true
      return 'Access Key is required.'
    }
  ]
  
  const secretToken = ref<string>('')
  const secretTokenRules = [
    (value: string | any[]) => {
      if (value?.length > 0) return true
      return 'Secret Access key is required.'
    }
  ]
  
  
  
  const integrationName = ref<string>('')
  const integrationNameRules = [
    (value: string | any[]) => {
      if (value?.length > 0) return true
      return 'Azure Integration Name is required.'
    }
  ]
  
  
  
  let breadcrumbItem = ref([
    {
      title: 'SignUp',
      disabled: false
    },
    {
      title: 'Choose Platform',
      disabled: true
    }
  ])
  
  const getBack = () => {
      selectedAccountType.value = ''
      selectingAcount.value = true
      selectedAccount.value = false
  }
  
  const activeCard = ref(0)
  const selectedCard = (cardNumber: number, cardName: string) => {
    selectingAcount.value = false
    selectedAccount.value = true
    selectedAccountType.value = cardName
    topPanelValue.value = 'Sign Up'
    if (selectedAccountType.value === 'Azure'){
      breadcrumbItem.value = [
        {
          title: 'SignUp',
          disabled: false
        },
        {
          title: 'Choose Platform',
          disabled: false
        },
        {
          title: 'Sign up for Azure',
          disabled: true
        }
      ]
    }
    activeCard.value = activeCard.value === cardNumber ? 0 : cardNumber
  }
  
  
  //Signup Function for Azure
  const comfirmBtn = async () => {
    const currenttime = new Date().toISOString()
    const modifiedtime = new Date().toISOString()
    if (
      clientID.value !== '' &&
      tenantID.value !== '' &&
      clientSecretKey.value !== '' &&
      integrationName.value !== ''
    ) {
      isLoading.value = true
      breadcrumbItem.value = [
        {
          title: 'SignUp',
          disabled: false
        },
        {
          title: 'Choose Platform',
          disabled: false
        },
        {
          title: 'Sign up for Azure',
          disabled: false
        },
        {
          title: 'Get FinId',
          disabled: true
        }
      ]
      let data = {
        integration_name: integrationName.value,
        user_email: clientUsername.value,
        created_at : currenttime,
        modified_at : modifiedtime,
        platform : "AZURE",
        client_id: clientID.value,
        client_secret: clientSecretKey.value,
        tenant_id: tenantID.value,
      }
      setTimeout(function() {
        isLoading.value = false;
      }, 6000);
      console.log(data)
      const response = await UserRegistrationInAzure.signUp(data)
      if (response.status === 200 || response.status === 202) {
        visibleBackBtn.value = false
        selectedAccount.value = false
        accountCreated.value = true
        topPanelValue.value = 'Azure Sign Up Completed'
        isLoading.value = false
      } else {
        visibleBackBtn.value = false
        selectedAccount.value = true
        accountCreated.value = false
        isLoading.value = false
      }
    }
  }
  
  </script>
  
  <style scoped>
  .top-panel {
    background: var(--blue-blue-95, #e6f5ff);
    width: 100%;
    height: 160px;
    flex-shrink: 0;
    position: relative;
  }
  
  .breadcrumbs {
    color: var(--wb-grey-20, #333);
    font-family: MB Corpo S Text WEB;
    font-size: 12px;
    font-style: normal;
    font-weight: 400;
    line-height: 16px;
    letter-spacing: 0.2px;
  }
  
  .top-panel-conent {
    color: #000;
    text-align: center;
    font-family: MB Corpo A Text Cond WEB;
    font-size: 40px;
    font-style: normal;
    font-weight: 400;
    line-height: 48px;
    position: absolute;
    top: 0;
    bottom: 0;
  }
  
  .conetnt {
    color: var(--grey-grey-20, #333);
    font-family: MB Corpo S Text WEB;
    font-size: 24px;
    font-style: normal;
    font-weight: 400;
    line-height: 24px; /* 100% */
  }
  
  .card {
    transition: filter 0.5s ease;
  }
  
  .active {
    opacity: 0.5;
  }
  
  .card:not(.active) .card {
    opacity: unset;
  }
  
  .sign-card {
    border-radius: 12px;
    border: 1px solid var(--blue-blue-90, #cce8ff);
    box-shadow: 2px 5px 6px 0px rgba(0, 0, 0, 0.1);
  }
  
  .bottom-panel {
    border-radius: 4px;
    border: 1px solid var(--info-light, #3393de);
  }
  
  .bottom-panel p {
    color: var(--blue-blue-40, #036dc1);
    font-family: MB Corpo S Text WEB;
    font-size: 14px;
    font-style: normal;
    font-weight: 400;
    line-height: 20px;
  }
  
  .bottom-panel span {
    color: var(--blue-blue-50, #008dfc);
    font-family: MB Corpo S Text WEB;
    font-size: 14px;
    font-style: normal;
    font-weight: 700;
    line-height: 20px;
    text-decoration-line: underline;
  }
  
  .success {
    color: #198025;
    text-align: center;
    font-family: MB Corpo S Text WEB;
    font-size: 20px;
    font-style: normal;
    font-weight: 700;
    line-height: 28px; /* 140% */
  }
  
  .fin-ops {
    color: var(--test-text-grey-12, #4c4b4b);
    text-align: center;
    font-family: MB Corpo S Text WEB;
    font-size: 16px;
    font-style: normal;
    font-weight: 400;
    line-height: 24px; /* 150% */
  }
  .fin-ops-id {
    color: #000;
    text-align: center;
    font-family: MB Corpo S Title WEB;
    font-size: 26px;
    font-style: normal;
    font-weight: 400;
    line-height: 32px; /* 123.077% */
    letter-spacing: 1.3px;
  }
  .clipboard {
    border-radius: 4px;
    border: 1px solid var(--blue-blue-75, #80c6ff);
    box-shadow: unset;
    color: var(--blue-blue-75, #80c6ff);
    text-align: center;
    font-family: MB Corpo S Text WEB;
    font-size: 14px;
    font-style: normal;
    font-weight: 400;
    line-height: 20px; /* 142.857% */
  }
  
  .bottom-text {
    color: #373636;
    text-align: center;
    font-family: MB Corpo S Text WEB;
    font-size: 16px;
    font-style: normal;
    font-weight: 400;
    line-height: 24px; /* 150% */
  }
  
  .back-btn {
    z-index: 9;
  }
  </style>