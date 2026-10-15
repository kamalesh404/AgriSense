import { useEffect, useMemo, useState } from "react";
import { getDiseases, type Disease } from "../api/client";
import {
  AlertIcon,
  BookIcon,
  CheckIcon,
  CloseIcon,
  LeafIcon,
  SearchIcon,
} from "../components/Icons";

const SEVERITIES: Disease["severity"][] = ["low", "medium", "high"];

export default function DiseaseEncyclopedia() {
  const [diseases, setDiseases] = useState<Disease[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [query, setQuery] = useState("");
  const [severity, setSeverity] = useState<"all" | Disease["severity"]>("all");
  const [selected, setSelected] = useState<Disease | null>(null);

  useEffect(() => {
    let cancelled = false;
    getDiseases()
      .then((data) => {
        if (!cancelled) setDiseases(data);
      })
      .catch(() => {
        if (!cancelled) setError("Failed to load disease database.");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return diseases.filter((d) => {
      const matchesQuery =
        !q ||
        d.display_name.toLowerCase().includes(q) ||
        d.name.toLowerCase().includes(q) ||
        d.affected_crops.some((c) => c.toLowerCase().includes(q));
      const matchesSeverity = severity === "all" || d.severity === severity;
      return matchesQuery && matchesSeverity;
    });
  }, [diseases, query, severity]);

  return (
    <div className="page animate-fade-in">
      <div className="page-header">
        <h2>Disease Encyclopedia</h2>
        <p className="subtitle">
          Search and explore the complete crop disease database
        </p>
      </div>

      <div className="toolbar">
        <div className="search-box">
          <SearchIcon width={16} height={16} />
          <input
            type="text"
            placeholder="Search diseases or affected crops..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          {query && (
            <button className="clear-btn" onClick={() => setQuery("")}>
              <CloseIcon width={14} height={14} />
            </button>
          )}
        </div>
        <div className="severity-filter">
          {(["all", ...SEVERITIES] as const).map((s) => (
            <button
              key={s}
              className={`filter-chip ${severity === s ? "active" : ""}`}
              onClick={() => setSeverity(s)}
            >
              {s === "all" ? "All" : s.toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="disease-grid">
          {Array.from({ length: 6 }).map((_, i) => (
            <div key={i} className="disease-card skeleton-card">
              <div className="skeleton skeleton-img" />
              <div className="skeleton skeleton-line" />
              <div className="skeleton skeleton-line short" />
            </div>
          ))}
        </div>
      ) : error ? (
        <div className="alert error">{error}</div>
      ) : filtered.length === 0 ? (
        <div className="empty-state">
          <BookIcon width={40} height={40} />
          <p>No diseases match your search.</p>
        </div>
      ) : (
        <>
          <div className="disease-grid">
            {filtered.map((d) => (
              <button
                key={d.name}
                className="disease-card"
                onClick={() => setSelected(d)}
              >
                <div className="disease-icon">
                  <LeafIcon width={28} height={28} />
                </div>
                <div className="disease-info">
                  <h3>{d.display_name}</h3>
                  <span className={`sev-dot sev-${d.severity}`}>
                    {d.severity.toUpperCase()}
                  </span>
                  <p>{d.affected_crops.slice(0, 3).join(", ")}</p>
                </div>
              </button>
            ))}
          </div>

          {selected && (
            <DiseaseModal disease={selected} onClose={() => setSelected(null)} />
          )}
        </>
      )}
    </div>
  );
}

function DiseaseModal({
  disease,
  onClose,
}: {
  disease: Disease;
  onClose: () => void;
}) {
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        className="modal animate-pop"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
      >
        <div className="modal-head">
          <div>
            <span className={`severity-badge severity-${disease.severity}`}>
              {disease.severity.toUpperCase()}
            </span>
            <h3>{disease.display_name}</h3>
            <span className="latin-name">{disease.name.replace(/_/g, " ")}</span>
          </div>
          <button className="icon-btn" onClick={onClose} aria-label="Close">
            <CloseIcon />
          </button>
        </div>

        <div className="modal-body">
          <section className="modal-section">
            <h4>Description</h4>
            <p>{disease.description}</p>
          </section>

          <section className="modal-section">
            <h4>Symptoms</h4>
            <ul className="check-list">
              {disease.symptoms.map((s) => (
                <li key={s}>
                  <AlertIcon width={14} height={14} />
                  <span>{s}</span>
                </li>
              ))}
            </ul>
          </section>

          <section className="modal-section">
            <h4>Treatment</h4>
            <p>{disease.treatment}</p>
          </section>

          <section className="modal-section">
            <h4>Prevention Tips</h4>
            <ul className="check-list">
              {disease.prevention.map((p) => (
                <li key={p}>
                  <CheckIcon width={14} height={14} />
                  <span>{p}</span>
                </li>
              ))}
            </ul>
          </section>

          <section className="modal-section">
            <h4>Affected Crops</h4>
            <div className="disease-tags">
              {disease.affected_crops.map((c) => (
                <span key={c} className="tag">
                  {c}
                </span>
              ))}
            </div>
          </section>
        </div>
      </div>
    </div>
  );
}
