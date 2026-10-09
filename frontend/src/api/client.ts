export interface UserProfile {
  id: number
  email: string
  full_name: string
  age: number
  grade: string
  knowledge_level: string
  preferred_language: string
  has_custom_api_key: boolean
  created_at: string
}

export interface BoundingBox {
  ymin: number
  xmin: number
  ymax: number
  xmax: number
}

export interface DetectedObject {
  name: string
  name_en: string
  category: string
  educational_hook: string
  subjects: string[]
  confidence: number
  bounding_box?: BoundingBox
}

export interface ScanResponse {
  detected_objects: DetectedObject[]
  image_preview?: string
  source: string
}

export interface ConceptItem {
  headline: string
  explanation: string
  formula?: string
  real_world_example?: string
}

export interface SubjectModule {
  subject: string
  title: string
  icon?: string
  concepts: ConceptItem[]
  real_world_connection: string
}

export interface LessonExperiment {
  title: string
  materials: string[]
  steps: string[]
  science_behind_it: string
  safety_note?: string
}

export interface FunFact {
  fact: string
  why_cool: string
}

export interface VocabularyItem {
  term: string
  definition: string
}

export interface LessonDetail {
  id: number
  exploration_id: number
  object_name: string
  object_name_en?: string
  title: string
  summary: string
  subjects: SubjectModule[]
  experiments: LessonExperiment[]
  fun_facts: FunFact[]
  vocabulary: VocabularyItem[]
  language: string
  created_at: string
}

export interface QuizQuestion {
  id: number
  question: string
  options: string[]
  correct_index: number
  explanation: string
  subject: string
}

export interface QuizDetail {
  id: number
  lesson_id: number
  questions: QuizQuestion[]
}

export interface AnswerEvaluation {
  question_id: number
  question: string
  user_answer_index: number
  correct_answer_index: number
  is_correct: boolean
  explanation: string
  subject: string
}

export interface QuizSubmitResponse {
  attempt_id: number
  quiz_id: number
  score: number
  total_questions: number
  percentage: number
  evaluations: AnswerEvaluation[]
  feedback: string
}

export interface TutorChatResponse {
  reply: string
  suggested_prompts: string[]
}

export interface TutorMessage {
  id: number
  role: string
  content: string
  created_at: string
}

export interface ExplorationSummary {
  id: number
  object_name: string
  category?: string
  primary_subject: string
  language: string
  image_thumbnail?: string
  created_at: string
  quiz_completed: boolean
  best_score?: number
  total_questions?: number
}

export interface SubjectMastery {
  subject: string
  points: number
  lessons_count: number
}

export interface Achievement {
  id: string
  title: string
  description: string
  icon: string
  unlocked: boolean
  progress: number
  max_progress: number
}

export interface DashboardStats {
  total_explorations: number
  total_quizzes_completed: number
  average_quiz_score: number
  current_streak_days: number
  subject_mastery: SubjectMastery[]
  recent_explorations: ExplorationSummary[]
  achievements: Achievement[]
}

const API_BASE = '/api'

function getAuthHeader(): Record<string, string> {
  const token = localStorage.getItem('token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}

async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let errorDetail = 'Network request failed'
    try {
      const errJson = await res.json()
      errorDetail = errJson.detail || errorDetail
    } catch {
      // ignore
    }
    throw new Error(errorDetail)
  }
  return res.json()
}

export const api = {
  // Auth
  async register(data: { email: string; password: string; full_name: string; age?: number; grade?: string; knowledge_level?: string; preferred_language?: string }) {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    return handleResponse<{ access_token: string; user: UserProfile }>(res)
  },

  async login(data: { email: string; password: string }) {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    return handleResponse<{ access_token: string; user: UserProfile }>(res)
  },

  async getMe() {
    const res = await fetch(`${API_BASE}/auth/me`, {
      headers: { ...getAuthHeader() },
    })
    return handleResponse<UserProfile>(res)
  },

  async updateProfile(data: Partial<UserProfile> & { custom_api_key?: string }) {
    const res = await fetch(`${API_BASE}/auth/profile`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeader(),
      },
      body: JSON.stringify(data),
    })
    return handleResponse<UserProfile>(res)
  },

  // Scan
  async scanFile(file: File, language: string) {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('language', language)

    const res = await fetch(`${API_BASE}/scan/upload`, {
      method: 'POST',
      headers: { ...getAuthHeader() },
      body: formData,
    })
    return handleResponse<ScanResponse>(res)
  },

  async scanBase64(imageBase64: string, language: string) {
    const formData = new FormData()
    formData.append('image_base64', imageBase64)
    formData.append('language', language)

    const res = await fetch(`${API_BASE}/scan/upload`, {
      method: 'POST',
      headers: { ...getAuthHeader() },
      body: formData,
    })
    return handleResponse<ScanResponse>(res)
  },

  async getSamples(language: string) {
    const res = await fetch(`${API_BASE}/scan/samples?language=${encodeURIComponent(language)}`)
    return handleResponse<any[]>(res)
  },

  // Lessons
  async generateLesson(payload: {
    object_name: string
    object_name_en?: string
    category?: string
    language?: string
    age?: number
    grade?: string
    knowledge_level?: string
    image_thumbnail?: string
  }) {
    const res = await fetch(`${API_BASE}/lessons/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeader(),
      },
      body: JSON.stringify(payload),
    })
    return handleResponse<LessonDetail>(res)
  },

  async getLesson(lessonId: number) {
    const res = await fetch(`${API_BASE}/lessons/${lessonId}`, {
      headers: { ...getAuthHeader() },
    })
    return handleResponse<LessonDetail>(res)
  },

  async getLessonByExploration(explorationId: number) {
    const res = await fetch(`${API_BASE}/lessons/by-exploration/${explorationId}`, {
      headers: { ...getAuthHeader() },
    })
    return handleResponse<LessonDetail>(res)
  },

  // Quizzes
  async getQuizByLesson(lessonId: number) {
    const res = await fetch(`${API_BASE}/quizzes/by-lesson/${lessonId}`, {
      headers: { ...getAuthHeader() },
    })
    return handleResponse<QuizDetail>(res)
  },

  async submitQuiz(quizId: number, answers: number[]) {
    const res = await fetch(`${API_BASE}/quizzes/submit`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeader(),
      },
      body: JSON.stringify({ quiz_id: quizId, answers }),
    })
    return handleResponse<QuizSubmitResponse>(res)
  },

  // Tutor
  async tutorChat(explorationId: number, message: string, language: string) {
    const res = await fetch(`${API_BASE}/tutor/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeader(),
      },
      body: JSON.stringify({ exploration_id: explorationId, message, language }),
    })
    return handleResponse<TutorChatResponse>(res)
  },

  async getTutorHistory(explorationId: number) {
    const res = await fetch(`${API_BASE}/tutor/history/${explorationId}`, {
      headers: { ...getAuthHeader() },
    })
    return handleResponse<TutorMessage[]>(res)
  },

  // Dashboard
  async getDashboardStats() {
    const res = await fetch(`${API_BASE}/dashboard/stats`, {
      headers: { ...getAuthHeader() },
    })
    return handleResponse<DashboardStats>(res)
  },
}
