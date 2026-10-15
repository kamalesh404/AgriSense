import io
import math
from dataclasses import dataclass, field

import numpy as np
from PIL import Image, ImageFilter

DISEASE_CLASSES = [
    "healthy",
    "leaf_blight",
    "leaf_spot",
    "powdery_mildew",
    "root_rot",
    "rust",
    "wilt",
    "bacterial_blight",
    "anthracnose",
    "downy_mildew",
]

DISEASE_PROFILES = {
    "healthy": {
        "hsv_h_range": (35, 145),
        "hsv_s_range": (30, 95),
        "hsv_v_range": (30, 95),
        "green_ratio_min": 0.45,
        "edge_density_range": (0.0, 0.2),
        "brown_ratio_max": 0.12,
    },
    "leaf_blight": {
        "hsv_h_range": (10, 35),
        "hsv_s_range": (40, 90),
        "hsv_v_range": (20, 60),
        "green_ratio_min": 0.15,
        "edge_density_range": (0.08, 0.30),
        "brown_ratio_max": 0.35,
    },
    "leaf_spot": {
        "hsv_h_range": (15, 45),
        "hsv_s_range": (30, 85),
        "hsv_v_range": (25, 65),
        "green_ratio_min": 0.20,
        "edge_density_range": (0.10, 0.35),
        "brown_ratio_max": 0.30,
    },
    "powdery_mildew": {
        "hsv_h_range": (0, 180),
        "hsv_s_range": (0, 30),
        "hsv_v_range": (70, 100),
        "green_ratio_min": 0.10,
        "edge_density_range": (0.01, 0.10),
        "brown_ratio_max": 0.10,
    },
    "root_rot": {
        "hsv_h_range": (10, 40),
        "hsv_s_range": (50, 95),
        "hsv_v_range": (10, 45),
        "green_ratio_min": 0.05,
        "edge_density_range": (0.03, 0.20),
        "brown_ratio_max": 0.40,
    },
    "rust": {
        "hsv_h_range": (5, 25),
        "hsv_s_range": (60, 100),
        "hsv_v_range": (30, 70),
        "green_ratio_min": 0.10,
        "edge_density_range": (0.08, 0.30),
        "brown_ratio_max": 0.35,
    },
    "wilt": {
        "hsv_h_range": (20, 50),
        "hsv_s_range": (20, 60),
        "hsv_v_range": (30, 60),
        "green_ratio_min": 0.15,
        "edge_density_range": (0.05, 0.25),
        "brown_ratio_max": 0.25,
    },
    "bacterial_blight": {
        "hsv_h_range": (30, 60),
        "hsv_s_range": (25, 70),
        "hsv_v_range": (20, 55),
        "green_ratio_min": 0.15,
        "edge_density_range": (0.06, 0.25),
        "brown_ratio_max": 0.30,
    },
    "anthracnose": {
        "hsv_h_range": (5, 30),
        "hsv_s_range": (50, 100),
        "hsv_v_range": (15, 50),
        "green_ratio_min": 0.08,
        "edge_density_range": (0.10, 0.35),
        "brown_ratio_max": 0.35,
    },
    "downy_mildew": {
        "hsv_h_range": (40, 90),
        "hsv_s_range": (10, 50),
        "hsv_v_range": (40, 75),
        "green_ratio_min": 0.25,
        "edge_density_range": (0.03, 0.18),
        "brown_ratio_max": 0.15,
    },
}


@dataclass
class ImageFeatures:
    hsv_h_mean: float = 0.0
    hsv_s_mean: float = 0.0
    hsv_v_mean: float = 0.0
    green_ratio: float = 0.0
    brown_ratio: float = 0.0
    edge_density: float = 0.0
    color_histogram: np.ndarray = field(default_factory=lambda: np.zeros(8))
    texture_contrast: float = 0.0
    texture_homogeneity: float = 0.0
    leaf_coverage: float = 0.0
    lesion_ratio: float = 0.0
    yellow_ratio: float = 0.0
    dark_spot_ratio: float = 0.0


def rgb_to_hsv(rgb: np.ndarray) -> np.ndarray:
    r, g, b = rgb[..., 0] / 255.0, rgb[..., 1] / 255.0, rgb[..., 2] / 255.0
    mx = np.max(rgb / 255.0, axis=-1)
    mn = np.min(rgb / 255.0, axis=-1)
    diff = mx - mn

    h = np.zeros_like(mx)
    mask = diff > 0
    safe_diff = np.where(diff == 0, 1, diff)
    r_max = (mx == r) & mask
    g_max = (mx == g) & mask & ~r_max
    b_max = mask & ~r_max & ~g_max
    h[r_max] = (60 * ((g - b) / safe_diff) % 360)[r_max]
    h[g_max] = (60 * ((b - r) / safe_diff) + 120)[g_max]
    h[b_max] = (60 * ((r - g) / safe_diff) + 240)[b_max]

    s = np.where(mx > 0, diff / np.where(mx == 0, 1, mx), 0)
    v = mx

    return np.stack([h, s * 100, v * 100], axis=-1)


def sobel_edge_detection(gray: np.ndarray) -> np.ndarray:
    kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float64)
    ky = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float64)

    from scipy.signal import convolve2d
    gx = convolve2d(gray, kx, mode="same", boundary="symm")
    gy = convolve2d(gray, ky, mode="same", boundary="symm")
    magnitude = np.sqrt(gx ** 2 + gy ** 2)

    max_val = magnitude.max()
    if max_val > 0:
        magnitude = magnitude / max_val

    return magnitude


def compute_color_histogram(img: np.ndarray, bins: int = 8) -> np.ndarray:
    hist = np.zeros(bins, dtype=np.float64)
    total_pixels = img.shape[0] * img.shape[1]

    for i in range(bins):
        lo = i * (256 // bins)
        hi = (i + 1) * (256 // bins)
        mask = (img >= lo) & (img < hi)
        hist[i] = mask.sum() / total_pixels

    return hist


def compute_glcm_features(gray: np.ndarray) -> tuple[float, float]:
    gray_uint = gray.astype(np.uint8)
    levels = 16
    quantized = (gray_uint / (256 // levels)).astype(np.int32)
    quantized = np.clip(quantized, 0, levels - 1)

    glcm = np.zeros((levels, levels), dtype=np.float64)
    for i in range(quantized.shape[0] - 1):
        for j in range(quantized.shape[1] - 1):
            row = quantized[i, j]
            col = quantized[i + 1, j + 1]
            glcm[row, col] += 1

    total = glcm.sum()
    if total > 0:
        glcm /= total

    contrast = 0.0
    homogeneity = 0.0
    for i in range(levels):
        for j in range(levels):
            contrast += glcm[i, j] * (i - j) ** 2
            homogeneity += glcm[i, j] / (1 + (i - j) ** 2)

    return float(contrast), float(homogeneity)


def segment_leaf(img: np.ndarray) -> np.ndarray:
    hsv = rgb_to_hsv(img)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]

    green_mask = ((h >= 25) & (h <= 150) & (s > 10) & (v > 8))
    yellow_mask = ((h >= 15) & (h < 40) & (s > 15) & (v > 12))
    brown_mask = ((h >= 5) & (h < 30) & (s > 25) & (v > 5) & (v < 70))

    leaf_mask = green_mask | yellow_mask | brown_mask

    from scipy import ndimage
    leaf_mask = ndimage.binary_fill_holes(leaf_mask)
    leaf_mask = ndimage.binary_opening(leaf_mask, iterations=1)

    labeled, num_features = ndimage.label(leaf_mask)
    if num_features > 0:
        sizes = ndimage.sum(leaf_mask, labeled, range(1, num_features + 1))
        largest = np.argmax(sizes) + 1
        leaf_mask = labeled == largest

    return leaf_mask


def extract_features(img: Image.Image) -> ImageFeatures:
    img_resized = img.resize((224, 224))
    arr = np.array(img_resized, dtype=np.float64)

    leaf_mask = segment_leaf(arr)
    leaf_coverage = float(leaf_mask.sum()) / leaf_mask.size

    hsv = rgb_to_hsv(arr)
    h_ch, s_ch, v_ch = hsv[..., 0], hsv[..., 1], hsv[..., 2]

    leaf_pixels = leaf_mask
    if leaf_pixels.sum() > 0:
        h_mean = float(h_ch[leaf_pixels].mean())
        s_mean = float(s_ch[leaf_pixels].mean())
        v_mean = float(v_ch[leaf_pixels].mean())
    else:
        h_mean = float(h_ch.mean())
        s_mean = float(s_ch.mean())
        v_mean = float(v_ch.mean())

    green_mask = (h_ch > 35) & (h_ch < 150) & (s_ch > 20) & (v_ch > 15) & leaf_pixels
    brown_mask = (h_ch > 5) & (h_ch < 35) & (s_ch > 40) & (v_ch < 60) & leaf_pixels
    yellow_mask = (h_ch > 20) & (h_ch < 45) & (s_ch > 30) & (v_ch > 40) & leaf_pixels
    dark_mask = (v_ch < 30) & leaf_pixels

    leaf_count = max(int(leaf_pixels.sum()), 1)
    green_ratio = float(green_mask.sum()) / leaf_count
    brown_ratio = float(brown_mask.sum()) / leaf_count
    yellow_ratio = float(yellow_mask.sum()) / leaf_count
    dark_spot_ratio = float(dark_mask.sum()) / leaf_count

    gray = img_resized.convert("L")
    gray_arr = np.array(gray, dtype=np.float64)
    edges = sobel_edge_detection(gray_arr)
    edge_density = float(edges[leaf_pixels].mean()) if leaf_pixels.sum() > 0 else 0.0

    color_hist = compute_color_histogram(np.array(img_resized.convert("L")))

    contrast, homogeneity = compute_glcm_features(gray_arr)

    lesion_mask = (brown_mask | dark_mask) & leaf_pixels
    lesion_ratio = float(lesion_mask.sum()) / leaf_count

    return ImageFeatures(
        hsv_h_mean=h_mean,
        hsv_s_mean=s_mean,
        hsv_v_mean=v_mean,
        green_ratio=green_ratio,
        brown_ratio=brown_ratio,
        edge_density=edge_density,
        color_histogram=color_hist,
        texture_contrast=contrast,
        texture_homogeneity=homogeneity,
        leaf_coverage=leaf_coverage,
        lesion_ratio=lesion_ratio,
        yellow_ratio=yellow_ratio,
        dark_spot_ratio=dark_spot_ratio,
    )


def compute_disease_scores(features: ImageFeatures) -> dict[str, float]:
    scores = {}
    for disease, profile in DISEASE_PROFILES.items():
        score = 0.0
        weights = 0.0

        h_lo, h_hi = profile["hsv_h_range"]
        if h_lo <= features.hsv_h_mean <= h_hi:
            score += 1.0
        else:
            dist = min(abs(features.hsv_h_mean - h_lo), abs(features.hsv_h_mean - h_hi))
            score += max(0, 1.0 - dist / 60.0)
        weights += 1.0

        if features.green_ratio >= profile["green_ratio_min"]:
            score += 1.0
        else:
            score += features.green_ratio / max(profile["green_ratio_min"], 0.01)
        weights += 1.0

        if features.brown_ratio <= profile["brown_ratio_max"]:
            score += 1.0
        else:
            score += max(0, 1.0 - (features.brown_ratio - profile["brown_ratio_max"]) / 0.2)
        weights += 1.0

        e_lo, e_hi = profile["edge_density_range"]
        if e_lo <= features.edge_density <= e_hi:
            score += 1.0
        else:
            dist = min(abs(features.edge_density - e_lo), abs(features.edge_density - e_hi))
            score += max(0, 1.0 - dist / 0.15)
        weights += 1.0

        if disease == "powdery_mildew":
            if features.hsv_s_mean < 30 and features.hsv_v_mean > 70:
                score += 2.0
            weights += 2.0
        elif disease == "rust":
            if features.brown_ratio > 0.2 and features.hsv_s_mean > 60:
                score += 1.5
            weights += 2.0
        elif disease == "healthy":
            if features.green_ratio > 0.5 and features.lesion_ratio < 0.05:
                score += 2.0
            weights += 2.0
        else:
            if features.lesion_ratio > 0.1:
                score += 1.5
            weights += 2.0

        s_lo, s_hi = profile["hsv_s_range"]
        if s_lo <= features.hsv_s_mean <= s_hi:
            score += 1.0
        else:
            dist = min(abs(features.hsv_s_mean - s_lo), abs(features.hsv_s_mean - s_hi))
            score += max(0, 1.0 - dist / 50.0)
        weights += 1.0

        v_lo, v_hi = profile["hsv_v_range"]
        if v_lo <= features.hsv_v_mean <= v_hi:
            score += 1.0
        else:
            dist = min(abs(features.hsv_v_mean - v_lo), abs(features.hsv_v_mean - v_hi))
            score += max(0, 1.0 - dist / 50.0)
        weights += 1.0

        scores[disease] = score / weights if weights > 0 else 0.0

    return scores


def softmax(scores: dict[str, float]) -> dict[str, float]:
    vals = np.array(list(scores.values()))
    exp_vals = np.exp(vals - np.max(vals))
    probs = exp_vals / exp_vals.sum()
    return dict(zip(scores.keys(), probs))


TREATMENT_DB = {
    "healthy": {
        "description": "No disease detected. Plant appears healthy with normal green coloration.",
        "treatment": "Continue regular monitoring and good agricultural practices. Maintain proper spacing and irrigation schedule.",
        "severity": "none",
        "organic_treatment": "No treatment needed. Use neem oil as preventive measure.",
    },
    "leaf_blight": {
        "description": "Caused by fungal pathogens (Helminthosporium, Alternaria). Appears as brown to dark brown lesions with concentric rings on leaves.",
        "treatment": "Apply copper-based fungicide (Bordeaux mixture). Remove and destroy infected leaves. Improve air circulation through proper spacing.",
        "severity": "high",
        "organic_treatment": "Spray neem oil (5ml/L) or garlic extract. Apply compost tea to boost plant immunity.",
    },
    "leaf_spot": {
        "description": "Bacterial or fungal infection causing dark brown to black spots with yellow halos on leaves.",
        "treatment": "Apply copper oxychloride fungicide. Avoid overhead watering. Use disease-resistant varieties for next season.",
        "severity": "medium",
        "organic_treatment": "Spray baking soda solution (1 tsp/L with neem oil). Remove infected leaves and destroy them.",
    },
    "powdery_mildew": {
        "description": "White powdery coating on leaf surfaces caused by fungal infection (Erysiphe, Sphaerotheca).",
        "treatment": "Apply sulfur-based fungicide or tridemorph. Increase spacing between plants. Reduce humidity around crop canopy.",
        "severity": "medium",
        "organic_treatment": "Spray milk solution (1:9 milk to water ratio). Apply potassium bicarbonate solution.",
    },
    "root_rot": {
        "description": "Fungal infection of roots (Fusarium, Pythium) causing wilting, yellowing, and root browning.",
        "treatment": "Improve field drainage. Apply Trichoderma viride to soil. Remove severely infected plants immediately.",
        "severity": "high",
        "organic_treatment": "Apply Pseudomonas fluorescens to soil. Use mustard cake as soil amendment.",
    },
    "rust": {
        "description": "Orange, yellow, or brown pustules on leaf surfaces caused by rust fungi (Puccinia species).",
        "treatment": "Apply triazole fungicide (propiconazole). Remove infected plant debris. Practice crop rotation.",
        "severity": "high",
        "organic_treatment": "Spray sulfur dust or sulfur-based organic fungicide. Apply wood ash solution.",
    },
    "wilt": {
        "description": "Bacterial or fungal infection (Fusarium oxysporum, Ralstonia) causing sudden wilting and vascular discoloration.",
        "treatment": "Use resistant varieties. Solarize soil before planting. Apply biocontrol agents (Trichoderma, Pseudomonas).",
        "severity": "high",
        "organic_treatment": "Apply Trichoderma harzianum as soil treatment. Use biogas slurry as soil amendment.",
    },
    "bacterial_blight": {
        "description": "Xanthomonas infection causing water-soaked lesions that turn brown/black with yellow margins.",
        "treatment": "Apply copper-based bactericide. Avoid working in wet fields. Use certified disease-free seeds.",
        "severity": "high",
        "organic_treatment": "Apply copper oxychloride with streptomycin. Use botanical extracts from neem and turmeric.",
    },
    "anthracnose": {
        "description": "Fungal disease (Colletotrichum) causing dark sunken lesions on leaves, stems, and fruits.",
        "treatment": "Apply chlorothalonil or mancozeb fungicide. Remove infected plant parts. Maintain field sanitation.",
        "severity": "high",
        "organic_treatment": "Spray copper-based organic fungicide. Apply Trichoderma-based biocontrol.",
    },
    "downy_mildew": {
        "description": "Oomycete infection causing yellow patches on upper leaf surface and grayish growth on underside.",
        "treatment": "Apply metalaxyl or mancozeb fungicide. Ensure good drainage. Reduce canopy humidity.",
        "severity": "medium",
        "organic_treatment": "Spray copper hydroxide solution. Apply compost extract as foliar spray.",
    },
}


class DiseasePredictor:
    def __init__(self) -> None:
        self.classes = DISEASE_CLASSES
        self.treatment_db = TREATMENT_DB
        self.is_loaded = False

    def load_model(self) -> None:
        self.is_loaded = True

    def predict(self, image_bytes: bytes) -> dict:
        try:
            img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            features = extract_features(img)
            raw_scores = compute_disease_scores(features)
            probabilities = softmax(raw_scores)

            sorted_probs = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
            predicted = sorted_probs[0][0]
            confidence = float(sorted_probs[0][1])
            runner_up = sorted_probs[1][1]

            if confidence < 0.3:
                confidence = 0.3 + confidence * 0.3

            margin = confidence - runner_up
            calibrated_confidence = confidence * (0.5 + 0.5 * margin / max(confidence, 0.01))
            calibrated_confidence = min(max(calibrated_confidence, 0.25), 0.99)

            info = TREATMENT_DB.get(predicted, TREATMENT_DB["healthy"])

            return {
                "disease": predicted,
                "confidence": round(calibrated_confidence, 4),
                "probabilities": {k: round(float(v), 4) for k, v in sorted_probs},
                "treatment": info["treatment"],
                "description": info["description"],
                "severity": info["severity"],
                "organic_treatment": info["organic_treatment"],
                "features": {
                    "leaf_coverage": round(features.leaf_coverage, 4),
                    "green_ratio": round(features.green_ratio, 4),
                    "brown_ratio": round(features.brown_ratio, 4),
                    "yellow_ratio": round(features.yellow_ratio, 4),
                    "lesion_ratio": round(features.lesion_ratio, 4),
                    "dark_spot_ratio": round(features.dark_spot_ratio, 4),
                    "edge_density": round(features.edge_density, 4),
                    "hsv_h_mean": round(features.hsv_h_mean, 2),
                    "hsv_s_mean": round(features.hsv_s_mean, 2),
                    "hsv_v_mean": round(features.hsv_v_mean, 2),
                    "texture_contrast": round(features.texture_contrast, 2),
                    "texture_homogeneity": round(features.texture_homogeneity, 4),
                },
                "image_stats": {
                    "width": img.width,
                    "height": img.height,
                },
                "model_loaded": self.is_loaded,
            }
        except Exception as exc:
            return {
                "disease": "unknown",
                "confidence": 0.0,
                "probabilities": {},
                "treatment": "Could not analyze image. Please try a clearer photo of a leaf.",
                "description": str(exc),
                "severity": "unknown",
                "organic_treatment": "N/A",
                "features": {},
                "image_stats": {},
                "model_loaded": self.is_loaded,
            }

    def predict_batch(self, image_bytes_list: list[bytes]) -> list[dict]:
        return [self.predict(b) for b in image_bytes_list]

    def get_feature_importance(self, image_bytes: bytes) -> dict:
        try:
            img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            features = extract_features(img)
            raw_scores = compute_disease_scores(features)
            probabilities = softmax(raw_scores)

            return {
                "features": {
                    "leaf_coverage": round(features.leaf_coverage, 4),
                    "green_ratio": round(features.green_ratio, 4),
                    "brown_ratio": round(features.brown_ratio, 4),
                    "yellow_ratio": round(features.yellow_ratio, 4),
                    "lesion_ratio": round(features.lesion_ratio, 4),
                    "dark_spot_ratio": round(features.dark_spot_ratio, 4),
                    "edge_density": round(features.edge_density, 4),
                    "hsv_h_mean": round(features.hsv_h_mean, 2),
                    "hsv_s_mean": round(features.hsv_s_mean, 2),
                    "hsv_v_mean": round(features.hsv_v_mean, 2),
                    "texture_contrast": round(features.texture_contrast, 2),
                    "texture_homogeneity": round(features.texture_homogeneity, 4),
                },
                "disease_scores": {k: round(v, 4) for k, v in raw_scores.items()},
                "probabilities": {k: round(float(v), 4) for k, v in probabilities.items()},
            }
        except Exception as exc:
            return {"error": str(exc)}


_predictor: DiseasePredictor | None = None


def get_predictor() -> DiseasePredictor:
    global _predictor
    if _predictor is None:
        _predictor = DiseasePredictor()
    return _predictor
