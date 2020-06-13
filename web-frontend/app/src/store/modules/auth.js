import Services from "@/services/Services";
import axios from "axios"

// initial state
const state = {
  token: localStorage.getItem('user-token') || '',
  status: {},
}

// getters
const getters = {
  isAuthenticated: state => !!state.token,
}

// actions
const actions = {
  register({
    dispatch,
    commit
  }, user) {
    commit('authRequest', user);
    return new Promise((resolve, reject) => { // The Promise used for router redirect in login
      Services.register(user)
        .then(
          resp => {
            const token = resp.data.token
            commit("authSuccess", token)
            dispatch("after_login")
            resolve(resp)
          },
          err => {
            commit("authError", err)
            reject(err)
          }
        );
    });
  },
  login: ({
    commit,
    dispatch
  }, user) => {
    return new Promise((resolve, reject) => { // The Promise used for router redirect in login
      commit("authRequest")
      Services.login(user)
        .then(
          resp => {
            const token = resp.data.token
            commit("authSuccess", token)
            dispatch("after_login")
            resolve(resp)
          },
          err => {
            commit("authError", err)
            reject(err)
          })
    })
  },
  logout({
    commit
  }) {
    return new Promise((resolve, reject) => {
      commit('logout')
      resolve()
    })
  },
  after_login: ({
    state,
    commit,
    dispatch,
    getters
  }) => {
    if (getters.isAuthenticated) {
      console.log('Setup token for axios: ' + state.token)
      axios.defaults.headers.common['Authorization'] = 'Bearer ' + state.token
    }
  }
}

// mutations
const mutations = {
  authRequest: (state) => {
    state.status = {
      processing: true
    };
  },
  authSuccess: (state, token) => {
    state.status = {
      loggedIn: true
    };
    state.token = token
    localStorage.setItem('user-token', token)
  },
  authError: (state) => {
    state.status = {};
    localStorage.removeItem('user-token')
    delete axios.defaults.headers.common['Authorization']
  },
  logout(state) {
    state.status = {};
    state.token = ''
    localStorage.removeItem('user-token')
    delete axios.defaults.headers.common['Authorization']
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
