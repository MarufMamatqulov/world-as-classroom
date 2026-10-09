<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
    <!-- View Header -->
    <div class="mb-8">
      <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-bold border border-emerald-500/20 mb-2">
        <LayoutDashboardIcon class="w-3.5 h-3.5" />
        <span>{{ t.nav.dashboard }}</span>
      </div>
      <h1 class="text-2xl sm:text-3xl font-extrabold text-white">
        {{ t.dashboard.title }}
      </h1>
      <p class="text-xs sm:text-sm text-slate-400 mt-1">
        {{ t.dashboard.subtitle }}
      </p>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="min-h-[40vh] flex items-center justify-center">
      <Loader2Icon class="w-10 h-10 text-emerald-400 animate-spin" />
    </div>

    <!-- Active Dashboard Content -->
    <div v-else class="space-y-10">
      <!-- 4 Stats Cards Grid -->
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
        <!-- 1. Explorations -->
        <div class="glass-card rounded-2xl p-5 border border-slate-800 flex items-center gap-4">
          <div class="w-12 h-12 rounded-xl bg-emerald-500/15 border border-emerald-500/30 flex items-center justify-center text-emerald-400 shrink-0">
            <CameraIcon class="w-6 h-6" />
          </div>
          <div>
            <span class="text-xs font-semibold text-slate-400 block">{{ t.dashboard.totalExplored }}</span>
            <span class="text-2xl sm:text-3xl font-black text-white mt-0.5 block">
              {{ stats?.total_explorations || 0 }}
            </span>
          </div>
        </div>

        <!-- 2. Quizzes Completed -->
        <div class="glass-card rounded-2xl p-5 border border-slate-800 flex items-center gap-4">
          <div class="w-12 h-12 rounded-xl bg-teal-500/15 border border-teal-500/30 flex items-center justify-center text-teal-400 shrink-0">
            <CheckCircle2Icon class="w-6 h-6" />
          </div>
          <div>
            <span class="text-xs font-semibold text-slate-400 block">{{ t.dashboard.quizzesCompleted }}</span>
            <span class="text-2xl sm:text-3xl font-black text-white mt-0.5 block">
              {{ stats?.total_quizzes_completed || 0 }}
            </span>
          </div>
        </div>

        <!-- 3. Average Score -->
        <div class="glass-card rounded-2xl p-5 border border-slate-800 flex items-center gap-4">
          <div class="w-12 h-12 rounded-xl bg-cyan-500/15 border border-cyan-500/30 flex items-center justify-center text-cyan-400 shrink-0">
            <TrophyIcon class="w-6 h-6" />
          </div>
          <div>
            <span class="text-xs font-semibold text-slate-400 block">{{ t.dashboard.averageScore }}</span>
            <span class="text-2xl sm:text-3xl font-black text-white mt-0.5 block">
              {{ stats?.average_quiz_score || 0 }}%
            </span>
          </div>
        </div>

        <!-- 4. Streak -->
        <div class="glass-card rounded-2xl p-5 border border-slate-800 flex items-center gap-4">
          <div class="w-12 h-12 rounded-xl bg-amber-500/15 border border-amber-500/30 flex items-center justify-center text-amber-400 shrink-0">
            <FlameIcon class="w-6 h-6" />
          </div>
          <div>
            <span class="text-xs font-semibold text-slate-400 block">{{ t.dashboard.learningStreak }}</span>
            <span class="text-2xl sm:text-3xl font-black text-white mt-0.5 block">
              {{ stats?.current_streak_days || 0 }} kun
            </span>
          </div>
        </div>
      </div>

      <!-- Subject Mastery & Achievements Row -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <!-- Subject Mastery Meters -->
        <div class="lg:col-span-6 glass-panel rounded-3xl p-6 sm:p-8 border border-slate-800 bg-slate-900/90 shadow-2xl">
          <h2 class="text-lg sm:text-xl font-bold text-white flex items-center gap-2 mb-6">
            <BookOpenIcon class="w-5 h-5 text-emerald-400" />
            <span>{{ t.dashboard.subjectMastery }}</span>
          </h2>

          <div class="space-y-4">
            <div
              v-for="subj in stats?.subject_mastery"
              :key="subj.subject"
              class="space-y-1.5"
            >
              <div class="flex items-center justify-between text-xs sm:text-sm">
                <span class="font-semibold text-slate-200">{{ subj.subject }}</span>
                <span class="text-emerald-400 font-bold">{{ subj.points }} ball ({{ subj.lessons_count }} dars)</span>
              </div>
              <div class="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
                <div
                  class="h-full bg-gradient-to-r from-emerald-500 to-teal-400 rounded-full transition-all duration-500"
                  :style="{ width: `${Math.min(100, Math.max(12, subj.points / 2))}%` }"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Badges & Achievements -->
        <div class="lg:col-span-6 glass-panel rounded-3xl p-6 sm:p-8 border border-slate-800 bg-slate-900/90 shadow-2xl">
          <h2 class="text-lg sm:text-xl font-bold text-white flex items-center gap-2 mb-6">
            <AwardIcon class="w-5 h-5 text-amber-400" />
            <span>{{ t.dashboard.achievementsTitle }}</span>
          </h2>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
            <div
              v-for="ach in stats?.achievements"
              :key="ach.id"
              class="p-4 rounded-2xl border transition-colors flex items-start gap-3"
              :class="ach.unlocked
                ? 'bg-amber-500/10 border-amber-500/40 text-slate-100'
                : 'bg-slate-950/40 border-slate-800/80 text-slate-400 opacity-60'"
            >
              <div
                class="w-10 h-10 rounded-xl flex items-center justify-center shrink-0"
                :class="ach.unlocked ? 'bg-amber-500/20 text-amber-400' : 'bg-slate-800 text-slate-500'"
              >
                <TrophyIcon class="w-5 h-5" />
              </div>
              <div>
                <h4 class="text-xs sm:text-sm font-bold" :class="ach.unlocked ? 'text-white' : 'text-slate-400'">
                  {{ ach.title }}
                </h4>
                <p class="text-[11px] mt-0.5 leading-snug">
                  {{ ach.description }}
                </p>
                <span v-if="ach.unlocked" class="inline-block mt-1 text-[10px] font-bold text-amber-400">
                  Ochilgan ✓
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Explorations Section -->
      <section class="glass-panel rounded-3xl p-6 sm:p-8 border border-slate-800 bg-slate-900/90 shadow-2xl">
        <h2 class="text-lg sm:text-xl font-bold text-white flex items-center gap-2 mb-6">
          <HistoryIcon class="w-5 h-5 text-emerald-400" />
          <span>{{ t.dashboard.recentTitle }}</span>
        </h2>

        <div v-if="stats?.recent_explorations && stats.recent_explorations.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
            v-for="item in stats.recent_explorations"
            :key="item.id"
            @click="openExploration(item.id)"
            class="glass-card glass-card-hover rounded-2xl p-5 cursor-pointer border border-slate-800 flex flex-col justify-between"
          >
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 border border-emerald-500/20">
                  {{ item.primary_subject }}
                </span>
                <span class="text-[11px] text-slate-400 font-medium">
                  {{ formatDate(item.created_at) }}
                </span>
              </div>

              <h4 class="text-base font-bold text-white group-hover:text-emerald-300">
                {{ item.object_name }}
              </h4>
              <p class="text-xs text-slate-400 mt-1">
                {{ item.category }}
              </p>
            </div>

            <div class="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between">
              <span v-if="item.quiz_completed" class="text-xs font-semibold text-emerald-400">
                Viktorina: {{ item.best_score }} / {{ item.total_questions }}
              </span>
              <span v-else class="text-xs text-slate-500">
                Viktorina topshirilmagan
              </span>

              <span class="text-xs font-bold text-emerald-400 flex items-center gap-1">
                <span>Darsga o'tish</span>
                <span>→</span>
              </span>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="text-center py-12">
          <CameraIcon class="w-12 h-12 text-slate-600 mx-auto mb-3" />
          <p class="text-sm text-slate-400 max-w-sm mx-auto mb-4">
            {{ t.dashboard.noExplorations }}
          </p>
          <router-link
            to="/scanner"
            class="px-5 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-sm inline-flex items-center gap-2"
          >
            <CameraIcon class="w-4 h-4" />
            <span>{{ t.dashboard.startFirst }}</span>
          </router-link>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from '@/i18n'
import { api, type DashboardStats } from '@/api/client'
import {
  LayoutDashboard as LayoutDashboardIcon,
  Camera as CameraIcon,
  CheckCircle2 as CheckCircle2Icon,
  Trophy as TrophyIcon,
  Flame as FlameIcon,
  BookOpen as BookOpenIcon,
  Award as AwardIcon,
  History as HistoryIcon,
  Loader2 as Loader2Icon
} from '@lucide/vue'

const { t } = useI18n()
const router = useRouter()
const stats = ref<DashboardStats | null>(null)
const isLoading = ref(true)

onMounted(async () => {
  try {
    stats.value = await api.getDashboardStats()
  } catch (e) {
    console.error('Failed to load dashboard:', e)
  } finally {
    isLoading.value = false
  }
})

const formatDate = (isoString: string) => {
  try {
    const d = new Date(isoString)
    return d.toLocaleDateString()
  } catch {
    return ''
  }
}

const openExploration = async (explorationId: number) => {
  try {
    const lesson = await api.getLessonByExploration(explorationId)
    if (lesson) {
      router.push({ name: 'Lesson', params: { id: lesson.id } })
    }
  } catch (err) {
    console.error('Failed to open lesson:', err)
  }
}
</script>
