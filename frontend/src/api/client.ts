export interface UserProfile {
  id: number
  email: string
  full_name: string
  age: number
  grade: string
  knowledge_level: string
  preferred_language: string
  has_custom_api_key: boolean
  xp?: number
  streak_days?: number
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
  quiz_completed?: boolean
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
  total_xp?: number
  subject_mastery: SubjectMastery[]
  recent_explorations: ExplorationSummary[]
  achievements: Achievement[]
}

// --- Real World Quests ---
export interface QuestResponse {
  id: number
  title: string
  title_en?: string
  description: string
  domain: string
  target_keyword: string
  xp_reward: number
  badge_icon: string
  badge_title: string
  validation_question: string
  validation_options: string[]
  is_daily: boolean
  status: 'active' | 'completed'
  completed_at?: string
}

export interface QuestSubmitResponse {
  quest_id: number
  success: boolean
  message: string
  xp_awarded: number
  badge_awarded?: string
  explanation?: string
}

export interface UserBadgeResponse {
  id: string
  title: string
  icon: string
  domain: string
  unlocked_at: string
  xp: number
}

// --- AI Scientist Mode ---
export interface ExperimentPlanItem {
  title: string
  materials: string[]
  steps: string[]
  safety_guidelines: string
  expected_observation: string
}

export interface ScientistInquiryResponse {
  object_name: string
  domain: string
  hypothesis_critique: string
  is_valid_hypothesis: boolean
  experiment_plan: ExperimentPlanItem
  scientific_principles: string[]
  ai_guidance: string
  xp_awarded: number
}

// --- Discovery Stories ---
export interface DiscoveryStoryCardResponse {
  exploration_id: number
  object_name: string
  object_name_en?: string
  category: string
  primary_subject: string
  key_formula?: string
  core_discovery: string
  explorer_callsign: string
  xp_earned: number
  discovery_date: string
  image_thumbnail?: string
  verified_badge: string
  share_url: string
}

// --- Knowledge Passport ---
export interface RealmStamp {
  id: string
  name: string
  domain: string
  icon: string
  color: string
  unlocked: boolean
  discoveries_count: number
  mastery_level: 'Novice' | 'Adept' | 'Master'
}

export interface PassportLevelInfo {
  current_level: number
  rank_title: string
  current_xp: number
  next_level_xp: number
  progress_percentage: number
}

export interface KnowledgePassportResponse {
  explorer_callsign: string
  member_since: string
  level_info: PassportLevelInfo
  total_discoveries: number
  streak_days: number
  stamps: RealmStamp[]
  recent_chronicle: ExplorationSummary[]
}

// --- Learning Analytics & System Monitoring ---
export interface AIRequestMetric {
  endpoint: string
  model_name: string
  prompt_tokens: number
  completion_tokens: number
  estimated_cost_usd: number
  latency_ms: number
  cache_hit: boolean
  created_at: string
}

export interface SystemCostAnalytics {
  total_api_calls: number
  total_prompt_tokens: number
  total_completion_tokens: number
  total_tokens: number
  total_cost_usd: number
  cache_hits: number
  cache_hit_rate_pct: number
  avg_latency_ms: number
  recent_logs: AIRequestMetric[]
}

export interface AnalyticsOverview {
  student_stats: DashboardStats
  passport: KnowledgePassportResponse
  system_monitoring?: SystemCostAnalytics
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
      const data = await res.json()
      errorDetail = data.detail || data.message || errorDetail
    } catch {
      // keep fallback
    }
    throw new Error(errorDetail)
  }
  return res.json()
}

export const api = {
  // Auth
  async register(data: any) {
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    })
    return handleResponse<{ access_token: string; user: UserProfile }>(res)
  },

  async login(data: any) {
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

  async updateProfile(data: any) {
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

  // Scanner
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

  async correctDetectedObject(original_name: string, corrected_name: string, category?: string, language: string = 'uz') {
    const res = await fetch(`${API_BASE}/scan/correct`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeader(),
      },
      body: JSON.stringify({ original_name, corrected_name, category, language }),
    })
    return handleResponse<{ success: boolean; corrected_object: DetectedObject }>(res)
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
    primary_focus_subject?: string
    difficulty_level?: string
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

  async getDiscoveryStoryCard(lessonId: number) {
    const res = await fetch(`${API_BASE}/lessons/${lessonId}/story-card`, {
      headers: { ...getAuthHeader() },
    })
    return handleResponse<DiscoveryStoryCardResponse>(res)
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

  // Real World Quests
  async getDailyQuests() {
    const res = await fetch(`${API_BASE}/quests/daily`, {
      headers: { ...getAuthHeader() },
    })
    return handleResponse<QuestResponse[]>(res)
  },

  async submitQuest(questId: number, selectedOptionIndex: number, explorationId?: number) {
    const res = await fetch(`${API_BASE}/quests/submit`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeader(),
      },
      body: JSON.stringify({
        quest_id: questId,
        selected_option_index: selectedOptionIndex,
        exploration_id: explorationId,
      }),
    })
    return handleResponse<QuestSubmitResponse>(res)
  },

  async getUserBadges() {
    const res = await fetch(`${API_BASE}/quests/badges`, {
      headers: { ...getAuthHeader() },
    })
    return handleResponse<UserBadgeResponse[]>(res)
  },

  // AI Scientist Mode
  async conductScientificInquiry(data: {
    object_name: string
    domain?: string
    observation: string
    hypothesis: string
    language?: string
    difficulty_level?: string
  }) {
    const res = await fetch(`${API_BASE}/scientist/inquiry`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeader(),
      },
      body: JSON.stringify(data),
    })
    return handleResponse<ScientistInquiryResponse>(res)
  },

  async getScientistHistory() {
    const res = await fetch(`${API_BASE}/scientist/history`, {
      headers: { ...getAuthHeader() },
    })
    return handleResponse<any[]>(res)
  },

  // Knowledge Passport
  async getMyPassport() {
    const res = await fetch(`${API_BASE}/passport/me`, {
      headers: { ...getAuthHeader() },
    })
    return handleResponse<KnowledgePassportResponse>(res)
  },

  // Learning Analytics & Monitoring
  async getSystemAnalytics() {
    const res = await fetch(`${API_BASE}/analytics/system`, {
      headers: { ...getAuthHeader() },
    })
    return handleResponse<SystemCostAnalytics>(res)
  },

  async getAnalyticsOverview() {
    const res = await fetch(`${API_BASE}/analytics/overview`, {
      headers: { ...getAuthHeader() },
    })
    return handleResponse<AnalyticsOverview>(res)
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
