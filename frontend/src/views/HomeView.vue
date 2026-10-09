<template>
  <div class="min-h-screen pb-24">
    <!-- Hero Section -->
    <section class="relative overflow-hidden pt-12 pb-20 sm:pt-20 sm:pb-28">
      <!-- Background Ambient Glows -->
      <div class="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-emerald-500/15 rounded-full blur-[120px] pointer-events-none"></div>
      <div class="absolute top-1/3 left-1/3 w-[300px] h-[300px] bg-cyan-500/10 rounded-full blur-[100px] pointer-events-none"></div>

      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
        <!-- Badge -->
        <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full glass-panel border border-emerald-500/30 text-emerald-400 text-xs font-bold uppercase tracking-wider mb-6 shadow-md shadow-emerald-500/10">
          <SparklesIcon class="w-4 h-4 animate-spin-slow" />
          <span>Google Gemini Multimodal AI Ta'lim Platformasi</span>
        </div>

        <!-- Main Title -->
        <h1 class="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-white max-w-4xl mx-auto leading-tight sm:leading-none">
          Olam — Sizning
          <span class="bg-gradient-to-r from-emerald-400 via-teal-300 to-cyan-400 bg-clip-text text-transparent">
            Sinfxonangiz
          </span>
        </h1>

        <!-- Subtitle -->
        <p class="mt-6 text-base sm:text-xl text-slate-300 max-w-2xl mx-auto font-normal leading-relaxed">
          Kamerangizni atrofingizdagi istalgan buyumga qarating — sun'iy intellekt uni taniydi va Fizika, Kimyo, Biologiya hamda Matematika fanlari bo'yicha interaktiv dars yaratadi!
        </p>

        <!-- CTA Action Buttons -->
        <div class="mt-8 sm:mt-10 flex flex-wrap items-center justify-center gap-4">
          <router-link
            to="/scanner"
            class="px-8 py-4 rounded-2xl bg-gradient-to-r from-emerald-500 via-teal-500 to-emerald-600 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-extrabold text-base sm:text-lg flex items-center gap-3 shadow-xl shadow-emerald-500/25 active:scale-95 transition-all group"
          >
            <CameraIcon class="w-6 h-6 group-hover:scale-110 transition-transform" />
            <span>Kamerani Ochish & Skanerlash</span>
          </router-link>

          <router-link
            to="/dashboard"
            class="px-7 py-4 rounded-2xl glass-card hover:bg-slate-800/80 border border-slate-700 text-slate-200 font-bold text-base flex items-center gap-2 active:scale-95 transition-all"
          >
            <LayoutDashboardIcon class="w-5 h-5 text-emerald-400" />
            <span>Mening Natijalarim</span>
          </router-link>
        </div>

        <!-- Real-world Workflow Pill Steps -->
        <div class="mt-14 max-w-3xl mx-auto grid grid-cols-2 sm:grid-cols-4 gap-3 text-left">
          <div class="glass-panel p-3.5 rounded-xl border border-slate-800/80">
            <span class="text-[10px] font-bold text-emerald-400 uppercase">1-qadam</span>
            <p class="text-xs font-semibold text-white mt-1">Kamerada suratga oling</p>
          </div>
          <div class="glass-panel p-3.5 rounded-xl border border-slate-800/80">
            <span class="text-[10px] font-bold text-teal-400 uppercase">2-qadam</span>
            <p class="text-xs font-semibold text-white mt-1">AI ob'ektni aniqlaydi</p>
          </div>
          <div class="glass-panel p-3.5 rounded-xl border border-slate-800/80">
            <span class="text-[10px] font-bold text-cyan-400 uppercase">3-qadam</span>
            <p class="text-xs font-semibold text-white mt-1">Fanlararo dars o'rganing</p>
          </div>
          <div class="glass-panel p-3.5 rounded-xl border border-slate-800/80">
            <span class="text-[10px] font-bold text-emerald-400 uppercase">4-qadam</span>
            <p class="text-xs font-semibold text-white mt-1">Viktorinada sinang</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Curated Educational Samples Showcase -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 border-t border-slate-800/80">
      <SampleGallery />
    </section>

    <!-- Core Features Grid -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div class="text-center mb-12">
        <h2 class="text-2xl sm:text-3xl font-extrabold text-white">
          Zamonaviy AI Ta'lim Imkoniyatlari
        </h2>
        <p class="text-xs sm:text-sm text-slate-400 max-w-md mx-auto mt-2">
          Har bir o'quvchi uchun shaxsiylashtirilgan fanlararo o'quv muhiti
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Feature 1 -->
        <div class="glass-card rounded-2xl p-6 border border-slate-800">
          <div class="w-12 h-12 rounded-xl bg-emerald-500/15 border border-emerald-500/30 flex items-center justify-center text-emerald-400 mb-4">
            <CameraIcon class="w-6 h-6" />
          </div>
          <h3 class="text-lg font-bold text-white mb-2">Ko'p Ob'ektli AI Skaner</h3>
          <p class="text-xs sm:text-sm text-slate-400 leading-relaxed">
            Kadrda velosiped, zanjir, g'ildirak yoki o'simlik barglarini bir vaqtda aniqlaydi va o'quvchiga tanlash imkonini beradi.
          </p>
        </div>

        <!-- Feature 2 -->
        <div class="glass-card rounded-2xl p-6 border border-slate-800">
          <div class="w-12 h-12 rounded-xl bg-teal-500/15 border border-teal-500/30 flex items-center justify-center text-teal-400 mb-4">
            <AtomIcon class="w-6 h-6" />
          </div>
          <h3 class="text-lg font-bold text-white mb-2">Fanlararo Darslar</h3>
          <p class="text-xs sm:text-sm text-slate-400 leading-relaxed">
            Fizika (Nyuton qonunlari), Kimyo (qotishmalar), Biologiya (inson mushaklari), Matematika va Texnologiya bog'lanishi.
          </p>
        </div>

        <!-- Feature 3 -->
        <div class="glass-card rounded-2xl p-6 border border-slate-800">
          <div class="w-12 h-12 rounded-xl bg-cyan-500/15 border border-cyan-500/30 flex items-center justify-center text-cyan-400 mb-4">
            <BotIcon class="w-6 h-6" />
          </div>
          <h3 class="text-lg font-bold text-white mb-2">Interaktiv AI Ustoz & Ovoz</h3>
          <p class="text-xs sm:text-sm text-slate-400 leading-relaxed">
            O'quvchi savollariga kontekstdan kelib chiqib javob beradi va darslarni ovozli ravishda eshittiradi.
          </p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import SampleGallery from '@/components/SampleGallery.vue'
import {
  Sparkles as SparklesIcon,
  Camera as CameraIcon,
  LayoutDashboard as LayoutDashboardIcon,
  Atom as AtomIcon,
  Bot as BotIcon
} from '@lucide/vue'
</script>
