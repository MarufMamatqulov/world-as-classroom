# 🌍 World as a Classroom (Olam Sinfxonasi)
### AI-Powered Interactive Real-World Learning Platform

> **Turn any real-world object into an interactive educational experience using AI and your smartphone camera.**

---

## 🚀 Key Highlights & Features

1. **AI Camera Scanner:**
   - Real-time mobile/desktop camera capture with front/back camera switching.
   - Upload existing images or select from curated classroom objects.
   - Multimodal object detection using Google Gemini. Detects multiple objects in a scene and lets students choose which specific object or component to explore.
2. **Smart Interdisciplinary Lesson Generator:**
   - Automatically generates structured lessons covering:
     - 🚀 **Physics** (Newton's laws, mechanics, friction, angular momentum, formulas)
     - 📐 **Mathematics** (Circumference, gear ratios, velocities, geometry)
     - 🧬 **Biology** (Cellular respiration, biomechanics, botany, ecology)
     - ⚗️ **Chemistry** (Materials science, vulcanization, polymers, reactions)
     - 🏛️ **History & Society** (Inventions, societal impact, historical milestones)
     - 💻 **Technology & Engineering** (Modern hydraulics, sensors, renewables)
3. **Adaptive Learning:**
   - Customizes lesson complexity according to the student's age (8–18+), grade level (4th–11th / University), and complexity level (*Beginner*, *Intermediate*, *Advanced*).
4. **Interactive AI Tutor with Speech Synthesis (TTS):**
   - Contextual Q&A tutor understanding the scanned object and lesson history.
   - Built-in text-to-speech audio read-aloud functionality.
   - Instant suggested prompt chips.
5. **Interactive AI Quizzes:**
   - 3–5 multi-disciplinary questions per lesson.
   - Immediate evaluation with pedagogical explanations for correct/incorrect answers.
   - Confetti celebration upon completion and progress recording.
6. **Learning Dashboard & Gamification:**
   - Tracks total objects explored, quizzes completed, average score, and daily learning streaks.
   - Subject mastery points radar/meters.
   - Unlockable achievement badges (*Birinchi Qadam*, *Viktorina Ustasi*, *Yosh Alloma*).
7. **Multilingual Architecture:**
   - **Uzbek (O'zbek tili)** as primary native interface and curriculum language.
   - **English** and **Russian (Русский язык)** fully supported with dynamic language switching.
8. **Robust Database & Offline Fallback:**
   - Supports **PostgreSQL** for production and **SQLite** out-of-the-box for instant local development.
   - Includes high-quality educational catalog fallback for instant testing without an active Gemini API key.

---

## 🛠️ Technology Stack

- **Frontend:** Vue 3 (Composition API) + TypeScript + Tailwind CSS + Pinia + Vue Router + Lucide Icons + Canvas Confetti
- **Backend:** Python FastAPI + SQLAlchemy (Async) + Pydantic v2 + Uvicorn + PyJWT + Bcrypt
- **AI Engine:** Google Gemini Multimodal API (`google-genai` SDK)
- **Database:** PostgreSQL (with SQLite async fallback)

---

## 📁 Project Architecture

```
world as  Classroom/
├── backend/
│   ├── app/
│   │   ├── main.py               # FastAPI app entry point & lifespan
│   │   ├── config.py             # App configurations & environment variables
│   │   ├── database.py           # Async SQLAlchemy engine (SQLite / PostgreSQL)
│   │   ├── models.py             # Database models (User, Exploration, Lesson, Quiz, etc.)
│   │   ├── schemas.py            # Pydantic request/response schemas
│   │   ├── auth.py               # Password hashing & JWT token management
│   │   ├── dependencies.py       # Auth dependencies (optional & required)
│   │   ├── routers/
│   │   │   ├── auth_router.py    # Register, login, profile endpoints
│   │   │   ├── scan_router.py    # Camera upload & sample objects
│   │   │   ├── lesson_router.py  # Lesson generation & retrieval
│   │   │   ├── quiz_router.py    # Quiz retrieval & score evaluation
│   │   │   ├── tutor_router.py   # AI tutor chat with memory
│   │   │   └── dashboard_router.py # Student progress & achievements
│   │   └── services/
│   │       ├── gemini_service.py # Gemini multimodal integration
│   │       └── mock_curriculum.py # Multilingual pedagogical catalog
│   ├── requirements.txt
│   └── run.py
├── frontend/
│   ├── src/
│   │   ├── api/client.ts         # Typed API client
│   │   ├── stores/               # Pinia stores (auth, exploration)
│   │   ├── i18n/                 # Multilingual localization (uz, en, ru)
│   │   ├── components/
│   │   │   ├── Navbar.vue
│   │   │   ├── CameraScanner.vue # Real-time camera & upload
│   │   │   ├── ObjectSelector.vue# Multi-object selector
│   │   │   ├── SubjectTabs.vue   # Multi-subject interactive viewer
│   │   │   ├── ExperimentCard.vue# Try This At Home hands-on card
│   │   │   ├── InteractiveQuiz.vue
│   │   │   ├── AITutorChat.vue   # AI Tutor chat with TTS
│   │   │   └── SampleGallery.vue
│   │   ├── views/                # Routed views (Home, Scanner, Lesson, Dashboard, Settings, Login)
│   │   ├── router/index.ts
│   │   ├── App.vue
│   │   ├── main.ts
│   │   └── style.css
│   ├── package.json
│   ├── vite.config.ts
│   └── tailwind.config.js
├── .env.example
├── README.md
├── start.bat
└── start.ps1
```

---

## ⚡ Quick Start Instructions

### 1. Prerequisites
- **Node.js**: v18+ (Node v25 installed)
- **Python**: 3.10+ (Python 3.14 installed)
- *(Optional)* PostgreSQL 17 or above.

### 2. Environment Configuration
Create or inspect the `.env` file in the root workspace:
```bash
# Gemini API Key (optional for offline testing, required for live multimodal AI)
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# Database URL:
# Defaults to SQLite (zero setup required):
DATABASE_URL=sqlite+aiosqlite:///./world_classroom.db

# Or connect to your PostgreSQL:
# DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/world_classroom

SECRET_KEY=world-as-a-classroom-super-secret-key-2026
```

### 3. Launching Locally

#### Method A: Using 1-Click Launch Script (Windows)
Double-click `start.bat` or run:
```powershell
.\start.ps1
```

#### Method B: Manual Startup

**Start Backend:**
```powershell
.\venv\Scripts\python backend\run.py
```
Backend will be available at: `http://localhost:8000`  
Interactive Swagger API docs at: `http://localhost:8000/docs`

**Start Frontend:**
```powershell
cd frontend
npm run dev
```
Frontend will be available at: `http://localhost:5173`

---

## 🧪 Testing the Core Workflow

1. Open `http://localhost:5173`.
2. Click **"Kamerani Ochish & Skanerlash"** (Open Camera & Scan).
3. Point your camera at a real object or click one of the curated classroom objects (e.g., **Velosiped / Bicycle** or **O'simlik Bargi / Plant Leaf**).
4. The AI identifies the object and generates a personalized lesson across Physics, Mathematics, Biology, Chemistry, Technology, and History.
5. Review the **"Uyda O'tkaziladigan Sinov" (Try This At Home)** experiment with materials checklist and safety instructions.
6. Solve the **AI Quiz** and submit to check your score and view detailed educational explanations.
7. Ask questions to the **AI Tutor** and test the text-to-speech audio pronunciation.
8. Navigate to **"Mening Natijalarim" (Dashboard)** to verify your saved scores, streak, and unlocked achievement badges.
