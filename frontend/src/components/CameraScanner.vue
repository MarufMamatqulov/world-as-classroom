<template>
  <div class="relative w-full max-w-2xl mx-auto rounded-3xl overflow-hidden glass-panel border border-slate-800 bg-slate-900/90 shadow-2xl">
    <!-- Camera Viewport / Preview Box -->
    <div class="relative w-full aspect-[4/3] sm:aspect-[16/10] bg-slate-950 flex items-center justify-center overflow-hidden select-none">
      <!-- 1. Live Video Stream -->
      <video
        v-show="isCameraActive && !capturedPreview"
        ref="videoElement"
        autoplay
        playsinline
        muted
        class="w-full h-full object-cover"
      ></video>

      <!-- 2. Captured Image Preview with Bounding Boxes -->
      <div v-if="capturedPreview || explorationStore.imagePreview" class="relative w-full h-full">
        <img
          :src="capturedPreview || explorationStore.imagePreview || ''"
          alt="Captured preview"
          class="w-full h-full object-cover"
        />

        <!-- Clickable Magic Vision Bounding Boxes -->
        <div
          v-if="explorationStore.detectedObjects.length > 0 && !explorationStore.isAnalyzing"
          class="absolute inset-0 pointer-events-auto"
        >
          <div
            v-for="(obj, idx) in explorationStore.detectedObjects"
            :key="idx"
            v-show="obj.bounding_box"
            @click.stop="selectObject(obj)"
            class="absolute border-2 transition-all duration-200 cursor-pointer rounded-xl flex flex-col justify-between group"
            :class="explorationStore.selectedObject?.name === obj.name
              ? 'border-emerald-400 bg-emerald-500/25 shadow-[0_0_20px_rgba(16,185,129,0.5)] z-30 ring-2 ring-emerald-300 scale-[1.01]'
              : 'border-cyan-400/80 bg-cyan-500/10 hover:border-cyan-300 hover:bg-cyan-500/20 z-20'"
            :style="{
              top: `${(obj.bounding_box?.ymin ?? 0) * 100}%`,
              left: `${(obj.bounding_box?.xmin ?? 0) * 100}%`,
              width: `${Math.max(0.12, ((obj.bounding_box?.xmax ?? 1) - (obj.bounding_box?.xmin ?? 0))) * 100}%`,
              height: `${Math.max(0.12, ((obj.bounding_box?.ymax ?? 1) - (obj.bounding_box?.ymin ?? 0))) * 100}%`
            }"
          >
            <!-- Label Tag -->
            <div class="p-1 sm:p-1.5 flex items-center justify-between pointer-events-none">
              <span
                class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded-lg text-[10px] sm:text-xs font-bold text-white shadow-lg bg-slate-950/90 backdrop-blur-md border"
                :class="explorationStore.selectedObject?.name === obj.name ? 'border-emerald-400 text-emerald-300' : 'border-cyan-400 text-cyan-200'"
              >
                <span
                  class="w-1.5 h-1.5 rounded-full"
                  :class="explorationStore.selectedObject?.name === obj.name ? 'bg-emerald-400 animate-pulse' : 'bg-cyan-400'"
                ></span>
                <span>{{ obj.name }}</span>
                <span class="text-[9px] text-slate-400">{{ Math.round(obj.confidence * 100) }}%</span>
              </span>
            </div>

            <!-- Bottom Action: Quick edit prompt -->
            <div class="p-1 flex justify-end">
              <button
                @click.stop="openCorrectionModal(obj)"
                class="opacity-0 group-hover:opacity-100 transition-opacity px-2 py-0.5 rounded bg-slate-900/90 hover:bg-slate-800 text-[10px] text-emerald-400 border border-emerald-500/40 flex items-center gap-1 shadow pointer-events-auto"
                title="Nomini to'g'rilash"
              >
                <Edit3Icon class="w-3 h-3" />
                <span>To'g'rilash</span>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- 3. Camera Idle State (when camera is not started & no image) -->
      <div
        v-if="!isCameraActive && !capturedPreview && !explorationStore.imagePreview"
        class="flex flex-col items-center justify-center p-8 text-center text-slate-400"
      >
        <div class="w-20 h-20 rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center mb-4 text-emerald-400 shadow-inner">
          <CameraIcon class="w-10 h-10" />
        </div>
        <h3 class="text-lg font-semibold text-white mb-2">{{ t.scanner.title }}</h3>
        <p class="text-xs sm:text-sm text-slate-400 max-w-sm mb-6">
          {{ t.scanner.subtitle }}
        </p>
        <div class="flex flex-wrap items-center justify-center gap-3">
          <button
            @click="startCamera()"
            class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-500 hover:from-emerald-400 hover:to-teal-400 text-slate-950 font-bold text-sm flex items-center gap-2 shadow-lg shadow-emerald-500/20 active:scale-95 transition-all"
          >
            <CameraIcon class="w-4 h-4" />
            <span>{{ t.scanner.startCamera }}</span>
          </button>
          <label class="px-5 py-2.5 rounded-xl bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700 text-slate-200 font-semibold text-sm flex items-center gap-2 cursor-pointer active:scale-95 transition-all">
            <UploadIcon class="w-4 h-4 text-emerald-400" />
            <span>{{ t.scanner.uploadImage }}</span>
            <input
              type="file"
              accept="image/*"
              class="hidden"
              @change="handleFileUpload"
            />
          </label>
        </div>
      </div>

      <!-- 4. Scanning Laser Overlay Animation -->
      <div
        v-if="explorationStore.isAnalyzing"
        class="absolute inset-0 pointer-events-none flex flex-col justify-between z-40"
      >
        <div class="w-full h-1 bg-gradient-to-r from-transparent via-emerald-400 to-transparent shadow-[0_0_15px_#10b981] animate-scan relative"></div>
        <div class="absolute inset-0 bg-emerald-500/10 backdrop-blur-[2px] flex flex-col items-center justify-center p-4">
          <div class="px-6 py-4 rounded-2xl glass-panel bg-slate-950/90 border border-emerald-500/40 text-center shadow-2xl flex flex-col items-center gap-3">
            <Loader2Icon class="w-8 h-8 text-emerald-400 animate-spin" />
            <div>
              <p class="font-bold text-white text-base">{{ t.scanner.analyzing }}</p>
              <p class="text-xs text-slate-400 max-w-xs mt-1">AI ob'ektlarni aniqlamoqda va chegaralarni belgilamoqda...</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 5. Viewfinder Frame UI Guidelines -->
      <div
        v-if="isCameraActive && !capturedPreview && !explorationStore.isAnalyzing"
        class="absolute inset-6 pointer-events-none border border-emerald-500/30 rounded-2xl flex flex-col justify-between p-3"
      >
        <div class="flex justify-between">
          <div class="w-6 h-6 border-t-2 border-l-2 border-emerald-400"></div>
          <div class="w-6 h-6 border-t-2 border-r-2 border-emerald-400"></div>
        </div>
        <div class="flex justify-between">
          <div class="w-6 h-6 border-b-2 border-l-2 border-emerald-400"></div>
          <div class="w-6 h-6 border-b-2 border-r-2 border-emerald-400"></div>
        </div>
      </div>

      <!-- Flash Animation on capture -->
      <div
        v-if="showFlash"
        class="absolute inset-0 bg-white pointer-events-none transition-opacity duration-300 opacity-80 z-50"
      ></div>

      <!-- Error / Permission notification banner -->
      <div
        v-if="errorMessage"
        class="absolute top-4 left-4 right-4 p-3 rounded-xl bg-rose-500/90 text-white text-xs font-medium flex items-center justify-between shadow-lg z-50"
      >
        <span>{{ errorMessage }}</span>
        <button @click="errorMessage = ''" class="text-white hover:text-slate-200">✕</button>
      </div>
    </div>

    <!-- Active Camera Controls Toolbar -->
    <div
      v-if="isCameraActive || capturedPreview || explorationStore.imagePreview"
      class="p-4 sm:p-5 bg-slate-900 border-t border-slate-800 flex items-center justify-between"
    >
      <!-- Left: Switch camera or stop -->
      <div class="flex items-center gap-2">
        <button
          v-if="isCameraActive && !capturedPreview"
          @click="toggleCameraFacing()"
          class="p-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition-colors"
          :title="t.scanner.switchCamera"
        >
          <SwitchCameraIcon class="w-5 h-5 text-emerald-400" />
        </button>

        <button
          v-if="isCameraActive && !capturedPreview"
          @click="stopCamera()"
          class="p-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-rose-400 transition-colors"
          :title="t.scanner.stopCamera"
        >
          <VideoOffIcon class="w-5 h-5" />
        </button>

        <button
          v-if="capturedPreview || explorationStore.imagePreview"
          @click="retakePhoto()"
          class="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs sm:text-sm font-semibold flex items-center gap-2 transition-colors"
        >
          <RotateCcwIcon class="w-4 h-4 text-emerald-400" />
          <span>{{ t.scanner.retake }}</span>
        </button>
      </div>

      <!-- Center: Shutter Button -->
      <div v-if="isCameraActive && !capturedPreview">
        <button
          @click="capturePhoto()"
          :disabled="explorationStore.isAnalyzing"
          class="w-16 h-16 rounded-full bg-slate-950 p-1 border-2 border-emerald-400/80 shadow-lg shadow-emerald-500/30 hover:scale-105 active:scale-95 transition-all flex items-center justify-center group"
          :title="t.scanner.capturePhoto"
        >
          <div class="w-full h-full rounded-full bg-emerald-500 group-hover:bg-emerald-400 transition-colors flex items-center justify-center">
            <CameraIcon class="w-7 h-7 text-slate-950" />
          </div>
        </button>
      </div>

      <!-- Right: Correction Button & Upload -->
      <div class="flex items-center gap-2">
        <button
          v-if="explorationStore.selectedObject"
          @click="openCorrectionModal(explorationStore.selectedObject)"
          class="px-3 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-emerald-400 hover:text-emerald-300 text-xs font-semibold flex items-center gap-1.5 transition-colors border border-slate-700"
          title="Nomini o'zgartirish"
        >
          <Edit3Icon class="w-4 h-4" />
          <span class="hidden sm:inline">To'g'rilash</span>
        </button>

        <label class="p-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white flex items-center justify-center cursor-pointer transition-colors" :title="t.scanner.uploadImage">
          <UploadIcon class="w-5 h-5 text-emerald-400" />
          <input
            type="file"
            accept="image/*"
            class="hidden"
            @change="handleFileUpload"
          />
        </label>
      </div>
    </div>

    <!-- Modal: Object Recognition Correction / Rename -->
    <div
      v-if="isCorrectionOpen"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm"
      @click.self="isCorrectionOpen = false"
    >
      <div class="w-full max-w-md rounded-2xl glass-panel bg-slate-900 border border-slate-700 p-6 shadow-2xl space-y-4">
        <div class="flex items-center justify-between border-b border-slate-800 pb-3">
          <h4 class="text-base font-bold text-white flex items-center gap-2">
            <SparklesIcon class="w-4 h-4 text-emerald-400" />
            <span>Ob'ekt Nomini To'g'rilash</span>
          </h4>
          <button @click="isCorrectionOpen = false" class="text-slate-400 hover:text-white">✕</button>
        </div>

        <p class="text-xs text-slate-300">
          Agar sun'iy intellekt ob'ektni noaniq aniqlagan bo'lsa yoki o'rganmoqchi bo'lgan maxsus qismingizni aniq ko'rsatmoqchi bo'lsangiz, to'g'ri nomini kiriting:
        </p>

        <div>
          <label class="block text-xs font-semibold text-slate-300 mb-1">To'g'ri ob'ekt nomi:</label>
          <input
            v-model="correctionInput"
            type="text"
            placeholder="Masalan: Optik Mikroskop, Quyosh paneli, Kvars soat"
            class="w-full px-4 py-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-sm focus:border-emerald-500 focus:outline-none"
            @keyup.enter="applyCorrection"
          />
        </div>

        <div class="flex justify-end gap-2 pt-2">
          <button
            @click="isCorrectionOpen = false"
            class="px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white bg-slate-800"
          >
            Bekor qilish
          </button>
          <button
            @click="applyCorrection"
            class="px-4 py-2 rounded-xl text-xs font-bold text-slate-950 bg-emerald-500 hover:bg-emerald-400 transition-colors"
          >
            Saqlash va Yangilash
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onUnmounted } from 'vue'
import { useI18n } from '@/i18n'
import { useExplorationStore } from '@/stores/exploration'
import type { DetectedObject } from '@/api/client'
import {
  Camera as CameraIcon,
  Upload as UploadIcon,
  SwitchCamera as SwitchCameraIcon,
  VideoOff as VideoOffIcon,
  RotateCcw as RotateCcwIcon,
  Loader2 as Loader2Icon,
  Sparkles as SparklesIcon,
  Edit3 as Edit3Icon
} from '@lucide/vue'

const emit = defineEmits<{
  (e: 'scanned'): void
}>()

const { t, lang } = useI18n()
const explorationStore = useExplorationStore()

const videoElement = ref<HTMLVideoElement | null>(null)
const isCameraActive = ref(false)
const facingMode = ref<'environment' | 'user'>('environment')
const capturedPreview = ref<string | null>(null)
const showFlash = ref(false)
const errorMessage = ref('')
let mediaStream: MediaStream | null = null

// Correction modal state
const isCorrectionOpen = ref(false)
const correctionInput = ref('')

const selectObject = (obj: DetectedObject) => {
  explorationStore.selectedObject = obj
}

const openCorrectionModal = (obj: DetectedObject) => {
  correctionInput.value = obj.name
  isCorrectionOpen.value = true
}

const applyCorrection = async () => {
  if (!correctionInput.value.trim()) return
  await explorationStore.correctSelectedObject(correctionInput.value.trim(), undefined, lang.value)
  isCorrectionOpen.value = false
}

const startCamera = async () => {
  errorMessage.value = ''
  capturedPreview.value = null

  try {
    if (mediaStream) {
      stopCamera()
    }
    const constraints: MediaStreamConstraints = {
      video: {
        facingMode: { ideal: facingMode.value },
        width: { ideal: 1280 },
        height: { ideal: 720 }
      },
      audio: false
    }

    mediaStream = await navigator.mediaDevices.getUserMedia(constraints)
    if (videoElement.value) {
      videoElement.value.srcObject = mediaStream
      await videoElement.value.play()
    }
    isCameraActive.value = true
  } catch (err: any) {
    console.error('Camera access error:', err)
    errorMessage.value = t.value.scanner.permissionDenied
    isCameraActive.value = false
  }
}

const stopCamera = () => {
  if (mediaStream) {
    mediaStream.getTracks().forEach(track => track.stop())
    mediaStream = null
  }
  isCameraActive.value = false
}

const toggleCameraFacing = async () => {
  facingMode.value = facingMode.value === 'environment' ? 'user' : 'environment'
  await startCamera()
}

const capturePhoto = async () => {
  if (!videoElement.value) return

  // Flash animation
  showFlash.value = true
  setTimeout(() => (showFlash.value = false), 200)

  // Draw current frame to hidden canvas
  const video = videoElement.value
  const canvas = document.createElement('canvas')
  canvas.width = video.videoWidth || 640
  canvas.height = video.videoHeight || 480
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  ctx.drawImage(video, 0, 0, canvas.width, canvas.height)
  const base64 = canvas.toDataURL('image/jpeg', 0.85)

  capturedPreview.value = base64
  stopCamera()

  // Send to AI for multimodal detection
  try {
    await explorationStore.scanBase64(base64, lang.value)
    emit('scanned')
  } catch (err: any) {
    errorMessage.value = err.message || 'Error scanning image'
  }
}

const retakePhoto = async () => {
  capturedPreview.value = null
  explorationStore.resetScanner()
  await startCamera()
}

const handleFileUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement
  if (!target.files || target.files.length === 0) return
  const file = target.files[0]

  stopCamera()

  // Generate preview immediately
  const reader = new FileReader()
  reader.onload = async (e) => {
    capturedPreview.value = e.target?.result as string
    try {
      await explorationStore.scanFile(file, lang.value)
      emit('scanned')
    } catch (err: any) {
      errorMessage.value = err.message || 'Error analyzing uploaded image'
    }
  }
  reader.readAsDataURL(file)
}

onUnmounted(() => {
  stopCamera()
})
</script>
