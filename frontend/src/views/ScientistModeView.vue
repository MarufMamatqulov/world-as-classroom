<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
    <!-- Header Hero Banner -->
    <div class="rounded-3xl glass-panel bg-gradient-to-r from-cyan-950/40 via-slate-900 to-indigo-950/40 border border-cyan-500/30 p-6 sm:p-8 shadow-2xl space-y-3">
      <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/20 text-cyan-300 text-xs font-bold border border-cyan-500/30">
        <FlaskConicalIcon class="w-4 h-4 text-cyan-400" />
        <span>Ilmiy Metod Laboratoriyasi</span>
      </div>
      <h1 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
        AI Scientist Mode (Olim Rejimi)
      </h1>
      <p class="text-xs sm:text-sm text-slate-300 max-w-2xl leading-relaxed">
        Oddiy savol-javobdan yuqori darajaga chiqing. Kuzating, gipoteza tuzing, xavfsiz uy tajribasini loyihalashtiring va ilmiy xulosalarga erishing.
      </p>
    </div>

    <!-- Inquiry Input Form -->
    <div class="rounded-2xl glass-panel bg-slate-900/90 border border-slate-800 p-6 sm:p-8 shadow-xl space-y-6">
      <h2 class="text-base sm:text-lg font-bold text-white flex items-center gap-2 border-b border-slate-800 pb-3">
        <SearchIcon class="w-5 h-5 text-cyan-400" />
        <span>1. Ilmiy Gipoteza Shakllantirish</span>
      </h2>

      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div>
          <label class="block text-xs font-bold text-slate-300 mb-1.5">
            O'rganilayotgan ob'ekt nomi:
          </label>
          <input
            v-model="objectName"
            type="text"
            placeholder="Masalan: Velosiped zanjiri, Kvars soat, Lupa"
            class="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm focus:border-cyan-500 focus:outline-none"
          />
        </div>

        <div>
          <label class="block text-xs font-bold text-slate-300 mb-1.5">
            Fan Sohasi:
          </label>
          <select
            v-model="domain"
            class="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm focus:border-cyan-500 focus:outline-none"
          >
            <option value="Physics">Fizika & Mexanika</option>
            <option value="Optics">Optika & Nur</option>
            <option value="Biology">Biologiya & Tirik Tabiat</option>
            <option value="Chemistry">Kimyo & Materiallar</option>
            <option value="Thermodynamics">Termodinamika</option>
            <option value="Technology">Muhandislik & Texnologiya</option>
          </select>
        </div>
      </div>

      <!-- Observation Box -->
      <div>
        <label class="block text-xs font-bold text-slate-300 mb-1.5">
          Kuzatuv (Siz nimani ko'rdingiz va qanday xususiyatni payqadingiz?):
        </label>
        <textarea
          v-model="observation"
          rows="3"
          placeholder="Masalan: Velosiped kichik tishli g'ildiragiga zanjir tushganda orqa g'ildirak juda tez aylanmoqda, lekin tepalikka chiqishda pedal bosish og'irlashyapti..."
          class="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm focus:border-cyan-500 focus:outline-none leading-relaxed"
        ></textarea>
      </div>

      <!-- Hypothesis Box -->
      <div>
        <div class="flex items-center justify-between mb-1.5">
          <label class="block text-xs font-bold text-slate-300">
            Sizning Gipotezangiz (Agar X bo'lsa, unda Y bo'ladi):
          </label>
          <button
            @click="useHypothesisTemplate"
            class="text-[11px] text-cyan-400 hover:text-cyan-300 underline"
          >
            Namuna shablondan foydalanish
          </button>
        </div>
        <textarea
          v-model="hypothesis"
          rows="3"
          placeholder="Masalan: Agar orqa tishli g'ildirak diametri 2 marta kichraytirilsa, aylanma tezlik 2 marta oshadi, ammo talab qilinadigan kuch ham 2 marta ortadi."
          class="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm focus:border-cyan-500 focus:outline-none leading-relaxed"
        ></textarea>
      </div>

      <!-- Submit Inquiry Button -->
      <button
        @click="runInquiry"
        :disabled="loading || !objectName || !observation || !hypothesis"
        class="w-full py-3.5 px-6 rounded-xl bg-gradient-to-r from-cyan-500 via-teal-500 to-emerald-500 hover:from-cyan-400 hover:to-teal-400 text-slate-950 font-bold text-sm sm:text-base flex items-center justify-center gap-2 shadow-lg shadow-cyan-500/20 active:scale-[0.99] transition-all disabled:opacity-50"
      >
        <Loader2Icon v-if="loading" class="w-5 h-5 animate-spin" />
        <FlaskConicalIcon v-else class="w-5 h-5" />
        <span>{{ loading ? 'AI Bosh Olim tahlil qilmoqda...' : 'Gipotezani Sinash & Xavfsiz Tajriba Olish (+50 XP)' }}</span>
      </button>
    </div>

    <!-- AI Scientist Results Output -->
    <div v-if="result" class="space-y-6 animate-fade-in">
      <!-- Critique & Scientific Feedback -->
      <div class="rounded-2xl glass-panel bg-slate-900 border border-cyan-500/40 p-6 space-y-4">
        <div class="flex items-center justify-between">
          <h3 class="text-base font-bold text-white flex items-center gap-2">
            <CheckCircleIcon class="w-5 h-5 text-emerald-400" />
            <span>AI Bosh Olim Xulosasi</span>
          </h3>
          <span class="px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-300 text-xs font-bold border border-emerald-500/30">
            +{{ result.xp_awarded }} XP Berildi
          </span>
        </div>

        <p class="text-sm text-slate-200 leading-relaxed bg-slate-950/60 p-4 rounded-xl border border-slate-800">
          {{ result.hypothesis_critique }}
        </p>

        <!-- Scientific Principles -->
        <div>
          <span class="text-xs font-bold text-cyan-400 uppercase tracking-wider block mb-2">Asosiy Ilmiy Qonuniyatlar:</span>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="(p, i) in result.scientific_principles"
              :key="i"
              class="px-3 py-1 rounded-lg bg-slate-950 text-xs font-medium text-slate-300 border border-slate-800"
            >
              ⚛️ {{ p }}
            </span>
          </div>
        </div>
      </div>

      <!-- Safe DIY Household Experiment Plan -->
      <div class="rounded-2xl glass-panel bg-slate-900 border border-slate-800 p-6 space-y-5">
        <div class="flex items-center justify-between border-b border-slate-800 pb-3">
          <h3 class="text-base font-bold text-white flex items-center gap-2">
            <BeakerIcon class="w-5 h-5 text-emerald-400" />
            <span>{{ result.experiment_plan.title }}</span>
          </h3>
          <span class="px-2.5 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-bold border border-emerald-500/20">
            100% Xavfsiz Uy Tajribasi
          </span>
        </div>

        <!-- Materials -->
        <div>
          <h4 class="text-xs font-bold text-slate-300 mb-2">Kerakli xavfsiz materiallar:</h4>
          <ul class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs text-slate-300">
            <li
              v-for="(m, mi) in result.experiment_plan.materials"
              :key="mi"
              class="flex items-center gap-2 bg-slate-950 p-2.5 rounded-lg border border-slate-800"
            >
              <span class="w-1.5 h-1.5 rounded-full bg-cyan-400"></span>
              <span>{{ m }}</span>
            </li>
          </ul>
        </div>

        <!-- Steps -->
        <div>
          <h4 class="text-xs font-bold text-slate-300 mb-2">Tajriba qadamlari:</h4>
          <div class="space-y-2 text-xs text-slate-300">
            <div
              v-for="(step, si) in result.experiment_plan.steps"
              :key="si"
              class="p-3 rounded-xl bg-slate-950 border border-slate-800/80 leading-relaxed"
            >
              {{ step }}
            </div>
          </div>
        </div>

        <!-- Safety Advice -->
        <div class="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-200 text-xs space-y-1">
          <span class="font-bold flex items-center gap-1.5">
            <ShieldAlertIcon class="w-4 h-4 text-amber-400" />
            <span>Xavfsizlik yo'riqnomasi:</span>
          </span>
          <p>{{ result.experiment_plan.safety_guidelines }}</p>
        </div>

        <!-- Expected Observation -->
        <div class="p-3.5 rounded-xl bg-emerald-950/40 border border-emerald-500/30 text-emerald-200 text-xs space-y-1">
          <span class="font-bold">Kutilgan ilmiy natija:</span>
          <p>{{ result.experiment_plan.expected_observation }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { api, type ScientistInquiryResponse } from '@/api/client'
import confetti from 'canvas-confetti'
import {
  FlaskConical as FlaskConicalIcon,
  Search as SearchIcon,
  CheckCircle as CheckCircleIcon,
  Beaker as BeakerIcon,
  ShieldAlert as ShieldAlertIcon,
  Loader2 as Loader2Icon
} from '@lucide/vue'

const objectName = ref('Velosiped tishli uzatmasi')
const domain = ref('Physics')
const observation = ref('Pedal 1 marta aylanganda, kichik tishli g\'ildirak 3 marta aylanadi va velosiped tezlashadi.')
const hypothesis = ref('Agar oldingi va orqa tishli g\'ildiraklar tishlar soni nisbati 3:1 bo\'lsa, g\'ildirak burchak tezligi pedalga nisbatan 3 barobar katta bo\'ladi.')
const loading = ref(false)
const result = ref<ScientistInquiryResponse | null>(null)

const useHypothesisTemplate = () => {
  hypothesis.value = `Agar ${objectName.value || 'ob\'ekt'} ustidagi o'zgaruvchi parametr oshirilsa, natijada uning harakat/issiqlik ko'rsatkichi to'g'ri mutanosib ravishda o'zgaradi.`
}

const runInquiry = async () => {
  if (!objectName.value || !observation.value || !hypothesis.value) return
  loading.value = true
  result.value = null

  try {
    const res = await api.conductScientificInquiry({
      object_name: objectName.value,
      domain: domain.value,
      observation: observation.value,
      hypothesis: hypothesis.value,
      language: 'uz'
    })
    result.value = res

    confetti({
      particleCount: 70,
      spread: 60,
      origin: { y: 0.6 }
    })
  } catch (err) {
    console.error('Scientist inquiry error:', err)
  } finally {
    loading.value = false
  }
}
</script>
