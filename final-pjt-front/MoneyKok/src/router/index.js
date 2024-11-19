import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import DepositsView from '@/views/DepositsView.vue'
import SavingsView from '@/views/SavingsView.vue'
import AiView from '@/views/AiView.vue'
import CommunityView from '@/views/CommunityView.vue'
import BankView from '@/views/BankView.vue'
import ExchangeRateView from '@/views/ExchangeRateView.vue'
import SignUp from '@/components/SignUp.vue'
import Login from '@/components/Login.vue'
import UserInfo from '@/components/UserInfo.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/deposits',
      name: 'deposits',
      component: DepositsView,
    },
    {
      path: '/savings',
      name: 'savings',
      component: SavingsView
    },
    {
      path: '/ai',
      name: 'ai',
      component: AiView
    },
    {
      path: '/community',
      name: 'community',
      component: CommunityView
    },
    {
      path: '/bank',
      name: 'bank',
      component: BankView
    },
    {
      path: '/exchangerate',
      name: 'exchangerate',
      component: ExchangeRateView
    },
    {
      path: '/signup',
      name: 'signup',
      component: SignUp
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/userinfo',
      name: 'userinfo',
      component: UserInfo
    },
  ],
})

export default router
