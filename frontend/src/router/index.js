import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Callback from '../views/Callback.vue'
import Demo from '../views/Demo.vue'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: Login
        },
        {
            path: '/demo',
            query: true,
            component: Demo
        },
        {
            path: '/login',
            query: true,
            component: Login
        },
        {
            path: '/callback/:login_type',
            query: true,
            component: Callback
        },
    ]
})

export default router
