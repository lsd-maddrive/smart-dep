import Vue from 'vue'
import Router from 'vue-router'
import RoomsSelector from '@/components/RoomsSelector'
import RoomControl from '@/components/RoomControl'
import LoginPage from '@/components/LoginPage'

import store from '@/store'

Vue.use(Router)


let router = new Router({
  routes: [{
      path: '/404',
      component: {
        template: '<p>Page Not Found</p>'
      },
    },
    {
      path: '*',
      redirect: '/404'
    },
    {
      path: '/room/:id',
      name: 'RoomControl',
      component: RoomControl,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/',
      name: 'Home',
      component: RoomsSelector,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginPage,
      meta: {
        hideForAuth: true
      }
    },
  ]
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (store.getters["auth/isAuthenticated"]) next()
    else next({
      name: "Login"
    })
  } else {
    next()
  }

  if (to.matched.some(record => record.meta.hideForAuth)) {
    if (store.getters["auth/isAuthenticated"]) {
      next({
        name: "Home"
      });
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
