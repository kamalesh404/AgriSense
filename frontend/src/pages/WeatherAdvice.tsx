import { useState } from "react";
import { getWeatherAdvice, type WeatherData } from "../api/client";

export default function WeatherAdvice() {
  const [temperature, setTemperature] = useState(30);
  const [humidity, setHumidity] = useState(60);
  const [condition, setCondition] = useState("sunny");
  const [result, setResult] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const data = await getWeatherAdvice(temperature, humidity, condition);
      setResult(data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <h2>Weather-Based Farming Advice</h2>
      <form onSubmit={handleSubmit} className="weather-form">
        <div className="form-row">
          <div className="form-group">
            <label>Temperature (Celsius)</label>
            <input
              type="number"
              value={temperature}
              onChange={(e) => setTemperature(Number(e.target.value))}
              min="-10"
              max="55"
              step="0.5"
            />
          </div>
          <div className="form-group">
            <label>Humidity (%)</label>
            <input
              type="number"
              value={humidity}
              onChange={(e) => setHumidity(Number(e.target.value))}
              min="0"
              max="100"
            />
          </div>
          <div className="form-group">
            <label>Condition</label>
            <select
              value={condition}
              onChange={(e) => setCondition(e.target.value)}
            >
              <option value="sunny">Sunny</option>
              <option value="cloudy">Cloudy</option>
              <option value="rainy">Rainy</option>
              <option value="humid">Humid</option>
            </select>
          </div>
        </div>
        <button type="submit" disabled={loading}>
          {loading ? "Getting Advice..." : "Get Farming Advice"}
        </button>
      </form>

      {result && (
        <div className="result-section">
          <div className="card advice-card">
            <h3>Irrigation Advice</h3>
            <p>{result.irrigation_advice}</p>
          </div>
          <div className="card advice-card">
            <h3>Disease Risk Assessment</h3>
            <p>{result.disease_risk}</p>
          </div>
          <div className="card advice-card">
            <h3>General Recommendation</h3>
            <p>{result.recommendation}</p>
          </div>
        </div>
      )}
    </div>
  );
}
