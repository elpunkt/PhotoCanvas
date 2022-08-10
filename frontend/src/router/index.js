import { createRouter, createWebHistory } from 'vue-router'
import LoggedInRoute from '@/views/main/protected/RouteGuard'
import AdminRoute from '@/views/main/admin/RouteGuard'
import Login from '../views/Login.vue'

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
    redirect: 'admin/photos/list',
    component: AdminRoute,
    children: [
      {
        name: 'Photo List',
        path: 'photos/list',
        component: () => import(/* webpackChunkName: "admin/allPhotos" */ '../views/main/admin/photos/List.vue')
      },
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
      }
    ]
  },
  {
    path: '/',
    name: 'Home',
    redirect: '/protected/slideshow'
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
