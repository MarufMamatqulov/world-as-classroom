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
    subject_mastery: List[SubjectMastery]
    recent_explorations: List[ExplorationSummary]
    achievements: List[Achievement]
