import Services from "@/services/Services";

// convertion functions
function extData2Internal(payload) {
  return {
    id: payload.device_id,
    enabled: payload.state.enabled
  }
}

function internal2ExtData(payload) {
  return {
    device_id: payload.id,
    place_id: payload.place_id,
    type: "light",
    ts: Math.round(new Date().getTime()/1000),
    cmd: {
      enable: payload.enabled
    }
  }
}

// initial state
const state = {
  units: []
}

// getters
const getters = {
  enabled: (state, getters, rootState) => (id) => {
    let unit = state.units.find(unit => unit.id == id)
    return unit.enabled
  }
}

// actions
const actions = {
  syncUnits({ state, commit, rootState }) {
    commit('clearStates')

    Services.getLights({
      place_id: rootState.currentPlaceId
    }).then(
      response => {
        for (let unit of response.data) {
          commit('setState', extData2Internal(unit))
        }
      },
      error => {
        console.log("Failed to request light units")
        console.log(error)
        // Debug light
        commit('setState', {
          id: 'sample_0',
          enabled: true
        })
      }
    )
  },

  setExtState: ({ commit }, payload) => {
    commit('setState', extData2Internal(payload))
  },

  setState({ state, commit, rootState }, payload) {
    commit('setState', payload)
    console.log(rootState)
    payload.place_id = rootState.currentPlace.id
    this._vm.$socket.emit('set_state', internal2ExtData(payload));
  }
}

// mutations
const mutations = {
  clearStates: (state) => {
    state.units = [];
  },

  setState: (state, payload) => {
    let unit = state.units.find(unit => unit.id == payload.id)
    if (unit === undefined) {
      state.units.push({
        id: payload.id,
        enabled: payload.enabled
      })
    } else {
      unit.enabled = payload.enabled
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
