<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12">
    <!-- View Header -->
    <div class="text-center max-w-2xl mx-auto mb-8">
      <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-bold border border-emerald-500/20 mb-3">
        <CameraIcon class="w-3.5 h-3.5" />
        <span>{{ t.scanner.title }}</span>
      </div>
      <h2 class="text-2xl sm:text-3xl font-extrabold text-white">
        Atrofingizdagi Olamni O'rganing
      </h2>
      <p class="text-xs sm:text-sm text-slate-400 mt-2 leading-relaxed">
        {{ t.scanner.subtitle }}
      </p>
    </div>

    <!-- Scanner Core Component -->
    <CameraScanner @scanned="handleScanned()" />

    <!-- Detected Objects Selection Panel -->
    <ObjectSelector />

    <!-- Curated Sample Objects Section -->
    <div class="mt-16 pt-12 border-t border-slate-800/80">
      <SampleGallery />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useI18n } from '@/i18n'
import CameraScanner from '@/components/CameraScanner.vue'
import ObjectSelector from '@/components/ObjectSelector.vue'
import SampleGallery from '@/components/SampleGallery.vue'
import { Camera as CameraIcon } from '@lucide/vue'

const { t } = useI18n()

const handleScanned = () => {
  // Smooth scroll down to detected objects if needed
  setTimeout(() => {
    window.scrollBy({ top: 300, behavior: 'smooth' })
  }, 100)
}
</script>
