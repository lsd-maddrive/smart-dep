// initial state
const state = {
  units: [{
      enabled: true,
      id: "0"
    },
    {
      enabled: true,
      id: "1"
    }
  ]
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
  setState({
    commit
  }, payload) {
    commit('setState', payload)
  }
}

// mutations
const mutations = {
  setState: (state, payload) => {
    let unit = state.units.find(unit => unit.id == payload.id)
    unit.enabled = payload.state
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
