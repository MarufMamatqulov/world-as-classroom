<template>
  <div class="glass-panel rounded-3xl p-5 sm:p-6 border border-slate-800 bg-slate-900/90 shadow-2xl flex flex-col h-[560px]">
    <!-- Header -->
    <div class="flex items-center justify-between pb-4 border-b border-slate-800 shrink-0">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-emerald-500 to-teal-500 flex items-center justify-center text-slate-950 font-bold shadow-md shadow-emerald-500/20">
          <BotIcon class="w-6 h-6" />
        </div>
        <div>
          <h3 class="text-base font-bold text-white flex items-center gap-2">
            <span>{{ t.tutor.title }}</span>
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          </h3>
          <p class="text-xs text-slate-400">{{ objectName }} bo'yicha ilmiy ustoz</p>
        </div>
      </div>
    </div>

    <!-- Messages List -->
    <div ref="chatContainer" class="flex-1 overflow-y-auto py-4 space-y-3.5 pr-1 scrollbar-thin">
      <!-- Welcome message -->
      <div class="flex items-start gap-2.5">
        <div class="w-7 h-7 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center shrink-0 mt-0.5">
          <SparklesIcon class="w-4 h-4" />
        </div>
        <div class="bg-slate-950/80 rounded-2xl rounded-tl-sm p-3.5 border border-slate-800/80 max-w-[85%] text-xs sm:text-sm text-slate-200 leading-relaxed shadow-sm">
          <p>
            Salom! Men sizning AI ustozingizman. <strong>{{ objectName }}</strong> bo'yicha istalgan savolingizni berishingiz mumkin!
          </p>
        </div>
      </div>

      <!-- Historical / active messages -->
      <div
        v-for="(msg, idx) in messages"
        :key="idx"
        class="flex items-start gap-2.5"
        :class="msg.role === 'user' ? 'flex-row-reverse' : ''"
      >
        <div
          class="w-7 h-7 rounded-lg flex items-center justify-center shrink-0 mt-0.5 text-xs font-bold"
          :class="msg.role === 'user' ? 'bg-emerald-500 text-slate-950' : 'bg-slate-800 text-emerald-400 border border-slate-700'"
        >
          <UserIcon v-if="msg.role === 'user'" class="w-4 h-4" />
          <BotIcon v-else class="w-4 h-4" />
        </div>

        <div
          class="rounded-2xl p-3.5 max-w-[85%] text-xs sm:text-sm leading-relaxed relative group"
          :class="msg.role === 'user'
            ? 'bg-emerald-600 text-white rounded-tr-sm shadow-md shadow-emerald-500/10'
            : 'bg-slate-950/90 text-slate-200 rounded-tl-sm border border-slate-800/80 shadow-sm'"
        >
          <p class="whitespace-pre-wrap">{{ msg.content }}</p>

          <!-- Text-to-Speech audio button for assistant messages -->
          <button
            v-if="msg.role === 'assistant'"
            @click="speak(msg.content)"
            class="mt-2 text-[11px] font-semibold text-emerald-400 hover:text-emerald-300 flex items-center gap-1 opacity-80 hover:opacity-100 transition-opacity"
            :title="t.tutor.listen"
          >
            <Volume2Icon class="w-3.5 h-3.5" />
            <span>{{ t.tutor.listen }}</span>
          </button>
        </div>
      </div>

      <!-- Thinking indicator -->
      <div v-if="isThinking" class="flex items-start gap-2.5">
        <div class="w-7 h-7 rounded-lg bg-slate-800 text-emerald-400 flex items-center justify-center shrink-0 mt-0.5">
          <BotIcon class="w-4 h-4" />
        </div>
        <div class="bg-slate-950/80 rounded-2xl rounded-tl-sm px-4 py-3 border border-slate-800/80 flex items-center gap-2 text-xs text-slate-400">
          <Loader2Icon class="w-3.5 h-3.5 animate-spin text-emerald-400" />
          <span>{{ t.tutor.thinking }}</span>
        </div>
      </div>
    </div>

    <!-- Quick Prompt Suggestions Chips -->
    <div v-if="suggestedPrompts.length > 0" class="py-2 shrink-0 flex items-center gap-1.5 overflow-x-auto scrollbar-none">
      <button
        v-for="(p, pIdx) in suggestedPrompts"
        :key="pIdx"
        @click="sendPrompt(p)"
        class="text-[11px] font-medium px-3 py-1.5 rounded-full bg-slate-950/80 hover:bg-slate-800 border border-slate-800 hover:border-emerald-500/40 text-slate-300 hover:text-emerald-300 whitespace-nowrap transition-colors"
      >
        {{ p }}
      </button>
    </div>

    <!-- Input Form -->
    <form @submit.prevent="sendMessage()" class="pt-3 border-t border-slate-800 shrink-0 flex items-center gap-2">
      <input
        v-model="inputMessage"
        type="text"
        :placeholder="t.tutor.placeholder"
        :disabled="isThinking"
        class="flex-1 bg-slate-950/90 border border-slate-800 focus:border-emerald-500 rounded-xl px-4 py-2.5 text-xs sm:text-sm text-slate-200 placeholder-slate-500 focus:outline-none transition-colors"
      />
      <button
        type="submit"
        :disabled="!inputMessage.trim() || isThinking"
        class="p-2.5 sm:px-4 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold text-xs sm:text-sm flex items-center gap-1.5 transition-all disabled:opacity-40 shadow-md shadow-emerald-500/20 active:scale-95"
      >
        <SendIcon class="w-4 h-4" />
        <span class="hidden sm:inline">{{ t.tutor.send }}</span>
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { useI18n } from '@/i18n'
import { api } from '@/api/client'
import {
  Bot as BotIcon,
  User as UserIcon,
  Sparkles as SparklesIcon,
  Send as SendIcon,
  Volume2 as Volume2Icon,
  Loader2 as Loader2Icon
} from '@lucide/vue'

const props = defineProps<{
  explorationId: number
  objectName: string
}>()

const { t, lang } = useI18n()
const messages = ref<{ role: string; content: string }[]>([])
const inputMessage = ref('')
const isThinking = ref(false)
const chatContainer = ref<HTMLDivElement | null>(null)

const suggestedPrompts = ref<string[]>([
  `${props.objectName} qanday harakatlanadi?`,
  `Fizika qonunlarini soddaroq tushuntiring`,
  `Uyda qanday sinov o'tkazsam bo'ladi?`
])

const scrollToBottom = async () => {
  await nextTick()
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

onMounted(async () => {
  try {
    const history = await api.getTutorHistory(props.explorationId)
    if (history.length > 0) {
      messages.value = history.map(h => ({ role: h.role, content: h.content }))
      scrollToBottom()
    }
  } catch (e) {
    console.error('Failed to load chat history:', e)
  }
})

const sendMessage = async () => {
  const text = inputMessage.value.trim()
  if (!text || isThinking.value) return

  messages.value.push({ role: 'user', content: text })
  inputMessage.value = ''
  isThinking.value = true
  scrollToBottom()

  try {
    const res = await api.tutorChat(props.explorationId, text, lang.value)
    messages.value.push({ role: 'assistant', content: res.reply })
    if (res.suggested_prompts && res.suggested_prompts.length > 0) {
      suggestedPrompts.value = res.suggested_prompts
    }
    scrollToBottom()
  } catch (err: any) {
    messages.value.push({
      role: 'assistant',
      content: 'Kechirasiz, javob olishda xatolik yuz berdi. Iltimos qaytadan urinib ko\'ring.'
    })
  } finally {
    isThinking.value = false
    scrollToBottom()
  }
}

const sendPrompt = (promptText: string) => {
  inputMessage.value = promptText
  sendMessage()
}

// Browser Text-to-Speech
const speak = (text: string) => {
  if (!('speechSynthesis' in window)) return

  window.speechSynthesis.cancel() // stop any previous speech
  const utterance = new SpeechSynthesisUtterance(text)

  if (lang.value === 'ru') {
    utterance.lang = 'ru-RU'
  } else if (lang.value === 'en') {
    utterance.lang = 'en-US'
  } else {
    // Uzbek doesn't always have a default TTS engine in all OS, falls back to default voice
    utterance.lang = 'uz-UZ'
  }

  utterance.rate = 1.0
  window.speechSynthesis.speak(utterance)
}
</script>
