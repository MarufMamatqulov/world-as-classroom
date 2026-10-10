<template>
  <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
    <!-- Header Banner -->
    <div class="rounded-3xl glass-panel bg-gradient-to-r from-amber-950/40 via-slate-900 to-slate-950 border border-amber-500/30 p-6 sm:p-8 shadow-2xl flex flex-col md:flex-row items-center justify-between gap-6">
      <div class="space-y-2 text-center md:text-left">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/20 text-amber-400 text-xs font-bold border border-amber-500/30">
          <FlameIcon class="w-4 h-4 text-amber-400 animate-bounce" />
          <span>Kundalik Ilmiy Missiyalar</span>
        </div>
        <h1 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          Haqiqiy Olam Kashfiyotlari (Real World Quests)
        </h1>
        <p class="text-xs sm:text-sm text-slate-300 max-w-xl">
          Atrofdagi fizik, kimyoviy va biologik hodisalarni toping, ilmiy tekshiruvdan o'tkazing, tajriba o'tkazib XP va maxsus ilmiy nishonlarni qo'lga kiriting!
        </p>
      </div>

      <!-- Streak & XP Counter Card -->
      <div class="flex items-center gap-4 bg-slate-950/80 p-4 rounded-2xl border border-slate-800 shadow-xl flex-shrink-0">
        <div class="text-center px-3">
          <div class="text-xl sm:text-2xl font-black text-amber-400 flex items-center justify-center gap-1">
            <FlameIcon class="w-5 h-5 text-amber-500" />
            <span>{{ userStreak }}</span>
          </div>
          <span class="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Kunlik Ketma-ketlik</span>
        </div>
        <div class="w-px h-10 bg-slate-800"></div>
        <div class="text-center px-3">
          <div class="text-xl sm:text-2xl font-black text-emerald-400">
            +{{ totalQuestXp }}
          </div>
          <span class="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">Missiya XP</span>
        </div>
      </div>
    </div>

    <!-- Quests List & Badges Section -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Left 2 Cols: Active Daily Quests -->
      <div class="lg:col-span-2 space-y-4">
        <div class="flex items-center justify-between">
          <h2 class="text-lg font-bold text-white flex items-center gap-2">
            <CompassIcon class="w-5 h-5 text-emerald-400" />
            <span>Bugungi Missiyalar</span>
          </h2>
          <span class="text-xs font-semibold text-slate-400">
            {{ completedCount }}/{{ quests.length }} Bajarildi
          </span>
        </div>

        <!-- Skeleton Loader -->
        <div v-if="loading" class="space-y-4">
          <div v-for="i in 3" :key="i" class="h-32 rounded-2xl bg-slate-900/60 animate-pulse border border-slate-800"></div>
        </div>

        <!-- Quest Cards -->
        <div v-else class="space-y-4">
          <div
            v-for="quest in quests"
            :key="quest.id"
            class="rounded-2xl glass-panel p-5 sm:p-6 border transition-all duration-200 relative overflow-hidden"
            :class="quest.status === 'completed'
              ? 'bg-emerald-950/20 border-emerald-500/40 shadow-sm'
              : 'bg-slate-900/80 border-slate-800 hover:border-slate-700 hover:bg-slate-850'"
          >
            <!-- Top Tag & XP -->
            <div class="flex items-start justify-between gap-3 mb-3">
              <div class="flex items-center gap-2">
                <span class="px-2.5 py-0.5 rounded-lg text-[10px] font-bold uppercase tracking-wider bg-slate-800 text-slate-300 border border-slate-700">
                  {{ quest.domain }}
                </span>
                <span
                  v-if="quest.status === 'completed'"
                  class="px-2 py-0.5 rounded-md text-[10px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 flex items-center gap-1"
                >
                  ✓ Bajarildi
                </span>
              </div>
              <span class="px-2.5 py-1 rounded-xl bg-amber-500/10 text-amber-300 border border-amber-500/30 text-xs font-extrabold flex items-center gap-1">
                <SparklesIcon class="w-3.5 h-3.5 text-amber-400" />
                <span>+{{ quest.xp_reward }} XP</span>
              </span>
            </div>

            <!-- Title & Description -->
            <h3 class="text-base sm:text-lg font-bold text-white mb-1.5">
              {{ quest.title }}
            </h3>
            <p class="text-xs sm:text-sm text-slate-300 leading-relaxed mb-4">
              {{ quest.description }}
            </p>

            <!-- Bottom Action Footer -->
            <div class="flex items-center justify-between pt-3 border-t border-slate-800/80">
              <div class="flex items-center gap-2 text-xs text-slate-400">
                <AwardIcon class="w-4 h-4 text-emerald-400" />
                <span class="font-semibold text-slate-300">{{ quest.badge_title }}</span>
              </div>

              <div class="flex items-center gap-2">
                <button
                  v-if="quest.status !== 'completed'"
                  @click="openQuestModal(quest)"
                  class="px-4 py-2 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-bold text-xs flex items-center gap-1.5 shadow-md shadow-emerald-500/20 active:scale-95 transition-all"
                >
                  <span>Tekshirish & Tasdiqlash</span>
                  <ChevronRightIcon class="w-3.5 h-3.5" />
                </button>
                <span v-else class="text-xs text-emerald-400 font-bold flex items-center gap-1">
                  Mukofot olindi
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Col: Unlocked Badges Cabinet -->
      <div class="space-y-4">
        <h2 class="text-lg font-bold text-white flex items-center gap-2">
          <AwardIcon class="w-5 h-5 text-amber-400" />
          <span>Ilmiy Nishonlarim (Badges)</span>
        </h2>

        <div class="rounded-2xl glass-panel bg-slate-900/80 border border-slate-800 p-5 space-y-4">
          <div v-if="badges.length === 0" class="text-center py-8 text-slate-400 text-xs">
            Hozircha nishonlar yo'q. Birinchi missiyani bajaring!
          </div>

          <div v-else class="grid grid-cols-2 gap-3">
            <div
              v-for="b in badges"
              :key="b.id"
              class="p-3.5 rounded-xl bg-slate-950 border border-emerald-500/30 hover:border-emerald-400/60 transition-all flex flex-col items-center text-center gap-2 group shadow"
            >
              <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-emerald-500/20 to-teal-500/20 border border-emerald-500/40 flex items-center justify-center text-emerald-400 group-hover:scale-110 transition-transform">
                <AwardIcon class="w-6 h-6" />
              </div>
              <div class="space-y-0.5">
                <h4 class="text-xs font-bold text-white leading-tight">
                  {{ b.title }}
                </h4>
                <span class="text-[10px] text-slate-400 block">
                  {{ b.domain }}
                </span>
              </div>
              <span class="text-[10px] font-extrabold text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
                +{{ b.xp }} XP
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal: Verification Challenge -->
    <div
      v-if="activeQuest"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md"
      @click.self="activeQuest = null"
    >
      <div class="w-full max-w-lg rounded-3xl glass-panel bg-slate-900 border border-slate-700 p-6 sm:p-8 shadow-2xl space-y-6 animate-scale-up">
        <div class="flex items-center justify-between border-b border-slate-800 pb-3">
          <div>
            <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
              {{ activeQuest.domain }}
            </span>
            <h3 class="text-base sm:text-lg font-bold text-white mt-1">
              {{ activeQuest.title }}
            </h3>
          </div>
          <button @click="activeQuest = null" class="text-slate-400 hover:text-white p-2">✕</button>
        </div>

        <!-- Question Box -->
        <div class="space-y-3">
          <p class="text-xs sm:text-sm font-semibold text-slate-200">
            Kashfiyotni tasdiqlash uchun ilmiy savolga javob bering:
          </p>
          <div class="p-4 rounded-xl bg-slate-950 border border-slate-800 text-sm font-bold text-emerald-300">
            {{ activeQuest.validation_question }}
          </div>

          <!-- Multiple choice options -->
          <div class="space-y-2 pt-2">
            <button
              v-for="(opt, idx) in activeQuest.validation_options"
              :key="idx"
              @click="selectedOptionIndex = idx"
              class="w-full text-left p-3.5 rounded-xl text-xs sm:text-sm font-semibold border transition-all flex items-center justify-between"
              :class="selectedOptionIndex === idx
                ? 'bg-emerald-950/50 border-emerald-500 text-emerald-300 shadow-md'
                : 'bg-slate-950/60 border-slate-800 text-slate-300 hover:bg-slate-800/40 hover:border-slate-700'"
            >
              <span>{{ opt }}</span>
              <span
                class="w-4 h-4 rounded-full border flex items-center justify-center text-[10px]"
                :class="selectedOptionIndex === idx ? 'border-emerald-400 bg-emerald-500 text-slate-950 font-bold' : 'border-slate-600'"
              >
                {{ selectedOptionIndex === idx ? '✓' : '' }}
              </span>
            </button>
          </div>
        </div>

        <!-- Feedback Alert if wrong -->
        <div v-if="submitFeedback" class="p-3 rounded-xl bg-amber-500/20 border border-amber-500/40 text-amber-200 text-xs">
          {{ submitFeedback }}
        </div>

        <!-- Modal Footer -->
        <div class="flex items-center justify-between pt-2">
          <button
            @click="activeQuest = null"
            class="px-4 py-2.5 rounded-xl text-xs font-semibold text-slate-400 hover:text-white bg-slate-800"
          >
            Yopish
          </button>
          <button
            @click="submitVerification"
            :disabled="selectedOptionIndex === null || submitting"
            class="px-5 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-extrabold text-xs flex items-center gap-1.5 shadow-lg shadow-emerald-500/25 disabled:opacity-50 transition-all"
          >
            <Loader2Icon v-if="submitting" class="w-4 h-4 animate-spin" />
            <span v-else>Tasdiqlash & XP Olish</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { api, type QuestResponse, type UserBadgeResponse } from '@/api/client'
import { useAuthStore } from '@/stores/auth'
import confetti from 'canvas-confetti'
import {
  Compass as CompassIcon,
  Flame as FlameIcon,
  Sparkles as SparklesIcon,
  Award as AwardIcon,
  ChevronRight as ChevronRightIcon,
  Loader2 as Loader2Icon
} from '@lucide/vue'

const authStore = useAuthStore()

const loading = ref(true)
const quests = ref<QuestResponse[]>([])
const badges = ref<UserBadgeResponse[]>([])
const activeQuest = ref<QuestResponse | null>(null)
const selectedOptionIndex = ref<number | null>(null)
const submitting = ref(false)
const submitFeedback = ref('')

const completedCount = computed(() => quests.value.filter(q => q.status === 'completed').length)
const totalQuestXp = computed(() => badges.value.reduce((acc, b) => acc + (b.xp || 0), 0))
const userStreak = computed(() => authStore.user?.streak_days || 1)

const loadData = async () => {
  loading.value = true
  try {
    const [qList, bList] = await Promise.all([
      api.getDailyQuests(),
      api.getUserBadges()
    ])
    quests.value = qList
    badges.value = bList
  } catch (err) {
    console.error('Failed to load quests data:', err)
  } finally {
    loading.value = false
  }
}

const openQuestModal = (q: QuestResponse) => {
  activeQuest.value = q
  selectedOptionIndex.value = null
  submitFeedback.value = ''
}

const submitVerification = async () => {
  if (!activeQuest.value || selectedOptionIndex.value === null) return
  submitting.value = true
  submitFeedback.value = ''

  try {
    const res = await api.submitQuest(activeQuest.value.id, selectedOptionIndex.value)
    if (res.success) {
      // Confetti celebration
      confetti({
        particleCount: 80,
        spread: 60,
        origin: { y: 0.6 }
      })
      activeQuest.value.status = 'completed'
      activeQuest.value = null
      await loadData()
    } else {
      submitFeedback.value = res.message || 'Noto\'g\'ri javob. Qayta urinib ko\'ring.'
    }
  } catch (err: any) {
    submitFeedback.value = err.message || 'Xatolik yuz berdi'
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>
