import asyncio
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import init_db

# Initialize database tables
asyncio.run(init_db())

@pytest.mark.anyio
async def test_health_check():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "healthy"
        assert "World as a Classroom" in data["app"]

@pytest.mark.anyio
async def test_scanner_samples():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/scan/samples?language=uz")
        assert res.status_code == 200
        samples = res.json()
        assert len(samples) >= 4
        assert any(s["id"] == "bicycle" for s in samples)

@pytest.mark.anyio
async def test_scanner_object_correction():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/api/scan/correct", json={
            "original_name": "Temir quti",
            "corrected_name": "Optik Mikroskop",
            "category": "Optika",
            "language": "uz"
        })
        assert res.status_code == 200
        data = res.json()
        assert data["success"] is True
        assert data["corrected_object"]["name"] == "Optik Mikroskop"
        assert data["corrected_object"]["bounding_box"] is not None

@pytest.mark.anyio
async def test_lesson_generation_and_caching():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # First call (generates & caches)
        res1 = await client.post("/api/lessons/generate", json={
            "object_name": "Velosiped",
            "object_name_en": "Bicycle",
            "category": "Mexanika",
            "language": "uz",
            "difficulty_level": "intermediate",
            "primary_focus_subject": "Physics"
        })
        assert res1.status_code == 200
        data1 = res1.json()
        assert data1["object_name"] == "Velosiped"
        assert len(data1["subjects"]) > 0
        lesson_id = data1["id"]

        # Story card test
        res_card = await client.get(f"/api/lessons/{lesson_id}/story-card")
        assert res_card.status_code == 200
        card = res_card.json()
        assert card["object_name"] == "Velosiped"
        assert "Yosh Tadqiqotchi" in card["explorer_callsign"]

        # Second call with same parameters (hits cache)
        res2 = await client.post("/api/lessons/generate", json={
            "object_name": "Velosiped",
            "object_name_en": "Bicycle",
            "category": "Mexanika",
            "language": "uz",
            "difficulty_level": "intermediate",
            "primary_focus_subject": "Physics"
        })
        assert res2.status_code == 200
        data2 = res2.json()
        assert data2["title"] == data1["title"]

@pytest.mark.anyio
async def test_daily_quests_and_verification():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Fetch daily quests
        res = await client.get("/api/quests/daily")
        assert res.status_code == 200
        quests = res.json()
        assert len(quests) >= 4
        quest1 = quests[0]

        # 2. Submit wrong answer
        res_wrong = await client.post("/api/quests/submit", json={
            "quest_id": quest1["id"],
            "selected_option_index": 3
        })
        assert res_wrong.status_code == 200
        assert res_wrong.json()["success"] is False
        assert res_wrong.json()["xp_awarded"] == 0

        # 3. Submit correct answer
        res_correct = await client.post("/api/quests/submit", json={
            "quest_id": quest1["id"],
            "selected_option_index": 0
        })
        assert res_correct.status_code == 200
        assert res_correct.json()["success"] is True
        assert res_correct.json()["xp_awarded"] > 0

        # 4. Badges check
        res_badges = await client.get("/api/quests/badges")
        assert res_badges.status_code == 200
        assert len(res_badges.json()) > 0

@pytest.mark.anyio
async def test_ai_scientist_mode():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.post("/api/scientist/inquiry", json={
            "object_name": "Velosiped zanjiri",
            "domain": "Physics",
            "observation": "Zanjir tishli g'ildiraklar orqali orqa g'ildirakka aylanma kuch uzatadi.",
            "hypothesis": "Agar orqa tishli g'ildirak kichikroq bo'lsa, pedal bosish qiyinlashadi, ammo tezlik oshadi.",
            "language": "uz",
            "difficulty_level": "intermediate"
        })
        assert res.status_code == 200
        data = res.json()
        assert data["is_valid_hypothesis"] is True
        assert len(data["experiment_plan"]["steps"]) > 0
        assert "safety_guidelines" in data["experiment_plan"]
        assert data["xp_awarded"] == 50

@pytest.mark.anyio
async def test_knowledge_passport():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/passport/me")
        assert res.status_code == 200
        passport = res.json()
        assert "level_info" in passport
        assert len(passport["stamps"]) >= 6
        assert passport["level_info"]["current_level"] >= 1

@pytest.mark.anyio
async def test_analytics_and_monitoring():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res_sys = await client.get("/api/analytics/system")
        assert res_sys.status_code == 200
        sys_data = res_sys.json()
        assert "total_api_calls" in sys_data
        assert "cache_hit_rate_pct" in sys_data

        res_overview = await client.get("/api/analytics/overview")
        assert res_overview.status_code == 200
        overview = res_overview.json()
        assert "student_stats" in overview
        assert "passport" in overview
        assert "system_monitoring" in overview
