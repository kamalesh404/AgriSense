import io

import numpy as np
import pytest
from PIL import Image

from app.core.model import (
    DISEASE_CLASSES,
    DiseasePredictor,
    compute_disease_scores,
    extract_features,
    get_predictor,
    rgb_to_hsv,
    segment_leaf,
    softmax,
)


def create_test_image(color: tuple[int, int, int], size: tuple[int, int] = (224, 224)) -> bytes:
    img = Image.new("RGB", size, color)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def create_green_leaf_image() -> bytes:
    arr = np.zeros((224, 224, 3), dtype=np.uint8)
    arr[:, :, 1] = 140
    arr[:, :, 0] = 40
    arr[:, :, 2] = 40
    img = Image.fromarray(arr)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def create_brown_diseased_image() -> bytes:
    arr = np.zeros((224, 224, 3), dtype=np.uint8)
    arr[:, :, 0] = 140
    arr[:, :, 1] = 60
    arr[:, :, 2] = 30
    img = Image.fromarray(arr)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


class TestRGBToHSV:
    def test_green_pixel(self):
        rgb = np.array([[[50, 150, 50]]], dtype=np.float64)
        hsv = rgb_to_hsv(rgb)
        assert 100 < hsv[0, 0, 0] < 140

    def test_red_pixel(self):
        rgb = np.array([[[200, 50, 50]]], dtype=np.float64)
        hsv = rgb_to_hsv(rgb)
        assert hsv[0, 0, 0] < 15 or hsv[0, 0, 0] > 345

    def test_blue_pixel(self):
        rgb = np.array([[[50, 50, 200]]], dtype=np.float64)
        hsv = rgb_to_hsv(rgb)
        assert 200 < hsv[0, 0, 0] < 260


class TestSegmentLeaf:
    def test_green_leaf_segmentation(self):
        arr = np.zeros((100, 100, 3), dtype=np.uint8)
        arr[20:80, 20:80, 1] = 140
        arr[20:80, 20:80, 0] = 40
        arr[20:80, 20:80, 2] = 40
        mask = segment_leaf(arr)
        assert mask.sum() > 100

    def test_no_leaf_returns_empty(self):
        arr = np.zeros((100, 100, 3), dtype=np.uint8)
        mask = segment_leaf(arr)
        assert mask.sum() == 0


class TestExtractFeatures:
    def test_green_image_features(self):
        img_data = create_green_leaf_image()
        img = Image.open(io.BytesIO(img_data))
        features = extract_features(img)
        assert features.green_ratio > 0.3
        assert features.leaf_coverage > 0.1

    def test_brown_image_features(self):
        img_data = create_brown_diseased_image()
        img = Image.open(io.BytesIO(img_data))
        features = extract_features(img)
        assert features.brown_ratio > 0.1

    def test_features_have_all_fields(self):
        img_data = create_green_leaf_image()
        img = Image.open(io.BytesIO(img_data))
        features = extract_features(img)
        assert hasattr(features, "hsv_h_mean")
        assert hasattr(features, "edge_density")
        assert hasattr(features, "texture_contrast")
        assert hasattr(features, "lesion_ratio")


class TestDiseaseScores:
    def test_scores_for_all_diseases(self):
        img_data = create_green_leaf_image()
        img = Image.open(io.BytesIO(img_data))
        features = extract_features(img)
        scores = compute_disease_scores(features)
        assert len(scores) == len(DISEASE_CLASSES)
        for disease in DISEASE_CLASSES:
            assert disease in scores
            assert 0 <= scores[disease] <= 1.5

    def test_healthy_scores_higher_for_green(self):
        img_data = create_green_leaf_image()
        img = Image.open(io.BytesIO(img_data))
        features = extract_features(img)
        scores = compute_disease_scores(features)
        assert scores["healthy"] > 0.3


class TestSoftmax:
    def test_softmax_sums_to_one(self):
        scores = {"a": 0.5, "b": 0.3, "c": 0.2}
        probs = softmax(scores)
        assert abs(sum(probs.values()) - 1.0) < 1e-6

    def test_softmax_preserves_order(self):
        scores = {"a": 0.9, "b": 0.5, "c": 0.1}
        probs = softmax(scores)
        assert probs["a"] > probs["b"] > probs["c"]


class TestDiseasePredictor:
    def test_predictor_returns_valid_disease(self):
        predictor = DiseasePredictor()
        img_data = create_green_leaf_image()
        result = predictor.predict(img_data)
        assert result["disease"] in DISEASE_CLASSES

    def test_predictor_returns_confidence(self):
        predictor = DiseasePredictor()
        img_data = create_green_leaf_image()
        result = predictor.predict(img_data)
        assert 0 < result["confidence"] <= 1.0

    def test_predictor_returns_probabilities(self):
        predictor = DiseasePredictor()
        img_data = create_green_leaf_image()
        result = predictor.predict(img_data)
        assert "probabilities" in result
        assert len(result["probabilities"]) == len(DISEASE_CLASSES)

    def test_predictor_returns_treatment(self):
        predictor = DiseasePredictor()
        img_data = create_green_leaf_image()
        result = predictor.predict(img_data)
        assert "treatment" in result
        assert len(result["treatment"]) > 0

    def test_predictor_returns_features(self):
        predictor = DiseasePredictor()
        img_data = create_green_leaf_image()
        result = predictor.predict(img_data)
        assert "features" in result
        assert "leaf_coverage" in result["features"]

    def test_predictor_handles_invalid_image(self):
        predictor = DiseasePredictor()
        result = predictor.predict(b"not an image")
        assert result["disease"] == "unknown"
        assert result["confidence"] == 0.0

    def test_batch_predict(self):
        predictor = DiseasePredictor()
        images = [create_green_leaf_image(), create_brown_diseased_image()]
        results = predictor.predict_batch(images)
        assert len(results) == 2
        for r in results:
            assert r["disease"] in DISEASE_CLASSES

    def test_get_predictor_singleton(self):
        p1 = get_predictor()
        p2 = get_predictor()
        assert p1 is p2

    def test_model_load(self):
        predictor = DiseasePredictor()
        predictor.load_model()
        assert predictor.is_loaded is True

    def test_feature_importance(self):
        predictor = DiseasePredictor()
        img_data = create_green_leaf_image()
        result = predictor.get_feature_importance(img_data)
        assert "features" in result
        assert "disease_scores" in result
        assert "probabilities" in result
