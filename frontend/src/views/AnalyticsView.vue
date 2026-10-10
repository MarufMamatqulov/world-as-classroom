<template>
  <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
    <!-- Header -->
    <div class="rounded-3xl glass-panel bg-gradient-to-r from-emerald-950/40 via-slate-900 to-indigo-950/40 border border-slate-800 p-6 sm:p-8 shadow-2xl flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
      <div>
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-bold border border-emerald-500/20 mb-2">
          <ActivityIcon class="w-4 h-4 text-emerald-400" />
          <span>Ta'limiy Tahlil & AI Resurslari Nazorati</span>
        </div>
        <h1 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          Learning Analytics & Cost Monitoring
        </h1>
        <p class="text-xs sm:text-sm text-slate-300 max-w-xl">
          Talabaning o'quv faolligi, kashfiyotlar statistikasi va Gemini multimodal AI generatsiya xarajatlari hamda kesh samaradorligi real vaqtda.
        </p>
      </div>

      <button
        @click="loadData"
        class="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold flex items-center gap-2 border border-slate-700 transition-colors"
      >
        <RefreshCwIcon class="w-3.5 h-3.5 text-emerald-400" :class="{ 'animate-spin': loading }" />
        <span>Yangilash</span>
      </button>
    </div>

    <!-- Top Metric KPI Cards -->
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="p-5 rounded-2xl glass-panel bg-slate-900/80 border border-slate-800 space-y-2">
        <span class="text-xs font-bold text-slate-400 uppercase tracking-wider block">Kashfiyotlar</span>
        <div class="text-2xl sm:text-3xl font-black text-white">
          {{ overview?.student_stats.total_explorations || 0 }}
        </div>
        <span class="text-[11px] text-emerald-400">Jami ob'ektlar o'rganildi</span>
      </div>

      <div class="p-5 rounded-2xl glass-panel bg-slate-900/80 border border-slate-800 space-y-2">
        <span class="text-xs font-bold text-slate-400 uppercase tracking-wider block">Viktorina Natijasi</span>
        <div class="text-2xl sm:text-3xl font-black text-cyan-400">
          {{ overview?.student_stats.average_quiz_score || 0 }}%
        </div>
        <span class="text-[11px] text-slate-400">{{ overview?.student_stats.total_quizzes_completed || 0 }} ta test topshirildi</span>
      </div>

      <div class="p-5 rounded-2xl glass-panel bg-slate-900/80 border border-slate-800 space-y-2">
        <span class="text-xs font-bold text-slate-400 uppercase tracking-wider block">Jami AI So'rovlari</span>
        <div class="text-2xl sm:text-3xl font-black text-indigo-400">
          {{ overview?.system_monitoring?.total_api_calls || 0 }}
        </div>
        <span class="text-[11px] text-indigo-300">
          {{ overview?.system_monitoring?.cache_hit_rate_pct || 0 }}% kesh tejamkorligi
        </span>
      </div>

      <div class="p-5 rounded-2xl glass-panel bg-slate-900/80 border border-slate-800 space-y-2">
        <span class="text-xs font-bold text-slate-400 uppercase tracking-wider block">AI Sarflangan Xarajat</span>
        <div class="text-2xl sm:text-3xl font-black text-amber-400">
          ${{ overview?.system_monitoring?.total_cost_usd?.toFixed(4) || '0.0000' }}
        </div>
        <span class="text-[11px] text-slate-400 font-mono">{{ overview?.system_monitoring?.total_tokens || 0 }} jami tokenlar</span>
      </div>
    </div>

    <!-- AI Cost & Performance Telemetry Card -->
    <div class="rounded-2xl glass-panel bg-slate-900/90 border border-slate-800 p-6 space-y-5">
      <div class="flex items-center justify-between border-b border-slate-800 pb-3">
        <div class="flex items-center gap-2">
          <CpuIcon class="w-5 h-5 text-emerald-400" />
          <h2 class="text-base sm:text-lg font-bold text-white">
            AI Cost Monitoring & Cache Efficiency (Google Gemini 2.5 Flash)
          </h2>
        </div>
        <span class="px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-mono font-bold border border-emerald-500/20">
          Avg {{ overview?.system_monitoring?.avg_latency_ms || 0 }} ms
        </span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
        <div class="p-4 rounded-xl bg-slate-950 border border-slate-800/80 space-y-1">
          <span class="text-slate-400 font-semibold block">Prompt (Kirish) Tokenlar:</span>
          <span class="text-base font-bold text-white font-mono">{{ overview?.system_monitoring?.total_prompt_tokens || 0 }}</span>
          <span class="text-[10px] text-slate-400 block">$0.075 / 1M token stavkasi</span>
        </div>

        <div class="p-4 rounded-xl bg-slate-950 border border-slate-800/80 space-y-1">
          <span class="text-slate-400 font-semibold block">Completion (Chiqish) Tokenlar:</span>
          <span class="text-base font-bold text-white font-mono">{{ overview?.system_monitoring?.total_completion_tokens || 0 }}</span>
          <span class="text-[10px] text-slate-400 block">$0.30 / 1M token stavkasi</span>
        </div>

        <div class="p-4 rounded-xl bg-slate-950 border border-slate-800/80 space-y-1">
          <span class="text-slate-400 font-semibold block">Kesh Hitlar (0$ Xarajat):</span>
          <span class="text-base font-bold text-emerald-400 font-mono">{{ overview?.system_monitoring?.cache_hits || 0 }} ta so'rov</span>
          <span class="text-[10px] text-emerald-400 block">Keshdan o'qilganda $0 sarflandi</span>
        </div>
      </div>

      <!-- Live Requests Table -->
      <div class="space-y-3 pt-2">
        <h3 class="text-xs font-bold text-slate-300 uppercase tracking-wider">
          So'nggi AI So'rovlari Tarixi (Telemetry Logs):
        </h3>
        <div class="overflow-x-auto">
          <table class="w-full text-left text-xs text-slate-300 border-collapse">
            <thead>
              <tr class="border-b border-slate-800 text-slate-400 font-semibold text-[11px]">
                <th class="py-2.5 px-3">Endpoint</th>
                <th class="py-2.5 px-3">Model</th>
                <th class="py-2.5 px-3">Tokens</th>
                <th class="py-2.5 px-3">Narxi (USD)</th>
                <th class="py-2.5 px-3">Kesh</th>
                <th class="py-2.5 px-3">Kechikish</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-800/60 font-mono text-[11px]">
              <tr
                v-for="(log, idx) in overview?.system_monitoring?.recent_logs"
                :key="idx"
                class="hover:bg-slate-800/40"
              >
                <td class="py-2 px-3 font-semibold text-slate-200">{{ log.endpoint }}</td>
                <td class="py-2 px-3 text-slate-400">{{ log.model_name }}</td>
                <td class="py-2 px-3">{{ log.prompt_tokens + log.completion_tokens }}</td>
                <td class="py-2 px-3 text-amber-400">${{ log.estimated_cost_usd.toFixed(6) }}</td>
                <td class="py-2 px-3">
                  <span
                    class="px-2 py-0.5 rounded text-[10px] font-bold"
                    :class="log.cache_hit ? 'bg-emerald-500/20 text-emerald-300' : 'bg-slate-800 text-slate-400'"
                  >
                    {{ log.cache_hit ? 'HIT' : 'MISS' }}
                  </span>
                </td>
                <td class="py-2 px-3 text-slate-400">{{ log.latency_ms }} ms</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api, type AnalyticsOverview } from '@/api/client'
import {
  Activity as ActivityIcon,
  RefreshCw as RefreshCwIcon,
  Cpu as CpuIcon
} from '@lucide/vue'

const loading = ref(true)
const overview = ref<AnalyticsOverview | null>(null)

const loadData = async () => {
  loading.value = true
  try {
    const res = await api.getAnalyticsOverview()
    overview.value = res
  } catch (err) {
    console.error('Failed to load analytics overview:', err)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>
