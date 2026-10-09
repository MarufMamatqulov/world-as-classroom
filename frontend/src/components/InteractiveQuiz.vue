<template>
  <div v-if="quiz" class="glass-panel rounded-3xl p-6 sm:p-8 border border-slate-800 bg-slate-900/90 shadow-2xl relative">
    <!-- Header -->
    <div class="flex items-center justify-between pb-4 mb-6 border-b border-slate-800">
      <div>
        <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-cyan-500/15 text-cyan-400 border border-cyan-500/30">
          <HelpCircleIcon class="w-3.5 h-3.5" />
          <span>{{ t.quiz.title }}</span>
        </span>
        <h3 class="text-xl sm:text-2xl font-bold text-white mt-2">
          {{ t.lesson.quizTitle }}
        </h3>
      </div>
      <div v-if="!submitted" class="text-xs font-semibold text-slate-400">
        {{ answers.filter(a => a !== -1).length }} / {{ quiz.questions.length }} belgilandi
      </div>
    </div>

    <!-- Active Questions Form -->
    <div v-if="!submitted" class="space-y-6">
      <div
        v-for="(q, qIdx) in quiz.questions"
        :key="q.id"
        class="bg-slate-950/60 p-5 rounded-2xl border border-slate-800/80"
      >
        <div class="flex items-start justify-between gap-2 mb-4">
          <h4 class="text-sm sm:text-base font-bold text-slate-100 flex items-start gap-2.5">
            <span class="w-6 h-6 rounded-lg bg-emerald-500/20 text-emerald-400 text-xs flex items-center justify-center font-bold shrink-0 mt-0.5">
              {{ qIdx + 1 }}
            </span>
            <span>{{ q.question }}</span>
          </h4>
          <span class="text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-400 font-semibold shrink-0">
            {{ q.subject }}
          </span>
        </div>

        <!-- Options -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
          <button
            v-for="(opt, optIdx) in q.options"
            :key="optIdx"
            type="button"
            @click="selectAnswer(qIdx, optIdx)"
            class="p-3.5 rounded-xl border text-left text-xs sm:text-sm font-medium transition-all flex items-center gap-3"
            :class="answers[qIdx] === optIdx
              ? 'bg-emerald-500/20 border-emerald-500 text-emerald-300 font-semibold'
              : 'bg-slate-900/60 border-slate-800 text-slate-300 hover:bg-slate-800/60 hover:border-slate-700'"
          >
            <span
              class="w-6 h-6 rounded-lg text-xs font-bold flex items-center justify-center shrink-0 border"
              :class="answers[qIdx] === optIdx
                ? 'bg-emerald-500 text-slate-950 border-emerald-400'
                : 'bg-slate-800 border-slate-700 text-slate-400'"
            >
              {{ String.fromCharCode(65 + optIdx) }}
            </span>
            <span class="leading-snug">{{ opt }}</span>
          </button>
        </div>
      </div>

      <!-- Submit Button -->
      <button
        @click="submitQuiz()"
        :disabled="isSubmitting || answers.includes(-1)"
        class="w-full py-4 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-bold text-base flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/25 active:scale-[0.99] transition-all disabled:opacity-40"
      >
        <Loader2Icon v-if="isSubmitting" class="w-5 h-5 animate-spin" />
        <CheckCircle2Icon v-else class="w-5 h-5" />
        <span>{{ t.quiz.submit }}</span>
      </button>
    </div>

    <!-- Quiz Results & Explanations -->
    <div v-else class="space-y-6">
      <!-- Score Banner -->
      <div class="p-6 rounded-2xl bg-gradient-to-tr from-emerald-950/40 via-teal-950/30 to-slate-900 border border-emerald-500/30 text-center relative overflow-hidden">
        <TrophyIcon class="w-12 h-12 text-amber-400 mx-auto mb-2 animate-bounce" />
        <h3 class="text-2xl sm:text-3xl font-extrabold text-white">
          {{ resultData?.score }} / {{ resultData?.total_questions }}
        </h3>
        <p class="text-emerald-400 font-semibold text-sm mt-1">
          {{ resultData?.percentage }}% — {{ resultData?.feedback }}
        </p>
      </div>

      <!-- Detailed Question Explanations -->
      <div class="space-y-4">
        <div
          v-for="(evalItem, idx) in resultData?.evaluations"
          :key="idx"
          class="p-5 rounded-2xl border bg-slate-950/60"
          :class="evalItem.is_correct ? 'border-emerald-500/40' : 'border-rose-500/40'"
        >
          <div class="flex items-start justify-between gap-2 mb-2">
            <h4 class="text-sm font-bold text-white flex items-center gap-2">
              <span
                class="w-5 h-5 rounded-full text-xs font-bold flex items-center justify-center"
                :class="evalItem.is_correct ? 'bg-emerald-500 text-slate-950' : 'bg-rose-500 text-white'"
              >
                {{ evalItem.is_correct ? '✓' : '✗' }}
              </span>
              <span>{{ evalItem.question }}</span>
            </h4>
            <span
              class="text-xs font-bold px-2 py-0.5 rounded-full"
              :class="evalItem.is_correct ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'"
            >
              {{ evalItem.is_correct ? t.quiz.correct : t.quiz.incorrect }}
            </span>
          </div>

          <!-- Explanation text -->
          <div class="mt-3 p-3.5 rounded-xl bg-slate-900/90 border border-slate-800 text-xs sm:text-sm text-slate-300 leading-relaxed">
            <strong class="text-emerald-400">{{ t.quiz.explanationTitle }}:</strong>
            {{ evalItem.explanation }}
          </div>
        </div>
      </div>

      <!-- Retry Quiz Button -->
      <button
        @click="resetQuiz()"
        class="w-full py-3.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold text-sm flex items-center justify-center gap-2 transition-colors"
      >
        <RotateCcwIcon class="w-4 h-4 text-emerald-400" />
        <span>{{ t.quiz.retry }}</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useI18n } from '@/i18n'
import { api, type QuizDetail, type QuizSubmitResponse } from '@/api/client'
import confetti from 'canvas-confetti'
import {
  HelpCircle as HelpCircleIcon,
  CheckCircle2 as CheckCircle2Icon,
  Trophy as TrophyIcon,
  RotateCcw as RotateCcwIcon,
  Loader2 as Loader2Icon
} from '@lucide/vue'

const props = defineProps<{
  quiz: QuizDetail | null
}>()

const emit = defineEmits<{
  (e: 'completed', result: QuizSubmitResponse): void
}>()

const { t } = useI18n()
const answers = ref<number[]>([])
const isSubmitting = ref(false)
const submitted = ref(false)
const resultData = ref<QuizSubmitResponse | null>(null)

watch(
  () => props.quiz,
  (newQuiz) => {
    if (newQuiz) {
      answers.value = new Array(newQuiz.questions.length).fill(-1)
      submitted.value = false
      resultData.value = null
    }
  },
  { immediate: true }
)

const selectAnswer = (questionIdx: number, optionIdx: number) => {
  if (submitted.value) return
  answers.value[questionIdx] = optionIdx
}

const submitQuiz = async () => {
  if (!props.quiz || answers.value.includes(-1)) return
  isSubmitting.value = true
  try {
    const res = await api.submitQuiz(props.quiz.id, answers.value)
    resultData.value = res
    submitted.value = true
    emit('completed', res)

    // Trigger celebratory confetti if score >= 60%
    if (res.percentage >= 60) {
      try {
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.6 }
        })
      } catch {
        // ignore
      }
    }
  } catch (err: any) {
    console.error('Quiz submission error:', err)
  } finally {
    isSubmitting.value = false
  }
}

const resetQuiz = () => {
  if (props.quiz) {
    answers.value = new Array(props.quiz.questions.length).fill(-1)
  }
  submitted.value = false
  resultData.value = null
}
</script>
