import Api from '@/services/Api'

export default {
    getRooms (params) {
        return Api().get('/rooms')
    },
    getLights (params) {
        return Api().get('/lights')
    }
}
