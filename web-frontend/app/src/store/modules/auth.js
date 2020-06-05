import Services from "@/services/Services";
import axios from "axios"

// initial state
const state = {
  token: localStorage.getItem('user-token') || '',
  status: '',
}

// getters
const getters = {
  isAuthenticated: state => !!state.token,
  authStatus: state => state.status,
}

// actions
const actions = {
  login: ({
    commit,
    dispatch
  }, user) => {
    return new Promise((resolve, reject) => { // The Promise used for router redirect in login
      commit("auth_request")
      Services.loginRequest()
        .then(resp => {
          const token = resp.data.token
          commit("auth_success", token)
          commit('sync_token')
          resolve(resp)
        })
        .catch(err => {
          console.log('Failed login request')
          if (!Services.isDebug()) {
            commit("auth_error", err)
            commit('sync_token')
            reject(err)
          } else {
            console.warn(">>> Set test token")
            const token = Services.getSampleToken()
            commit("auth_success", token)
            commit('sync_token')
            resolve()
          }
        })
    })
  },
  logout({
    commit
  }) {
    return new Promise((resolve, reject) => {
      commit('logout')
      commit('sync_token')
      resolve()
    })
  },
}

// mutations
const mutations = {
  auth_request: (state) => {
    state.status = 'loading'
  },
  auth_success: (state, token) => {
    state.status = 'success'
    state.token = token
    localStorage.setItem('user-token', token)
  },
  auth_error: (state) => {
    state.status = 'error'
    localStorage.removeItem('user-token')
  },
  logout(state) {
    state.status = ''
    state.token = ''
    localStorage.removeItem('user-token')
  },
  sync_token(state) {
    if (!!state.token) {
      axios.defaults.headers.common['Authorization'] = 'Bearer ' + state.token
    } else {
      delete axios.defaults.headers.common['Authorization']
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
