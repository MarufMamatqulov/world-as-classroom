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
    created_at = Column(DateTime, default=datetime.utcnow)

    explorations = relationship("Exploration", back_populates="user", cascade="all, delete-orphan")
    quiz_attempts = relationship("QuizAttempt", back_populates="user", cascade="all, delete-orphan")


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
