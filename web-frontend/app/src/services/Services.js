import Api from '@/services/Api'

export default {
    getRooms (params) {
        return Api().get('/rooms')
    },
    getLights (params) {
        let url = "/room/" + params.place_id + "/lights"
        return Api().get(url)
    }
}
