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

export async function predictDisease(
  file: File
): Promise<Prediction> {
  const formData = new FormData();
  formData.append("file", file);
  const res = await fetch(`${BASE}/predict`, {
    method: "POST",
    body: formData,
  });
  return res.json();
}

export async function getCrops(): Promise<Crop[]> {
  const res = await fetch(`${BASE}/crops`);
  return res.json();
}

export async function getCrop(name: string): Promise<Crop> {
  const res = await fetch(`${BASE}/crops/${name}`);
  return res.json();
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
