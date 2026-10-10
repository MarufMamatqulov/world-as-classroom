from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False, default="Student")
    age = Column(Integer, default=14)
    grade = Column(String(50), default="8")
    knowledge_level = Column(String(50), default="intermediate")  # beginner, intermediate, advanced
    preferred_language = Column(String(10), default="uz")  # uz, en, ru
    custom_api_key = Column(String(255), nullable=True)
    xp = Column(Integer, default=0)
    streak_days = Column(Integer, default=1)
    last_active_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    explorations = relationship("Exploration", back_populates="user", cascade="all, delete-orphan")
    quiz_attempts = relationship("QuizAttempt", back_populates="user", cascade="all, delete-orphan")
    quest_progress = relationship("UserQuestProgress", back_populates="user", cascade="all, delete-orphan")
    scientist_sessions = relationship("ScientistSession", back_populates="user", cascade="all, delete-orphan")


class Exploration(Base):
    __tablename__ = "explorations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    object_name = Column(String(255), nullable=False)
    object_name_en = Column(String(255), nullable=True)
    category = Column(String(100), nullable=True)
    image_thumbnail = Column(Text, nullable=True)
    detected_objects_json = Column(Text, nullable=True)  # JSON serialized
    primary_subject = Column(String(50), default="Physics")
    language = Column(String(10), default="uz")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="explorations")
    lesson = relationship("Lesson", back_populates="exploration", uselist=False, cascade="all, delete-orphan")
    tutor_messages = relationship("TutorMessage", back_populates="exploration", cascade="all, delete-orphan")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    exploration_id = Column(Integer, ForeignKey("explorations.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    summary = Column(Text, nullable=False)
    subjects_json = Column(Text, nullable=False)  # JSON serialized dict of subjects
    experiments_json = Column(Text, nullable=True)  # JSON serialized list of experiments
    fun_facts_json = Column(Text, nullable=True)  # JSON serialized list of fun facts
    vocabulary_json = Column(Text, nullable=True)  # JSON serialized list of terms
    created_at = Column(DateTime, default=datetime.utcnow)

    exploration = relationship("Exploration", back_populates="lesson")
    quiz = relationship("Quiz", back_populates="lesson", uselist=False, cascade="all, delete-orphan")


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False, index=True)
    questions_json = Column(Text, nullable=False)  # JSON serialized list of questions
    created_at = Column(DateTime, default=datetime.utcnow)

    lesson = relationship("Lesson", back_populates="quiz")
    attempts = relationship("QuizAttempt", back_populates="quiz", cascade="all, delete-orphan")


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id", ondelete="CASCADE"), nullable=False, index=True)
    score = Column(Integer, nullable=False)
    total_questions = Column(Integer, nullable=False)
    answers_json = Column(Text, nullable=True)
    completed_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="attempts")


class TutorMessage(Base):
    __tablename__ = "tutor_messages"

    id = Column(Integer, primary_key=True, index=True)
    exploration_id = Column(Integer, ForeignKey("explorations.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    role = Column(String(50), nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    exploration = relationship("Exploration", back_populates="tutor_messages")


class Quest(Base):
    __tablename__ = "quests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    title_en = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    description_en = Column(Text, nullable=True)
    domain = Column(String(50), nullable=False)  # Mechanics, Optics, Botany, Chemistry, Thermodynamics, Technology
    target_keyword = Column(String(100), nullable=False)
    xp_reward = Column(Integer, default=100)
    badge_icon = Column(String(50), default="Award")
    badge_title = Column(String(100), default="Junior Explorer")
    validation_question = Column(Text, nullable=False)
    validation_options_json = Column(Text, nullable=False)  # JSON list of strings
    correct_option_index = Column(Integer, default=0)
    validation_explanation = Column(Text, nullable=True)
    is_daily = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    progress_records = relationship("UserQuestProgress", back_populates="quest", cascade="all, delete-orphan")


class UserQuestProgress(Base):
    __tablename__ = "user_quest_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    quest_id = Column(Integer, ForeignKey("quests.id", ondelete="CASCADE"), nullable=False, index=True)
    exploration_id = Column(Integer, ForeignKey("explorations.id", ondelete="SET NULL"), nullable=True)
    status = Column(String(20), default="in_progress")  # in_progress, completed
    earned_xp = Column(Integer, default=0)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="quest_progress")
    quest = relationship("Quest", back_populates="progress_records")


class AIUsageLog(Base):
    __tablename__ = "ai_usage_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    endpoint = Column(String(100), nullable=False)
    model_name = Column(String(100), nullable=False)
    prompt_tokens = Column(Integer, default=0)
    completion_tokens = Column(Integer, default=0)
    estimated_cost_usd = Column(Float, default=0.0)
    latency_ms = Column(Integer, default=0)
    cache_hit = Column(Integer, default=0)  # 1 = hit, 0 = miss
    created_at = Column(DateTime, default=datetime.utcnow)


class LessonCache(Base):
    __tablename__ = "lesson_caches"

    id = Column(Integer, primary_key=True, index=True)
    cache_key = Column(String(255), unique=True, index=True, nullable=False)
    response_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class ScientistSession(Base):
    __tablename__ = "scientist_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    object_name = Column(String(255), nullable=False)
    domain = Column(String(100), default="Physics")
    observation = Column(Text, nullable=False)
    hypothesis = Column(Text, nullable=False)
    experiment_plan_json = Column(Text, nullable=True)  # JSON of steps, materials, safety
    results_notes = Column(Text, nullable=True)
    ai_evaluation_json = Column(Text, nullable=True)  # JSON evaluation & feedback
    xp_earned = Column(Integer, default=50)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="scientist_sessions")

