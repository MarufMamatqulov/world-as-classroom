import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { api, type UserProfile } from '@/api/client'
import { useI18n, type SupportedLanguage } from '@/i18n'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<UserProfile | null>(null)
  const isGuest = ref<boolean>(!token.value)
  const { setLanguage } = useI18n()

  const isAuthenticated = computed(() => !!token.value && !!user.value)

  const initAuth = async () => {
    if (!token.value) {
      isGuest.value = true
      return
    }
    try {
      const profile = await api.getMe()
      user.value = profile
      isGuest.value = false
      if (profile.preferred_language) {
        setLanguage(profile.preferred_language as SupportedLanguage)
      }
    } catch (e) {
      console.warn('Failed to fetch user with existing token, falling back to guest.', e)
      logout()
    }
  }

  const setAuthData = (newToken: string, newUser: UserProfile) => {
    token.value = newToken
    user.value = newUser
    isGuest.value = false
    localStorage.setItem('token', newToken)
    if (newUser.preferred_language) {
      setLanguage(newUser.preferred_language as SupportedLanguage)
    }
  }

  const login = async (credentials: { email: string; password: string }) => {
    const res = await api.login(credentials)
    setAuthData(res.access_token, res.user)
  }

  const register = async (data: {
    email: string
    password: string
    full_name: string
    age?: number
    grade?: string
    knowledge_level?: string
    preferred_language?: string
  }) => {
    const res = await api.register(data)
    setAuthData(res.access_token, res.user)
  }

  const updateProfile = async (updates: Partial<UserProfile> & { custom_api_key?: string }) => {
    const updated = await api.updateProfile(updates)
    user.value = updated
    if (updated.preferred_language) {
      setLanguage(updated.preferred_language as SupportedLanguage)
    }
  }

  const logout = () => {
    token.value = null
    user.value = null
    isGuest.value = true
    localStorage.removeItem('token')
  }

  return {
    token,
    user,
    isGuest,
    isAuthenticated,
    initAuth,
    login,
    register,
    updateProfile,
    logout
  }
})
