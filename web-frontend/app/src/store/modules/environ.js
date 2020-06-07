import Services from "@/services/Services";

// initial state
const state = {
  data: [],
  dataLimit: 20
}

// getters
const getters = {
  tempVal(state, getters, rootState) {
    let item = state.data[state.data.length - 1]
    if (item === undefined)
      return 0
    return item.temp
  },
  humidVal(state, getters, rootState) {
    let item = state.data[state.data.length - 1]
    if (item === undefined)
      return 0
    return item.humid
  },
  lightVal(state, getters, rootState) {
    let item = state.data[state.data.length - 1]
    if (item === undefined)
      return 0
    return item.light
  },
  times: (state, getters, rootState) => {
    // Looks like it requires in [ms]
    return state.data.map(pnt => pnt.ts * 1000)
  },
  temps: (state) => {
    return state.data.map(pnt => pnt.temp)
  },
  humids: (state) => {
    return state.data.map(pnt => pnt.humid)
  }
}

// actions
const actions = {
  syncData({
    state,
    commit,
    rootState
  }, data) {
    commit('clearState')
    const placeId = data.placeId

    return new Promise((resolve, reject) => {
      Services.getEnvironmentStates({
        place_id: placeId,
        count: state.dataLimit
      }).then(
        response => {
          for (let data of response.data) {
            commit('setExtState', data)
          }
          resolve()
        },
        error => {
          console.log("Failed to request environment data: " + error)
          reject(error)
        }
      )
    })
  },
}

// mutations
const mutations = {
  clearState: (state) => {
    state.data = [];
  },

  setExtState: (state, payload) => {
    // console.log('New env data:')
    // console.log(payload)
    // console.log(state.data)
    state.data.push({
      temp: payload.state.temperature,
      humid: payload.state.humidity,
      light: payload.state.lightness,
      ts: payload.ts
    });

    if (state.data.length > state.dataLimit) {
      state.data.shift()
    }
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
