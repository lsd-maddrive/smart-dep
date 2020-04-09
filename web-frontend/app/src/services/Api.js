import axios from 'axios'

console.log("Api:")
console.log(process.env.API_URL)

export default() => {
    return axios.create({
        baseURL: process.env.API_URL + '/api/v1',
        withCredentials: false,
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    })
}
