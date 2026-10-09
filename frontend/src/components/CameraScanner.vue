<template>
  <div class="relative w-full max-w-2xl mx-auto rounded-3xl overflow-hidden glass-panel border border-slate-800 bg-slate-900/90 shadow-2xl">
    <!-- Camera Viewport / Preview Box -->
    <div class="relative w-full aspect-[4/3] sm:aspect-[16/10] bg-slate-950 flex items-center justify-center overflow-hidden">
      <!-- 1. Live Video Stream -->
      <video
        v-show="isCameraActive && !capturedPreview"
        ref="videoElement"
        autoplay
        playsinline
        muted
        class="w-full h-full object-cover"
      ></video>

      <!-- 2. Captured Image Preview -->
      <img
        v-if="capturedPreview"
        :src="capturedPreview"
        alt="Captured preview"
        class="w-full h-full object-cover"
      />

      <!-- 3. Camera Idle State (when camera is not started & no image) -->
      <div
        v-if="!isCameraActive && !capturedPreview"
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
        class="absolute inset-0 pointer-events-none flex flex-col justify-between"
      >
        <div class="w-full h-1 bg-gradient-to-r from-transparent via-emerald-400 to-transparent shadow-[0_0_15px_#10b981] animate-scan relative"></div>
        <div class="absolute inset-0 bg-emerald-500/5 backdrop-blur-[1px] flex flex-col items-center justify-center p-4">
          <div class="px-6 py-4 rounded-2xl glass-panel bg-slate-950/90 border border-emerald-500/40 text-center shadow-2xl flex flex-col items-center gap-3">
            <Loader2Icon class="w-8 h-8 text-emerald-400 animate-spin" />
            <div>
              <p class="font-bold text-white text-base">{{ t.scanner.analyzing }}</p>
              <p class="text-xs text-slate-400 max-w-xs mt-1">{{ t.scanner.analyzingSubtitle }}</p>
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
        class="absolute inset-0 bg-white pointer-events-none transition-opacity duration-300 opacity-80"
      ></div>

      <!-- Error / Permission notification banner -->
      <div
        v-if="errorMessage"
        class="absolute top-4 left-4 right-4 p-3 rounded-xl bg-rose-500/90 text-white text-xs font-medium flex items-center justify-between shadow-lg"
      >
        <span>{{ errorMessage }}</span>
        <button @click="errorMessage = ''" class="text-white hover:text-slate-200">✕</button>
      </div>
    </div>

    <!-- Active Camera Controls Toolbar -->
    <div
      v-if="isCameraActive || capturedPreview"
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
          v-if="capturedPreview"
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

      <!-- Right: Upload or Browse -->
      <div>
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
  </div>
</template>

<script setup lang="ts">
import { ref, onUnmounted } from 'vue'
import { useI18n } from '@/i18n'
import { useExplorationStore } from '@/stores/exploration'
import {
  Camera as CameraIcon,
  Upload as UploadIcon,
  SwitchCamera as SwitchCameraIcon,
  VideoOff as VideoOffIcon,
  RotateCcw as RotateCcwIcon,
  Loader2 as Loader2Icon
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
