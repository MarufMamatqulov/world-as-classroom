<template>
  <div v-if="experiments && experiments.length > 0" class="w-full">
    <div
      v-for="(exp, idx) in experiments"
      :key="idx"
      class="glass-panel rounded-3xl p-6 sm:p-8 border border-slate-800 bg-slate-900/90 shadow-2xl relative overflow-hidden"
    >
      <!-- Header -->
      <div class="flex items-start justify-between gap-4 mb-6 pb-4 border-b border-slate-800">
        <div>
          <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-amber-500/15 text-amber-400 border border-amber-500/30">
            <FlaskConicalIcon class="w-3.5 h-3.5" />
            <span>{{ t.lesson.tryExperiment }}</span>
          </span>
          <h3 class="text-xl sm:text-2xl font-bold text-white mt-2">
            {{ exp.title }}
          </h3>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Materials List -->
        <div class="md:col-span-1 bg-slate-950/60 p-5 rounded-2xl border border-slate-800/80">
          <h4 class="text-sm font-bold text-slate-200 flex items-center gap-2 mb-3">
            <CheckCircle2Icon class="w-4 h-4 text-emerald-400" />
            <span>{{ t.lesson.experimentMaterials }}</span>
          </h4>
          <ul class="space-y-2">
            <li
              v-for="(item, mIdx) in exp.materials"
              :key="mIdx"
              class="flex items-center gap-2 text-xs sm:text-sm text-slate-300"
            >
              <input
                type="checkbox"
                class="rounded border-slate-700 bg-slate-800 text-emerald-500 focus:ring-emerald-500 cursor-pointer"
              />
              <span>{{ item }}</span>
            </li>
          </ul>
        </div>

        <!-- Steps -->
        <div class="md:col-span-2 space-y-4">
          <h4 class="text-sm font-bold text-slate-200 flex items-center gap-2">
            <ListOrderedIcon class="w-4 h-4 text-emerald-400" />
            <span>{{ t.lesson.experimentSteps }}</span>
          </h4>

          <ol class="space-y-3">
            <li
              v-for="(step, sIdx) in exp.steps"
              :key="sIdx"
              class="flex items-start gap-3 bg-slate-950/40 p-3.5 rounded-xl border border-slate-800/60 text-xs sm:text-sm text-slate-300"
            >
              <span class="w-6 h-6 rounded-full bg-emerald-500/20 text-emerald-400 font-bold text-xs flex items-center justify-center shrink-0 mt-0.5">
                {{ sIdx + 1 }}
              </span>
              <span class="leading-relaxed">{{ step }}</span>
            </li>
          </ol>

          <!-- Science behind it -->
          <div class="mt-5 p-4 rounded-xl bg-slate-900 border border-slate-800 flex items-start gap-3">
            <SparklesIcon class="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
            <div>
              <h5 class="text-xs font-bold uppercase tracking-wider text-emerald-400 mb-1">
                {{ t.lesson.scienceBehind }}
              </h5>
              <p class="text-xs sm:text-sm text-slate-300 leading-relaxed">
                {{ exp.science_behind_it }}
              </p>
            </div>
          </div>

          <!-- Safety Note -->
          <div v-if="exp.safety_note" class="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center gap-2.5 text-xs text-amber-300">
            <ShieldAlertIcon class="w-4 h-4 text-amber-400 shrink-0" />
            <span><strong class="font-bold">{{ t.lesson.safetyNote }}:</strong> {{ exp.safety_note }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from '@/i18n'
import type { LessonExperiment } from '@/api/client'
import {
  FlaskConical as FlaskConicalIcon,
  CheckCircle2 as CheckCircle2Icon,
  ListOrdered as ListOrderedIcon,
  Sparkles as SparklesIcon,
  ShieldAlert as ShieldAlertIcon
} from '@lucide/vue'

defineProps<{
  experiments: LessonExperiment[]
}>()

const { t } = useI18n()
</script>
