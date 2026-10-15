from fastapi import APIRouter, File, HTTPException, Query, UploadFile

from ..core.model import get_predictor
from ..core.knowledge import (
    CropInfo,
    WeatherAdvice,
    get_all_crops,
    get_all_diseases,
    get_all_pesticides,
    get_crop_info,
    get_disease_info,
    get_market_price,
)
from ..core.recommendations import (
    FertilizerRecommendation,
    RotationPlan,
    SeasonalCalendar,
    YieldPrediction,
    calculate_fertilizer,
    generate_seasonal_calendar,
    get_pest_lifecycle,
    get_weather_alerts,
    plan_crop_rotation,
    predict_yield,
)
from .weather import get_disease_risk_forecast, get_irrigation_advice

router = APIRouter(prefix="/api", tags=["agrisense"])


@router.post("/predict", response_model=dict)
async def predict_disease(file: UploadFile = File(...)) -> dict:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(400, "File must be an image")
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(400, "Image too large (max 10MB)")
    predictor = get_predictor()
    return predictor.predict(contents)


@router.post("/batch-predict", response_model=list[dict])
async def batch_predict_disease(files: list[UploadFile] = File(default=None)) -> list[dict]:
    if not files or len(files) == 0:
        raise HTTPException(400, "No files uploaded")
    if len(files) > 10:
        raise HTTPException(400, "Maximum 10 images allowed per batch")

    predictor = get_predictor()
    results = []

    for file in files:
        if not file.content_type or not file.content_type.startswith("image/"):
            raise HTTPException(400, f"File {file.filename} is not an image")
        contents = await file.read()
        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(400, f"Image {file.filename} too large (max 10MB)")
        results.append(predictor.predict(contents))

    return results


@router.get("/crops", response_model=list[CropInfo])
async def list_crops() -> list[CropInfo]:
    return get_all_crops()


@router.get("/crops/{crop_name}", response_model=CropInfo)
async def get_crop(crop_name: str) -> CropInfo:
    crop = get_crop_info(crop_name)
    if not crop:
        raise HTTPException(404, "Crop not found")
    return crop


@router.get("/diseases")
async def list_diseases() -> list[dict]:
    diseases = get_all_diseases()
    return [d.model_dump() for d in diseases]


@router.get("/diseases/{name}")
async def get_disease(name: str) -> dict:
    disease = get_disease_info(name)
    if not disease:
        raise HTTPException(404, "Disease not found")
    return disease.model_dump()


@router.get("/recommendations/rotation", response_model=RotationPlan)
async def crop_rotation(current_crop: str = Query(...)) -> RotationPlan:
    try:
        return plan_crop_rotation(current_crop)
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.get("/recommendations/fertilizer", response_model=FertilizerRecommendation)
async def fertilizer_calculator(
    crop: str = Query(...),
    soil_type: str = Query(default="loam"),
    area_acres: float = Query(default=1.0),
) -> FertilizerRecommendation:
    try:
        return calculate_fertilizer(crop, soil_type, area_acres)
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.get("/calendar/{crop}", response_model=SeasonalCalendar)
async def farming_calendar(crop: str) -> SeasonalCalendar:
    try:
        return generate_seasonal_calendar(crop)
    except ValueError as e:
        raise HTTPException(404, str(e))


@router.get("/pesticides")
async def list_pesticides() -> list[dict]:
    pesticides = get_all_pesticides()
    return [p.model_dump() for p in pesticides]


@router.get("/market-prices/{crop}")
async def market_price(crop: str) -> dict:
    price = get_market_price(crop)
    if not price:
        raise HTTPException(404, "No market price data for this crop")
    return price


@router.get("/pest-lifecycle/{pest_name}")
async def pest_lifecycle(pest_name: str) -> dict:
    lifecycle = get_pest_lifecycle(pest_name)
    if not lifecycle:
        raise HTTPException(404, "Pest not found")
    return lifecycle.model_dump()


@router.get("/yield-prediction")
async def yield_prediction(
    crop: str = Query(...),
    area_acres: float = Query(default=1.0),
    soil_type: str = Query(default="loam"),
    season: str = Query(default="kharif"),
) -> YieldPrediction:
    try:
        return predict_yield(crop, area_acres, soil_type, season)
    except ValueError as e:
        raise HTTPException(404, str(e))


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


@router.get("/weather/irrigation-advice")
async def irrigation_advice(
    temperature: float = 30.0,
    humidity: float = 60.0,
    rain_probability: float = 0.0,
    soil_type: str = "loam",
) -> dict:
    return {
        "advice": get_irrigation_advice(temperature, humidity, rain_probability, soil_type),
        "inputs": {
            "temperature": temperature,
            "humidity": humidity,
            "rain_probability": rain_probability,
            "soil_type": soil_type,
        },
    }


@router.get("/weather/disease-risk")
async def disease_risk(
    temperature: float = 30.0,
    humidity: float = 60.0,
    rain_probability: float = 0.0,
) -> dict:
    return get_disease_risk_forecast(temperature, humidity, rain_probability)


@router.get("/weather/alerts")
async def weather_alerts(
    temperature: float = 30.0,
    humidity: float = 60.0,
    rain_probability: float = 0.0,
) -> list[dict]:
    alerts = get_weather_alerts(temperature, humidity, rain_probability)
    return [a.model_dump() for a in alerts]
