<template>
  <div class="w-full max-w-4xl mx-auto mt-10">
    <div class="text-center mb-6">
      <h3 class="text-lg sm:text-xl font-bold text-white flex items-center justify-center gap-2">
        <SparklesIcon class="w-5 h-5 text-emerald-400" />
        <span>{{ t.scanner.sampleTitle }}</span>
      </h3>
      <p class="text-xs sm:text-sm text-slate-400 mt-1">
        {{ t.scanner.sampleSubtitle }}
      </p>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div
        v-for="sample in samples"
        :key="sample.id"
        @click="selectSample(sample)"
        class="glass-card glass-card-hover rounded-2xl p-5 cursor-pointer relative overflow-hidden flex flex-col justify-between group border border-slate-800"
      >
        <div class="flex items-center justify-between mb-3">
          <div class="w-12 h-12 rounded-xl bg-slate-900 border border-slate-700/60 flex items-center justify-center text-emerald-400 group-hover:scale-110 transition-transform">
            <component :is="getSampleIcon(sample.icon)" class="w-6 h-6" />
          </div>
          <span class="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-slate-800 text-slate-300">
            {{ sample.category }}
          </span>
        </div>

        <div>
          <h4 class="font-bold text-white text-base group-hover:text-emerald-300 transition-colors">
            {{ sample.name }}
          </h4>
          <p class="text-xs text-slate-400 mt-1.5 line-clamp-2 leading-relaxed">
            {{ sample.hook }}
          </p>
        </div>

        <div class="mt-4 pt-3 border-t border-slate-800/80 flex items-center justify-between">
          <div class="flex gap-1">
            <span
              v-for="subj in sample.subjects.slice(0, 2)"
              :key="subj"
              class="text-[9px] px-1.5 py-0.5 rounded bg-slate-900 text-slate-300 font-medium"
            >
              {{ subj }}
            </span>
          </div>
          <span class="text-xs font-bold text-emerald-400 flex items-center gap-1 group-hover:translate-x-1 transition-transform">
            <span>{{ t.scanner.exploreBtn }}</span>
            <span>→</span>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from '@/i18n'
import { useExplorationStore } from '@/stores/exploration'
import { useAuthStore } from '@/stores/auth'
import { api } from '@/api/client'
import {
  Sparkles as SparklesIcon,
  Bike as BikeIcon,
  Leaf as LeafIcon,
  Clock as ClockIcon,
  Search as SearchIcon,
  BookOpen as BookOpenIcon
} from '@lucide/vue'

const { t, lang } = useI18n()
const router = useRouter()
const explorationStore = useExplorationStore()
const authStore = useAuthStore()

const samples = ref<any[]>([])

const fetchSamples = async () => {
  try {
    samples.value = await api.getSamples(lang.value)
  } catch (e) {
    console.error('Failed to load samples:', e)
  }
}

onMounted(fetchSamples)
watch(lang, fetchSamples)

const getSampleIcon = (iconName: string) => {
  switch (iconName) {
    case 'Bike': return BikeIcon
    case 'Leaf': return LeafIcon
    case 'Clock': return ClockIcon
    case 'Search': return SearchIcon
    default: return BookOpenIcon
  }
}

const selectSample = async (sample: any) => {
  explorationStore.setManualSample(sample)
  const lesson = await explorationStore.generateLessonForSelected(authStore.user, lang.value)
  if (lesson) {
    router.push({ name: 'Lesson', params: { id: lesson.id } })
  }
}
</script>
