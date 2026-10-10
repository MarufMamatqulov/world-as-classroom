<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/85 backdrop-blur-md transition-all"
    @click.self="closeModal"
  >
    <div class="relative w-full max-w-lg rounded-3xl overflow-hidden glass-panel border border-emerald-500/30 bg-slate-900/95 shadow-2xl p-6 sm:p-8 space-y-6 animate-scale-up">
      <!-- Modal Header -->
      <div class="flex items-center justify-between border-b border-slate-800 pb-4">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center">
            <Share2Icon class="w-4 h-4" />
          </div>
          <div>
            <h3 class="text-base font-bold text-white">Ilmiy Kashfiyot Kartasi</h3>
            <p class="text-xs text-slate-400">Xavfsiz, shaxsiy ma'lumotlarsiz ulashish kartasi</p>
          </div>
        </div>
        <button
          @click="closeModal"
          class="p-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
        >
          ✕
        </button>
      </div>

      <!-- Discovery Story Card (Preview) -->
      <div
        ref="cardElement"
        class="relative rounded-2xl overflow-hidden border border-emerald-400/50 bg-gradient-to-br from-slate-950 via-slate-900 to-emerald-950/40 p-6 shadow-2xl space-y-4"
      >
        <!-- Card Top Bar: Badge & Date -->
        <div class="flex items-center justify-between text-xs">
          <span class="px-2.5 py-1 rounded-full bg-emerald-500/20 text-emerald-300 font-bold border border-emerald-500/30 flex items-center gap-1.5">
            <SparklesIcon class="w-3.5 h-3.5 text-emerald-400" />
            <span>{{ cardData?.verified_badge || 'Haqiqiy Ilmiy Kashfiyot' }}</span>
          </span>
          <span class="text-slate-400 font-mono text-[11px]">{{ cardData?.discovery_date }}</span>
        </div>

        <!-- Object Hero Preview -->
        <div class="flex items-center gap-4 py-2">
          <div v-if="cardData?.image_thumbnail" class="w-20 h-20 rounded-2xl overflow-hidden border border-slate-700 flex-shrink-0 shadow-md">
            <img :src="cardData.image_thumbnail" alt="Object thumbnail" class="w-full h-full object-cover" />
          </div>
          <div v-else class="w-20 h-20 rounded-2xl bg-slate-800/80 border border-slate-700 flex items-center justify-center flex-shrink-0 text-emerald-400">
            <AtomIcon class="w-10 h-10" />
          </div>
          <div class="space-y-1">
            <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-800 text-emerald-400 border border-slate-700">
              {{ cardData?.primary_subject }} • {{ cardData?.category }}
            </span>
            <h4 class="text-xl font-extrabold text-white tracking-tight">
              {{ cardData?.object_name }}
            </h4>
            <p v-if="cardData?.object_name_en && cardData.object_name_en !== cardData.object_name" class="text-xs text-slate-400">
              {{ cardData.object_name_en }}
            </p>
          </div>
        </div>

        <!-- Core Insight & Formula -->
        <div class="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800/80 space-y-2">
          <p class="text-xs font-semibold text-slate-200 leading-relaxed">
            💡 {{ cardData?.core_discovery }}
          </p>
          <div v-if="cardData?.key_formula" class="inline-block px-3 py-1 rounded-lg bg-emerald-950/50 border border-emerald-500/30 text-emerald-300 font-mono text-xs font-bold">
            {{ cardData.key_formula }}
          </div>
        </div>

        <!-- Card Footer: Callsign & XP -->
        <div class="flex items-center justify-between pt-2 border-t border-slate-800/80">
          <div class="flex items-center gap-2">
            <div class="w-7 h-7 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-xs font-bold">
              ★
            </div>
            <span class="text-xs font-bold text-slate-300 font-mono">{{ cardData?.explorer_callsign }}</span>
          </div>
          <div class="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs font-extrabold">
            <span>+{{ cardData?.xp_earned }} XP</span>
          </div>
        </div>

        <!-- Watermark / Branding -->
        <div class="text-center pt-1 text-[10px] text-slate-500 tracking-wider uppercase font-semibold">
          World as a Classroom • Olam Sinfxonasi
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-wrap items-center justify-between gap-3 pt-2">
        <button
          @click="copyStoryText"
          class="flex-1 py-3 px-4 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold flex items-center justify-center gap-2 transition-all border border-slate-700"
        >
          <CopyIcon class="w-4 h-4 text-emerald-400" />
          <span>{{ copied ? 'Nusxa olindi!' : 'Matnni Nusxalash' }}</span>
        </button>

        <button
          @click="shareLink"
          class="flex-1 py-3 px-4 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 text-xs font-extrabold flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/20 transition-all"
        >
          <Share2Icon class="w-4 h-4" />
          <span>Ulashish (Share)</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { DiscoveryStoryCardResponse } from '@/api/client'
import {
  Share2 as Share2Icon,
  Sparkles as SparklesIcon,
  Atom as AtomIcon,
  Copy as CopyIcon
} from '@lucide/vue'

const props = defineProps<{
  isOpen: boolean
  cardData: DiscoveryStoryCardResponse | null
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

const copied = ref(false)

const closeModal = () => {
  emit('close')
}

const copyStoryText = async () => {
  if (!props.cardData) return
  const text = `🌟 [Ilmiy Kashfiyot]: Men "World as a Classroom" orqali ${props.cardData.object_name} ob'ektini o'rgandim!\n\n💡 Qonuniyat: ${props.cardData.core_discovery}${props.cardData.key_formula ? '\n📐 Formula: ' + props.cardData.key_formula : ''}\n🏆 +${props.cardData.xp_earned} XP to'plandi.\n\nSiz ham atrofdagi olamni fan orqali kashf qiling!`
  try {
    await navigator.clipboard.writeText(text)
    copied.value = true
    setTimeout(() => { copied.value = false }, 2500)
  } catch (err) {
    console.error('Clipboard copy failed:', err)
  }
}

const shareLink = async () => {
  if (navigator.share && props.cardData) {
    try {
      await navigator.share({
        title: `Kashfiyot: ${props.cardData.object_name}`,
        text: `Men hozirgina ${props.cardData.object_name} bo'yicha ilmiy kashfiyot qildim!`,
        url: window.location.href,
      })
    } catch {
      await copyStoryText()
    }
  } else {
    await copyStoryText()
  }
}
</script>
