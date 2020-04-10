import Api from '@/services/Api'

export default {
    getPlaces(params) {
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

    sendCommand(params) {
        let url = "/cmd/" + params.place_id
        let data = params.data

        const config = {
            headers: { 'content-type': 'application/json' }
        }

        return Api().post(url, data, config)
    }
}
