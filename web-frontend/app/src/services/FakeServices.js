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
          }
        ]
        resolve({data: data});
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
        resolve({data: data});
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
        resolve({data: data});
      }, timeout);
    });
  },

  login(user) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
          const data = {
              token: "dakfemvevm;adeoafpemfs21412fwqf23f3q"
            };
          resolve({data: data});
        }, timeout);
      });
  },

  register(user) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
          const data = {
              token: "dakfemvevm;adeoafpemfs21412fwqf23f3q"
            };
          resolve({data: data});
        }, timeout);
      });
  },

  sendCommand(params) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
          const data = {
              msg: "Ok"
            };
          resolve({data: data});
        }, timeout);
      });
  },

  isDebug() {
    return process.env.NODE_ENV !== 'production'
  },
}

export default services
