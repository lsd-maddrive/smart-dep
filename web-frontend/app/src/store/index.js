import Vue from 'vue'
import Vuex from 'vuex'
import light from './modules/light'
import power from './modules/power'
import environ from './modules/environ'

Vue.use(Vuex)

const debug = process.env.NODE_ENV !== 'production'

export default new Vuex.Store({
  modules: {
    light,
    power,
    environ
  },
  strict: debug,
  plugins: []
})
