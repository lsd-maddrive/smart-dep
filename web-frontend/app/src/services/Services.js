import Api from '@/services/Api'
import fakeServices from '@/services/FakeServices'

const realServices = {
  createPlace(place) {
    return Api().post('/place', place)
  },
  getPlaces() {
    // return axios.get('/api/v1/place', { params: {} })
    return Api().get('/place')
  },
  updatePlace(place) {
    return Api().put('/place', place)
  },
  deletePlace(place) {
    return Api().delete('/place', { data: place })
  },

  sendPlaceImage(place, form) {
    return Api().post(`/place/${place.id}/image`, form, { headers: { 'Content-Type': 'multipart/form-data' } })
  },
  getPlaceImage(place) {
    return Api().get(`/place/${place.id}/image`)
  },
  getApiPrefix(place) {
    return `${process.env.API_URL}/api/v1`
  },

  getDeviceTypes() {
    return Api().get('/device/types')
  },
  getPlaceDevices(place) {
    return Api().get(`/device?place_id=${place.id}`)
  },
  getNewDevices() {
    return Api().get('/device/new')
  },
  createDevice(device) {
    // return Api().post('/device', device)
  },
  updateDevice(device) {
    return Api().put('/device', device)
  },
  resetDevice(device) {
    device.reset = true;
    return Api().delete('/device', { data: device })
  },
  deleteDevice(device) {
    device.reset = false;
    return Api().delete('/device', { data: device })
  },

  getDevicesLastStates(place) {
    // Seconds
    return Api().get(`/device/states/${place.id}`, { params: { duration_s: 5 * 60 } })
  },

  login(user) {
    return Api().post('/login', user)
  },
  register(user) {
    return Api().post('/register', user)
  },

  pingDevice(device) {
    return Api().post('/device/ping', device)
  },
  sendCommand(command) {
    return Api().post('/device/cmd', command)
  },

  isDebug() {
    return process.env.NODE_ENV !== 'production'
  },

  getIcons() {
    return [
      'mdi-home',
      'mdi-presentation-play',
      'mdi-desk',
      'mdi-printer',
      'mdi-desktop-tower-monitor'
    ]
  }
}

const isFake = process.env.FAKE_SERVICES ? process.env.FAKE_SERVICES : false && process.env.NODE_ENV !== 'production';

let services;

if (isFake) {
  services = Object.assign(realServices, fakeServices)
} else {
  services = realServices
}

export default services;
