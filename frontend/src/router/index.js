import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/Login.vue'
import DataProcessing from '../views/DataProcessing.vue'
import Profile from '../views/Profile.vue'
import Video from '../views/Video.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Login',
    component: Login
  },
  {
    path: '/DataProcessing',
    name: 'DataProcessing',
    component: DataProcessing
  },
  {
    path: '/Profile',
    name: 'Profile',
    component: Profile
  },
  {
    path: '/Video',
    name: 'Video',
    component: Video
  },
  // {
  //   path: '/about',
  //   name: 'About',
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () => import(/* webpackChunkName: "about" */ '../views/About.vue')
  // }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
