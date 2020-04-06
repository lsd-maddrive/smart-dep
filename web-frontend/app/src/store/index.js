import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

import light from './modules/light'
import power from './modules/power'
import environ from './modules/environ'

const debug = process.env.NODE_ENV !== 'production'

import Services from "@/services/Services";

export default new Vuex.Store({
  state: {
    isConnected: false,
    isSidemenuOpen: false,
    rooms: []
  },
  modules: {
    light,
    power,
    environ
  },
  actions: {
    syncRooms({ commit }) {
      Services.getRooms().then(
        response => {
          commit('setRooms', response.data)
        },
        error => {
          console.log("Failed to request rooms")
          console.log(error)
          commit('setRooms', [
            {
              id: '8201',
              name: 'KEMZ',
            },
            {
              id: '8203',
              name: 'ELESI'
            }
          ])
        }
      )
    },

    socket_state({ commit }, payload) {
      console.log(payload)

      for (let unit of payload) {
        if (unit.type == "light") {
          commit('light/setState', {
            id: unit.device_id,
            enabled: unit.state.enabled
          })
        }
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

    toggleSidemenu(state) {
      state.isSidemenuOpen = !state.isSidemenuOpen
    },

    setRooms(state, rooms) {
      state.rooms = rooms
    }
  },

  strict: debug,
  plugins: []
})
