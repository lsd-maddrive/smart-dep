// initial state
const state = {
  units: [{
      enabled: true,
      id: 0
    },
    {
      enabled: true,
      id: 1
    }
  ]
}

// getters
const getters = {}

// actions
const actions = {
  getAllProducts({
    commit
  }) {
    shop.getProducts(products => {
      commit('setProducts', products)
    })
  }
}

// mutations
const mutations = {
  setProducts(state, products) {
    state.all = products
  },

  decrementProductInventory(state, {
    id
  }) {
    const product = state.all.find(product => product.id === id)
    product.inventory--
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
