import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    // Pages
    {
      path: '/',
      component: () => import('../views/Login.vue')
    },
    {
      path: '/Register',
      component: () => import('../views/register.vue')
    },
    {
      path: '/Learnmore',
      component: () => import('../views/Learnmore.vue')
    },
    {
      path: '/Service',
      component: () => import('../views/Service.vue')
    },
    {
      path: '/Main',
      component: () => import('../views/Main.vue'),
      children: [
        // Dashboard
        {
          path: '/Dashboard',
          component: () => import('../views/Dashboard.vue')
        },
        {
          path: '/OrphanResources',
          component: () => import('../views/Services/OrphanResources.vue')
        },
        {
          path: '/UnderutilizedResources',
          component: () => import('../views/Services/UnderutilizedResources.vue')
        },
        {
          path: '/AdvisorRecommendation',
          component: () => import('../views/Services/AdvisorRecommendation.vue')
        },
        {
          path: '/PublicResources',
          component: () => import('../views/Services/PublicResources.vue')
        },
        {
          path: '/UntaggedResources',
          component: () => import('../views/Services/UntaggedResources.vue')
        },
      ]
    }
  ]
})

export default router