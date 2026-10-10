<template>
  <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
    <!-- Knowledge Passport Document Header -->
    <div class="rounded-3xl glass-panel bg-gradient-to-br from-slate-900 via-slate-950 to-indigo-950/40 border border-indigo-500/30 p-6 sm:p-8 shadow-2xl relative overflow-hidden">
      <!-- Watermark / Stamp Hologram in background -->
      <div class="absolute -right-10 -bottom-10 w-48 h-48 rounded-full border-4 border-indigo-500/10 flex items-center justify-center pointer-events-none transform rotate-12">
        <span class="text-indigo-400/20 font-black text-2xl uppercase tracking-widest">PASSPORT</span>
      </div>

      <div class="relative z-10 space-y-6">
        <!-- Top bar: Emblem & Callsign -->
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-slate-800 pb-5">
          <div class="flex items-center gap-3.5">
            <div class="w-14 h-14 rounded-2xl bg-gradient-to-tr from-indigo-500 via-purple-500 to-emerald-400 p-[2px] shadow-lg shadow-indigo-500/20">
              <div class="w-full h-full bg-slate-950 rounded-[14px] flex items-center justify-center text-indigo-400 font-bold text-xl">
                ★
              </div>
            </div>
            <div>
              <div class="flex items-center gap-2">
                <span class="text-xs font-bold uppercase tracking-wider text-indigo-400">Bilim Pasporti • Science Passport</span>
                <span class="px-2 py-0.5 rounded text-[10px] bg-indigo-500/20 text-indigo-300 font-mono">VERIFIED</span>
              </div>
              <h1 class="text-xl sm:text-2xl font-black text-white tracking-tight">
                {{ passport?.explorer_callsign || 'Yosh Tadqiqotchi' }}
              </h1>
            </div>
          </div>

          <div class="flex items-center gap-4 bg-slate-950/80 px-4 py-2.5 rounded-2xl border border-slate-800">
            <div>
              <span class="text-[10px] text-slate-400 uppercase font-semibold block">Daraja (Rank)</span>
              <span class="text-xs font-extrabold text-emerald-400">{{ passport?.level_info.rank_title }}</span>
            </div>
            <div class="w-px h-8 bg-slate-800"></div>
            <div>
              <span class="text-[10px] text-slate-400 uppercase font-semibold block">Kashfiyotlar</span>
              <span class="text-xs font-extrabold text-white">{{ passport?.total_discoveries || 0 }} ta</span>
            </div>
          </div>
        </div>

        <!-- Level XP Progress Bar -->
        <div class="space-y-2">
          <div class="flex justify-between text-xs font-semibold">
            <span class="text-slate-300">Level {{ passport?.level_info.current_level }} O'sishi</span>
            <span class="text-emerald-400 font-mono">{{ passport?.level_info.current_xp }} / {{ passport?.level_info.next_level_xp }} XP ({{ passport?.level_info.progress_percentage }}%)</span>
          </div>
          <div class="w-full h-3 rounded-full bg-slate-950 overflow-hidden border border-slate-800 p-0.5">
            <div
              class="h-full rounded-full bg-gradient-to-r from-emerald-500 via-teal-400 to-indigo-500 transition-all duration-500 shadow-md shadow-emerald-500/30"
              :style="{ width: `${passport?.level_info.progress_percentage || 15}%` }"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Realm Visa Stamps Grid (Olam Vizalari) -->
    <div class="space-y-4">
      <div class="flex items-center justify-between">
        <div>
          <h2 class="text-lg font-bold text-white flex items-center gap-2">
            <GlobeIcon class="w-5 h-5 text-indigo-400" />
            <span>Fan Sohalari Vizalari (Realm Stamps)</span>
          </h2>
          <p class="text-xs text-slate-400">Atrofdagi real buyumlarni tadqiq qilib, har bir sohada tamg'alarni oching</p>
        </div>
      </div>

      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3.5">
        <div
          v-for="stamp in passport?.stamps"
          :key="stamp.id"
          class="rounded-2xl p-4 border transition-all duration-300 flex flex-col items-center text-center gap-2 relative overflow-hidden"
          :class="stamp.unlocked
            ? 'glass-panel bg-slate-900/90 border-emerald-500/40 shadow-lg shadow-emerald-500/5'
            : 'bg-slate-950/60 border-slate-800/80 opacity-60 grayscale hover:grayscale-0'"
        >
          <!-- Holographic seal corner -->
          <div
            v-if="stamp.unlocked"
            class="w-12 h-12 rounded-full border-2 border-emerald-400/30 flex items-center justify-center p-1 bg-gradient-to-tr from-emerald-500/10 to-teal-500/20"
          >
            <ShieldCheckIcon class="w-6 h-6 text-emerald-400" />
          </div>
          <div
            v-else
            class="w-12 h-12 rounded-full border-2 border-slate-700 flex items-center justify-center p-1 bg-slate-900"
          >
            <LockIcon class="w-5 h-5 text-slate-500" />
          </div>

          <div class="space-y-0.5">
            <h4 class="text-xs font-bold text-white leading-tight">
              {{ stamp.name }}
            </h4>
            <span class="text-[10px] text-slate-400 block font-mono">
              {{ stamp.mastery_level }}
            </span>
          </div>

          <span
            class="text-[10px] font-bold px-2 py-0.5 rounded-full"
            :class="stamp.unlocked ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30' : 'bg-slate-800 text-slate-400'"
          >
            {{ stamp.discoveries_count }} kashfiyot
          </span>
        </div>
      </div>
    </div>

    <!-- Discovery Chronicle Timeline (Kashfiyotlar Tarixi) -->
    <div class="space-y-4">
      <div class="flex items-center justify-between">
        <h2 class="text-lg font-bold text-white flex items-center gap-2">
          <BookOpenIcon class="w-5 h-5 text-emerald-400" />
          <span>Kashfiyotlar Kundaligi (Discovery Chronicle)</span>
        </h2>
        <router-link to="/scanner" class="text-xs font-bold text-emerald-400 hover:text-emerald-300 flex items-center gap-1">
          <span>Yangi ob'ektni skanerlash</span>
          <ChevronRightIcon class="w-3.5 h-3.5" />
        </router-link>
      </div>

      <div class="rounded-2xl glass-panel bg-slate-900/80 border border-slate-800 p-4 sm:p-6">
        <div v-if="!passport?.recent_chronicle || passport.recent_chronicle.length === 0" class="text-center py-10 text-slate-400 text-xs">
          Hozircha kashfiyotlar yo'q. Birinchi ob'ektingizni skanerlab dars boshlang!
        </div>

        <div v-else class="divide-y divide-slate-800">
          <div
            v-for="item in passport.recent_chronicle"
            :key="item.id"
            class="py-3.5 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 group"
          >
            <div class="flex items-center gap-3">
              <div v-if="item.image_thumbnail" class="w-12 h-12 rounded-xl overflow-hidden border border-slate-700 flex-shrink-0">
                <img :src="item.image_thumbnail" alt="thumbnail" class="w-full h-full object-cover" />
              </div>
              <div v-else class="w-12 h-12 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center flex-shrink-0 text-emerald-400">
                <SparklesIcon class="w-5 h-5" />
              </div>

              <div>
                <h4 class="text-sm font-bold text-white group-hover:text-emerald-300 transition-colors">
                  {{ item.object_name }}
                </h4>
                <div class="flex items-center gap-2 text-[11px] text-slate-400">
                  <span class="text-emerald-400 font-semibold">{{ item.primary_subject }}</span>
                  <span>•</span>
                  <span>{{ item.category }}</span>
                  <span>•</span>
                  <span>{{ new Date(item.created_at).toLocaleDateString() }}</span>
                </div>
              </div>
            </div>

            <div class="flex items-center gap-2">
              <button
                @click="openStoryCard(item.id)"
                class="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white text-xs font-semibold flex items-center gap-1.5 transition-colors border border-slate-700"
                title="Kashfiyot kartasini ochish"
              >
                <Share2Icon class="w-3.5 h-3.5 text-emerald-400" />
                <span>Kartochka</span>
              </button>

              <router-link
                :to="`/lesson/${item.id}`"
                class="px-3.5 py-1.5 rounded-xl bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 text-xs font-bold border border-emerald-500/30 flex items-center gap-1 transition-colors"
              >
                <span>Darsga o'tish</span>
                <ChevronRightIcon class="w-3.5 h-3.5" />
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Discovery Story Card Modal -->
    <DiscoveryStoryModal
      :isOpen="isStoryModalOpen"
      :cardData="activeStoryCard"
      @close="isStoryModalOpen = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { api, type KnowledgePassportResponse, type DiscoveryStoryCardResponse } from '@/api/client'
import DiscoveryStoryModal from '@/components/DiscoveryStoryModal.vue'
import {
  Globe as GlobeIcon,
  ShieldCheck as ShieldCheckIcon,
  Lock as LockIcon,
  BookOpen as BookOpenIcon,
  Sparkles as SparklesIcon,
  Share2 as Share2Icon,
  ChevronRight as ChevronRightIcon
} from '@lucide/vue'

const passport = ref<KnowledgePassportResponse | null>(null)
const isStoryModalOpen = ref(false)
const activeStoryCard = ref<DiscoveryStoryCardResponse | null>(null)

const loadPassport = async () => {
  try {
    const res = await api.getMyPassport()
    passport.value = res
  } catch (err) {
    console.error('Failed to load passport:', err)
  }
}

const openStoryCard = async (explorationId: number) => {
  try {
    const card = await api.getDiscoveryStoryCard(explorationId)
    activeStoryCard.value = card
    isStoryModalOpen.value = true
  } catch (err) {
    console.error('Failed to load story card:', err)
  }
}

onMounted(() => {
  loadPassport()
})
</script>
