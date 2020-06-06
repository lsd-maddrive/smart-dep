// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'

Vue.config.productionTip = false
Vue.config.ignoredElements = [/^ion-/]

import BootstrapVue from 'bootstrap-vue'
Vue.use(BootstrapVue)
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import App from './App'
import store from './store'
import router from './router'

const debug = process.env.NODE_ENV !== 'production'

import VueSocketIOExt from 'vue-socket.io-extended';
import io from 'socket.io-client';
const socket = io(process.env.API_URL, {autoConnect: !debug});
Vue.use(VueSocketIOExt, socket, {
  store
});


import Toasted from 'vue-toasted';
Vue.use(Toasted, {
  position: 'top-right',
  duration: 5000,
  keepOnHover: true,
  iconPack : 'material'
})

import VeeValidate, { Validator } from 'vee-validate';
import ru from 'vee-validate/dist/locale/ru';

Validator.localize('ru', ru);
Vue.use(VeeValidate, {
  locale: 'ru',
});

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: {
    App
  },
  template: '<App/>',
	beforeCreate() {
		this.$store.dispatch('auth/after_login')
	}
})
