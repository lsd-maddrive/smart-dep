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
    commit('registerRequest', user);
    return new Promise((resolve, reject) => { // The Promise used for router redirect in login
    Services.register(user)
      .then(
        user => {
          commit('registerSuccess', user);
          router.push('/login');
          // setTimeout(() => {
            // display success message after route change completes
            // dispatch('alert/success', 'Registration successful', {
            //   root: true
            // });
          // })
          resolve()
        },
        error => {
          commit('registerFailure', error);
          // dispatch('alert/error', error, {
          //   root: true
          // });
          reject()
        }
      );
    });
  },
  login: ({
    commit,
    dispatch
  }, user) => {
    return new Promise((resolve, reject) => { // The Promise used for router redirect in login
      commit("auth_request")
      Services.login(user)
        .then(resp => {
          const token = resp.data.token
          commit("auth_success", token)
          dispatch("after_login")
          resolve(resp)
        }, err => {
          console.log('Failed login request')
          if (!Services.isDebug()) {
            commit("auth_error", err)
            reject(err)
          } else {
            console.warn(">>> Set test token")
            const token = Services.getSampleToken()
            commit("auth_success", token)
            dispatch("after_login")
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
      console.log('Setup token for axios')
      axios.defaults.headers.common['Authorization'] = 'Bearer ' + state.token
    }
  }
}

// mutations
const mutations = {
  auth_request: (state) => {
    state.status = {
      loggingIn: true
    };
  },
  auth_success: (state, token) => {
    state.status = {
      loggedIn: true
    };
    state.token = token
    localStorage.setItem('user-token', token)
  },
  auth_error: (state) => {
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
  registerRequest(state, user) {
    state.status = {
      registering: true
    };
  },
  registerSuccess(state, user) {
    state.status = {};
  },
  registerFailure(state, error) {
    state.status = {};
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
