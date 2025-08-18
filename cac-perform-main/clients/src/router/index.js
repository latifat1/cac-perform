import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import NewClient from '../views/NewClient.vue'
import NewMission from '../views/NewMission.vue'
import GroupingAnalyse from '../views/GroupingAnalyse.vue'
import LoginView from '@/views/LoginView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/connexion',
      name: 'login',
      component: LoginView
    },
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/client/:clientId',
      name: 'clientSpace',
      component: () => import('../views/ClientSpace.vue'),
      props: true
    },
    {
      path: '/newClient',
      name: 'newClient',
      component: NewClient
    },
    {
      path: '/newMission/:clientId',
      name: 'newMission',
      component: NewMission,
      props: true
    },
    {
      path: '/grouping-analyse/:missionId',
      name: 'groupingAnalyse',
      component: GroupingAnalyse,
      props: true
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    }
  ]
})

export default router
