import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

import light from './modules/light'
import power from './modules/power'
import environ from './modules/environ'

const debug = process.env.NODE_ENV !== 'production'

export default new Vuex.Store({
  state: {
    isConnected: false
  },
  modules: {
    light,
    power,
    environ
  },
  actions: {
    // startStatesReceive({
    //   commit
    // }, payload) {

    // }

    socket_state({commit}, payload) {
      console.log(payload)

      if (payload.type == "light") {
        commit('light/setState', {
          id: payload.device_id,
          enabled: payload.state.enabled
        })
      }
    },
  },

  mutations: {
    SOCKET_CONNECT(state) {
      state.isConnected = true;
      console.log("Socket connected")
    },

    SOCKET_DISCONNECT(state) {
      state.isConnected = false;
    },
  },

  strict: debug,
  plugins: []
})
