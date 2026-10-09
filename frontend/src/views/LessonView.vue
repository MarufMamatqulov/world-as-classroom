<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
    <!-- Loading State -->
    <div v-if="isLoading" class="min-h-[50vh] flex flex-col items-center justify-center gap-4">
      <Loader2Icon class="w-12 h-12 text-emerald-400 animate-spin" />
      <p class="text-white font-bold text-lg">{{ t.lesson.generating }}</p>
      <p class="text-xs text-slate-400">{{ t.lesson.generatingSubtitle }}</p>
    </div>

    <!-- Active Lesson Content -->
    <div v-else-if="lesson" class="space-y-10">
      <!-- Top Action Navigation -->
      <div class="flex items-center justify-between flex-wrap gap-4">
        <router-link
          to="/scanner"
          class="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl bg-slate-900 border border-slate-800 text-xs sm:text-sm font-semibold text-slate-300 hover:text-white hover:border-slate-700 transition-colors"
        >
          <ArrowLeftIcon class="w-4 h-4 text-emerald-400" />
          <span>{{ t.lesson.backToScanner }}</span>
        </router-link>

        <div class="flex items-center gap-2">
          <!-- Tutor Toggle Button -->
          <button
            @click="showTutorDrawer = !showTutorDrawer"
            class="px-4 py-2 rounded-xl bg-slate-900 border border-emerald-500/40 text-emerald-400 text-xs sm:text-sm font-bold flex items-center gap-2 shadow-sm hover:bg-emerald-500/10 transition-colors"
          >
            <BotIcon class="w-4 h-4" />
            <span>{{ t.lesson.askTutorBtn }}</span>
          </button>

          <!-- Scroll to Quiz Button -->
          <button
            @click="scrollToQuiz()"
            class="px-4 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 text-xs sm:text-sm font-bold flex items-center gap-2 transition-colors shadow-md shadow-emerald-500/20"
          >
            <HelpCircleIcon class="w-4 h-4" />
            <span>{{ t.lesson.takeQuizBtn }}</span>
          </button>
        </div>
      </div>

      <!-- Lesson Hero Banner -->
      <div class="glass-panel rounded-3xl p-6 sm:p-10 border border-slate-800 bg-slate-900/90 shadow-2xl relative overflow-hidden">
        <div class="absolute -top-32 -left-32 w-80 h-80 bg-emerald-500/15 rounded-full blur-3xl pointer-events-none"></div>

        <div class="relative z-10 flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div class="max-w-3xl">
            <div class="flex flex-wrap items-center gap-2.5 mb-3">
              <span class="px-3 py-1 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                {{ lesson.object_name }}
              </span>
              <span class="px-3 py-1 rounded-full text-xs font-semibold bg-slate-800 text-slate-300">
                {{ lesson.subjects.length }} ta Fan
              </span>
              <span class="px-3 py-1 rounded-full text-xs font-semibold bg-slate-800/80 text-teal-300 border border-slate-700/60">
                {{ t.lesson.personalizedBadge }}
              </span>
            </div>

            <h1 class="text-2xl sm:text-4xl font-extrabold text-white tracking-tight leading-tight">
              {{ lesson.title }}
            </h1>

            <p class="text-sm sm:text-base text-slate-300 mt-4 leading-relaxed">
              {{ lesson.summary }}
            </p>
          </div>

          <!-- Image thumbnail if available -->
          <div v-if="lessonImage" class="w-28 h-28 sm:w-36 sm:h-36 rounded-2xl overflow-hidden border-2 border-emerald-500/40 shrink-0 shadow-lg shadow-emerald-500/20">
            <img :src="lessonImage" alt="Lesson thumbnail" class="w-full h-full object-cover" />
          </div>
        </div>
      </div>

      <!-- Main Layout: Subject Modules & AI Tutor Drawer -->
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        <!-- Main Curriculum Column -->
        <div class="lg:col-span-8 space-y-10">
          <!-- Interdisciplinary Subject Modules -->
          <section>
            <div class="mb-4">
              <h2 class="text-xl sm:text-2xl font-bold text-white flex items-center gap-2">
                <AtomIcon class="w-6 h-6 text-emerald-400" />
                <span>{{ t.lesson.subjectsTitle }}</span>
              </h2>
            </div>
            <SubjectTabs :modules="lesson.subjects" />
          </section>

          <!-- Try This At Home: Experiment -->
          <section v-if="lesson.experiments && lesson.experiments.length > 0">
            <ExperimentCard :experiments="lesson.experiments" />
          </section>

          <!-- Fun Facts & Did You Know -->
          <section v-if="lesson.fun_facts && lesson.fun_facts.length > 0">
            <div class="glass-panel rounded-3xl p-6 sm:p-8 border border-slate-800 bg-slate-900/90 shadow-2xl">
              <h3 class="text-xl font-bold text-white flex items-center gap-2 mb-6">
                <SparklesIcon class="w-5 h-5 text-amber-400" />
                <span>{{ t.lesson.didYouKnow }}</span>
              </h3>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div
                  v-for="(f, fIdx) in lesson.fun_facts"
                  :key="fIdx"
                  class="bg-slate-950/60 p-5 rounded-2xl border border-slate-800/80 hover:border-amber-500/30 transition-colors"
                >
                  <p class="text-sm sm:text-base font-semibold text-slate-100 leading-snug">
                    "{{ f.fact }}"
                  </p>
                  <p class="text-xs text-amber-400/90 mt-2 font-medium">
                    {{ f.why_cool }}
                  </p>
                </div>
              </div>
            </div>
          </section>

          <!-- Vocabulary Glossary -->
          <section v-if="lesson.vocabulary && lesson.vocabulary.length > 0">
            <div class="glass-panel rounded-3xl p-6 sm:p-8 border border-slate-800 bg-slate-900/90 shadow-2xl">
              <h3 class="text-xl font-bold text-white flex items-center gap-2 mb-6">
                <BookOpenIcon class="w-5 h-5 text-emerald-400" />
                <span>{{ t.lesson.vocabulary }}</span>
              </h3>

              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                <div
                  v-for="(v, vIdx) in lesson.vocabulary"
                  :key="vIdx"
                  class="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80"
                >
                  <span class="text-xs sm:text-sm font-bold text-emerald-400 block mb-1">
                    {{ v.term }}
                  </span>
                  <span class="text-xs text-slate-300 leading-relaxed block">
                    {{ v.definition }}
                  </span>
                </div>
              </div>
            </div>
          </section>

          <!-- Quiz Section -->
          <section id="quiz-section" class="scroll-mt-24">
            <InteractiveQuiz :quiz="quizData" @completed="onQuizCompleted" />
          </section>
        </div>

        <!-- Sidebar / Persistent AI Tutor Chat Column -->
        <div class="lg:col-span-4 sticky top-24 space-y-6">
          <AITutorChat
            :exploration-id="lesson.exploration_id"
            :object-name="lesson.object_name"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from '@/i18n'
import { useExplorationStore } from '@/stores/exploration'
import { api, type LessonDetail, type QuizDetail } from '@/api/client'
import SubjectTabs from '@/components/SubjectTabs.vue'
import ExperimentCard from '@/components/ExperimentCard.vue'
import InteractiveQuiz from '@/components/InteractiveQuiz.vue'
import AITutorChat from '@/components/AITutorChat.vue'
import {
  ArrowLeft as ArrowLeftIcon,
  Atom as AtomIcon,
  Bot as BotIcon,
  HelpCircle as HelpCircleIcon,
  Sparkles as SparklesIcon,
  BookOpen as BookOpenIcon,
  Loader2 as Loader2Icon
} from '@lucide/vue'

const { t } = useI18n()
const route = useRoute()
const router = useRouter()
const explorationStore = useExplorationStore()

const isLoading = ref(true)
const lesson = ref<LessonDetail | null>(null)
const quizData = ref<QuizDetail | null>(null)
const showTutorDrawer = ref(false)

const lessonImage = computed(() => {
  return explorationStore.imagePreview || null
})

onMounted(async () => {
  const lessonIdParam = route.params.id

  if (lessonIdParam) {
    const id = parseInt(lessonIdParam as string, 10)
    try {
      const fetched = await api.getLesson(id)
      lesson.value = fetched
      explorationStore.currentLesson = fetched
      const q = await api.getQuizByLesson(fetched.id)
      quizData.value = q
    } catch (e) {
      console.error('Failed to load lesson:', e)
    } finally {
      isLoading.value = false
    }
  } else if (explorationStore.currentLesson) {
    lesson.value = explorationStore.currentLesson
    try {
      const q = await api.getQuizByLesson(explorationStore.currentLesson.id)
      quizData.value = q
    } catch (e) {
      console.error('Quiz fetch error:', e)
    } finally {
      isLoading.value = false
    }
  } else {
    router.replace({ name: 'Scanner' })
  }
})

const scrollToQuiz = () => {
  const el = document.getElementById('quiz-section')
  if (el) {
    el.scrollIntoView({ behavior: 'smooth' })
  }
}

const onQuizCompleted = (result: any) => {
  console.log('Quiz completed with result:', result)
}
</script>
