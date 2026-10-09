<template>
  <div v-if="modules && modules.length > 0" class="w-full">
    <!-- Subject Selection Tabs -->
    <div class="flex items-center gap-2 overflow-x-auto pb-3 mb-6 scrollbar-thin">
      <button
        v-for="mod in modules"
        :key="mod.subject"
        @click="activeSubject = mod.subject"
        class="flex items-center gap-2 px-4 py-2.5 rounded-xl font-semibold text-xs sm:text-sm whitespace-nowrap transition-all border"
        :class="activeSubject === mod.subject
          ? 'bg-emerald-500 text-slate-950 border-emerald-400 shadow-lg shadow-emerald-500/25 scale-105'
          : 'bg-slate-900/80 text-slate-300 border-slate-800 hover:border-slate-700 hover:text-white'"
      >
        <component :is="getSubjectIcon(mod.subject)" class="w-4 h-4" />
        <span>{{ getSubjectName(mod.subject) }}</span>
      </button>
    </div>

    <!-- Active Subject Module Content -->
    <div v-if="currentModule" class="glass-panel rounded-3xl p-6 sm:p-8 border border-slate-800 bg-slate-900/90 shadow-2xl relative overflow-hidden">
      <!-- Glow background accent -->
      <div class="absolute -top-24 -right-24 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>

      <div class="flex items-center justify-between mb-6 pb-4 border-b border-slate-800">
        <div>
          <span class="text-xs font-bold uppercase tracking-wider text-emerald-400">
            {{ getSubjectName(currentModule.subject) }}
          </span>
          <h3 class="text-xl sm:text-2xl font-bold text-white mt-1">
            {{ currentModule.title }}
          </h3>
        </div>
        <div class="w-12 h-12 rounded-2xl bg-emerald-500/15 border border-emerald-500/30 flex items-center justify-center text-emerald-400 shadow-inner">
          <component :is="getSubjectIcon(currentModule.subject)" class="w-6 h-6" />
        </div>
      </div>

      <!-- Concepts List -->
      <div class="space-y-6">
        <div
          v-for="(c, idx) in currentModule.concepts"
          :key="idx"
          class="bg-slate-950/60 rounded-2xl p-5 border border-slate-800/80 hover:border-slate-700/80 transition-colors"
        >
          <h4 class="text-base sm:text-lg font-bold text-slate-100 flex items-center gap-2">
            <span class="w-6 h-6 rounded-lg bg-emerald-500/20 text-emerald-400 text-xs flex items-center justify-center font-bold">
              {{ idx + 1 }}
            </span>
            <span>{{ c.headline }}</span>
          </h4>

          <p class="text-sm sm:text-base text-slate-300 mt-3 leading-relaxed">
            {{ c.explanation }}
          </p>

          <!-- Mathematical / Chemical Formula -->
          <div v-if="c.formula" class="mt-4 p-3.5 rounded-xl bg-slate-900/90 border border-emerald-500/30 flex items-center justify-between flex-wrap gap-2">
            <div class="flex items-center gap-2">
              <span class="text-[11px] font-bold uppercase tracking-wider text-emerald-400">Formula:</span>
              <code class="font-mono text-sm sm:text-base font-semibold text-emerald-300">
                {{ c.formula }}
              </code>
            </div>
          </div>

          <!-- Real World Example -->
          <div v-if="c.real_world_example" class="mt-3.5 flex items-start gap-2.5 text-xs sm:text-sm text-slate-400 bg-slate-900/40 p-3 rounded-xl border border-slate-800/60">
            <LightbulbIcon class="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
            <div>
              <strong class="text-slate-300">Hayotiy misol:</strong> {{ c.real_world_example }}
            </div>
          </div>
        </div>
      </div>

      <!-- Industrial & Space Connection Box -->
      <div v-if="currentModule.real_world_connection" class="mt-6 p-5 rounded-2xl bg-gradient-to-r from-emerald-950/40 via-teal-950/20 to-slate-900 border border-emerald-500/30 flex items-start gap-3.5">
        <RocketIcon class="w-6 h-6 text-emerald-400 shrink-0 mt-0.5" />
        <div>
          <h5 class="text-sm font-bold text-emerald-300 mb-1">
            Zamonaviy Texnologiyalar va Sanoatdagi O'rni
          </h5>
          <p class="text-xs sm:text-sm text-slate-300 leading-relaxed">
            {{ currentModule.real_world_connection }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import { useI18n } from '@/i18n'
import type { SubjectModule } from '@/api/client'
import {
  Atom as AtomIcon,
  Calculator as CalculatorIcon,
  HeartPulse as HeartPulseIcon,
  FlaskConical as FlaskConicalIcon,
  Landmark as LandmarkIcon,
  Cpu as CpuIcon,
  BookOpen as BookOpenIcon,
  Lightbulb as LightbulbIcon,
  Rocket as RocketIcon
} from '@lucide/vue'

const props = defineProps<{
  modules: SubjectModule[]
}>()

const { t } = useI18n()
const activeSubject = ref<string>(props.modules[0]?.subject || 'Physics')

watch(
  () => props.modules,
  (newMods) => {
    if (newMods && newMods.length > 0) {
      activeSubject.value = newMods[0].subject
    }
  },
  { immediate: true }
)

const currentModule = computed(() => {
  return props.modules.find(m => m.subject.toLowerCase() === activeSubject.value.toLowerCase()) || props.modules[0]
})

const getSubjectName = (subjectKey: string) => {
  const norm = subjectKey.toLowerCase()
  if (norm.includes('physic') || norm.includes('fizik')) return t.value.subjects.Physics
  if (norm.includes('math') || norm.includes('matem')) return t.value.subjects.Mathematics
  if (norm.includes('bio')) return t.value.subjects.Biology
  if (norm.includes('chem') || norm.includes('kimyo')) return t.value.subjects.Chemistry
  if (norm.includes('hist') || norm.includes('tarix')) return t.value.subjects.History
  if (norm.includes('tech') || norm.includes('texno')) return t.value.subjects.Technology
  return subjectKey
}

const getSubjectIcon = (subjectKey: string) => {
  const norm = subjectKey.toLowerCase()
  if (norm.includes('physic') || norm.includes('fizik')) return AtomIcon
  if (norm.includes('math') || norm.includes('matem')) return CalculatorIcon
  if (norm.includes('bio')) return HeartPulseIcon
  if (norm.includes('chem') || norm.includes('kimyo')) return FlaskConicalIcon
  if (norm.includes('hist') || norm.includes('tarix')) return LandmarkIcon
  if (norm.includes('tech') || norm.includes('texno')) return CpuIcon
  return BookOpenIcon
}
</script>
