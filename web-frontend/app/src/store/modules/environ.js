import Services from "@/services/Services";

// initial state
const state = {
  data: new Map(),
  times: [],
  dataLimit: 20,
  deviceId: null
}

// getters
const getters = {
  tempVal(state, getters, rootState) {
    let ts = state.times[state.times.length - 1]
    if (ts === undefined)
      return 0
    return state.data.get(ts).temp
  },
  humidVal(state, getters, rootState) {
    let ts = state.times[state.times.length - 1]
    if (ts === undefined)
      return 0
    return state.data.get(ts).humid
  },
  lightVal(state, getters, rootState) {
    let ts = state.times[state.times.length - 1]
    if (ts === undefined)
      return 0
    return state.data.get(ts).light
  },
  times: (state, getters, rootState) => {
    // Looks like it requires in [ms]
    return state.times.map(t => t * 1000)
  },
  temps: (state) => {
    return state.times.map(t => state.data.get(t).temp)
  },
  humids: (state) => {
    return state.times.map(t => state.data.get(t).humid)
  }
}

// actions
const actions = {
}

// mutations
const mutations = {
  clear: (state) => {
    state.data.clear();
  },

  setExtState: (state, payload) => {
    if (payload.device_id != state.deviceId) {
      state.data.clear();
      state.times = [];
      state.deviceId = payload.device_id;
    }

    let ts = payload.ts;
    if (!state.data.has(ts)) {
      state.data.set(payload.ts, {
        temp: payload.state.temperature,
        humid: payload.state.humidity,
        light: payload.state.lightness,
      })
      state.times.push(ts);
    }

    if (state.times.length > state.dataLimit) {
      let rm_ts = state.times.shift();
      state.data.delete(rm_ts);
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
