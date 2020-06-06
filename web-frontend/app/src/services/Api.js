import axios from 'axios'

console.log("Api URL: " + process.env.API_URL)

export default () => {
  // Create each call =(
  return axios.create({
    baseURL: process.env.API_URL + '/api/v1',
    withCredentials: false,
    // headers: {
      // 'Accept': 'application/json',
      // 'Content-Type': 'application/json',
    // }
  })
}
