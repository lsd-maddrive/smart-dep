import Api from '@/services/Api'

const api = Api();

export default {

  getPlaces() {
    // return axios.get('/api/v1/place', { params: {} })
    return api.get('/place')
  },
  getLights(params) {
    let url = "/place/" + params.place_id + "/lights"
    return api.get(url)
  },
  getPowers(params) {
    let url = "/place/" + params.place_id + "/powers"
    return api.get(url)
  },
  login(user) {
    let url = "/login"
    return api.post(url, user)
  },
  register(user) {
    let url = "/register"
    return api.post(url, user)
  },

  sendCommand(params) {
    let url = "/cmd/" + params.place_id

    return api.post(url, params.data)
  },

  // Debug data
  getTestPlaces() {
    return [{
        id: '8201',
        name: 'KEMZ',
      },
      {
        id: '8203',
        name: 'ELESI'
      }
    ]
  },
  getSampleToken() {
      return "dakfemvevm;adeoafpemfs21412fwqf23f3q"
  },

  isDebug() {
    return process.env.NODE_ENV !== 'production'
  },
}
