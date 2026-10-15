import { useEffect, useState } from "react";
import {
  getCropRotation,
  getFarmingCalendar,
  getFertilizerRecommendation,
  getPesticides,
  type CropRotation,
  type FarmingCalendar,
  type FertilizerRecommendation,
  type Pesticide,
} from "../api/client";
import {
  CalendarIcon,
  CheckIcon,
  FlaskIcon,
  LeafIcon,
  SearchIcon,
  SprayIcon,
} from "../components/Icons";

type Tab = "rotation" | "fertilizer" | "calendar" | "pesticides";

const CROPS = [
  "Rice",
  "Wheat",
  "Maize",
  "Cotton",
  "Sugarcane",
  "Tomato",
  "Groundnut",
  "Soybean",
];

const SOILS = ["Alluvial", "Black", "Red", "Sandy", "Clay", "Loamy"];

export default function SmartRecommendations() {
  const [tab, setTab] = useState<Tab>("rotation");

  return (
    <div className="page animate-fade-in">
      <div className="page-header">
        <h2>Smart Recommendations</h2>
        <p className="subtitle">
          AI-powered crop planning, fertilizer calculation, and pesticide guidance
        </p>
      </div>

      <div className="tabs">
        <button
          className={`tab ${tab === "rotation" ? "active" : ""}`}
          onClick={() => setTab("rotation")}
        >
          <LeafIcon width={16} height={16} />
          Crop Rotation
        </button>
        <button
          className={`tab ${tab === "fertilizer" ? "active" : ""}`}
          onClick={() => setTab("fertilizer")}
        >
          <FlaskIcon width={16} height={16} />
          Fertilizer Calculator
        </button>
        <button
          className={`tab ${tab === "calendar" ? "active" : ""}`}
          onClick={() => setTab("calendar")}
        >
          <CalendarIcon width={16} height={16} />
          Farming Calendar
        </button>
        <button
          className={`tab ${tab === "pesticides" ? "active" : ""}`}
          onClick={() => setTab("pesticides")}
        >
          <SprayIcon width={16} height={16} />
          Pesticide Database
        </button>
      </div>

      {tab === "rotation" && <RotationPlanner />}
      {tab === "fertilizer" && <FertilizerCalculator />}
      {tab === "calendar" && <FarmingCalendarView />}
      {tab === "pesticides" && <PesticideDatabase />}
    </div>
  );
}

function RotationPlanner() {
  const [crop, setCrop] = useState(CROPS[0]);
  const [data, setData] = useState<CropRotation | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      setData(await getCropRotation(crop));
    } catch {
      setError("Could not load rotation suggestions.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="tab-panel">
      <div className="form-row">
        <div className="form-group">
          <label>Current Crop</label>
          <select value={crop} onChange={(e) => setCrop(e.target.value)}>
            {CROPS.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </div>
        <div className="form-group form-action">
          <button className="primary-btn" onClick={load} disabled={loading}>
            {loading ? "Loading..." : "Get Rotation Plan"}
          </button>
        </div>
      </div>

      {error && <div className="alert error">{error}</div>}

      {loading && <div className="skeleton-card skeleton-tall" />}

      {data && !loading && (
        <div className="card-grid animate-fade-in">
          {data.suggestions.map((s) => (
            <div key={s.crop} className="result-mini-card">
              <div className="mini-head">
                <LeafIcon width={20} height={20} />
                <h4>{s.crop}</h4>
                <span className={`diff diff-${s.difficulty}`}>{s.difficulty}</span>
              </div>
              <p>{s.reason}</p>
              <div className="mini-meta">
                <span>Season: {s.season}</span>
                <span>Nitrogen: {s.nitrogen_impact}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

function FertilizerCalculator() {
  const [crop, setCrop] = useState(CROPS[0]);
  const [soil, setSoil] = useState(SOILS[0]);
  const [area, setArea] = useState(1);
  const [data, setData] = useState<FertilizerRecommendation | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    if (area <= 0) {
      setError("Area must be greater than zero.");
      return;
    }
    setLoading(true);
    setError(null);
    try {
      setData(await getFertilizerRecommendation(crop, soil, area));
    } catch {
      setError("Could not calculate fertilizer requirements.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="tab-panel">
      <div className="form-row">
        <div className="form-group">
          <label>Crop</label>
          <select value={crop} onChange={(e) => setCrop(e.target.value)}>
            {CROPS.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </div>
        <div className="form-group">
          <label>Soil Type</label>
          <select value={soil} onChange={(e) => setSoil(e.target.value)}>
            {SOILS.map((s) => (
              <option key={s} value={s}>
                {s}
              </option>
            ))}
          </select>
        </div>
        <div className="form-group">
          <label>Area (acres)</label>
          <input
            type="number"
            min="0.1"
            step="0.1"
            value={area}
            onChange={(e) => setArea(Number(e.target.value))}
          />
        </div>
        <div className="form-group form-action">
          <button className="primary-btn" onClick={load} disabled={loading}>
            {loading ? "Calculating..." : "Calculate"}
          </button>
        </div>
      </div>

      {error && <div className="alert error">{error}</div>}

      {loading && <div className="skeleton-card skeleton-tall" />}

      {data && !loading && (
        <div className="card-grid animate-fade-in">
          {data.recommendations.map((r) => (
            <div key={r.fertilizer} className="result-mini-card">
              <div className="mini-head">
                <FlaskIcon width={20} height={20} />
                <h4>{r.fertilizer}</h4>
                <span className="pill">{r.quantity}</span>
              </div>
              <p>{r.purpose}</p>
              <div className="mini-meta">
                <span>Timing: {r.timing}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

function FarmingCalendarView() {
  const [crop, setCrop] = useState(CROPS[0]);
  const [data, setData] = useState<FarmingCalendar | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      setData(await getFarmingCalendar(crop));
    } catch {
      setError("Could not load farming calendar.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="tab-panel">
      <div className="form-row">
        <div className="form-group">
          <label>Crop</label>
          <select value={crop} onChange={(e) => setCrop(e.target.value)}>
            {CROPS.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
        </div>
        <div className="form-group form-action">
          <button className="primary-btn" onClick={load} disabled={loading}>
            {loading ? "Loading..." : "Show Calendar"}
          </button>
        </div>
      </div>

      {error && <div className="alert error">{error}</div>}

      {loading && <div className="skeleton-card skeleton-tall" />}

      {data && !loading && (
        <div className="calendar-grid animate-fade-in">
          {data.months.map((m) => (
            <div key={m.month} className="calendar-card">
              <div className="calendar-head">
                <span className="month-badge">{m.month.slice(0, 3)}</span>
                <span className="stage-label">{m.stage}</span>
              </div>
              <ul className="task-list">
                {m.tasks.map((t) => (
                  <li key={t}>
                    <CheckIcon width={13} height={13} />
                    <span>{t}</span>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

function PesticideDatabase() {
  const [items, setItems] = useState<Pesticide[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [query, setQuery] = useState("");

  useEffect(() => {
    let cancelled = false;
    getPesticides()
      .then((data) => {
        if (!cancelled) setItems(data);
      })
      .catch(() => {
        if (!cancelled) setError("Failed to load pesticide database.");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const filtered = items.filter((p) => {
    const q = query.trim().toLowerCase();
    if (!q) return true;
    return (
      p.name.toLowerCase().includes(q) ||
      p.target_pests.some((t) => t.toLowerCase().includes(q))
    );
  });

  return (
    <section className="tab-panel">
      <div className="search-box search-inline">
        <SearchIcon width={16} height={16} />
        <input
          type="text"
          placeholder="Search by pesticide name or target pest..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
      </div>

      {loading ? (
        <div className="skeleton-card skeleton-tall" />
      ) : error ? (
        <div className="alert error">{error}</div>
      ) : (
        <div className="card-grid animate-fade-in">
          {filtered.map((p) => (
            <div key={p.name} className="result-mini-card">
              <div className="mini-head">
                <SprayIcon width={20} height={20} />
                <h4>{p.name}</h4>
                <span className={`pill ${p.organic ? "pill-green" : ""}`}>
                  {p.organic ? "Organic" : "Chemical"}
                </span>
              </div>
              <div className="mini-meta">
                <span>Type: {p.type}</span>
                <span>Dosage: {p.dosage}</span>
                <span>Safety: {p.safety_period_days} days</span>
              </div>
              <div className="disease-tags">
                {p.target_pests.map((t) => (
                  <span key={t} className="tag">
                    {t}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
