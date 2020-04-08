import Api from '@/services/Api'

export default {
    getRooms (params) {
        return Api().get('/rooms')
    },
    getLights (params) {
        let url = "/room/" + params.place_id + "/lights"
        return Api().get(url)
    },
    getPowers (params) {
        let url = "/room/" + params.place_id + "/powers"
        return Api().get(url)
    }
}
