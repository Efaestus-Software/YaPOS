import { createRouter, createWebHistory, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import PageNotFound from '../views/PageNotFound.vue'
import Logout from '../views/Logout'
import PaymentInputView from '../views/PaymentInputView.vue'
import InventoryView from '../views/InventoryView.vue'
import AdjustmentsView from '@/views/AdjustmentsView.vue'
import ReceivingReportView from '@/views/ReceivingReportView.vue'
import SalesView from '@/views/SalesView.vue'
import RRList from '@/views/RRList.vue'
import ADList from '@/views/ADList.vue'
import SIList from '@/views/SIList.vue'
import CustomersView from '@/views/CustomersView.vue'
import SuppliersView from '@/views/SuppliersView.vue'
import InventoryList from '@/views/InventoryList.vue'
import ReceiptView from '@/views/ReceiptView.vue'
import UserSettingsView from '@/views/UserSettingsView.vue'
import BusinessSettingsView from '@/views/BusinessSettingsView.vue'
import AddUserView from '@/views/AddUserView.vue'
import PageForbidden from '@/views/PageForbidden.vue'
import store from '@/store'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: {
      requiresLogin: true
    },
    transition: 'slide',
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    //meta: {
    //  requiresLogin: true
    //}
  },
  {
    path: '/logout',
    name: 'logout',
    component: Logout,
  },
  {
    path: '/:pathMatch(.*)*',
    component: PageNotFound
  },
  {
    path: '/forbidden',
    name: 'forbidden',
    component: PageForbidden
  },
  {
    path: '/payment-input',
    name: 'payment-input',
    meta: {
      requiresLogin: true
    },
    component: PaymentInputView
  },
  {
    path: '/inventory',
    name: 'inventory',
    meta: {
      requiresLogin: true
    },
    component: InventoryView,
    beforeEnter(to, from, next) {
      if (store.state.myDetails.is_superuser) {
        next()
      } else {
        next('/forbidden')
      }
    }
  },
  {
    path: '/inventory-list',
    name: 'inventory-list',
    meta: {
      requiresLogin: true
    },
    component: InventoryList,
    beforeEnter(to, from, next) {
      if (store.state.myDetails.is_superuser) {
        next()
      } else {
        next('/forbidden')
      }
    }
  },
  {
    path: '/adjustments',
    name: 'adjustments',
    meta: {
      requiresLogin: true
    },
    component: AdjustmentsView,
    beforeEnter(to, from, next) {
      if (store.state.myDetails.is_superuser) {
        next()
      } else {
        next('/forbidden')
      }
    }
  },
  {
    path: '/receive',
    name: 'receive',
    meta: {
      requiresLogin: true
    },
    component: ReceivingReportView,
    beforeEnter(to, from, next) {
      if (store.state.myDetails.is_superuser) {
        next()
      } else {
        next('/forbidden')
      }
    }
  },
  {
    path: '/sales',
    name: 'sales',
    meta: {
      requiresLogin: true
    },
    component: SalesView
  },
  {
    path: '/rr-list',
    name: 'rr-list',
    meta: {
      requiresLogin: true
    },
    component: RRList,
    beforeEnter(to, from, next) {
      if (store.state.myDetails.is_superuser) {
        next()
      } else {
        next('/forbidden')
      }
    }
  },
  {
    path: '/ad-list',
    name: 'ad-list',
    meta: {
      requiresLogin: true,
    },
    component: ADList,
    beforeEnter(to, from, next) {
      if (store.state.myDetails.is_superuser) {
        next()
      } else {
        next('/forbidden')
      }
    }
  },
  {
    path: '/si-list',
    name: "si-list",
    meta: {
      requiresLogin: true
    },
    component: SIList,
    beforeEnter(to, from, next) {
      if (store.state.myDetails.is_superuser) {
        next()
      } else {
        next('/forbidden')
      }
    }
  },
  {
    path: '/suppliers',
    name: 'suppliers',
    meta: {
      requiresLogin: true
    },
    component: SuppliersView,
    beforeEnter(to, from, next) {
      if (store.state.myDetails.is_superuser) {
        next()
      } else {
        next('/forbidden')
      }
    }
  },
  {
    path: '/customers',
    name: 'customers',
    meta: {
      requiresLogin: true
    },
    component: CustomersView,
    beforeEnter(to, from, next) {
      if (store.state.myDetails.is_superuser) {
        next()
      } else {
        next('/forbidden')
      }
    }
  },
  {
    path: '/receipt/:id',
    name: 'receipt',
    props: true,
    meta: {
      requiresLogin: true
    },
    component: ReceiptView
  },
  {
    path: '/user-settings',
    name: 'user-settings',
    meta: {
      requiresLogin: true
    },
    component: UserSettingsView
  },
  {
    path: '/business-settings',
    name: 'business-settings',
    meta: {
      requiresLogin: true
    },
    component: BusinessSettingsView,
    beforeEnter(to, from, next) {
      if (store.state.myDetails.is_superuser) {
        next()
      } else {
        next('/forbidden')
      }
    }
  },
  {
    path: '/add-user',
    name: 'add-user',
    meta: {
      requiresLogin: true
    },
    component: AddUserView,
    beforeEnter(to, from, next) {
      if (store.state.myDetails.is_superuser) {
        next()
      } else {
        next('/forbidden')
      }
    }
  }

  // {
  //   path: '/about',
  //   name: 'about',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  // }
]

const router = createRouter({
  history: process.env.IS_ELECTRON ? createWebHashHistory() : createWebHistory(),
  routes
})

export default router
