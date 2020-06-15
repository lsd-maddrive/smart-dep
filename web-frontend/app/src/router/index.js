import Vue from 'vue'
import Router from 'vue-router'
import RoomsPage from '@/components/RoomsPage'
import EditRoomPage from '@/components/EditRoomPage'
import RoomControlPage from '@/components/RoomControlPage'
import LoginPage from '@/components/LoginPage'
import RegisterPage from '@/components/RegisterPage'
import TitlePage from '@/components/TitlePage'
import RegDevicesPage from '@/components/RegDevicesPage'

import store from '@/store'

Vue.use(Router)

let router = new Router({
  routes: [{
      path: '*',
      redirect: {
        name: 'Home'
      }
    },
    {
      path: '/room/:id',
      name: 'RoomControl',
      component: RoomControlPage,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/editroom/:id',
      name: 'EditRoom',
      component: EditRoomPage,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/newroom',
      name: 'NewRoom',
      component: EditRoomPage,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/home',
      name: 'Home',
      component: RoomsPage,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/newdevices',
      name: 'RegDevices',
      component: RegDevicesPage,
      meta: {
        requiresAuth: true
      }
    },
    // {
    //   path: '/',
    //   name: 'Title',
    //   component: TitlePage,
    //   meta: {}
    // },
    {
      path: '/login',
      name: 'Login',
      component: LoginPage,
      meta: {
        hideForAuth: true
      }
    },
    {
      path: '/register',
      name: 'Register',
      component: RegisterPage,
      meta: {
        hideForAuth: true
      }
    },
  ]
})

router.beforeEach((to, from, next) => {
  const {
    requiresAuth,
    hideForAuth
  } = to.meta;

  if (requiresAuth) {
    if (!store.getters["auth/isAuthenticated"]) {
      return next({
        name: "Login",
        // Move where we go after success login
        query: {
          returnUrl: to.path
        }
      })
    }
  }

  if (hideForAuth) {
    if (store.getters["auth/isAuthenticated"]) {
      return next({
        name: "Home"
      });
    }
  }

  next()

})

export default router;
