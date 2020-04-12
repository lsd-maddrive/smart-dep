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
    // Looks like it keep in [ms]
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
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
