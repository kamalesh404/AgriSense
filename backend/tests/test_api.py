import io

import numpy as np
import pytest
from fastapi.testclient import TestClient
from PIL import Image

from app.main import app

client = TestClient(app)


def create_test_image_bytes(color: tuple[int, int, int] = (50, 150, 50)) -> bytes:
    arr = np.random.randint(0, 30, (100, 100, 3), dtype=np.uint8)
    arr[:, :, 0] = color[0] + arr[:, :, 0]
    arr[:, :, 1] = color[1] + arr[:, :, 1]
    arr[:, :, 2] = color[2] + arr[:, :, 2]
    img = Image.fromarray(arr)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


class TestHealth:
    def test_health(self):
        resp = client.get("/api/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "healthy"

    def test_model_status(self):
        resp = client.get("/api/model-status")
        assert resp.status_code == 200
        data = resp.json()
        assert "loaded" in data
        assert "classes" in data


class TestPredict:
    def test_predict(self):
        img_bytes = create_test_image_bytes()
        resp = client.post(
            "/api/predict",
            files={"file": ("test.png", img_bytes, "image/png")},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "disease" in data
        assert "confidence" in data
        assert "treatment" in data
        assert "probabilities" in data
        assert "features" in data

    def test_predict_rejects_non_image(self):
        resp = client.post(
            "/api/predict",
            files={"file": ("test.txt", b"not an image", "text/plain")},
        )
        assert resp.status_code == 400

    def test_predict_rejects_oversized(self):
        resp = client.post(
            "/api/predict",
            files={"file": ("test.png", b"x" * (11 * 1024 * 1024), "image/png")},
        )
        assert resp.status_code == 400


class TestBatchPredict:
    def test_batch_predict(self):
        img1 = create_test_image_bytes((50, 150, 50))
        img2 = create_test_image_bytes((150, 80, 40))
        resp = client.post(
            "/api/batch-predict",
            files=[
                ("files", ("test1.png", img1, "image/png")),
                ("files", ("test2.png", img2, "image/png")),
            ],
        )
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 2
        for item in data:
            assert "disease" in item
            assert "confidence" in item

    def test_batch_predict_empty(self):
        resp = client.post("/api/batch-predict", files=[])
        assert resp.status_code == 400

    def test_batch_predict_too_many(self):
        files = []
        for i in range(11):
            files.append(("files", (f"test{i}.png", create_test_image_bytes(), "image/png")))
        resp = client.post("/api/batch-predict", files=files)
        assert resp.status_code == 400


class TestCrops:
    def test_list_crops(self):
        resp = client.get("/api/crops")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 20

    def test_get_crop(self):
        resp = client.get("/api/crops/rice")
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "Rice"

    def test_get_crop_not_found(self):
        resp = client.get("/api/crops/nonexistent")
        assert resp.status_code == 404


class TestDiseases:
    def test_list_diseases(self):
        resp = client.get("/api/diseases")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 10
        for disease in data:
            assert "name" in disease
            assert "description" in disease
            assert "treatment" in disease

    def test_get_disease(self):
        resp = client.get("/api/diseases/leaf_blight")
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "leaf_blight"
        assert "symptoms" in data

    def test_get_disease_not_found(self):
        resp = client.get("/api/diseases/nonexistent")
        assert resp.status_code == 404


class TestRecommendations:
    def test_rotation(self):
        resp = client.get("/api/recommendations/rotation?current_crop=rice")
        assert resp.status_code == 200
        data = resp.json()
        assert data["current_crop"] == "rice"
        assert len(data["recommended_next_crops"]) > 0

    def test_rotation_invalid(self):
        resp = client.get("/api/recommendations/rotation?current_crop=invalid")
        assert resp.status_code == 404

    def test_fertilizer(self):
        resp = client.get("/api/recommendations/fertilizer?crop=rice&soil_type=clay_loam&area_acres=1.0")
        assert resp.status_code == 200
        data = resp.json()
        assert data["crop"] == "rice"
        assert data["urea_kg"] > 0
        assert data["estimated_cost_inr"] > 0

    def test_fertilizer_invalid(self):
        resp = client.get("/api/recommendations/fertilizer?crop=invalid&soil_type=loam&area_acres=1.0")
        assert resp.status_code == 404


class TestCalendar:
    def test_calendar(self):
        resp = client.get("/api/calendar/rice")
        assert resp.status_code == 200
        data = resp.json()
        assert data["crop"] == "rice"
        assert len(data["entries"]) > 0

    def test_calendar_invalid(self):
        resp = client.get("/api/calendar/invalid")
        assert resp.status_code == 404


class TestPesticides:
    def test_list_pesticides(self):
        resp = client.get("/api/pesticides")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 5
        for p in data:
            assert "name" in p
            assert "dosage_per_litre" in p
            assert "safety_interval_days" in p


class TestMarketPrices:
    def test_market_price(self):
        resp = client.get("/api/market-prices/rice")
        assert resp.status_code == 200
        data = resp.json()
        assert "msP_quintal" in data

    def test_market_price_not_found(self):
        resp = client.get("/api/market-prices/invalid")
        assert resp.status_code == 404


class TestPestLifecycle:
    def test_pest_lifecycle(self):
        resp = client.get("/api/pest-lifecycle/aphid")
        assert resp.status_code == 200
        data = resp.json()
        assert data["pest_name"] == "aphid"
        assert len(data["control_measures"]) > 0

    def test_pest_lifecycle_not_found(self):
        resp = client.get("/api/pest-lifecycle/invalid")
        assert resp.status_code == 404


class TestYieldPrediction:
    def test_yield_prediction(self):
        resp = client.get("/api/yield-prediction?crop=rice&area_acres=1.0&soil_type=clay_loam&season=kharif")
        assert resp.status_code == 200
        data = resp.json()
        assert data["crop"] == "rice"
        assert data["predicted_yield_quintals"] > 0

    def test_yield_prediction_invalid(self):
        resp = client.get("/api/yield-prediction?crop=invalid&area_acres=1.0&soil_type=loam&season=kharif")
        assert resp.status_code == 404


class TestWeatherEndpoints:
    def test_weather_advice(self):
        resp = client.get("/api/weather-advice?temperature=35&humidity=70&condition=sunny")
        assert resp.status_code == 200
        data = resp.json()
        assert "irrigation_advice" in data
        assert "disease_risk" in data

    def test_irrigation_advice(self):
        resp = client.get("/api/weather/irrigation-advice?temperature=35&humidity=60&rain_probability=20&soil_type=loam")
        assert resp.status_code == 200
        data = resp.json()
        assert "advice" in data

    def test_disease_risk(self):
        resp = client.get("/api/weather/disease-risk?temperature=30&humidity=80&rain_probability=60")
        assert resp.status_code == 200
        data = resp.json()
        assert "overall_risk" in data
        assert "recommendations" in data

    def test_weather_alerts(self):
        resp = client.get("/api/weather/alerts?temperature=40&humidity=90&rain_probability=80")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) > 0
        for alert in data:
            assert "alert_type" in alert
            assert "severity" in alert
