const BASE = "/api";

export interface Prediction {
  disease: string;
  confidence: number;
  probabilities: Record<string, number>;
  treatment: string;
  description: string;
  severity: string;
  image_stats: {
    width: number;
    height: number;
    r_mean: number;
    g_mean: number;
    b_mean: number;
  };
}

export interface Crop {
  name: string;
  soil_type: string;
  water_requirement: string;
  growing_season: string;
  common_diseases: string[];
}

export interface WeatherData {
  temperature: number;
  humidity: number;
  condition: string;
  irrigation_advice: string;
  disease_risk: string;
  recommendation: string;
}

export interface Disease {
  name: string;
  display_name: string;
  description: string;
  symptoms: string[];
  treatment: string;
  prevention: string[];
  severity: "low" | "medium" | "high";
  affected_crops: string[];
  image_url: string | null;
}

export interface CropRotation {
  current_crop: string;
  suggestions: RotationSuggestion[];
}

export interface RotationSuggestion {
  crop: string;
  reason: string;
  season: string;
  nitrogen_impact: string;
  difficulty: "easy" | "moderate" | "hard";
}

export interface FertilizerRecommendation {
  crop: string;
  soil_type: string;
  area: number;
  recommendations: FertilizerDose[];
}

export interface FertilizerDose {
  fertilizer: string;
  quantity: string;
  timing: string;
  purpose: string;
}

export interface FarmingCalendar {
  crop: string;
  months: CalendarMonth[];
}

export interface CalendarMonth {
  month: string;
  stage: string;
  tasks: string[];
}

export interface Pesticide {
  name: string;
  type: string;
  target_pests: string[];
  dosage: string;
  safety_period_days: number;
  organic: boolean;
}

export interface WeatherAlert {
  id: string;
  title: string;
  description: string;
  severity: "info" | "warning" | "critical";
  category: string;
}

export interface ForecastDay {
  day: string;
  temp_high: number;
  temp_low: number;
  condition: string;
  humidity: number;
  farming_advice: string;
  disease_risk: "low" | "medium" | "high";
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, init);
  if (!res.ok) {
    throw new Error(`Request failed: ${res.status} ${res.statusText}`);
  }
  return res.json() as Promise<T>;
}

export async function predictDisease(file: File): Promise<Prediction> {
  const formData = new FormData();
  formData.append("file", file);
  return request<Prediction>("/predict", { method: "POST", body: formData });
}

export async function batchPredict(files: File[]): Promise<Prediction[]> {
  const formData = new FormData();
  files.forEach((f) => formData.append("files", f));
  return request<Prediction[]>("/predict/batch", {
    method: "POST",
    body: formData,
  });
}

export async function getCrops(): Promise<Crop[]> {
  return request<Crop[]>("/crops");
}

export async function getCrop(name: string): Promise<Crop> {
  return request<Crop>(`/crops/${encodeURIComponent(name)}`);
}

export async function getDiseases(): Promise<Disease[]> {
  return request<Disease[]>("/diseases");
}

export async function getDiseaseDetail(name: string): Promise<Disease> {
  return request<Disease>(`/diseases/${encodeURIComponent(name)}`);
}

export async function getCropRotation(
  currentCrop: string
): Promise<CropRotation> {
  return request<CropRotation>(
    `/crop-rotation?current_crop=${encodeURIComponent(currentCrop)}`
  );
}

export async function getFertilizerRecommendation(
  crop: string,
  soil: string,
  area: number
): Promise<FertilizerRecommendation> {
  const params = new URLSearchParams({
    crop,
    soil,
    area: String(area),
  });
  return request<FertilizerRecommendation>(`/fertilizer?${params}`);
}

export async function getFarmingCalendar(
  crop: string
): Promise<FarmingCalendar> {
  return request<FarmingCalendar>(
    `/farming-calendar?crop=${encodeURIComponent(crop)}`
  );
}

export async function getPesticides(): Promise<Pesticide[]> {
  return request<Pesticide[]>("/pesticides");
}

export async function getWeatherAlerts(
  lat?: number,
  lon?: number
): Promise<WeatherAlert[]> {
  const params = new URLSearchParams();
  if (lat !== undefined) params.set("lat", String(lat));
  if (lon !== undefined) params.set("lon", String(lon));
  const query = params.toString();
  return request<WeatherAlert[]>(`/weather-alerts${query ? `?${query}` : ""}`);
}

export async function getWeatherAdvice(
  temperature: number,
  humidity: number,
  condition: string
): Promise<WeatherData> {
  const params = new URLSearchParams({
    temperature: String(temperature),
    humidity: String(humidity),
    condition,
  });
  const res = await fetch(`${BASE}/weather-advice?${params}`);
  return res.json();
}
