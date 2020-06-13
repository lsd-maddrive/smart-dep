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
    deviceTypes: []
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
        dev => dev.id == id
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
              console.log("Found: " + place.id)
              resolve(place)
            }
          }).catch((err) => {
            console.log("Failed to sync places: " + err)
            reject(err)
          })
      })
    },

    startSocketLink({state}) {
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

    /**
     * Socket handler for input data
     */
    socket_state({
      commit,
      dispatch
    }, payload) {
      dispatch("processInputStates", payload)
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
            dispatch("processInputStates", response.data)
            resolve()
          },
          error => {
            console.log("Failed to request light units: " + error)
            reject(error)
          }
        )
      })
    },

    processInputStates({
      commit,
      dispatch
    }, states) {
      for (let state of states) {
        if (['light', 'power'].indexOf(state.type) != -1) {
          commit('setDeviceState', state)
        } else if (state.type == "env") {
          commit('environ/setExtState', state)
        }
      }
    },

    commandState({
      state,
      commit,
      getters
    }, data) {

      const deviceState = Object.assign({}, getters.getDeviceById(data.id));
      // Append PlaceID to know where to send
      deviceState.place_id = state.currentPlaceId
      deviceState.cmd = {
        enabled: data.enabled
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
    }
  },

  mutations: {
    SOCKET_CONNECT(state) {
      state.isConnected = true;
      console.log("Socket connected")
    },

    SOCKET_DISCONNECT(state) {
      state.isConnected = false;
    },

    clearDeviceStates(state) {
      state.deviceStates = []
    },

    setDeviceState(state, deviceState) {
      let unit = state.deviceStates.find(dst => dst.id == deviceState.device_id)
      if (typeof unit === 'undefined') {
        state.deviceStates.push(deviceState)
      } else {
        unit.state = deviceState.state
      }
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
