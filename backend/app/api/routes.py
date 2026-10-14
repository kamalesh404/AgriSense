from fastapi import APIRouter, File, HTTPException, UploadFile

from ..core.model import get_predictor
from ..core.knowledge import CropInfo, WeatherAdvice

router = APIRouter(prefix="/api", tags=["agrisense"])

CROP_DB: dict[str, CropInfo] = {
    "rice": CropInfo(
        name="Rice",
        soil_type="Clay loam",
        water_requirement="High (flooded fields)",
        growing_season="Kharif (June-November)",
        common_diseases=["leaf_blight", "leaf_spot", "wilt"],
    ),
    "wheat": CropInfo(
        name="Wheat",
        soil_type="Loam",
        water_requirement="Medium",
        growing_season="Rabi (October-March)",
        common_diseases=["rust", "powdery_mildew", "wilt"],
    ),
    "cotton": CropInfo(
        name="Cotton",
        soil_type="Black soil",
        water_requirement="Low-Medium",
        growing_season="Kharif (May-November)",
        common_diseases=["leaf_spot", "wilt", "root_rot"],
    ),
    "tomato": CropInfo(
        name="Tomato",
        soil_type="Sandy loam",
        water_requirement="Medium",
        growing_season="Year-round",
        common_diseases=["leaf_blight", "leaf_spot", "wilt"],
    ),
}


@router.post("/predict", response_model=dict)
async def predict_disease(file: UploadFile = File(...)) -> dict:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(400, "File must be an image")
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(400, "Image too large (max 10MB)")
    predictor = get_predictor()
    return predictor.predict(contents)


@router.get("/crops", response_model=list[CropInfo])
async def list_crops() -> list[CropInfo]:
    return list(CROP_DB.values())


@router.get("/crops/{crop_name}", response_model=CropInfo)
async def get_crop(crop_name: str) -> CropInfo:
    crop = CROP_DB.get(crop_name.lower())
    if not crop:
        raise HTTPException(404, "Crop not found")
    return crop


@router.get("/weather-advice", response_model=WeatherAdvice)
async def weather_advice(
    temperature: float = 30.0,
    humidity: float = 60.0,
    condition: str = "sunny",
) -> WeatherAdvice:
    if temperature > 38:
        irrigation = "Irrigate immediately. High evapotranspiration."
        disease_risk = "Low (hot conditions inhibit most fungi)"
    elif temperature > 30:
        irrigation = "Irrigate in early morning or late evening."
        disease_risk = "Moderate (monitor for leaf spot and blight)"
    else:
        irrigation = "Normal irrigation schedule."
        disease_risk = "High humidity increases fungal disease risk"

    if humidity > 80:
        disease_risk = "High — apply preventive fungicide spray"

    return WeatherAdvice(
        temperature=temperature,
        humidity=humidity,
        condition=condition,
        irrigation_advice=irrigation,
        disease_risk=disease_risk,
        recommendation="Monitor field regularly and maintain proper spacing between plants.",
    )
