import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: '首页',
      component: HomeView
    },
    {
      path: '/about',
      name: '关于',
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/login',
      name: '登录',
      component: () => import('../views/LoginView.vue')
    },
    {
      path: '/register',
      name: '注册',
      component: () => import('../views/RegisterView.vue')
    },
    {
      path: '/dashboard',
      name: '控制面板',
      component: () => import('../views/DashboardView.vue'),
      meta: { requiresAuth: true }
    }
  ]
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router
