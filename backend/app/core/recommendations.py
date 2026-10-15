from pydantic import BaseModel

from .knowledge import (
    CROP_ROTATION_DB,
    FARMING_CALENDAR,
    FERTILIZER_DB,
    PEST_LIFECYCLE_DB,
    get_crop_info,
    get_market_price,
)


class RotationPlan(BaseModel):
    current_crop: str
    recommended_next_crops: list[str]
    rotation_benefit: str
    soil_impact: str
    risk_level: str


class FertilizerRecommendation(BaseModel):
    crop: str
    soil_type: str
    area_acres: float
    urea_kg: float
    dap_kg: float
    mop_kg: float
    organic_manure_kg: float
    application_schedule: list[dict[str, str]]
    estimated_cost_inr: float


class YieldPrediction(BaseModel):
    crop: str
    area_acres: float
    soil_type: str
    season: str
    predicted_yield_quintals: float
    yield_range_low: float
    yield_range_high: float
    influencing_factors: list[str]
    improvement_suggestions: list[str]


class PestLifecycleInfo(BaseModel):
    pest_name: str
    scientific_name: str
    life_cycle_days: str
    reproduction: str
    peak_activity: str
    damage_type: str
    affected_crops: list[str]
    control_measures: list[str]
    economic_threshold: str


class FarmingCalendarEntry(BaseModel):
    month: str
    activity: str
    priority: str


class SeasonalCalendar(BaseModel):
    crop: str
    entries: list[FarmingCalendarEntry]
    planting_window: str
    harvest_window: str
    critical_stages: list[str]


class WeatherBasedAlert(BaseModel):
    alert_type: str
    severity: str
    message: str
    recommended_action: str
    affected_diseases: list[str]


def plan_crop_rotation(current_crop: str) -> RotationPlan:
    current = get_crop_info(current_crop)
    if not current:
        raise ValueError(f"Unknown crop: {current_crop}")

    recommendations = CROP_ROTATION_DB.get(current_crop.lower(), [])

    if not recommendations:
        recommendations = ["black_gram", "green_gram", "groundnut"]

    benefits = {
        "rice": "Legumes fix atmospheric nitrogen, reducing fertilizer needs for next crop by 30-40%.",
        "wheat": "Breaks pest cycle and improves soil structure through different root systems.",
        "cotton": "Legumes restore soil nitrogen depleted by cotton's heavy feeding.",
        "maize": "Legumes improve soil nitrogen and break maize pest cycles.",
        "sugarcane": "Short-duration pulses utilize residual moisture and add nitrogen.",
        "banana": "Root-knot nematode suppression and soil organic matter addition.",
        "tomato": "Breaks soil-borne pathogen cycles (Fusarium, Verticillium).",
        "chili": "Reduces soil-borne disease pressure and improves soil health.",
    }

    soil_impacts = {
        "rice": "Improves soil structure and drainage. Reduces soil salinity buildup.",
        "wheat": "Adds organic matter and improves water holding capacity.",
        "cotton": "Replenishes soil nitrogen and improves microbial activity.",
        "maize": "Enhances soil fertility through biological nitrogen fixation.",
        "sugarcane": "Maintains soil organic carbon and reduces erosion.",
        "banana": "Adds organic matter and improves soil biology.",
        "tomato": "Reduces soil pathogen load and improves microbial diversity.",
        "chili": "Breaks disease cycles and adds nitrogen to soil.",
    }

    risk_levels = {
        "rice": "Low risk - well-established rotation system",
        "wheat": "Low risk - traditional rotation practice",
        "cotton": "Low risk - common practice in Tamil Nadu",
        "maize": "Low risk - widely followed",
        "sugarcane": "Medium risk - requires careful water management",
        "banana": "Low risk - compatible intercropping options",
        "tomato": "Medium risk - requires market planning",
        "chili": "Medium risk - market price fluctuation risk",
    }

    return RotationPlan(
        current_crop=current_crop,
        recommended_next_crops=recommendations,
        rotation_benefit=benefits.get(current_crop.lower(), "Improves soil fertility through nitrogen fixation and breaks pest cycles."),
        soil_impact=soil_impacts.get(current_crop.lower(), "Improves soil structure and adds organic matter."),
        risk_level=risk_levels.get(current_crop.lower(), "Medium risk - monitor market and weather conditions"),
    )


def calculate_fertilizer(crop: str, soil_type: str, area_acres: float) -> FertilizerRecommendation:
    crop_data = FERTILIZER_DB.get(crop.lower())
    if not crop_data:
        raise ValueError(f"No fertilizer data for crop: {crop}")

    soil_key = soil_type.lower().replace(" ", "_")
    soil_data = crop_data.get(soil_key, crop_data.get("loam"))

    if not soil_data:
        raise ValueError(f"No fertilizer data for soil type: {soil_type}")

    n_per_acre = soil_data.get("N_kg_per_acre", 40)
    p_per_acre = soil_data.get("P_kg_per_acre", 20)
    k_per_acre = soil_data.get("K_kg_per_acre", 20)
    organic_per_acre = soil_data.get("organic_matter_kg", 2000)

    urea_kg = (n_per_acre / 0.46) * area_acres
    dap_kg = (p_per_acre / 0.46) * area_acres
    mop_kg = (k_per_acre / 0.60) * area_acres
    organic_kg = organic_per_acre * area_acres

    urea_cost = urea_kg * 6
    dap_cost = dap_kg * 28
    mop_cost = mop_kg * 20
    organic_cost = organic_kg * 2
    total_cost = urea_cost + dap_cost + mop_cost + organic_cost

    schedule = [
        {"stage": "Basal (at planting)", "application": f"Full DAP ({round(dap_kg)} kg), Full MOP ({round(mop_kg)} kg), 1/3 Urea ({round(urea_kg/3)} kg), Full organic manure ({round(organic_kg)} kg)"},
        {"stage": "Vegetative (30-40 days)", "application": f"1/3 Urea ({round(urea_kg/3)} kg) top dressing"},
        {"stage": "Flowering/Reproductive (60-70 days)", "application": f"Remaining 1/3 Urea ({round(urea_kg/3)} kg) + micronutrients if needed"},
    ]

    return FertilizerRecommendation(
        crop=crop,
        soil_type=soil_type,
        area_acres=area_acres,
        urea_kg=round(urea_kg, 1),
        dap_kg=round(dap_kg, 1),
        mop_kg=round(mop_kg, 1),
        organic_manure_kg=round(organic_kg, 1),
        application_schedule=schedule,
        estimated_cost_inr=round(total_cost, 2),
    )


def get_pest_lifecycle(pest_name: str) -> PestLifecycleInfo | None:
    data = PEST_LIFECYCLE_DB.get(pest_name.lower().replace(" ", "_"))
    if not data:
        return None
    return PestLifecycleInfo(
        pest_name=pest_name,
        scientific_name=data["scientific_name"],
        life_cycle_days=data["life_cycle_days"],
        reproduction=data["reproduction"],
        peak_activity=data["peak_activity"],
        damage_type=data["damage_type"],
        affected_crops=data["crops_affected"],
        control_measures=data["control_measures"],
        economic_threshold=data["economic_threshold"],
    )


def generate_seasonal_calendar(crop: str) -> SeasonalCalendar:
    crop_info = get_crop_info(crop)
    if not crop_info:
        raise ValueError(f"Unknown crop: {crop}")

    calendar_data = FARMING_CALENDAR.get(crop.lower(), [])
    entries = [FarmingCalendarEntry(**entry) for entry in calendar_data]

    planting = "Kharif (June-July)"
    harvest = "October-November"

    if crop.lower() == "wheat":
        planting = "Rabi (October-November)"
        harvest = "March-April"
    elif crop.lower() in ["potato", "onion"]:
        planting = "Rabi (October-November)"
        harvest = "February-March"
    elif crop.lower() == "banana":
        planting = "Year-round (best: April-June)"
        harvest = "10-12 months after planting"
    elif crop.lower() in ["tomato", "chili", "brinjal"]:
        planting = "Year-round"
        harvest = "60-90 days after transplanting"

    critical = []
    if crop.lower() == "rice":
        critical = ["Panicle initiation", "Flowering stage", "Grain filling"]
    elif crop.lower() == "wheat":
        critical = ["Crown root initiation", "Flowering", "Grain filling"]
    elif crop.lower() == "cotton":
        critical = ["Square formation", "Boll opening", "Peak flowering"]
    elif crop.lower() in ["tomato", "chili", "brinjal"]:
        critical = ["Transplanting recovery", "Flowering", "Fruit setting"]

    return SeasonalCalendar(
        crop=crop,
        entries=entries,
        planting_window=planting,
        harvest_window=harvest,
        critical_stages=critical,
    )


def predict_yield(crop: str, area_acres: float, soil_type: str, season: str) -> YieldPrediction:
    crop_info = get_crop_info(crop)
    if not crop_info:
        raise ValueError(f"Unknown crop: {crop}")

    yield_per_acre = {
        "rice": 25,
        "wheat": 18,
        "cotton": 8,
        "tomato": 120,
        "banana": 300,
        "sugarcane": 4000,
        "maize": 22,
        "groundnut": 10,
        "mango": 50,
        "coconut": 6000,
        "chili": 80,
        "brinjal": 100,
        "onion": 100,
        "potato": 150,
        "soybean": 12,
        "turmeric": 150,
        "ginger": 120,
        "pigeon_pea": 8,
        "black_gram": 7,
        "green_gram": 6,
    }

    base_yield = yield_per_acre.get(crop.lower(), 15)

    soil_multiplier = {
        "clay loam": 1.0,
        "loam": 1.1,
        "sandy loam": 0.85,
        "black soil": 1.05,
        "sandy": 0.7,
    }

    mult = soil_multiplier.get(soil_type.lower().replace(" ", "_"), 1.0)

    if season.lower() == "kharif":
        season_mult = 1.0
    elif season.lower() == "rabi":
        season_mult = 0.9 if crop.lower() not in ["wheat", "potato", "onion"] else 1.1
    else:
        season_mult = 0.95

    predicted = base_yield * mult * season_mult * area_acres
    low = predicted * 0.75
    high = predicted * 1.15

    factors = [
        f"Soil type: {soil_type} ({'favorable' if mult >= 1 else 'suboptimal'} for {crop})",
        f"Season: {season}",
        f"Base yield potential: {base_yield} quintals/acre",
    ]

    if mult < 1.0:
        factors.append("Sandy soils may require additional organic matter and more frequent irrigation")

    suggestions = []
    if mult < 1.0:
        suggestions.append("Add compost or farmyard manure to improve soil water holding capacity")
        suggestions.append("Consider drip irrigation for efficient water use")
    if season.lower() == "rabi" and crop.lower() not in ["wheat", "potato", "onion"]:
        suggestions.append("Ensure adequate irrigation during rabi season")
    suggestions.append("Use disease-resistant varieties to minimize yield loss from diseases")
    suggestions.append("Maintain optimal plant population through proper spacing")

    return YieldPrediction(
        crop=crop,
        area_acres=area_acres,
        soil_type=soil_type,
        season=season,
        predicted_yield_quintals=round(predicted, 1),
        yield_range_low=round(low, 1),
        yield_range_high=round(high, 1),
        influencing_factors=factors,
        improvement_suggestions=suggestions,
    )


def get_weather_alerts(temperature: float, humidity: float, rain_probability: float) -> list[WeatherBasedAlert]:
    alerts = []

    if temperature > 38:
        alerts.append(WeatherBasedAlert(
            alert_type="heat_stress",
            severity="high",
            message=f"Extreme heat detected ({temperature}°C). High risk of heat stress for most crops.",
            recommended_action="Irrigate in early morning or late evening. Use shade nets for sensitive crops.",
            affected_diseases=["wilt", "root_rot"],
        ))
    elif temperature > 34:
        alerts.append(WeatherBasedAlert(
            alert_type="heat_stress",
            severity="medium",
            message=f"High temperature ({temperature}°C). Monitor crops for heat stress symptoms.",
            recommended_action="Increase irrigation frequency. Apply mulch to reduce soil temperature.",
            affected_diseases=["wilt"],
        ))

    if humidity > 85:
        alerts.append(WeatherBasedAlert(
            alert_type="disease_favorable",
            severity="high",
            message=f"Very high humidity ({humidity}%). Favorable conditions for fungal diseases.",
            recommended_action="Apply preventive fungicide spray. Improve field ventilation.",
            affected_diseases=["leaf_blight", "leaf_spot", "powdery_mildew", "anthracnose", "downy_mildew"],
        ))
    elif humidity > 70:
        alerts.append(WeatherBasedAlert(
            alert_type="disease_favorable",
            severity="medium",
            message=f"High humidity ({humidity}%). Increased risk of fungal diseases.",
            recommended_action="Monitor fields regularly for early disease symptoms.",
            affected_diseases=["leaf_spot", "rust", "downy_mildew"],
        ))

    if rain_probability > 80:
        alerts.append(WeatherBasedAlert(
            alert_type="heavy_rain",
            severity="high",
            message=f"Heavy rain expected ({rain_probability}% probability). Risk of waterlogging and disease spread.",
            recommended_action="Ensure proper drainage. Avoid pesticide application. Postpone irrigation.",
            affected_diseases=["root_rot", "leaf_blight", "bacterial_blight"],
        ))
    elif rain_probability > 50:
        alerts.append(WeatherBasedAlert(
            alert_type="moderate_rain",
            severity="medium",
            message=f"Rain expected ({rain_probability}% probability). Moderate disease risk.",
            recommended_action="Monitor drainage. Reduce irrigation scheduling.",
            affected_diseases=["leaf_spot", "downy_mildew"],
        ))

    if temperature < 15 and humidity > 80:
        alerts.append(WeatherBasedAlert(
            alert_type="cool_wet",
            severity="medium",
            message=f"Cool and wet conditions ({temperature}°C, {humidity}% humidity). Risk of downy mildew.",
            recommended_action="Apply copper-based preventive spray. Ensure good air circulation.",
            affected_diseases=["downy_mildew", "root_rot"],
        ))

    if not alerts:
        alerts.append(WeatherBasedAlert(
            alert_type="favorable",
            severity="low",
            message="Weather conditions are favorable for crop growth.",
            recommended_action="Continue normal farming operations.",
            affected_diseases=[],
        ))

    return alerts
