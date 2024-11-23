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
import PasswordChange from '@/components/PasswordChange.vue'
import DepositDetail from '@/components/DepositDetail.vue'
import CreateArticle from '@/components/CreateArticle.vue'
import ArticleDetail from '@/components/ArticleDetail.vue'
import MyProduct from '@/components/MyProduct.vue'
import PersonalInfo from '@/components/PersonalInfo.vue'
import AiRecommendations from '@/components/AiRecommendations.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
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
      path: '/ai-recommendations',
      name: 'ai-recommendations',
      component: AiRecommendations
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
      component: UserInfo,
      children: [
        {
          path: '', // 기본 경로
          name: 'subscribed-products',
          component: MyProduct
        },
        {
          path: 'personal-info',
          name: 'personal-info',
          component: PersonalInfo
        },
      ],
    },
    {
      path: '/passwordchange',
      name: 'passwordchange',
      component: PasswordChange
    },
    {
      path: '/deposits',
      name: 'deposits',
      component: DepositsView,
    },
    {
      path: '/deposits/:deposit_code',
      name: 'depositdetail',
      component: DepositDetail
    },
    {
      path: '/create-article',
      name: 'createarticle',
      component: CreateArticle
    },
    {
      path: '/article/:article_id',
      name: 'articledetail',
      component: ArticleDetail
    },
  ],
})

export default router
