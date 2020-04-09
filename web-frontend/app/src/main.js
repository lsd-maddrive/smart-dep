// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'

Vue.config.productionTip = false
Vue.config.ignoredElements = [/^ion-/]

import {
  BootstrapVue,
  IconsPlugin
} from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

import VueSocketIO from 'vue-socket.io';
Vue.use(VueSocketIO, process.env.API_URL, store)

import VueSocketIOExt from 'vue-socket.io-extended';
import io from 'socket.io-client';
const socket = io(process.env.API_URL);
Vue.use(VueSocketIOExt, socket, { store });

import App from './App'
import store from './store'
import router from './router'

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: {
    App
  },
  template: '<App/>'
})
