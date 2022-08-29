import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './assets/css/global.css'
import '@/index.css'

import VueSweetalert2 from 'vue-sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';

createApp(App).use(store).use(router).use(VueSweetalert2).mount('#app')

router.beforeEach((to, from, next) => {
    if (to.matched.some(record=>record.meta.requiresLogin)){
       if(!store.getters.loggedIn){
           next({name: 'login'})
       } else {
           next()
       }
    } else {
        next()
    }
})