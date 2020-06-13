const timeout = 400;

function generateEnvironData() {
  var i;
  let data = []
  let count = 20;
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

  return data;
}

const environData = generateEnvironData()

const services = {
  getPlaces() {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        const data = [{
            id: '1',
            num: '8201',
            name: 'KEMZ',
          },
          {
            id: '2',
            num: '8203',
            name: 'ELESI'
          },
          {
            id: '3',
            num: '8103',
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
          type: "env",
          name: "v",
          place: place.id
        }]

        resolve({
          data: data
        });
      }, timeout);
    });
  },
  getNewDevices() {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        const data = [{
          id: "11:11:11",
          ip_addr: "1.1.1.1",
          reg_ts: "1592044151",
        }, {
          id: "22:22:22",
          ip_addr: "1.1.1.2",
          reg_ts: "1592044150",
        }, {
          id: "333:333:333",
          ip_addr: "1.1.1.3",
          reg_ts: "1592044152",
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

  getDevicesLastStates(place) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        const data = [{
            id: 'lght0',
            name: 'Освещение доски',
            type: 'light',
            state: {
              enabled: true
            },
          },
          {
            id: 'lght1',
            name: 'Освещение стола',
            type: 'light',
            state: {
              enabled: false
            },
          },
          {
            id: 'pwr0',
            name: 'Принтер',
            type: 'power',
            state: {
              enabled: false
            },
          },
          {
            id: 'pwr1',
            name: 'Компьютер',
            type: 'power',
            state: {
              enabled: true
            },
          },
          {
            id: 'env1',
            type: 'env',
            state: {
              temperature: 25,
              lightness: 93,
              humidity: 39
            }
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
        resolve({
          data: environData
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
