import { createStore } from 'vuex'

const store = createStore({
  state: {
    serviceList: null,
    selectedService: null,
   
    jiraIntegration: []
  },

  mutations: {
    setServiceList(state: any, response: any) {
      console.log('hi')
      state.serviceList = response
    },
    setSelectedService(state: any, response: any) {
      state.selectedService = response
    },
    setjiraIntegration(state: any, response: any) {
      state.jiraIntegration = response
    }
  }
})

export default store