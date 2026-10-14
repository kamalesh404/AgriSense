from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"


def test_predict():
    resp = client.post(
        "/api/predict",
        files={"file": ("test.jpg", b"fake-image-data", "image/jpeg")},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "disease" in data
    assert "confidence" in data
    assert "treatment" in data


def test_crops():
    resp = client.get("/api/crops")
    assert resp.status_code == 200
    assert len(resp.json()) > 0
