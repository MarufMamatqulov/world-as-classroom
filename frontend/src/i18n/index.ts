import { ref, computed } from 'vue'
import { uz } from './uz'
import { en } from './en'
import { ru } from './ru'

export type SupportedLanguage = 'uz' | 'en' | 'ru'

const currentLang = ref<SupportedLanguage>(
  (localStorage.getItem('preferred_language') as SupportedLanguage) || 'uz'
)

export const translations = {
  uz,
  en,
  ru
}

export function useI18n() {
  const t = computed(() => translations[currentLang.value])

  const setLanguage = (lang: SupportedLanguage) => {
    currentLang.value = lang
    localStorage.setItem('preferred_language', lang)
    document.documentElement.lang = lang
  }

  return {
    lang: currentLang,
    t,
    setLanguage
  }
}
