import { defineStore } from 'pinia'
import { ref } from 'vue'
import {
  api,
  type DetectedObject,
  type LessonDetail,
  type UserProfile
} from '@/api/client'

export const useExplorationStore = defineStore('exploration', () => {
  const isAnalyzing = ref(false)
  const isGeneratingLesson = ref(false)
  const imagePreview = ref<string | null>(null)
  const detectedObjects = ref<DetectedObject[]>([])
  const selectedObject = ref<DetectedObject | null>(null)
  const currentLesson = ref<LessonDetail | null>(null)
  const activeSubject = ref<string>('Physics')

  const scanFile = async (file: File, lang: string) => {
    isAnalyzing.value = true
    try {
      const res = await api.scanFile(file, lang)
      imagePreview.value = res.image_preview || null
      detectedObjects.value = res.detected_objects
      if (res.detected_objects.length > 0) {
        selectedObject.value = res.detected_objects[0]
      }
      return res
    } finally {
      isAnalyzing.value = false
    }
  }

  const scanBase64 = async (base64: string, lang: string) => {
    isAnalyzing.value = true
    try {
      const res = await api.scanBase64(base64, lang)
      imagePreview.value = res.image_preview || null
      detectedObjects.value = res.detected_objects
      if (res.detected_objects.length > 0) {
        selectedObject.value = res.detected_objects[0]
      }
      return res
    } finally {
      isAnalyzing.value = false
    }
  }

  const setManualSample = (sample: any) => {
    selectedObject.value = {
      name: sample.name,
      name_en: sample.name_en,
      category: sample.category,
      educational_hook: sample.hook,
      subjects: sample.subjects,
      confidence: 0.99
    }
    detectedObjects.value = [selectedObject.value]
    imagePreview.value = null
  }

  const generateLessonForSelected = async (userProfile: UserProfile | null, lang: string) => {
    if (!selectedObject.value) return null
    isGeneratingLesson.value = true
    try {
      const lesson = await api.generateLesson({
        object_name: selectedObject.value.name,
        object_name_en: selectedObject.value.name_en,
        category: selectedObject.value.category,
        language: lang,
        age: userProfile?.age,
        grade: userProfile?.grade,
        knowledge_level: userProfile?.knowledge_level,
        image_thumbnail: imagePreview.value || undefined
      })
      currentLesson.value = lesson
      if (lesson.subjects && lesson.subjects.length > 0) {
        activeSubject.value = lesson.subjects[0].subject
      }
      return lesson
    } finally {
      isGeneratingLesson.value = false
    }
  }

  const fetchLesson = async (lessonId: number) => {
    isGeneratingLesson.value = true
    try {
      const lesson = await api.getLesson(lessonId)
      currentLesson.value = lesson
      if (lesson.subjects && lesson.subjects.length > 0) {
        activeSubject.value = lesson.subjects[0].subject
      }
      return lesson
    } finally {
      isGeneratingLesson.value = false
    }
  }

  const fetchLessonByExploration = async (explorationId: number) => {
    isGeneratingLesson.value = true
    try {
      const lesson = await api.getLessonByExploration(explorationId)
      currentLesson.value = lesson
      if (lesson.subjects && lesson.subjects.length > 0) {
        activeSubject.value = lesson.subjects[0].subject
      }
      return lesson
    } finally {
      isGeneratingLesson.value = false
    }
  }

  const resetScanner = () => {
    imagePreview.value = null
    detectedObjects.value = []
    selectedObject.value = null
  }

  return {
    isAnalyzing,
    isGeneratingLesson,
    imagePreview,
    detectedObjects,
    selectedObject,
    currentLesson,
    activeSubject,
    scanFile,
    scanBase64,
    setManualSample,
    generateLessonForSelected,
    fetchLesson,
    fetchLessonByExploration,
    resetScanner
  }
})
