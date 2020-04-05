import Vue from 'vue'
import Router from 'vue-router'
import RoomsSelector from '@/components/RoomsSelector'
import RoomControl from '@/components/RoomControl'

Vue.use(Router)

export default new Router({
  routes: [{
      path: '/404',
      component: {
        template: '<p>Page Not Found</p>'
      },
    },
    {
      path: '*',
      redirect: '/404'
    },
    {
      path: '/room/:id',
      component: RoomControl
    },
    {
      path: '/',
      component: RoomsSelector
    },
  ]
})
