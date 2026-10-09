<template>
  <div class="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
    <!-- Header -->
    <div class="mb-8">
      <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-bold border border-emerald-500/20 mb-2">
        <SettingsIcon class="w-3.5 h-3.5" />
        <span>{{ t.nav.settings }}</span>
      </div>
      <h1 class="text-2xl sm:text-3xl font-extrabold text-white">
        {{ t.settings.title }}
      </h1>
      <p class="text-xs sm:text-sm text-slate-400 mt-1">
        {{ t.settings.subtitle }}
      </p>
    </div>

    <!-- Settings Form Card -->
    <div class="glass-panel rounded-3xl p-6 sm:p-8 border border-slate-800 bg-slate-900/90 shadow-2xl">
      <!-- Success Banner -->
      <div
        v-if="showSuccess"
        class="mb-6 p-4 rounded-xl bg-emerald-500/15 border border-emerald-500/40 text-emerald-300 text-xs sm:text-sm font-semibold flex items-center gap-2"
      >
        <CheckCircle2Icon class="w-5 h-5 text-emerald-400" />
        <span>{{ t.settings.savedAlert }}</span>
      </div>

      <form @submit.prevent="saveSettings()" class="space-y-6">
        <!-- Full Name -->
        <div>
          <label class="block text-xs sm:text-sm font-bold text-slate-200 mb-2">
            {{ t.settings.nameLabel }}
          </label>
          <input
            v-model="form.full_name"
            type="text"
            required
            class="w-full bg-slate-950 border border-slate-800 focus:border-emerald-500 rounded-xl px-4 py-3 text-sm text-slate-100 focus:outline-none transition-colors"
          />
        </div>

        <!-- Age & Grade Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-xs sm:text-sm font-bold text-slate-200 mb-2">
              {{ t.settings.ageLabel }}
            </label>
            <input
              v-model.number="form.age"
              type="number"
              min="6"
              max="99"
              class="w-full bg-slate-950 border border-slate-800 focus:border-emerald-500 rounded-xl px-4 py-3 text-sm text-slate-100 focus:outline-none transition-colors"
            />
          </div>

          <div>
            <label class="block text-xs sm:text-sm font-bold text-slate-200 mb-2">
              {{ t.settings.gradeLabel }}
            </label>
            <select
              v-model="form.grade"
              class="w-full bg-slate-950 border border-slate-800 focus:border-emerald-500 rounded-xl px-4 py-3 text-sm text-slate-100 focus:outline-none transition-colors"
            >
              <option value="4">4-sinf (Boshlang'ich)</option>
              <option value="6">6-sinf</option>
              <option value="8">8-sinf (O'rta maktab)</option>
              <option value="10">10-sinf</option>
              <option value="11">11-sinf (Bitiruvchi)</option>
              <option value="University">Universitet / Havaskor</option>
            </select>
          </div>
        </div>

        <!-- Complexity Level -->
        <div>
          <label class="block text-xs sm:text-sm font-bold text-slate-200 mb-2">
            {{ t.settings.levelLabel }}
          </label>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <button
              type="button"
              @click="form.knowledge_level = 'beginner'"
              class="p-4 rounded-xl border text-left transition-all"
              :class="form.knowledge_level === 'beginner'
                ? 'bg-emerald-500/15 border-emerald-500 text-white font-semibold'
                : 'bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700'"
            >
              <span class="text-xs font-bold block mb-1">Boshlang'ich</span>
              <span class="text-[11px] block leading-tight text-slate-400">Sodda va hayotiy misollar</span>
            </button>

            <button
              type="button"
              @click="form.knowledge_level = 'intermediate'"
              class="p-4 rounded-xl border text-left transition-all"
              :class="form.knowledge_level === 'intermediate'
                ? 'bg-emerald-500/15 border-emerald-500 text-white font-semibold'
                : 'bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700'"
            >
              <span class="text-xs font-bold block mb-1">O'rta</span>
              <span class="text-[11px] block leading-tight text-slate-400">Formulalar va ilmiy atamalar</span>
            </button>

            <button
              type="button"
              @click="form.knowledge_level = 'advanced'"
              class="p-4 rounded-xl border text-left transition-all"
              :class="form.knowledge_level === 'advanced'
                ? 'bg-emerald-500/15 border-emerald-500 text-white font-semibold'
                : 'bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700'"
            >
              <span class="text-xs font-bold block mb-1">Ilg'or</span>
              <span class="text-[11px] block leading-tight text-slate-400">Akademik va muhandislik tahlili</span>
            </button>
          </div>
        </div>

        <!-- Preferred Instruction Language -->
        <div>
          <label class="block text-xs sm:text-sm font-bold text-slate-200 mb-2">
            {{ t.settings.langLabel }}
          </label>
          <div class="grid grid-cols-3 gap-3">
            <button
              type="button"
              @click="selectLang('uz')"
              class="p-3 rounded-xl border text-center font-bold text-xs sm:text-sm transition-all"
              :class="form.preferred_language === 'uz'
                ? 'bg-emerald-500 text-slate-950 border-emerald-400'
                : 'bg-slate-950 border-slate-800 text-slate-300 hover:border-slate-700'"
            >
              🇺🇿 O'zbekcha
            </button>

            <button
              type="button"
              @click="selectLang('en')"
              class="p-3 rounded-xl border text-center font-bold text-xs sm:text-sm transition-all"
              :class="form.preferred_language === 'en'
                ? 'bg-emerald-500 text-slate-950 border-emerald-400'
                : 'bg-slate-950 border-slate-800 text-slate-300 hover:border-slate-700'"
            >
              🇬🇧 English
            </button>

            <button
              type="button"
              @click="selectLang('ru')"
              class="p-3 rounded-xl border text-center font-bold text-xs sm:text-sm transition-all"
              :class="form.preferred_language === 'ru'
                ? 'bg-emerald-500 text-slate-950 border-emerald-400'
                : 'bg-slate-950 border-slate-800 text-slate-300 hover:border-slate-700'"
            >
              🇷🇺 Русский
            </button>
          </div>
        </div>

        <!-- Custom Gemini API Key -->
        <div class="pt-4 border-t border-slate-800">
          <label class="block text-xs sm:text-sm font-bold text-slate-200 mb-1">
            {{ t.settings.geminiKeyLabel }}
          </label>
          <p class="text-xs text-slate-400 mb-3">
            {{ t.settings.geminiKeyHelp }}
          </p>
          <div class="relative">
            <input
              v-model="form.custom_api_key"
              :type="showKey ? 'text' : 'password'"
              placeholder="AIzaSy..."
              class="w-full bg-slate-950 border border-slate-800 focus:border-emerald-500 rounded-xl px-4 py-3 text-sm text-slate-100 placeholder-slate-600 focus:outline-none transition-colors pr-10 font-mono"
            />
            <button
              type="button"
              @click="showKey = !showKey"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white"
            >
              <EyeIcon v-if="!showKey" class="w-4 h-4" />
              <EyeOffIcon v-else class="w-4 h-4" />
            </button>
          </div>
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          :disabled="isSaving"
          class="w-full py-4 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-bold text-base flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/25 active:scale-[0.99] transition-all disabled:opacity-50"
        >
          <Loader2Icon v-if="isSaving" class="w-5 h-5 animate-spin" />
          <SaveIcon v-else class="w-5 h-5" />
          <span>{{ t.settings.saveBtn }}</span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useI18n, type SupportedLanguage } from '@/i18n'
import { useAuthStore } from '@/stores/auth'
import {
  Settings as SettingsIcon,
  CheckCircle2 as CheckCircle2Icon,
  Save as SaveIcon,
  Eye as EyeIcon,
  EyeOff as EyeOffIcon,
  Loader2 as Loader2Icon
} from '@lucide/vue'

const { t, setLanguage } = useI18n()
const authStore = useAuthStore()

const isSaving = ref(false)
const showSuccess = ref(false)
const showKey = ref(false)

const form = ref({
  full_name: authStore.user?.full_name || 'Talaba',
  age: authStore.user?.age || 14,
  grade: authStore.user?.grade || '8',
  knowledge_level: authStore.user?.knowledge_level || 'intermediate',
  preferred_language: authStore.user?.preferred_language || 'uz',
  custom_api_key: ''
})

onMounted(() => {
  if (authStore.user) {
    form.value.full_name = authStore.user.full_name
    form.value.age = authStore.user.age
    form.value.grade = authStore.user.grade
    form.value.knowledge_level = authStore.user.knowledge_level
    form.value.preferred_language = authStore.user.preferred_language
  }
})

const selectLang = (code: SupportedLanguage) => {
  form.value.preferred_language = code
  setLanguage(code)
}

const saveSettings = async () => {
  isSaving.value = true
  showSuccess.value = false
  try {
    if (authStore.isAuthenticated) {
      await authStore.updateProfile(form.value)
    } else {
      // Local fallback for guest
      setLanguage(form.value.preferred_language as SupportedLanguage)
      localStorage.setItem('guest_profile', JSON.stringify(form.value))
    }
    showSuccess.value = true
    setTimeout(() => {
      showSuccess.value = false
    }, 4000)
  } catch (err: any) {
    console.error('Settings save error:', err)
  } finally {
    isSaving.value = false
  }
}
</script>
