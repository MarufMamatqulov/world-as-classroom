<template>
  <div v-if="explorationStore.detectedObjects.length > 0" class="w-full max-w-2xl mx-auto mt-6">
    <div class="glass-panel rounded-2xl p-6 border border-slate-800 bg-slate-900/80 shadow-xl">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h3 class="text-base sm:text-lg font-bold text-white flex items-center gap-2">
            <SparklesIcon class="w-5 h-5 text-emerald-400" />
            <span>{{ t.scanner.detectedObjects }}</span>
          </h3>
          <p class="text-xs text-slate-400 mt-0.5">
            {{ t.scanner.selectObjectPrompt }}
          </p>
        </div>
        <span class="px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-semibold border border-emerald-500/20">
          {{ explorationStore.detectedObjects.length }} ta aniqlandi
        </span>
      </div>

      <!-- Object Cards Grid -->
      <div class="space-y-3 mb-6">
        <div
          v-for="(obj, idx) in explorationStore.detectedObjects"
          :key="idx"
          @click="explorationStore.selectedObject = obj"
          class="p-4 rounded-xl border transition-all cursor-pointer relative overflow-hidden flex flex-col gap-2"
          :class="explorationStore.selectedObject?.name === obj.name
            ? 'bg-emerald-950/40 border-emerald-500/80 shadow-md shadow-emerald-500/10'
            : 'bg-slate-950/40 border-slate-800/80 hover:border-slate-700 hover:bg-slate-800/30'"
        >
          <!-- Active Selection Indicator -->
          <div
            v-if="explorationStore.selectedObject?.name === obj.name"
            class="absolute top-0 right-0 w-12 h-12 overflow-hidden"
          >
            <div class="bg-emerald-500 text-slate-950 transform rotate-45 translate-x-3 -translate-y-3 w-12 text-center text-[10px] font-bold py-0.5">
              ✓
            </div>
          </div>

          <div class="flex items-start justify-between pr-6">
            <div>
              <h4 class="text-base font-bold text-white flex items-center gap-2">
                <span>{{ obj.name }}</span>
                <span v-if="obj.name_en && obj.name_en !== obj.name" class="text-xs font-normal text-slate-400">
                  ({{ obj.name_en }})
                </span>
              </h4>
              <span class="inline-block px-2 py-0.5 rounded text-[11px] font-medium bg-slate-800 text-slate-300 mt-1">
                {{ obj.category }}
              </span>
            </div>
            <span class="text-xs font-semibold text-emerald-400">
              {{ Math.round(obj.confidence * 100) }}% aniqlik
            </span>
          </div>

          <p class="text-xs sm:text-sm text-slate-300 leading-relaxed">
            {{ obj.educational_hook }}
          </p>

          <!-- Subjects Tag Chips -->
          <div class="flex flex-wrap gap-1.5 mt-1">
            <span
              v-for="subj in obj.subjects"
              :key="subj"
              class="px-2 py-0.5 rounded-md text-[10px] font-semibold bg-slate-900 border border-slate-700/60 text-slate-300"
            >
              {{ subj }}
            </span>
          </div>
        </div>
      </div>

      <!-- Action Button -->
      <button
        @click="startLesson()"
        :disabled="explorationStore.isGeneratingLesson || !explorationStore.selectedObject"
        class="w-full py-3.5 px-6 rounded-xl bg-gradient-to-r from-emerald-500 via-teal-500 to-emerald-600 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-bold text-sm sm:text-base flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/25 active:scale-[0.99] transition-all disabled:opacity-50"
      >
        <Loader2Icon v-if="explorationStore.isGeneratingLesson" class="w-5 h-5 animate-spin" />
        <BookOpenIcon v-else class="w-5 h-5" />
        <span>{{ explorationStore.isGeneratingLesson ? t.lesson.generating : t.scanner.exploreBtn }}</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from '@/i18n'
import { useRouter } from 'vue-router'
import { useExplorationStore } from '@/stores/exploration'
import { useAuthStore } from '@/stores/auth'
import {
  Sparkles as SparklesIcon,
  BookOpen as BookOpenIcon,
  Loader2 as Loader2Icon
} from '@lucide/vue'

const { t, lang } = useI18n()
const router = useRouter()
const explorationStore = useExplorationStore()
const authStore = useAuthStore()

const startLesson = async () => {
  if (!explorationStore.selectedObject) return
  const lesson = await explorationStore.generateLessonForSelected(authStore.user, lang.value)
  if (lesson) {
    router.push({ name: 'Lesson', params: { id: lesson.id } })
  }
}
</script>
