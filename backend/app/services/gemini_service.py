import json
import re
import base64
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

    def _get_openai_client(self, custom_key: Optional[str] = None):
        key = (custom_key or "").strip()
        if not key.startswith("sk-"):
            key = (settings.OPENAI_API_KEY or "").strip()
        if not key or not key.startswith("sk-"):
            return None
        try:
            from openai import AsyncOpenAI
            return AsyncOpenAI(api_key=key)
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            return None

    def _get_client(self, custom_key: Optional[str] = None):
        key = (custom_key or "").strip() or (settings.GEMINI_API_KEY or "").strip()
        if not key or key.startswith("sk-"):
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
        openai_client = self._get_openai_client(custom_key)
        client = self._get_client(custom_key)
        if not client and not openai_client:
            logger.info("No Gemini or OpenAI API key provided. Using educational mock detection.")
            return get_fallback_detected_objects("bicycle", language)

        prompt = f"""
You are an expert educational AI in "World as a Classroom".
Analyze this image carefully. Identify 1 to 4 prominent real-world objects or key functional components that have high scientific and educational value for school students (e.g., Physics, Chemistry, Biology, Mathematics, Technology, History).

Respond strictly with a JSON object adhering to this schema:
{{
  "objects": [
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
}}
Language for name and educational_hook: {language}.
Return only valid JSON.
"""
        # 1. Try OpenAI Vision if key available
        if openai_client:
            try:
                base64_img = base64.b64encode(image_bytes).decode("utf-8")
                data_uri = f"data:{mime_type};base64,{base64_img}"
                response = await openai_client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {"type": "image_url", "image_url": {"url": data_uri}}
                            ]
                        }
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.2
                )
                raw = response.choices[0].message.content or ""
                cleaned = _clean_json_text(raw)
                data = json.loads(cleaned)
                if isinstance(data, dict) and "objects" in data and isinstance(data["objects"], list):
                    return data["objects"]
                elif isinstance(data, list) and len(data) > 0:
                    return data
            except Exception as e:
                logger.error(f"OpenAI object detection failed: {e}. Trying Gemini if configured.")

        # 2. Try Gemini Vision if key available
        if client:
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
        openai_client = self._get_openai_client(custom_key)
        client = self._get_client(custom_key)
        if not client and not openai_client:
            logger.info("No Gemini or OpenAI API key provided. Using educational mock lesson.")
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
        # 1. Try OpenAI if key available
        if openai_client:
            try:
                response = await openai_client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are the master curriculum creator for World as a Classroom."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.4
                )
                raw = response.choices[0].message.content or ""
                cleaned = _clean_json_text(raw)
                data = json.loads(cleaned)
                if isinstance(data, dict) and "modules" in data:
                    return data
            except Exception as e:
                logger.error(f"OpenAI lesson generation failed: {e}. Trying Gemini if configured.")

        # 2. Try Gemini if key available
        if client:
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
        openai_client = self._get_openai_client(custom_key)
        client = self._get_client(custom_key)
        target_lang_str = "Uzbek" if language == "uz" else ("Russian" if language == "ru" else "English")

        if not client and not openai_client:
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
        # 1. Try OpenAI if key available
        if openai_client:
            try:
                response = await openai_client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are the World as a Classroom Interactive AI Tutor."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.5
                )
                raw = response.choices[0].message.content or ""
                cleaned = _clean_json_text(raw)
                data = json.loads(cleaned)
                if isinstance(data, dict) and "reply" in data:
                    return data
            except Exception as e:
                logger.error(f"OpenAI tutor chat failed: {e}. Trying Gemini if configured.")

        # 2. Try Gemini if key available
        if client:
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

    async def conduct_scientific_inquiry(
        self,
        object_name: str,
        domain: str,
        observation: str,
        hypothesis: str,
        language: str = "uz",
        difficulty_level: str = "intermediate",
        custom_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """Provides guided scientific method reasoning, hypothesis analysis, and safe household experiment design."""
        openai_client = self._get_openai_client(custom_key)
        client = self._get_client(custom_key)
        target_lang_str = "Uzbek (O'zbek tili)" if language == "uz" else ("Russian (Русский язык)" if language == "ru" else "English")

        if not client and not openai_client:
            # High quality fallback scientific inquiry response
            if language == "uz":
                return {
                    "object_name": object_name,
                    "domain": domain,
                    "hypothesis_critique": f"Sizning '{hypothesis}' gipotezangiz ilmiy jihatdan juda qiziq va tajribada tekshirish mumkin bo'lgan aniq bog'liqlikni ifodalaydi. Ilmiy metodning eng muhim qoidasi — gipotezani o'lchash yoki solishtirish orqali isbotlashdir.",
                    "is_valid_hypothesis": True,
                    "experiment_plan": {
                        "title": f"'{object_name}' bo'yicha Xavfsiz Uy Laboratoriyasi Sinovi",
                        "materials": [
                            "O'rganilayotgan ob'ekt yoki uning modeli",
                            "Oddiy o'lchov asbobi (chizg'ich yoki telefon taymeri)",
                            "Kuzatuv daftari va qalam"
                        ],
                        "steps": [
                            f"1. Dastlabki holatni aniqlang: ob'ektning tinch yoki me'yoriy holatidagi parametrlarini yozib oling.",
                            f"2. Bir parametrni o'zgartiring va ikkinchi parametr qanday javob qaytarishini sinab ko'ring.",
                            f"3. Natijani 3 marta takrorlang (o'lchov aniqligi uchun o'rtacha qiymatni oling).",
                            f"4. Olingan natijalarni dastlabki gipotezangiz bilan taqqoslang."
                        ],
                        "safety_guidelines": "Tajriba mutlaqo xavfsiz. O'tkir jism, olov yoki xavfli moddalardan foydalanilmaydi. Xonani yorug' joyda o'tkazing.",
                        "expected_observation": f"Gipotezangiz to'g'ri bo'lsa, o'zgaruvchi oshganda kutilgan fizik jarayon kuchayishi yoki aniq qonuniyat bo'yicha o'zgarishi qayd etiladi."
                    },
                    "scientific_principles": [
                        "Sabab-oqibat bog'liqligi (Causality)",
                        "Nazorat qilinuvchi tajriba (Controlled Experimentation)",
                        "O'lchov xatoligi va takroriylik (Reproducibility)"
                    ],
                    "ai_guidance": "Siz haqiqiy yosh olim kabi fikrlayapsiz! Kuzatish va gipoteza tuzish zamonaviy ilm-fanning yuragidir.",
                    "xp_awarded": 50
                }
            elif language == "ru":
                return {
                    "object_name": object_name,
                    "domain": domain,
                    "hypothesis_critique": f"Ваша гипотеза '{hypothesis}' логически обоснована и формулирует проверяемую связь. Это отличный пример научного мышления.",
                    "is_valid_hypothesis": True,
                    "experiment_plan": {
                        "title": f"Безопасный домашний эксперимент с '{object_name}'",
                        "materials": ["Объект исследования", "Линейка или секундомер", "Блокнот для записей"],
                        "steps": [
                            "1. Зафиксируйте исходное состояние объекта.",
                            "2. Измените один фактор и наблюдайте реакцию системы.",
                            "3. Повторите замер 3 раза для статистической точности.",
                            "4. Сравните выводы с вашей гипотезой."
                        ],
                        "safety_guidelines": "Опыт безопасен, используются только бытовые предметы без огня и химикатов.",
                        "expected_observation": "Подтверждение математической или физической пропорциональности."
                    },
                    "scientific_principles": ["Принцип фальсифицируемости", "Воспроизводимость результатов"],
                    "ai_guidance": "Прекрасный научный подход! Продолжайте проверять гипотезы.",
                    "xp_awarded": 50
                }
            else:
                return {
                    "object_name": object_name,
                    "domain": domain,
                    "hypothesis_critique": f"Your hypothesis '{hypothesis}' is well-formulated and directly testable. Good science starts with asking questions that can be verified through observation.",
                    "is_valid_hypothesis": True,
                    "experiment_plan": {
                        "title": f"Safe Home Laboratory Inquiry: {object_name}",
                        "materials": ["The target object or model", "Ruler or smartphone stopwatch", "Observation notebook"],
                        "steps": [
                            "1. Record baseline conditions and observable state.",
                            "2. Modify one independent variable while keeping others constant.",
                            "3. Repeat 3 trials to compute average values.",
                            "4. Evaluate if outcome supports your initial hypothesis."
                        ],
                        "safety_guidelines": "100% child-safe. No hazardous chemicals, flames, or sharp tools required.",
                        "expected_observation": "Consistent physical response aligning with the test variable."
                    },
                    "scientific_principles": ["Hypothesis-Driven Inquiry", "Controlled Variables", "Empirical Verification"],
                    "ai_guidance": "Outstanding scientific reasoning! You are practicing genuine empirical methodology.",
                    "xp_awarded": 50
                }

        prompt = f"""
You are the AI Chief Scientist in 'World as a Classroom'.
Guide a student through the rigorous Scientific Method for: "{object_name}" ({domain}).

Student's Observation:
"{observation}"

Student's Proposed Hypothesis:
"{hypothesis}"

Student profile: Complexity level {difficulty_level}, Language: {target_lang_str}.

Analyze the hypothesis, provide constructive educational feedback, design a SAFE, child-friendly experiment (strictly household items, non-toxic, safe for school children), and identify core scientific principles.

Return strictly a JSON object adhering to:
{{
  "object_name": "{object_name}",
  "domain": "{domain}",
  "hypothesis_critique": "Insightful scientific feedback in {target_lang_str} assessing clarity, testability, and validity",
  "is_valid_hypothesis": true,
  "experiment_plan": {{
    "title": "Safe DIY Experiment Title in {target_lang_str}",
    "materials": ["Item 1", "Item 2", "Item 3"],
    "steps": ["Step 1", "Step 2", "Step 3", "Step 4"],
    "safety_guidelines": "Safety notes emphasizing non-hazardous child-safe steps in {target_lang_str}",
    "expected_observation": "What the student should observe in {target_lang_str}"
  }},
  "scientific_principles": ["Principle 1", "Principle 2", "Principle 3"],
  "ai_guidance": "Encouraging mentor conclusion in {target_lang_str}",
  "xp_awarded": 50
}}
Return only valid JSON.
"""
        # 1. Try OpenAI if key available
        if openai_client:
            try:
                response = await openai_client.chat.completions.create(
                    model=settings.OPENAI_MODEL,
                    messages=[
                        {"role": "system", "content": "You are the AI Chief Scientist in World as a Classroom."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.3
                )
                raw = response.choices[0].message.content or ""
                cleaned = _clean_json_text(raw)
                data = json.loads(cleaned)
                if isinstance(data, dict) and "hypothesis_critique" in data:
                    return data
            except Exception as e:
                logger.error(f"OpenAI scientific inquiry failed: {e}. Trying Gemini if configured.")

        # 2. Try Gemini if key available
        if client:
            try:
                from google.genai import types
                response = client.models.generate_content(
                    model=self.default_model,
                    contents=[prompt],
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        temperature=0.3
                    )
                )
                raw = response.text or ""
                cleaned = _clean_json_text(raw)
                data = json.loads(cleaned)
                if "hypothesis_critique" in data:
                    return data
            except Exception as e:
                logger.error(f"Gemini scientific inquiry failed: {e}")

        # Fallback if AI generation failed
        return {
            "object_name": object_name,
            "domain": domain,
            "hypothesis_critique": f"Gipotezangiz '{hypothesis}' ilmiy qiziqish uyg'otadi.",
            "is_valid_hypothesis": True,
            "experiment_plan": {
                "title": f"'{object_name}' bo'yicha Xavfsiz Tadqiqot",
                "materials": ["Ob'ekt", "Daftar"],
                "steps": ["1. O'lchang", "2. Qayd qiling"],
                "safety_guidelines": "Xavfsizlik qoidalariga rioya qiling.",
                "expected_observation": "O'zgarishlar qayd etiladi."
            },
            "scientific_principles": ["Ilmiy uslub", "Kuzatuv"],
            "ai_guidance": "Ajoyib boshlanish!",
            "xp_awarded": 50
        }

gemini_service = GeminiService()

