import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import ScannerView from '@/views/ScannerView.vue'
import LessonView from '@/views/LessonView.vue'
import DashboardView from '@/views/DashboardView.vue'
import SettingsView from '@/views/SettingsView.vue'
import LoginView from '@/views/LoginView.vue'
import QuestsView from '@/views/QuestsView.vue'
import PassportView from '@/views/PassportView.vue'
import ScientistModeView from '@/views/ScientistModeView.vue'
import AnalyticsView from '@/views/AnalyticsView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView,
  },
  {
    path: '/scanner',
    name: 'Scanner',
    component: ScannerView,
  },
  {
    path: '/lesson/:id?',
    name: 'Lesson',
    component: LessonView,
  },
  {
    path: '/quests',
    name: 'Quests',
    component: QuestsView,
  },
  {
    path: '/passport',
    name: 'Passport',
    component: PassportView,
  },
  {
    path: '/scientist',
    name: 'Scientist',
    component: ScientistModeView,
  },
  {
    path: '/analytics',
    name: 'Analytics',
    component: AnalyticsView,
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
  },
  {
    path: '/settings',
    name: 'Settings',
    component: SettingsView,
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})

export default router
