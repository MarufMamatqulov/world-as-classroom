<template>
  <div class="min-h-[80vh] flex items-center justify-center px-4 py-12">
    <div class="w-full max-w-md glass-panel rounded-3xl p-6 sm:p-8 border border-slate-800 bg-slate-900/90 shadow-2xl relative overflow-hidden">
      <!-- Glow accent -->
      <div class="absolute -top-24 -right-24 w-60 h-60 bg-emerald-500/15 rounded-full blur-3xl pointer-events-none"></div>

      <!-- Header Tabs: Login vs Register -->
      <div class="flex p-1 rounded-2xl bg-slate-950 border border-slate-800 mb-6">
        <button
          type="button"
          @click="isRegister = false; errorMsg = ''"
          class="flex-1 py-2.5 rounded-xl font-bold text-xs sm:text-sm transition-all"
          :class="!isRegister ? 'bg-emerald-500 text-slate-950 shadow-md' : 'text-slate-400 hover:text-white'"
        >
          {{ t.auth.loginTitle }}
        </button>
        <button
          type="button"
          @click="isRegister = true; errorMsg = ''"
          class="flex-1 py-2.5 rounded-xl font-bold text-xs sm:text-sm transition-all"
          :class="isRegister ? 'bg-emerald-500 text-slate-950 shadow-md' : 'text-slate-400 hover:text-white'"
        >
          {{ t.auth.registerTitle }}
        </button>
      </div>

      <!-- Error alert -->
      <div
        v-if="errorMsg"
        class="mb-5 p-3 rounded-xl bg-rose-500/20 border border-rose-500/40 text-rose-300 text-xs font-semibold"
      >
        {{ errorMsg }}
      </div>

      <!-- Auth Form -->
      <form @submit.prevent="handleSubmit()" class="space-y-4">
        <!-- Full Name (Register only) -->
        <div v-if="isRegister">
          <label class="block text-xs font-bold text-slate-300 mb-1.5">
            {{ t.auth.fullNameLabel }}
          </label>
          <input
            v-model="fullName"
            type="text"
            required
            placeholder="Ali Valiyev"
            class="w-full bg-slate-950 border border-slate-800 focus:border-emerald-500 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none transition-colors"
          />
        </div>

        <!-- Email -->
        <div>
          <label class="block text-xs font-bold text-slate-300 mb-1.5">
            {{ t.auth.emailLabel }}
          </label>
          <input
            v-model="email"
            type="email"
            required
            placeholder="talaba@maktab.uz"
            class="w-full bg-slate-950 border border-slate-800 focus:border-emerald-500 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none transition-colors"
          />
        </div>

        <!-- Password -->
        <div>
          <label class="block text-xs font-bold text-slate-300 mb-1.5">
            {{ t.auth.passwordLabel }}
          </label>
          <input
            v-model="password"
            type="password"
            required
            minlength="6"
            placeholder="••••••••"
            class="w-full bg-slate-950 border border-slate-800 focus:border-emerald-500 rounded-xl px-4 py-2.5 text-sm text-slate-100 focus:outline-none transition-colors"
          />
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          :disabled="isLoading"
          class="w-full mt-2 py-3.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-bold text-sm sm:text-base flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/25 active:scale-[0.99] transition-all disabled:opacity-50"
        >
          <Loader2Icon v-if="isLoading" class="w-5 h-5 animate-spin" />
          <span v-else>{{ isRegister ? t.auth.registerBtn : t.auth.loginBtn }}</span>
        </button>
      </form>

      <!-- Continue as Guest -->
      <div class="mt-6 pt-5 border-t border-slate-800 text-center">
        <button
          type="button"
          @click="continueAsGuest()"
          class="text-xs text-slate-400 hover:text-emerald-400 font-semibold transition-colors"
        >
          {{ t.auth.guestContinue }} →
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from '@/i18n'
import { useAuthStore } from '@/stores/auth'
import { Loader2 as Loader2Icon } from '@lucide/vue'

const { t, lang } = useI18n()
const router = useRouter()
const authStore = useAuthStore()

const isRegister = ref(false)
const email = ref('')
const password = ref('')
const fullName = ref('')
const errorMsg = ref('')
const isLoading = ref(false)

const handleSubmit = async () => {
  isLoading.value = true
  errorMsg.value = ''
  try {
    if (isRegister.value) {
      await authStore.register({
        email: email.value,
        password: password.value,
        full_name: fullName.value,
        preferred_language: lang.value
      })
    } else {
      await authStore.login({
        email: email.value,
        password: password.value
      })
    }
    router.push({ name: 'Scanner' })
  } catch (err: any) {
    errorMsg.value = err.message || 'Xatolik yuz berdi. Qaytadan urinib ko\'ring.'
  } finally {
    isLoading.value = false
  }
}

const continueAsGuest = () => {
  router.push({ name: 'Scanner' })
}
</script>
