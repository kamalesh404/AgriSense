import { useState } from "react";
import { predictDisease, type Prediction } from "../api/client";

export default function DiseaseDetection() {
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [result, setResult] = useState<Prediction | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const f = e.target.files?.[0];
    if (f) {
      setFile(f);
      setPreview(URL.createObjectURL(f));
      setResult(null);
      setError(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    setError(null);
    try {
      const prediction = await predictDisease(file);
      setResult(prediction);
    } catch (err) {
      setError("Failed to analyze image. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <h2>Crop Disease Detection</h2>
      <form onSubmit={handleSubmit} className="upload-form">
        <div className="upload-area">
          {preview ? (
            <img src={preview} alt="Preview" className="preview-img" />
          ) : (
            <div className="upload-placeholder">
              <p>Click to upload or drag and drop</p>
              <span>JPG, PNG up to 10MB</span>
            </div>
          )}
          <input
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            className="file-input"
          />
        </div>
        <button type="submit" disabled={!file || loading}>
          {loading ? "Analyzing..." : "Detect Disease"}
        </button>
      </form>

      {error && <div className="alert error">{error}</div>}

      {result && (
        <div className="result-section">
          <div className="card result-card">
            <h3>Diagnosis Result</h3>
            <div className={`severity-badge severity-${result.severity}`}>
              {result.severity.toUpperCase()}
            </div>
            <h4>{result.disease.replace(/_/g, " ")}</h4>
            <p className="confidence">Confidence: {(result.confidence * 100).toFixed(1)}%</p>
            <p>{result.description}</p>
          </div>

          <div className="card treatment-card">
            <h3>Recommended Treatment</h3>
            <p>{result.treatment}</p>
          </div>

          <div className="card probs-card">
            <h3>All Probabilities</h3>
            <div className="prob-list">
              {Object.entries(result.probabilities)
                .sort(([, a], [, b]) => b - a)
                .map(([disease, prob]) => (
                  <div key={disease} className="prob-row">
                    <span className="prob-label">{disease.replace(/_/g, " ")}</span>
                    <div className="prob-bar">
                      <div
                        className="prob-fill"
                        style={{ width: `${prob * 100}%` }}
                      />
                    </div>
                    <span className="prob-value">{(prob * 100).toFixed(1)}%</span>
                  </div>
                ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
