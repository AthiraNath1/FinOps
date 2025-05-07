import './assets/main.css'
import '@mdi/font/css/materialdesignicons.css'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router/index.ts'
import 'vuetify/styles'
import store  from './store/index.ts';
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const app = createApp(App)
const vuetify = createVuetify({
  theme: {
    defaultTheme: 'light'
  },
  components,
  directives
})
app.use(store);
app.use(router)
app.use(vuetify).mount('#app')