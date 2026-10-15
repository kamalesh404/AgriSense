import { useEffect, useState } from "react";
import { getWeatherAlerts, type ForecastDay, type WeatherAlert } from "../api/client";
import {
  AlertIcon,
  CloudIcon,
  DropletIcon,
  GaugeIcon,
  RainIcon,
  SunIcon,
  ThermometerIcon,
  WindIcon,
} from "../components/Icons";

interface CurrentWeather {
  temp: number;
  humidity: number;
  wind: number;
  condition: "Sunny" | "Cloudy" | "Rainy";
  irrigation: string;
  diseaseRisk: "low" | "medium" | "high";
}

const CURRENT: CurrentWeather = {
  temp: 32,
  humidity: 78,
  wind: 12,
  condition: "Cloudy",
  irrigation:
    "Delay irrigation today. Humidity is high and soil moisture should be adequate for 24-48 hours.",
  diseaseRisk: "high",
};

const FORECAST: ForecastDay[] = [
  {
    day: "Today",
    temp_high: 33,
    temp_low: 24,
    condition: "Cloudy",
    humidity: 78,
    farming_advice:
      "High humidity favors fungal diseases. Scout fields for early blight signs.",
    disease_risk: "high",
  },
  {
    day: "Tomorrow",
    temp_high: 30,
    temp_low: 23,
    condition: "Rainy",
    humidity: 92,
    farming_advice:
      "Rain expected. Avoid pesticide application. Check drainage channels before evening.",
    disease_risk: "high",
  },
  {
    day: "Day 3",
    temp_high: 31,
    temp_low: 23,
    condition: "Rainy",
    humidity: 88,
    farming_advice:
      "Wet leaf conditions persist. Consider preventive copper-based spray after rain stops.",
    disease_risk: "high",
  },
  {
    day: "Day 4",
    temp_high: 34,
    temp_low: 25,
    condition: "Sunny",
    humidity: 60,
    farming_advice:
      "Dry weather returns. Resume normal irrigation schedule in early morning hours.",
    disease_risk: "low",
  },
  {
    day: "Day 5",
    temp_high: 35,
    temp_low: 26,
    condition: "Sunny",
    humidity: 55,
    farming_advice:
      "Hot and dry. Increase irrigation frequency. Watch for spider mite infestations.",
    disease_risk: "low",
  },
];

function conditionIcon(condition: string) {
  if (condition === "Sunny") return <SunIcon width={30} height={30} />;
  if (condition === "Rainy") return <RainIcon width={30} height={30} />;
  return <CloudIcon width={30} height={30} />;
}

export default function WeatherDashboard() {
  const [alerts, setAlerts] = useState<WeatherAlert[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    getWeatherAlerts()
      .then((data) => {
        if (!cancelled) setAlerts(data);
      })
      .catch(() => {
        if (!cancelled) {
          setAlerts([
            {
              id: "local-1",
              title: "High Disease Pressure",
              description:
                "Wet and humid conditions over the past 72 hours significantly increase fungal disease risk.",
              severity: "warning",
              category: "Disease",
            },
            {
              id: "local-2",
              title: "Irrigation Window",
              description:
                "Soil moisture is adequate. Skip today's irrigation cycle to avoid waterlogging.",
              severity: "info",
              category: "Irrigation",
            },
          ]);
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className="page animate-fade-in">
      <div className="page-header">
        <h2>Weather Dashboard</h2>
        <p className="subtitle">
          Weather-aware farming alerts, forecasts, and irrigation planning
        </p>
      </div>

      <div className="weather-layout">
        <div className="panel weather-now">
          <div className="panel-head">
            <h3>Current Conditions</h3>
            <span className="live-pill">LIVE</span>
          </div>
          <div className="weather-main">
            <div className="weather-icon-large">
              {conditionIcon(CURRENT.condition)}
            </div>
            <div className="weather-temp">
              <strong>{CURRENT.temp}&deg;C</strong>
              <span>{CURRENT.condition}</span>
            </div>
          </div>
          <div className="weather-stats">
            <div className="stat">
              <DropletIcon width={18} height={18} />
              <span className="stat-value">{CURRENT.humidity}%</span>
              <span className="stat-label">Humidity</span>
            </div>
            <div className="stat">
              <WindIcon width={18} height={18} />
              <span className="stat-value">{CURRENT.wind} km/h</span>
              <span className="stat-label">Wind</span>
            </div>
            <div className="stat">
              <ThermometerIcon width={18} height={18} />
              <span className="stat-value">
                {Math.round(CURRENT.temp * 1.8 + 32)}&deg;F
              </span>
              <span className="stat-label">Feels like</span>
            </div>
          </div>
        </div>

        <div className="panel risk-panel">
          <div className="panel-head">
            <h3>
              <GaugeIcon width={18} height={18} />
              Disease Risk Meter
            </h3>
          </div>
          <RiskMeter level={CURRENT.diseaseRisk} />
          <div className="irrigation-widget">
            <div className="irrigation-head">
              <DropletIcon width={18} height={18} />
              <h4>Irrigation Recommendation</h4>
            </div>
            <p>{CURRENT.irrigation}</p>
          </div>
        </div>
      </div>

      <div className="panel alerts-panel">
        <div className="panel-head">
          <h3>
            <AlertIcon width={18} height={18} />
            Weather-Based Alerts
          </h3>
        </div>
        {loading ? (
          <div className="skeleton-card skeleton-tall" />
        ) : (
          <div className="alerts-list">
            {alerts.map((a) => (
              <div key={a.id} className={`alert-row sev-${a.severity}`}>
                <span className="alert-sev-badge">
                  {a.severity === "critical"
                    ? "CRITICAL"
                    : a.severity === "warning"
                      ? "WARNING"
                      : "INFO"}
                </span>
                <div className="alert-content">
                  <strong>{a.title}</strong>
                  <p>{a.description}</p>
                  <span className="alert-category">{a.category}</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="panel forecast-panel">
        <div className="panel-head">
          <h3>5-Day Farming Forecast</h3>
        </div>
        <div className="forecast-grid">
          {FORECAST.map((d) => (
            <div key={d.day} className="forecast-card">
              <div className="forecast-head">
                <span className="forecast-day">{d.day}</span>
                {conditionIcon(d.condition)}
              </div>
              <div className="forecast-temps">
                <span className="temp-high">{d.temp_high}&deg;</span>
                <span className="temp-low">{d.temp_low}&deg;</span>
              </div>
              <div className="forecast-meta">
                <span className="humidity-chip">
                  <DropletIcon width={13} height={13} />
                  {d.humidity}%
                </span>
                <span className={`risk-chip risk-${d.disease_risk}`}>
                  {d.disease_risk.toUpperCase()}
                </span>
              </div>
              <p className="forecast-advice">{d.farming_advice}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function RiskMeter({ level }: { level: "low" | "medium" | "high" }) {
  const pct = level === "high" ? 82 : level === "medium" ? 48 : 18;
  const color = level === "high" ? "#f85149" : level === "medium" ? "#d29922" : "#3fb950";
  const label = level === "high" ? "HIGH RISK" : level === "medium" ? "MODERATE" : "LOW";

  return (
    <div className="risk-meter">
      <div className="risk-track">
        <div
          className="risk-fill"
          style={{ width: `${pct}%`, background: color }}
        />
      </div>
      <div className="risk-info">
        <strong style={{ color }}>{label}</strong>
        <span>
          {level === "high"
            ? "Fungal and bacterial disease outbreak likely within 48 hours. Apply preventive treatment."
            : level === "medium"
              ? "Conditions may favor disease. Monitor crops closely."
              : "Weather conditions are unfavorable for disease spread."}
        </span>
      </div>
    </div>
  );
}
