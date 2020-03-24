// initial state
const state = {
  data: {
    temp: 36.6,
    humid: 40
  }
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
