import { createRouter, createWebHistory } from 'vue-router'
import LoggedInRoute from '@/views/main/protected/RouteGuard'
import AdminRoute from '@/views/main/admin/RouteGuard'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/password-recovery',
    name: 'PasswordRecovery',
    component: () => import(/* webpackChunkName: "password-recovery" */ '@/views/PasswordRecovery.vue')
  },
  {
    path: '/admin',
    redirect: 'admin/users/list',
    component: AdminRoute,
    children: [
      {
        name: 'User List',
        path: 'users/list',
        component: () => import(/* webpackChunkName: "admin/allPhotos" */ '../views/main/admin/users/List.vue')
      },
      {
        name: 'Create User',
        path: 'users/create',
        component: () => import(/* webpackChunkName: "admin-usercreate" */ '@/views/main/admin/users/Create.vue')
      },
    ]
  },
  {
    path: '/protected',
    redirect: '/protected/slideshow',
    component: LoggedInRoute,
    children: [
      {
        name: 'Slideshow',
        path: '/protected/slideshow',
        component: () => import(/* webpackChunkName: "protected/Slideshow" */ '../views/main/protected/Slideshow.vue')
      },
      {
        name: 'Photo List',
        path: '/protected/photolist',
        component: () => import(/* webpackChunkName: "protected/Photo List" */ '../views/main/protected/PhotoList.vue')
      },
    ]
  },
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/upload',
    name: 'Photo Upload',
    component: () => import(/* webpackChunkName: "UploadPhoto" */ '../views/Upload.vue')
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
