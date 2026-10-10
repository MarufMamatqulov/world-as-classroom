import base64
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from typing import Optional, List
from app.dependencies import get_current_user_optional
from app.models import User
from app.schemas import ScanResponse, DetectedObject, BoundingBox, ObjectCorrectionRequest, ObjectCorrectionResponse
from app.services.gemini_service import gemini_service
from app.services.mock_curriculum import get_fallback_detected_objects

router = APIRouter(prefix="/scan", tags=["Camera Scanner"])

def _clamp_box(raw_box: Optional[dict]) -> Optional[BoundingBox]:
    if not raw_box or not isinstance(raw_box, dict):
        return None
    try:
        ymin = max(0.0, min(1.0, float(raw_box.get("ymin", 0.0))))
        xmin = max(0.0, min(1.0, float(raw_box.get("xmin", 0.0))))
        ymax = max(0.0, min(1.0, float(raw_box.get("ymax", 1.0))))
        xmax = max(0.0, min(1.0, float(raw_box.get("xmax", 1.0))))
        if ymax <= ymin:
            ymax = min(1.0, ymin + 0.2)
        if xmax <= xmin:
            xmax = min(1.0, xmin + 0.2)
        return BoundingBox(ymin=ymin, xmin=xmin, ymax=ymax, xmax=xmax)
    except Exception:
        return BoundingBox(ymin=0.1, xmin=0.1, ymax=0.9, xmax=0.9)

@router.post("/upload", response_model=ScanResponse)
async def scan_image(
    file: Optional[UploadFile] = File(None),
    image_base64: Optional[str] = Form(None),
    language: str = Form("uz"),
    user: Optional[User] = Depends(get_current_user_optional)
):
    image_bytes = None
    mime_type = "image/jpeg"
    image_preview = None

    if file:
        image_bytes = await file.read()
        mime_type = file.content_type or "image/jpeg"
        # Generate thumbnail / data url for preview (no persistent disk storage)
        preview_b64 = base64.b64encode(image_bytes).decode('utf-8')
        image_preview = f"data:{mime_type};base64,{preview_b64}"
    elif image_base64:
        # Handles data:image/jpeg;base64,... or raw base64
        if "," in image_base64:
            header, encoded = image_base64.split(",", 1)
            image_preview = image_base64
            if "image/png" in header:
                mime_type = "image/png"
            elif "image/webp" in header:
                mime_type = "image/webp"
            image_bytes = base64.b64decode(encoded)
        else:
            image_bytes = base64.b64decode(image_base64)
            image_preview = f"data:image/jpeg;base64,{image_base64}"
    else:
        raise HTTPException(status_code=400, detail="No image provided. Please capture or upload a photo.")

    custom_key = user.custom_api_key if user else None

    # Detect objects using Gemini Multimodal
    raw_objects = await gemini_service.detect_objects(
        image_bytes=image_bytes,
        mime_type=mime_type,
        language=language,
        custom_key=custom_key
    )

    detected_objects: List[DetectedObject] = []
    for item in raw_objects:
        bbox = _clamp_box(item.get("bounding_box"))
        detected_objects.append(DetectedObject(
            name=item.get("name", "Object"),
            name_en=item.get("name_en", "Object"),
            category=item.get("category", "General Science"),
            educational_hook=item.get("educational_hook", "A fascinating object for scientific exploration."),
            subjects=item.get("subjects", ["Physics", "Mathematics"]),
            confidence=float(item.get("confidence", 0.95)),
            bounding_box=bbox
        ))

    return ScanResponse(
        detected_objects=detected_objects,
        image_preview=image_preview,
        source="upload" if file else "camera"
    )

@router.post("/correct", response_model=ObjectCorrectionResponse)
async def correct_detected_object(
    req: ObjectCorrectionRequest,
    user: Optional[User] = Depends(get_current_user_optional)
):
    """Allows user to correct inaccurate AI object recognition or provide a more specific name."""
    corrected_name = req.corrected_name.strip()
    if not corrected_name:
        raise HTTPException(status_code=400, detail="Corrected object name cannot be empty.")

    category = req.category or "General Science"
    subjects = ["Physics", "Technology", "Mathematics"]
    hook = f"{corrected_name} ob'ekti bo'yicha maxsus ilmiy dars va amaliy tajribalar tayyorlandi." if req.language == "uz" else f"Interactive scientific lesson and hands-on experiments for {corrected_name}."

    corrected_obj = DetectedObject(
        name=corrected_name,
        name_en=corrected_name,
        category=category,
        educational_hook=hook,
        subjects=subjects,
        confidence=1.0,
        bounding_box=BoundingBox(ymin=0.1, xmin=0.1, ymax=0.9, xmax=0.9)
    )

    return ObjectCorrectionResponse(
        success=True,
        corrected_object=corrected_obj
    )

@router.get("/samples")
async def get_sample_objects(language: str = "uz"):
    """Returns curated educational sample items for instant 1-click exploration."""
    samples = [
        {
            "id": "bicycle",
            "name": "Velosiped" if language == "uz" else ("Bicycle" if language == "en" else "Велосипед"),
            "name_en": "Bicycle",
            "category": "Mexanika & Harakat" if language == "uz" else ("Mechanics & Motion" if language == "en" else "Механика и движение"),
            "hook": "Nyuton qonunlari, tishli uzatmalar va inson biomexanikasi" if language == "uz" else ("Newton's laws, gear ratios, and human biomechanics" if language == "en" else "Законы Ньютона, передачи и биомеханика"),
            "icon": "Bike",
            "color": "from-emerald-500 to-teal-600",
            "subjects": ["Fizika", "Matematika", "Biologiya", "Kimyo"] if language == "uz" else ["Physics", "Mathematics", "Biology", "Chemistry"]
        },
        {
            "id": "plant",
            "name": "O'simlik Bargi" if language == "uz" else ("Green Leaf" if language == "en" else "Зеленый лист"),
            "name_en": "Plant Leaf",
            "category": "Fotosintez & Botanika" if language == "uz" else ("Photosynthesis & Botany" if language == "en" else "Фотосинтез и ботаника"),
            "hook": "Quyosh nuri, kvant xlorofill va suv kapillyarlari" if language == "uz" else ("Sunlight harvesting, quantum chlorophyll, and capillary action" if language == "en" else "Квантовый хлорофилл и капиллярное давление"),
            "icon": "Leaf",
            "color": "from-green-500 to-emerald-700",
            "subjects": ["Biologiya", "Kimyo", "Fizika", "Matematika"] if language == "uz" else ["Biology", "Chemistry", "Physics", "Mathematics"]
        },
        {
            "id": "clock",
            "name": "Mexanik / Kvars Soat" if language == "uz" else ("Quartz Clock" if language == "en" else "Кварцевые часы"),
            "name_en": "Clock",
            "category": "Tebranishlar & Vaqt" if language == "uz" else ("Oscillations & Time" if language == "en" else "Колебания и время"),
            "hook": "Pyezoelektr kvars tebranishi (32,768 Gts) va nisbiylik nazariyasi" if language == "uz" else ("Quartz piezoelectric resonance (32,768 Hz) & relativity" if language == "en" else "Пьезоэлектрический кварц и теория относительности"),
            "icon": "Clock",
            "color": "from-blue-500 to-indigo-600",
            "subjects": ["Fizika", "Matematika", "Texnologiya"] if language == "uz" else ["Physics", "Mathematics", "Technology"]
        },
        {
            "id": "microscope",
            "name": "Mikroskop" if language == "uz" else ("Microscope" if language == "en" else "Микроскоп"),
            "name_en": "Microscope",
            "category": "Optika & Hujayralar" if language == "uz" else ("Optics & Cells" if language == "en" else "Оптика и клетки"),
            "hook": "Yorug'lik sinishi, linzalar fokusi va mikroolam kashfiyoti" if language == "uz" else ("Refraction, lens focal geometry, and microscopic life" if language == "en" else "Преломление света и геометрия линз"),
            "icon": "Search",
            "color": "from-purple-500 to-violet-700",
            "subjects": ["Fizika", "Biologiya", "Tarix"] if language == "uz" else ["Physics", "Biology", "History"]
        }
    ]
    return samples
