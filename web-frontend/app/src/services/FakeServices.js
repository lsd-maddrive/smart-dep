const timeout = 400;
const services = {
  getPlaces() {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        const data = [{
            id: '8201',
            name: 'KEMZ',
          },
          {
            id: '8203',
            name: 'ELESI'
          },
          {
            id: '8103',
            name: 'FirstFloor'
          }
        ]
        resolve({
          data: data
        });
      }, timeout);
    });
  },

  createPlace(place) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        resolve({
          data: place
        });
      }, timeout);
    });
  },
  deletePlace(place) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        resolve({
          data: place
        });
      }, timeout);
    });
  },
  updatePlace(place) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        resolve({
          data: place
        });
      }, timeout);
    });
  },

  getPlaceDevices(place) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        const data = [{
          id: "11:11:11",
          type: "light",
          name: "a",
          place: place.id
        }, {
          id: "22:22:22",
          type: "power",
          name: "b",
          place: place.id
        }, {
          id: "333:333:333",
          type: "environ",
          name: "v",
          place: place.id
        }]

        resolve({
          data: data
        });
      }, timeout);
    });
  },

  createDevice(device) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        resolve({
          data: device
        });
      }, timeout);
    });
  },
  updateDevice(device) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        resolve({
          data: device
        });
      }, timeout);
    });
  },
  deleteDevice(device) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        resolve({
          data: device
        });
      }, timeout);
    });
  },


  getLights(params) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        const data = [{
            device_id: 'lght0',
            state: {
              enabled: true
            },
          },
          {
            device_id: 'lght1',
            state: {
              enabled: false
            },
          }
        ]
        resolve({
          data: data
        });
      }, timeout);
    });
  },

  getPowers(params) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        const data = [{
            device_id: 'pwr0',
            state: {
              enabled: false
            },
          },
          {
            device_id: 'pwr1',
            state: {
              enabled: true
            },
          }
        ]
        resolve({
          data: data
        });
      }, timeout);
    });
  },

  getEnvironmentStates(params) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        var i;
        let data = []
        let count = 50;
        let state = {
          temperature: 25,
          lightness: 93,
          humidity: 39
        }
        for (i = 0; i < count; i++) {
          state.temperature += (Math.random() * 2 - 1) * 2;
          state.humidity += (Math.random() * 2 - 1) * 1;

          data.push({
            ts: (new Date().getTime() / 1000) - (50 - i),
            state: Object.assign({}, state)
          })
        };
        resolve({
          data: data
        });
      }, timeout);
    });
  },

  login(user) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        const data = {
          token: "dakfemvevm;adeoafpemfs21412fwqf23f3q",
          username: user.username,
          role: "Guest"
        };
        resolve({
          data: data
        });
      }, timeout);
    });
  },

  register(user) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        const data = {
          token: "dakfemvevm;adeoafpemfs21412fwqf23f3q",
          username: user.username,
          role: "Guest"
        };
        resolve({
          data: data
        });
      }, timeout);
    });
  },

  sendCommand(params) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        const data = {
          msg: "Ok"
        };
        resolve({
          data: data
        });
      }, timeout);
    });
  },

  isDebug() {
    return process.env.NODE_ENV !== 'production'
  },
}

export default services
