<template>
  <header class="sticky top-0 z-50 glass-panel border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-xl">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Brand Logo -->
        <router-link to="/" class="flex items-center gap-3 group">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 via-teal-500 to-cyan-500 p-[2px] shadow-lg shadow-emerald-500/20 group-hover:scale-105 transition-transform duration-300">
            <div class="w-full h-full bg-slate-950 rounded-[10px] flex items-center justify-center">
              <SparklesIcon class="w-5 h-5 text-emerald-400 animate-pulse-subtle" />
            </div>
          </div>
          <div>
            <span class="text-lg font-bold tracking-tight bg-gradient-to-r from-white via-slate-100 to-emerald-300 bg-clip-text text-transparent">
              {{ t.appName }}
            </span>
            <span class="hidden sm:block text-[11px] font-medium text-slate-400">
              {{ t.appTagline }}
            </span>
          </div>
        </router-link>

        <!-- Desktop Navigation Links -->
        <nav class="hidden md:flex items-center gap-1 bg-slate-900/60 p-1.5 rounded-full border border-slate-800/60">
          <router-link
            to="/scanner"
            class="flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-all duration-200"
            :class="$route.path === '/scanner' ? 'bg-emerald-500 text-slate-950 font-semibold shadow-md shadow-emerald-500/25' : 'text-slate-300 hover:text-white hover:bg-slate-800/50'"
          >
            <CameraIcon class="w-4 h-4" />
            <span>{{ t.nav.scanner }}</span>
          </router-link>

          <router-link
            to="/dashboard"
            class="flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-all duration-200"
            :class="$route.path === '/dashboard' ? 'bg-emerald-500 text-slate-950 font-semibold shadow-md shadow-emerald-500/25' : 'text-slate-300 hover:text-white hover:bg-slate-800/50'"
          >
            <LayoutDashboardIcon class="w-4 h-4" />
            <span>{{ t.nav.dashboard }}</span>
          </router-link>

          <router-link
            to="/settings"
            class="flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-all duration-200"
            :class="$route.path === '/settings' ? 'bg-emerald-500 text-slate-950 font-semibold shadow-md shadow-emerald-500/25' : 'text-slate-300 hover:text-white hover:bg-slate-800/50'"
          >
            <SettingsIcon class="w-4 h-4" />
            <span>{{ t.nav.settings }}</span>
          </router-link>
        </nav>

        <!-- Right Side: Language & Auth -->
        <div class="flex items-center gap-3">
          <!-- Language Switcher -->
          <div class="relative">
            <button
              @click="langMenuOpen = !langMenuOpen"
              class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900 border border-slate-800 text-slate-300 hover:text-white hover:border-slate-700 text-xs font-semibold tracking-wider transition-colors"
              title="Change Language"
            >
              <GlobeIcon class="w-3.5 h-3.5 text-emerald-400" />
              <span>{{ langLabel(lang) }}</span>
              <ChevronDownIcon class="w-3.5 h-3.5 text-slate-400" />
            </button>

            <!-- Language Dropdown -->
            <div
              v-if="langMenuOpen"
              @click="langMenuOpen = false"
              class="absolute right-0 mt-2 w-36 rounded-xl glass-panel bg-slate-900/95 border border-slate-800 shadow-xl py-1 z-50 backdrop-blur-md"
            >
              <button
                @click="setLanguage('uz')"
                class="w-full text-left px-3.5 py-2 text-xs font-medium flex items-center justify-between hover:bg-emerald-500/10 hover:text-emerald-400 transition-colors"
                :class="lang === 'uz' ? 'text-emerald-400 font-bold' : 'text-slate-300'"
              >
                <span>🇺🇿 O'zbekcha</span>
                <CheckIcon v-if="lang === 'uz'" class="w-3.5 h-3.5 text-emerald-400" />
              </button>
              <button
                @click="setLanguage('en')"
                class="w-full text-left px-3.5 py-2 text-xs font-medium flex items-center justify-between hover:bg-emerald-500/10 hover:text-emerald-400 transition-colors"
                :class="lang === 'en' ? 'text-emerald-400 font-bold' : 'text-slate-300'"
              >
                <span>🇬🇧 English</span>
                <CheckIcon v-if="lang === 'en'" class="w-3.5 h-3.5 text-emerald-400" />
              </button>
              <button
                @click="setLanguage('ru')"
                class="w-full text-left px-3.5 py-2 text-xs font-medium flex items-center justify-between hover:bg-emerald-500/10 hover:text-emerald-400 transition-colors"
                :class="lang === 'ru' ? 'text-emerald-400 font-bold' : 'text-slate-300'"
              >
                <span>🇷🇺 Русский</span>
                <CheckIcon v-if="lang === 'ru'" class="w-3.5 h-3.5 text-emerald-400" />
              </button>
            </div>
          </div>

          <!-- User Authentication / Profile -->
          <div v-if="authStore.isAuthenticated" class="flex items-center gap-2">
            <router-link
              to="/settings"
              class="flex items-center gap-2 pl-2 pr-3 py-1.5 rounded-full bg-slate-900/80 border border-slate-800 hover:border-emerald-500/50 text-xs text-slate-200 transition-all"
            >
              <div class="w-6 h-6 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold text-[10px]">
                {{ authStore.user?.full_name?.charAt(0).toUpperCase() || 'U' }}
              </div>
              <span class="max-w-[100px] truncate font-medium">{{ authStore.user?.full_name }}</span>
            </router-link>
            <button
              @click="authStore.logout()"
              class="p-2 rounded-lg text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 transition-colors"
              :title="t.nav.logout"
            >
              <LogOutIcon class="w-4 h-4" />
            </button>
          </div>
          <div v-else class="flex items-center gap-2">
            <router-link
              to="/login"
              class="px-3.5 py-1.5 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-slate-950 text-xs font-bold transition-all shadow-sm shadow-emerald-500/20"
            >
              {{ t.nav.login }}
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Mobile Bottom Navigation Bar -->
    <div class="md:hidden fixed bottom-0 left-0 right-0 z-50 glass-panel bg-slate-950/95 border-t border-slate-800/80 px-6 py-2 flex items-center justify-around">
      <router-link
        to="/scanner"
        class="flex flex-col items-center gap-1 text-[11px] font-medium"
        :class="$route.path === '/scanner' ? 'text-emerald-400' : 'text-slate-400'"
      >
        <CameraIcon class="w-5 h-5" />
        <span>{{ t.nav.scanner }}</span>
      </router-link>

      <router-link
        to="/dashboard"
        class="flex flex-col items-center gap-1 text-[11px] font-medium"
        :class="$route.path === '/dashboard' ? 'text-emerald-400' : 'text-slate-400'"
      >
        <LayoutDashboardIcon class="w-5 h-5" />
        <span>{{ t.nav.dashboard }}</span>
      </router-link>

      <router-link
        to="/settings"
        class="flex flex-col items-center gap-1 text-[11px] font-medium"
        :class="$route.path === '/settings' ? 'text-emerald-400' : 'text-slate-400'"
      >
        <SettingsIcon class="w-5 h-5" />
        <span>{{ t.nav.settings }}</span>
      </router-link>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from '@/i18n'
import { useAuthStore } from '@/stores/auth'
import {
  Sparkles as SparklesIcon,
  Camera as CameraIcon,
  LayoutDashboard as LayoutDashboardIcon,
  Settings as SettingsIcon,
  Globe as GlobeIcon,
  ChevronDown as ChevronDownIcon,
  Check as CheckIcon,
  LogOut as LogOutIcon
} from '@lucide/vue'

const { lang, t, setLanguage } = useI18n()
const authStore = useAuthStore()
const langMenuOpen = ref(false)

const langLabel = (code: string) => {
  if (code === 'uz') return 'UZ'
  if (code === 'en') return 'EN'
  if (code === 'ru') return 'RU'
  return code.toUpperCase()
}
</script>
