from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# --- Authentication & User ---
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=2)
    age: Optional[int] = 14
    grade: Optional[str] = "8"
    knowledge_level: Optional[str] = "intermediate"  # beginner, intermediate, advanced
    preferred_language: Optional[str] = "uz"  # uz, en, ru

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    age: Optional[int] = None
    grade: Optional[str] = None
    knowledge_level: Optional[str] = None
    preferred_language: Optional[str] = None
    custom_api_key: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    age: int
    grade: str
    knowledge_level: str
    preferred_language: str
    has_custom_api_key: bool
    xp: int = 0
    streak_days: int = 1
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# --- Object Detection & Scanning ---
class BoundingBox(BaseModel):
    ymin: float = 0.0
    xmin: float = 0.0
    ymax: float = 1.0
    xmax: float = 1.0

class DetectedObject(BaseModel):
    name: str
    name_en: str
    category: str
    educational_hook: str
    subjects: List[str]
    confidence: float = 0.95
    bounding_box: Optional[BoundingBox] = None

class ScanResponse(BaseModel):
    detected_objects: List[DetectedObject]
    image_preview: Optional[str] = None
    source: str = "camera"  # "camera", "upload", "sample"

# --- Lesson Generation ---
class ConceptItem(BaseModel):
    headline: str
    explanation: str
    formula: Optional[str] = None
    real_world_example: Optional[str] = None

class SubjectModule(BaseModel):
    subject: str  # Physics, Chemistry, Biology, Mathematics, History, Technology
    title: str
    icon: Optional[str] = None
    concepts: List[ConceptItem]
    real_world_connection: str

class LessonExperiment(BaseModel):
    title: str
    materials: List[str]
    steps: List[str]
    science_behind_it: str
    safety_note: Optional[str] = None

class FunFact(BaseModel):
    fact: str
    why_cool: str

class VocabularyItem(BaseModel):
    term: str
    definition: str

class GenerateLessonRequest(BaseModel):
    object_name: str
    object_name_en: Optional[str] = None
    category: Optional[str] = None
    language: Optional[str] = "uz"  # uz, en, ru
    age: Optional[int] = 14
    grade: Optional[str] = "8"
    knowledge_level: Optional[str] = "intermediate"
    primary_focus_subject: Optional[str] = None  # Physics, Mathematics, Biology, Chemistry, Technology, History
    difficulty_level: Optional[str] = "intermediate"  # beginner, intermediate, advanced
    image_thumbnail: Optional[str] = None

class LessonDetail(BaseModel):
    id: int
    exploration_id: int
    object_name: str
    object_name_en: Optional[str] = None
    title: str
    summary: str
    subjects: List[SubjectModule]
    experiments: List[LessonExperiment]
    fun_facts: List[FunFact]
    vocabulary: List[VocabularyItem]
    language: str
    created_at: datetime

# --- Quizzes ---
class QuizQuestion(BaseModel):
    id: int
    question: str
    options: List[str]
    correct_index: int
    explanation: str
    subject: str

class QuizDetail(BaseModel):
    id: int
    lesson_id: int
    questions: List[QuizQuestion]

class QuizSubmitRequest(BaseModel):
    quiz_id: int
    answers: List[int]  # index selected for each question

class AnswerEvaluation(BaseModel):
    question_id: int
    question: str
    user_answer_index: int
    correct_answer_index: int
    is_correct: bool
    explanation: str
    subject: str

class QuizSubmitResponse(BaseModel):
    attempt_id: int
    quiz_id: int
    score: int
    total_questions: int
    percentage: float
    evaluations: List[AnswerEvaluation]
    feedback: str

# --- AI Tutor Chat ---
class TutorMessageSchema(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

class TutorChatRequest(BaseModel):
    exploration_id: int
    message: str
    language: Optional[str] = "uz"

class TutorChatResponse(BaseModel):
    reply: str
    suggested_prompts: List[str]

# --- Dashboard & Progress ---
class ExplorationSummary(BaseModel):
    id: int
    object_name: str
    category: Optional[str]
    primary_subject: str
    language: str
    image_thumbnail: Optional[str]
    created_at: datetime
    quiz_completed: bool = False
    best_score: Optional[int] = None
    total_questions: Optional[int] = None

class SubjectMastery(BaseModel):
    subject: str
    points: int
    lessons_count: int

class Achievement(BaseModel):
    id: str
    title: str
    description: str
    icon: str
    unlocked: bool
    progress: int
    max_progress: int

class DashboardStats(BaseModel):
    total_explorations: int
    total_quizzes_completed: int
    average_quiz_score: float
    current_streak_days: int
    total_xp: int = 0
    subject_mastery: List[SubjectMastery]
    recent_explorations: List[ExplorationSummary]
    achievements: List[Achievement]


# --- Object Recognition Correction ---
class ObjectCorrectionRequest(BaseModel):
    original_name: str
    corrected_name: str
    category: Optional[str] = "General Science"
    language: Optional[str] = "uz"


class ObjectCorrectionResponse(BaseModel):
    success: bool
    corrected_object: DetectedObject


# --- Real World Quests ---
class QuestResponse(BaseModel):
    id: int
    title: str
    title_en: Optional[str]
    description: str
    domain: str
    target_keyword: str
    xp_reward: int
    badge_icon: str
    badge_title: str
    validation_question: str
    validation_options: List[str]
    is_daily: bool
    status: str = "active"  # "active", "completed"
    completed_at: Optional[datetime] = None


class QuestSubmitRequest(BaseModel):
    quest_id: int
    exploration_id: Optional[int] = None
    selected_option_index: int


class QuestSubmitResponse(BaseModel):
    quest_id: int
    success: bool
    message: str
    xp_awarded: int
    badge_awarded: Optional[str] = None
    explanation: Optional[str] = None


class UserBadgeResponse(BaseModel):
    id: str
    title: str
    icon: str
    domain: str
    unlocked_at: datetime
    xp: int


# --- AI Scientist Mode ---
class ExperimentPlanItem(BaseModel):
    title: str
    materials: List[str]
    steps: List[str]
    safety_guidelines: str
    expected_observation: str


class ScientistInquiryRequest(BaseModel):
    object_name: str
    domain: Optional[str] = "Physics"
    observation: str
    hypothesis: str
    language: Optional[str] = "uz"
    difficulty_level: Optional[str] = "intermediate"


class ScientistInquiryResponse(BaseModel):
    object_name: str
    domain: str
    hypothesis_critique: str
    is_valid_hypothesis: bool
    experiment_plan: ExperimentPlanItem
    scientific_principles: List[str]
    ai_guidance: str
    xp_awarded: int = 50


# --- Discovery Stories ---
class DiscoveryStoryCardResponse(BaseModel):
    exploration_id: int
    object_name: str
    object_name_en: Optional[str]
    category: str
    primary_subject: str
    key_formula: Optional[str]
    core_discovery: str
    explorer_callsign: str
    xp_earned: int
    discovery_date: str
    image_thumbnail: Optional[str]
    verified_badge: str
    share_url: str


# --- Knowledge Passport ---
class RealmStamp(BaseModel):
    id: str
    name: str
    domain: str
    icon: str
    color: str
    unlocked: bool
    discoveries_count: int
    mastery_level: str  # "Novice", "Adept", "Master"


class PassportLevelInfo(BaseModel):
    current_level: int
    rank_title: str
    current_xp: int
    next_level_xp: int
    progress_percentage: float


class KnowledgePassportResponse(BaseModel):
    explorer_callsign: str
    member_since: str
    level_info: PassportLevelInfo
    total_discoveries: int
    streak_days: int
    stamps: List[RealmStamp]
    recent_chronicle: List[ExplorationSummary]


# --- Learning Analytics & Cost Monitoring ---
class AIRequestMetric(BaseModel):
    endpoint: str
    model_name: str
    prompt_tokens: int
    completion_tokens: int
    estimated_cost_usd: float
    latency_ms: int
    cache_hit: bool
    created_at: datetime


class SystemCostAnalytics(BaseModel):
    total_api_calls: int
    total_prompt_tokens: int
    total_completion_tokens: int
    total_tokens: int
    total_cost_usd: float
    cache_hits: int
    cache_hit_rate_pct: float
    avg_latency_ms: float
    recent_logs: List[AIRequestMetric]


class AnalyticsOverview(BaseModel):
    student_stats: DashboardStats
    passport: KnowledgePassportResponse
    system_monitoring: Optional[SystemCostAnalytics] = None

