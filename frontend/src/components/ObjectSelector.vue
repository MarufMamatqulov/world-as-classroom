<template>
  <div v-if="explorationStore.detectedObjects.length > 0" class="w-full max-w-2xl mx-auto mt-6">
    <div class="glass-panel rounded-2xl p-6 border border-slate-800 bg-slate-900/80 shadow-xl space-y-6">
      <!-- Section Header -->
      <div class="flex items-center justify-between border-b border-slate-800/80 pb-4">
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
      <div class="space-y-3">
        <div
          v-for="(obj, idx) in explorationStore.detectedObjects"
          :key="idx"
          @click="explorationStore.selectedObject = obj"
          class="p-4 rounded-xl border transition-all cursor-pointer relative overflow-hidden flex flex-col gap-2.5"
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

          <div class="flex items-start justify-between pr-8">
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
            <div class="flex flex-col items-end gap-1">
              <span class="text-xs font-semibold text-emerald-400">
                {{ Math.round(obj.confidence * 100) }}% aniqlik
              </span>
              <button
                @click.stop="openEditModal(obj)"
                class="px-2 py-0.5 rounded bg-slate-800/80 hover:bg-slate-700 text-[10px] font-medium text-slate-300 hover:text-emerald-400 border border-slate-700 flex items-center gap-1 transition-colors"
                title="Nomini o'zgartirish"
              >
                <Edit3Icon class="w-3 h-3 text-emerald-400" />
                <span>To'g'rilash</span>
              </button>
            </div>
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

      <!-- Module 2: Interactive Learning Customization Options -->
      <div class="p-4 rounded-xl bg-slate-950/60 border border-slate-800 space-y-4">
        <div>
          <label class="block text-xs font-bold text-slate-300 mb-2 flex items-center gap-1.5">
            <TargetIcon class="w-3.5 h-3.5 text-emerald-400" />
            <span>Asosiy yo'nalish fani (Primary Subject Focus):</span>
          </label>
          <div class="grid grid-cols-3 sm:grid-cols-6 gap-1.5">
            <button
              v-for="subj in subjectsList"
              :key="subj.key"
              type="button"
              @click="explorationStore.selectedSubject = subj.key"
              class="py-2 px-1 text-center rounded-lg text-xs font-semibold transition-all border"
              :class="explorationStore.selectedSubject === subj.key
                ? 'bg-emerald-500/20 border-emerald-400 text-emerald-300 font-bold shadow-sm'
                : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-white hover:bg-slate-800'"
            >
              {{ subj.label }}
            </button>
          </div>
        </div>

        <div>
          <label class="block text-xs font-bold text-slate-300 mb-2 flex items-center gap-1.5">
            <SlidersIcon class="w-3.5 h-3.5 text-cyan-400" />
            <span>Murakkablik darajasi (Difficulty Level):</span>
          </label>
          <div class="grid grid-cols-3 gap-2">
            <button
              v-for="lvl in difficultyLevels"
              :key="lvl.key"
              type="button"
              @click="explorationStore.selectedDifficulty = lvl.key"
              class="py-2 px-2 text-center rounded-lg text-xs font-semibold transition-all border flex flex-col items-center gap-0.5"
              :class="explorationStore.selectedDifficulty === lvl.key
                ? 'bg-cyan-500/20 border-cyan-400 text-cyan-200 font-bold shadow-sm'
                : 'bg-slate-900 border-slate-800 text-slate-400 hover:text-white hover:bg-slate-800'"
            >
              <span>{{ lvl.label }}</span>
              <span class="text-[10px] text-slate-400 font-normal">{{ lvl.desc }}</span>
            </button>
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
        <span>{{ explorationStore.isGeneratingLesson ? t.lesson.generating : 'Interaktiv Darsni Boshlash (+30 XP)' }}</span>
      </button>
    </div>

    <!-- Edit/Correct Modal -->
    <div
      v-if="isEditing"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm"
      @click.self="isEditing = false"
    >
      <div class="w-full max-w-md rounded-2xl glass-panel bg-slate-900 border border-slate-700 p-6 shadow-2xl space-y-4">
        <h4 class="text-base font-bold text-white flex items-center gap-2">
          <Edit3Icon class="w-4 h-4 text-emerald-400" />
          <span>Ob'ekt Nomini O'zgartirish</span>
        </h4>
        <p class="text-xs text-slate-300">
          Ushbu ob'ekt nomini dars uchun yanada aniqlashtiring:
        </p>
        <input
          v-model="editNameInput"
          type="text"
          class="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm focus:border-emerald-500 focus:outline-none"
          @keyup.enter="saveEdit"
        />
        <div class="flex justify-end gap-2 pt-2">
          <button
            @click="isEditing = false"
            class="px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white bg-slate-800"
          >
            Bekor qilish
          </button>
          <button
            @click="saveEdit"
            class="px-4 py-2 rounded-xl text-xs font-bold text-slate-950 bg-emerald-500 hover:bg-emerald-400"
          >
            Tasdiqlash
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from '@/i18n'
import { useRouter } from 'vue-router'
import { useExplorationStore } from '@/stores/exploration'
import { useAuthStore } from '@/stores/auth'
import type { DetectedObject } from '@/api/client'
import {
  Sparkles as SparklesIcon,
  BookOpen as BookOpenIcon,
  Loader2 as Loader2Icon,
  Target as TargetIcon,
  Sliders as SlidersIcon,
  Edit3 as Edit3Icon
} from '@lucide/vue'

const { t, lang } = useI18n()
const router = useRouter()
const explorationStore = useExplorationStore()
const authStore = useAuthStore()

const isEditing = ref(false)
const editNameInput = ref('')
const targetEditObj = ref<DetectedObject | null>(null)

const subjectsList = [
  { key: 'Physics', label: 'Fizika' },
  { key: 'Mathematics', label: 'Matematika' },
  { key: 'Biology', label: 'Biologiya' },
  { key: 'Chemistry', label: 'Kimyo' },
  { key: 'Technology', label: 'Texnologiya' },
  { key: 'History', label: 'Tarix' },
]

const difficultyLevels = [
  { key: 'beginner', label: 'Boshlang\'ich', desc: 'Sodda & qiziqarli' },
  { key: 'intermediate', label: 'O\'rta', desc: 'Maktab dasturi' },
  { key: 'advanced', label: 'Mukammal', desc: 'Formulalar & chuqur' },
]

const openEditModal = (obj: DetectedObject) => {
  targetEditObj.value = obj
  editNameInput.value = obj.name
  isEditing.value = true
}

const saveEdit = async () => {
  if (!editNameInput.value.trim()) return
  await explorationStore.correctSelectedObject(editNameInput.value.trim(), undefined, lang.value)
  isEditing.value = false
}

const startLesson = async () => {
  if (!explorationStore.selectedObject) return
  const lesson = await explorationStore.generateLessonForSelected(authStore.user, lang.value)
  if (lesson) {
    router.push({ name: 'Lesson', params: { id: lesson.id } })
  }
}
</script>
