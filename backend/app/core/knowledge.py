from pydantic import BaseModel


class PredictionResponse(BaseModel):
    disease: str
    confidence: float
    probabilities: dict[str, float]
    treatment: str
    description: str
    severity: str
    image_stats: dict


class WeatherAdvice(BaseModel):
    temperature: float
    humidity: float
    condition: str
    irrigation_advice: str
    disease_risk: str
    recommendation: str


class CropInfo(BaseModel):
    name: str
    soil_type: str
    water_requirement: str
    growing_season: str
    common_diseases: list[str]
