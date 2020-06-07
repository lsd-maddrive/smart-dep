import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

import light from './modules/light'
import power from './modules/power'
import environ from './modules/environ'
import auth from './modules/auth'

import Services from "@/services/Services";

export default new Vuex.Store({
  state: {
    isConnected: false,
    places: [],
    currentPlaceId: null
  },
  modules: {
    light,
    power,
    environ,
    auth
  },
  getters: {
    currentPlace: (state, getters) => {
      return state.places.find(
        place => place.id == state.currentPlaceId
      );
    },
    places: (state) => {
      return state.places
    },
  },
  actions: {
    /**
     * Action to update places and receive last state
     * Return: new places list
     */
    syncPlaces({
      commit
    }) {
      return new Promise((resolve, reject) => {
        Services.getPlaces()
          .then(resp => {
            const places = resp.data
            commit('setPlaces', places)
            resolve(places)
          })
          .catch(err => {
            console.log("Failed to request places")
            reject(err)
          })
      })
    },
    /**
     * Action to validate if room is valid
     * Return: found during validation place object
     */
    validatePlace({
      commit,
      dispatch,
    }, data) {
      const placeId = data.placeId
      return new Promise((resolve, reject) => {
        // TODO - make sync optional (use cached version)
        dispatch("syncPlaces")
          .then((resp) => {
            const places = resp;
            const place = places.find(
              place => place.id == placeId
            )
            if (place === undefined) {
              reject("Not found in list")
            } else {
              console.log("Found: " + place.id)
              resolve(place)
            }
          }).catch((err) => {
            console.log("Failed to sync places: " + err)
            reject(err)
          })
      })
    },

    startSocketLink({}, data) {
      const placeId = data.placeId
      
      /**
       * Lazy connection
       */
      if (!this._vm.$socket.client.connected) {
        this._vm.$socket.client.connect()
      }

      this._vm.$socket.client.emit("start_states", {
        period: 1,
        placeId: placeId
      });
    },

    /**
     * Socket handler for input data
     */
    socket_state({
      commit,
      dispatch
    }, payload) {
      for (let unit of payload) {
        if (unit.type == "light") {
          dispatch('light/setExtState', unit)
        } else if (unit.type == "power") {
          dispatch('power/setExtState', unit)
        } else if (unit.type == "env") {
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

    setPlaces(state, places) {
      state.places = places
    },

    setCurrentPlace(state, placeId) {
      state.currentPlaceId = placeId
    }
  },

  strict: Services.isDebug(),
  plugins: []
})
