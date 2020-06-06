import Api from '@/services/Api'
import fakeServices from '@/services/FakeServices'

const realServices = {
  getPlaces() {
    // return axios.get('/api/v1/place', { params: {} })
    return Api().get('/place')
  },
  getLights(params) {
    let url = "/place/" + params.place_id + "/lights"
    return Api().get(url)
  },
  getPowers(params) {
    let url = "/place/" + params.place_id + "/powers"
    return Api().get(url)
  },
  login(user) {
    let url = "/login"
    return Api().post(url, user)
  },
  register(user) {
    let url = "/register"
    return Api().post(url, user)
  },

  sendCommand(params) {
    let url = "/cmd/" + params.place_id

    return Api().post(url, params.data)
  },

  isDebug() {
    return process.env.NODE_ENV !== 'production'
  },
}

const isFake = process.env.FAKE_SERVICES ? process.env.FAKE_SERVICES : false && process.env.NODE_ENV !== 'production';

export default isFake ? fakeServices : realServices;
