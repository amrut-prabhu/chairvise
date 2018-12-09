import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Login from '@/components/Login'
import signUp from '@/components/Signup'
import history from '@/components/History'
import Result from '@/components/Result'
import MappingController from '@/components/MappingController'
//import TE from '@/components/Te'
//import firebase from 'firebase'
Vue.use(Router)

let router = new Router({
  routes: [{
      path: '/',
      name: 'Home',
      component: Home,
      props: true,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/login',
      name: 'Login',
      component: Login,
    },
    {
      path: '/signup',
      name: 'SignUp',
      component: signUp,
    },
    {
      path: '/history',
      name: 'History',
      component: history,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/result/:inputFileName',
      name: 'Result',
      component: Result,
      props: true,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '/mapping',
      name: 'MappingController',
      component: MappingController,
      props: true,
      meta: {
        requiresAuth: true
      }
    },
    {
      path: '*',
      redirect: '/',
    },
  ]
})

// Navigation guard, check if the route exists and requires authentication
router.beforeEach((to, from, next) => {
  let currentUser = localStorage.getItem('user');
  currentUser = currentUser ? JSON.parse(currentUser) : null;
  let requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  if (requiresAuth && !currentUser) next('/login')
  else if (currentUser && to.path === '/login') next('/')
  else next()
})

export default router
