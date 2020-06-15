import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

import environ from './modules/environ'
import auth from './modules/auth'

import Services from "@/services/Services";

export default new Vuex.Store({
  state: {
    isConnected: false,
    places: [],
    currentPlaceId: null,
    deviceStates: [],
    deviceTypes: [],
    toasts: [],

  },
  modules: {
    environ,
    auth
  },
  getters: {
    currentPlace: (state, getters) => {
      return state.places.find(
        place => place.id == state.currentPlaceId
      );
    },
    getPlaceById: (state, getters) => (id) => {
      return state.places.find(
        place => place.id == id
      )
    },
    getDeviceById: (state, getters) => (id) => {
      return state.deviceStates.find(
        dev => dev.device_id == id
      )
    }
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
    syncDeviceTypes({
      commit
    }) {
      return new Promise((resolve, reject) => {
        Services.getDeviceTypes()
          .then(resp => {
            const types = resp.data
            commit('setDeviceTypes', types)
            resolve(types)
          })
          .catch(err => {
            console.log("Failed to request device types")
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
              resolve(place)
            }
          }).catch((err) => {
            console.log("Failed to sync places: " + err)
            reject(err)
          })
      })
    },

    startSocketLink({ state }) {
      const placeId = state.currentPlaceId

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

    stopSocketLink({ state }) {
      const placeId = state.currentPlaceId

      /**
       * Lazy connection
       */
      if (!this._vm.$socket.client.connected) {
        this._vm.$socket.client.connect()
      }

      this._vm.$socket.client.emit("stop_states", {
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
      for (let state of payload) {
        if (['light', 'power'].indexOf(state.type) != -1) {
          commit('setDeviceState', state)
        } else if (state.type == "env") {
          commit('environ/setExtState', state)
        }
      }
    },

    syncDeviceStates({
      commit,
      dispatch
    }, data) {
      commit('clearDeviceStates')
      const placeId = data.placeId

      return new Promise((resolve, reject) => {
        Services.getDevicesLastStates({
          id: placeId
        }).then(
          response => {
            for (let state of response.data) {
              if (['light', 'power'].indexOf(state.type) != -1) {
                commit('addDevice', state)
              } else if (state.type == "env") {
                commit('environ/setExtState', state)
              }
            }
            resolve()
          },
          error => {
            console.log("Failed to request light units: " + error)
            reject(error)
          }
        )
      })
    },

    commandState({
      state,
      commit,
      getters
    }, data) {

      const deviceState = Object.assign({}, getters.getDeviceById(data.id));
      // Append PlaceID to know where to send
      deviceState.place_id = parseInt(state.currentPlaceId, 10)
      deviceState.cmd = {
        enable: data.enabled
      }
      deviceState.ts = new Date().getTime() / 1000
      deviceState.source_id = 'browser'

      return new Promise((resolve, reject) => {
        Services.sendCommand(deviceState)
          .then(resp => {
            console.log(resp);
            resolve(resp)
          }, err => {
            console.log(err);
            reject(err)
          });
      })
    },

    toast({
      state,
      commit
    }, tinfo) {
      commit('addToast', tinfo)
    }
  },

  mutations: {
    SOCKET_CONNECT(state) {
      state.isConnected = true;
    },

    SOCKET_DISCONNECT(state) {
      state.isConnected = false;
    },

    clearDeviceStates(state) {
      state.deviceStates = []
    },

    addDevice(state, deviceState) {
      if (deviceState.type == "light") {
        deviceState.icon_name = 'mdi-lightbulb-on'
      } else if (deviceState.type == "power") {
        deviceState.icon_name = 'mdi-lightning-bolt'
      }

      state.deviceStates.push(deviceState)
    },
    setDeviceState(state, deviceState) {
      let unit = state.deviceStates.find(dst => dst.device_id == deviceState.device_id)
      if (typeof unit === 'undefined') {
      } else {
        unit.state = deviceState.state
      }
    },

    addToast(state, tinfo) {
      let def_toast = {
        showing: true,
        text: '',
        timeout: 3000,
        color: 'info'
      }

      var new_toast = Object.assign(def_toast, tinfo)

      state.toasts = state.toasts.concat(new_toast);
    },

    /**
     * Places mutations
     */
    clearPlaces(state) {
      state.places = []
    },

    setPlaces(state, places) {
      state.places = places
    },

    setDeviceTypes(state, types) {
      state.deviceTypes = types
    },

    enterPlace(state, placeId) {
      state.currentPlaceId = placeId
    },
    leavePlace(state) {
      state.currentPlaceId = null
    }
  },

  strict: Services.isDebug(),
  plugins: []
})
