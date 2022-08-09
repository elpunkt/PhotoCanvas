import { createApp } from 'vue'
import App from './App.vue'
import router from '@/router'
import store from '@/store'
import { apiClient } from '@/api/api'

apiClient.interceptors.response.use(function (response) {
    return response;
}, function (error) {
  console.log(error);
  if (error.response) {
    if (401 === error.response.status) {
        store.dispatch('logOut')
    }
  }
  else {
      return Promise.reject(error);
  }
});



createApp(App).use(store).use(router).mount('#app')
