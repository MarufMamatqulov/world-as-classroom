import json
import re
import logging
from typing import List, Dict, Any, Optional
from app.config import settings
from app.services.mock_curriculum import (
    get_fallback_detected_objects,
    get_fallback_lesson
)

logger = logging.getLogger(__name__)

def _clean_json_text(text: str) -> str:
    """Strip markdown code blocks and whitespace from JSON response."""
    text = text.strip()
    match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
    if match:
        return match.group(1).strip()
    return text

class GeminiService:
    def __init__(self):
        self.default_model = settings.GEMINI_MODEL

    def _get_client(self, custom_key: Optional[str] = None):
        key = (custom_key or "").strip() or (settings.GEMINI_API_KEY or "").strip()
        if not key:
            return None
        try:
            from google import genai
            return genai.Client(api_key=key)
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            return None

    async def detect_objects(
        self,
        image_bytes: bytes,
        mime_type: str = "image/jpeg",
        language: str = "uz",
        custom_key: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        client = self._get_client(custom_key)
        if not client:
            logger.info("No Gemini API key provided. Using educational mock detection.")
            return get_fallback_detected_objects("bicycle", language)

        prompt = f"""
You are an expert educational AI in "World as a Classroom".
Analyze this image carefully. Identify 1 to 4 prominent real-world objects or key functional components that have high scientific and educational value for school students (e.g., Physics, Chemistry, Biology, Mathematics, Technology, History).

Respond strictly with a JSON array adhering to this schema:
[
  {{
    "name": "Object name translated into {language} (uz: Uzbek, en: English, ru: Russian)",
    "name_en": "Standard English name",
    "category": "Domain (e.g. Transport & Mechanics, Botany, Optics, Electronics)",
    "educational_hook": "A 1-sentence captivating hook in {language} explaining why this object is exciting to explore",
    "subjects": ["Physics", "Mathematics", "Biology", "Chemistry", "Technology", "History"],
    "confidence": 0.95,
    "bounding_box": {{"ymin": 0.1, "xmin": 0.1, "ymax": 0.9, "xmax": 0.9}}
  }}
]
Language for name and educational_hook: {language}.
Return only valid JSON.
"""
        try:
            from google.genai import types
            part = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
            
            response = client.models.generate_content(
                model=self.default_model,
                contents=[part, prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.2
                )
            )
            raw = response.text or ""
            cleaned = _clean_json_text(raw)
            data = json.loads(cleaned)
            if isinstance(data, list) and len(data) > 0:
                return data
            elif isinstance(data, dict) and "objects" in data:
                return data["objects"]
        except Exception as e:
            logger.error(f"Gemini object detection failed: {e}. Falling back.")
        
        return get_fallback_detected_objects("bicycle", language)

    async def generate_lesson(
        self,
        object_name: str,
        object_name_en: Optional[str] = None,
        language: str = "uz",
        age: int = 14,
        grade: str = "8",
        knowledge_level: str = "intermediate",
        custom_key: Optional[str] = None
    ) -> Dict[str, Any]:
        client = self._get_client(custom_key)
        if not client:
            logger.info("No Gemini API key provided. Using educational mock lesson.")
            return get_fallback_lesson(object_name, language)

        target_lang_str = "Uzbek (O'zbek tili, Lotin yozuvi)" if language == "uz" else ("Russian (Русский язык)" if language == "ru" else "English")
        level_instruction = {
            "beginner": "Use simple, visual, fun analogies without heavy calculus, focus on wonder and intuitive concepts.",
            "intermediate": "Provide clear scientific terms, fundamental formulas explained clearly, and everyday applications.",
            "advanced": "Include academic formulas, mathematical equations, in-depth chemical reactions, and engineering nuances."
        }.get(knowledge_level, "Provide clear scientific terms and engaging explanations.")

        prompt = f"""
You are the master curriculum creator for 'World as a Classroom', an innovative AI learning platform.
Create a rich, multi-disciplinary interactive lesson about the object: "{object_name}" (English: {object_name_en or object_name}).

Target Student Profile:
- Age: {age} years old
- Grade: {grade}
- Complexity Level: {knowledge_level} ({level_instruction})
- Language: {target_lang_str}

Please generate an extensive, inspiring lesson strictly formatted as the following JSON object:
{{
  "name": "{object_name}",
  "name_en": "{object_name_en or object_name}",
  "category": "Educational domain",
  "title": "Engaging, inspiring lesson title in {target_lang_str}",
  "summary": "2-3 comprehensive pedagogical paragraphs explaining the object's wonders in {target_lang_str}",
  "modules": [
    {{
      "subject": "Physics",
      "title": "Title in {target_lang_str}",
      "icon": "Atom",
      "concepts": [
        {{
          "headline": "Core concept headline",
          "explanation": "Detailed explanation tailored to student level",
          "formula": "Relevant mathematical/physical formula (e.g. F = m * a)",
          "real_world_example": "Concrete everyday example"
        }}
      ],
      "real_world_connection": "How this concept applies to modern industry, vehicles, or space"
    }},
    {{
      "subject": "Mathematics",
      "title": "Title in {target_lang_str}",
      "icon": "Calculator",
      "concepts": [
        {{
          "headline": "Core calculation or geometry",
          "explanation": "Calculation explanation",
          "formula": "Math formula",
          "real_world_example": "Numerical example"
        }}
      ],
      "real_world_connection": "Real world use"
    }},
    {{
      "subject": "Biology",
      "title": "Title in {target_lang_str}",
      "icon": "HeartPulse",
      "concepts": [
        {{
          "headline": "Biomechanics / Anatomy / Ecology",
          "explanation": "Biological explanation",
          "formula": null,
          "real_world_example": "Example in living organisms"
        }}
      ],
      "real_world_connection": "Connection to human body or nature"
    }},
    {{
      "subject": "Chemistry",
      "title": "Title in {target_lang_str}",
      "icon": "FlaskConical",
      "concepts": [
        {{
          "headline": "Materials science & Chemical reactions",
          "explanation": "Chemical properties and bonds",
          "formula": "Chemical formula or reaction",
          "real_world_example": "Material behavior"
        }}
      ],
      "real_world_connection": "Industrial chemistry or material innovation"
    }},
    {{
      "subject": "History",
      "title": "Title in {target_lang_str}",
      "icon": "Landmark",
      "concepts": [
        {{
          "headline": "Invention & Societal Impact",
          "explanation": "Historical timeline and transformation",
          "formula": null,
          "real_world_example": "Historical event"
        }}
      ],
      "real_world_connection": "Modern societal legacy"
    }},
    {{
      "subject": "Technology",
      "title": "Title in {target_lang_str}",
      "icon": "Cpu",
      "concepts": [
        {{
          "headline": "Engineering Innovation",
          "explanation": "Modern sensors, materials, or automation",
          "formula": null,
          "real_world_example": "High-tech implementation"
        }}
      ],
      "real_world_connection": "Future technology developments"
    }}
  ],
  "experiments": [
    {{
      "title": "Safe DIY Experiment Title in {target_lang_str}",
      "materials": ["Item 1", "Item 2", "Item 3"],
      "steps": ["Step 1", "Step 2", "Step 3", "Step 4"],
      "science_behind_it": "Clear scientific explanation of observed results",
      "safety_note": "Safety advice"
    }}
  ],
  "fun_facts": [
    {{
      "fact": "Mind-blowing trivia fact",
      "why_cool": "Why this fact will surprise friends"
    }},
    {{
      "fact": "Second fascinating fact",
      "why_cool": "Explanation"
    }}
  ],
  "vocabulary": [
    {{"term": "Scientific Term 1", "definition": "Definition in {target_lang_str}"}},
    {{"term": "Scientific Term 2", "definition": "Definition in {target_lang_str}"}},
    {{"term": "Scientific Term 3", "definition": "Definition in {target_lang_str}"}},
    {{"term": "Scientific Term 4", "definition": "Definition in {target_lang_str}"}}
  ],
  "quiz": [
    {{
      "id": 1,
      "question": "Question 1 testing Physics or Math in {target_lang_str}",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_index": 1,
      "explanation": "Detailed explanation why Option B is correct",
      "subject": "Physics"
    }},
    {{
      "id": 2,
      "question": "Question 2 testing Chemistry or Materials in {target_lang_str}",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_index": 2,
      "explanation": "Detailed explanation why Option C is correct",
      "subject": "Chemistry"
    }},
    {{
      "id": 3,
      "question": "Question 3 testing Biology or History in {target_lang_str}",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_index": 0,
      "explanation": "Detailed explanation why Option A is correct",
      "subject": "Biology"
    }},
    {{
      "id": 4,
      "question": "Question 4 testing Math or Technology in {target_lang_str}",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_index": 3,
      "explanation": "Detailed explanation why Option D is correct",
      "subject": "Technology"
    }}
  ]
}}

Everything must be written in {target_lang_str}. Return ONLY the JSON object.
"""
        try:
            from google.genai import types
            response = client.models.generate_content(
                model=self.default_model,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.4
                )
            )
            raw = response.text or ""
            cleaned = _clean_json_text(raw)
            data = json.loads(cleaned)
            if isinstance(data, dict) and "modules" in data:
                return data
        except Exception as e:
            logger.error(f"Gemini lesson generation failed: {e}. Falling back.")

        return get_fallback_lesson(object_name, language)

    async def tutor_chat(
        self,
        object_name: str,
        lesson_summary: str,
        chat_history: List[Dict[str, str]],
        user_message: str,
        language: str = "uz",
        custom_key: Optional[str] = None
    ) -> Dict[str, Any]:
        client = self._get_client(custom_key)
        target_lang_str = "Uzbek" if language == "uz" else ("Russian" if language == "ru" else "English")

        if not client:
            # High quality fallback response
            if language == "uz":
                reply = f"Ajoyib savol! '{object_name}' misolida bu hodisa fizika va muhandislikning eng qiziqarli qonuniyatlariga bog'liq. Har qanday murakkab texnik qurilma yoki tabiiy jarayon energiyaning bir turdan ikkinchi turga aylanishi tamoyiliga tayanadi. Sizni yana qaysi jihati qiziqtiradi?"
                prompts = [
                    f"{object_name} qanday harakatlanadi?",
                    "Fizika qonunlarini soddaroq tushuntiring",
                    "Uyda qanday tajriba o'tkazish mumkin?"
                ]
            elif language == "ru":
                reply = f"Отличный вопрос! На примере '{object_name}' это объясняется фундаментальными законами физики и инженерии. Энергия преобразуется из одной формы в другую с максимальной эффективностью. Какой конкретно аспект вам хотелось бы изучить глубже?"
                prompts = [
                    f"Как работает {object_name}?",
                    "Объясните физику простыми словами",
                    "Какой опыт можно провести дома?"
                ]
            else:
                reply = f"Great question! In the context of the {object_name}, this phenomenon demonstrates core physical and engineering principles such as mechanical advantage and conservation of energy. What specific aspect would you like to explore further?"
                prompts = [
                    f"How does {object_name} work?",
                    "Explain the physics in simple terms",
                    "What experiment can I try at home?"
                ]
            return {"reply": reply, "suggested_prompts": prompts}

        prompt = f"""
You are the World as a Classroom Interactive AI Tutor.
The student is studying the real-world object: "{object_name}".
Context of the lesson: {lesson_summary}

Recent conversation history:
{json.dumps(chat_history[-6:], ensure_ascii=False)}

Student's new question:
"{user_message}"

Respond as an inspiring, supportive, and clear educational mentor. Use analogies from everyday life.
Respond in {target_lang_str}.
Return a JSON object strictly matching:
{{
  "reply": "Your educational, engaging explanation in {target_lang_str}",
  "suggested_prompts": [
    "Suggested follow-up prompt 1 in {target_lang_str}",
    "Suggested follow-up prompt 2 in {target_lang_str}",
    "Suggested follow-up prompt 3 in {target_lang_str}"
  ]
}}
"""
        try:
            from google.genai import types
            response = client.models.generate_content(
                model=self.default_model,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    temperature=0.5
                )
            )
            raw = response.text or ""
            cleaned = _clean_json_text(raw)
            data = json.loads(cleaned)
            if "reply" in data:
                return data
        except Exception as e:
            logger.error(f"Gemini tutor chat failed: {e}")

        return {
            "reply": "Savolingiz uchun tashakkur! Ushbu ob'ekt bo'yicha ilmiy tamoyillar juda qiziq.",
            "suggested_prompts": ["Keyingi bosqichni ko'rsating", "Test savollariga o'tish"]
        }

gemini_service = GeminiService()
