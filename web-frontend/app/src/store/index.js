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
    places: [],
    currentPlaceId: null
  },
  modules: {
    light,
    power,
    environ
  },
  getters: {
    currentPlace: (state, getters) => {
      return state.places.find(
        place => place.id == state.currentPlaceId
      );
    }
  },
  actions: {
    async syncPlaces({ commit }) {
      try {
        let response = await Services.getPlaces()
        console.log(response)
        commit('setPlaces', response.data)
      } catch (error) {
        console.log("Failed to request places")
        console.log(error)
        commit('setPlaces', [
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
    },

    switchPlace({ commit, dispatch }, payload) {
      commit("setCurrentPlace", {
        place_id: payload.place_id
      });

      console.log("Update light units");
      dispatch("light/syncUnits");

      console.log("Update power units");
      dispatch("power/syncUnits");

      commit("environ/clearState");

      console.log('Send emit on "start_states"');
      this._vm.$socket.emit("start_states", {
        period: 3,
        place_id: payload.place_id
      });
    },

    socket_state({ commit, dispatch }, payload) {
      // console.log(payload)

      for (let unit of payload) {
        if (unit.type == "light") {
          dispatch('light/setExtState', unit)
        }
        else if (unit.type == "power") {
          dispatch('power/setExtState', unit)
        }
        else if (unit.type == "env") {
          commit('environ/setExtState', unit)
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

    setPlaces(state, places) {
      state.places = places
    },

    setCurrentPlace(state, payload) {
      state.currentPlaceId = payload.place_id
    }
  },

  strict: debug,
  plugins: []
})
