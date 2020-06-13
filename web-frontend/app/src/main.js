// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'

Vue.config.productionTip = false
Vue.config.ignoredElements = [/^ion-/]

import vuetify from '@/plugins/vuetify' // path to vuetify export
import 'material-design-icons-iconfont/dist/material-design-icons.css'

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

import VuetifyToast from 'vuetify-toast-snackbar'
Vue.use(VuetifyToast, {
	x: 'right', // default
	y: 'bottom', // default
	color: 'info', // default
	icon: 'info',
	iconColor: '', // default
	classes: [
		'body-2'
	],
	timeout: 3000, // default
	dismissable: true, // default
	multiLine: false, // default
	vertical: false, // default
	queueable: false, // default
	showClose: false, // default
	closeText: '', // default
	closeIcon: 'close', // default
	closeColor: '', // default
	slot: [], //default
	shorts: {
		custom: {
			color: 'purple'
		}
	},
	property: '$toasted' // default
})

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  vuetify,
  components: {
    App
  },
  template: '<App/>',
	beforeCreate() {
		this.$store.dispatch('auth/after_login')
	}
})
