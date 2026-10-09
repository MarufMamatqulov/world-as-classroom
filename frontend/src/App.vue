<template>
  <div class="min-h-screen flex flex-col bg-slate-950 text-slate-100 selection:bg-emerald-500 selection:text-white">
    <!-- Main Top Navbar -->
    <Navbar />

    <!-- Routed View -->
    <main class="flex-1 pb-16 md:pb-6">
      <router-view />
    </main>

    <!-- Global Footer -->
    <footer class="border-t border-slate-900 bg-slate-950/80 py-8 px-4 text-center text-xs text-slate-500 hidden md:block">
      <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
          <span class="font-semibold text-slate-400">World as a Classroom (Olam Sinfxonasi)</span>
          <span>v1.0.0</span>
        </div>
        <div class="flex items-center gap-4 text-slate-400">
          <span>🇺🇿 O'zbekcha</span>
          <span>•</span>
          <span>🇬🇧 English</span>
          <span>•</span>
          <span>🇷🇺 Русский</span>
        </div>
        <div>
          <span>Powered by Google Gemini Multimodal AI</span>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import Navbar from '@/components/Navbar.vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

onMounted(async () => {
  await authStore.initAuth()
})
</script>
