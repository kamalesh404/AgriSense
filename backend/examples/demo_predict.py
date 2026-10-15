import io
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.core.model import DiseasePredictor


def load_sample_image():
    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
        with open(sys.argv[1], "rb") as f:
            return f.read()
    arr = np.zeros((224, 224, 3), dtype=np.uint8)
    arr[:, :, 0] = 45
    arr[:, :, 1] = 140
    arr[:, :, 2] = 45
    rng = np.random.default_rng(42)
    for _ in range(25):
        cx = int(rng.integers(30, 194))
        cy = int(rng.integers(30, 194))
        r = int(rng.integers(5, 18))
        y1 = max(0, cy - r)
        y2 = min(224, cy + r)
        x1 = max(0, cx - r)
        x2 = min(224, cx + r)
        arr[y1:y2, x1:x2, 0] = 120
        arr[y1:y2, x1:x2, 1] = 80
        arr[y1:y2, x1:x2, 2] = 30
    img = Image.fromarray(arr)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


def main():
    image_bytes = load_sample_image()
    predictor = DiseasePredictor()
    predictor.load_model()
    result = predictor.predict(image_bytes)
    print("Disease: " + str(result.get("disease", "unknown")))
    print("Confidence: " + str(result.get("confidence", 0.0)))
    probs = result.get("probabilities", {})
    if probs:
        ranked = sorted(probs.items(), key=lambda x: x[1], reverse=True)[:3]
        for name, p in ranked:
            print(str(name) + ": " + str(round(float(p), 4)))
    print("Severity: " + str(result.get("severity", "unknown")))
    print("Treatment: " + str(result.get("treatment", "")))


if __name__ == "__main__":
    main()
