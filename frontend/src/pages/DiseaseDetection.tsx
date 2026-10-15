import { useCallback, useEffect, useRef, useState } from "react";
import { predictDisease, type Prediction } from "../api/client";
import {
  AlertIcon,
  CheckIcon,
  ChevronDownIcon,
  CloseIcon,
  DownloadIcon,
  LeafIcon,
  UploadIcon,
  ZoomIcon,
} from "../components/Icons";

const STEPS = [
  "Uploading image",
  "Preprocessing pixels",
  "Extracting leaf features",
  "Running model inference",
  "Compiling diagnosis",
];

interface AnalyzedImage {
  file: File;
  preview: string;
  result: Prediction | null;
  status: "pending" | "analyzing" | "done" | "error";
}

function confidenceColor(c: number): string {
  if (c >= 0.75) return "#3fb950";
  if (c >= 0.45) return "#d29922";
  return "#f85149";
}

function severityClass(severity: string): string {
  if (severity === "high" || severity === "medium") return severity;
  return "none";
}

export default function DiseaseDetection() {
  const [images, setImages] = useState<AnalyzedImage[]>([]);
  const [activeIndex, setActiveIndex] = useState<number | null>(null);
  const [dragOver, setDragOver] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [stepIndex, setStepIndex] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [reported, setReported] = useState(false);
  const [toast, setToast] = useState<string | null>(null);
  const [zoomed, setZoomed] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  const active = activeIndex !== null ? images[activeIndex] : null;

  useEffect(() => {
    if (!analyzing) return;
    setStepIndex(0);
    const id = window.setInterval(() => {
      setStepIndex((s) => Math.min(s + 1, STEPS.length - 1));
    }, 900);
    return () => window.clearInterval(id);
  }, [analyzing]);

  useEffect(() => {
    if (!toast) return;
    const id = window.setTimeout(() => setToast(null), 3500);
    return () => window.clearTimeout(id);
  }, [toast]);

  const addFiles = useCallback((list: FileList | File[]) => {
    const files = Array.from(list).filter((f) =>
      ["image/jpeg", "image/png", "image/webp"].includes(f.type)
    );
    if (files.length === 0) {
      setError("Only JPG, PNG, or WebP images are supported.");
      return;
    }
    setError(null);
    setReported(false);
    const next = files.map((file) => ({
      file,
      preview: URL.createObjectURL(file),
      result: null,
      status: "pending" as const,
    }));
    setImages((prev) => [...prev, ...next]);
    setActiveIndex((prev) => (prev === null ? 0 : prev));
  }, []);

  const handleInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) addFiles(e.target.files);
    e.target.value = "";
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    addFiles(e.dataTransfer.files);
  };

  const removeImage = (idx: number) => {
    setImages((prev) => {
      const copy = [...prev];
      URL.revokeObjectURL(copy[idx].preview);
      copy.splice(idx, 1);
      return copy;
    });
    setActiveIndex((prev) => {
      if (prev === null) return null;
      if (prev === idx) return images.length > 1 ? Math.min(idx, images.length - 2) : null;
      if (prev > idx) return prev - 1;
      return prev;
    });
  };

  const analyze = async () => {
    if (!active || active.status === "analyzing") return;
    setAnalyzing(true);
    setReported(false);
    setError(null);
    setImages((prev) =>
      prev.map((img, i) =>
        i === activeIndex ? { ...img, status: "analyzing" as const } : img
      )
    );
    try {
      const result = await predictDisease(active.file);
      setImages((prev) =>
        prev.map((img, i) =>
          i === activeIndex ? { ...img, result, status: "done" as const } : img
        )
      );
    } catch {
      setImages((prev) =>
        prev.map((img, i) =>
          i === activeIndex ? { ...img, status: "error" as const } : img
        )
      );
      setError("Analysis failed. Please try again with a clearer image.");
    } finally {
      setAnalyzing(false);
    }
  };

  const downloadReport = () => {
    if (!active?.result) return;
    const r = active.result;
    const lines = [
      "AgriSense Disease Analysis Report",
      "=================================",
      `Generated: ${new Date().toLocaleString()}`,
      `Image: ${active.file.name}`,
      "",
      "DIAGNOSIS",
      `Disease: ${r.disease.replace(/_/g, " ")}`,
      `Confidence: ${(r.confidence * 100).toFixed(1)}%`,
      `Severity: ${r.severity.toUpperCase()}`,
      "",
      "DESCRIPTION",
      r.description,
      "",
      "RECOMMENDED TREATMENT",
      r.treatment,
      "",
      "ALL PROBABILITIES",
      ...Object.entries(r.probabilities)
        .sort(([, a], [, b]) => b - a)
        .map(
          ([d, p]) => `  ${d.replace(/_/g, " ")}: ${(p * 100).toFixed(1)}%`
        ),
      "",
      "IMAGE STATISTICS",
      `  Dimensions: ${r.image_stats.width} x ${r.image_stats.height}`,
      `  Mean RGB: (${r.image_stats.r_mean.toFixed(1)}, ${r.image_stats.g_mean.toFixed(1)}, ${r.image_stats.b_mean.toFixed(1)})`,
    ];
    const blob = new Blob([lines.join("\n")], {
      type: "text/plain;charset=utf-8",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `agrisense-report-${r.disease}.txt`;
    a.click();
    URL.revokeObjectURL(url);
    setToast("Report downloaded successfully.");
  };

  const similarDiseases = active?.result
    ? Object.entries(active.result.probabilities)
        .filter(([d]) => d !== active.result!.disease)
        .sort(([, a], [, b]) => b - a)
        .slice(0, 3)
    : [];

  const gaugeRadius = 52;
  const circumference = 2 * Math.PI * gaugeRadius;

  return (
    <div className="page animate-fade-in">
      <div className="page-header">
        <h2>Crop Disease Detection</h2>
        <p className="subtitle">
          Upload leaf images for instant AI diagnosis with treatment guidance
        </p>
      </div>

      <div
        className={`dropzone ${dragOver ? "drag-over" : ""}`}
        onDragOver={(e) => {
          e.preventDefault();
          setDragOver(true);
        }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => {
          if (e.key === "Enter" || e.key === " ") inputRef.current?.click();
        }}
      >
        <div className="dropzone-inner">
          <span className="dropzone-icon">
            <UploadIcon width={40} height={40} />
          </span>
          <p className="dropzone-title">Drag and drop images here</p>
          <span className="dropzone-sub">or click to browse files</span>
          <span className="dropzone-hint">JPG, PNG, WebP up to 10MB each</span>
        </div>
        <input
          ref={inputRef}
          type="file"
          accept="image/jpeg,image/png,image/webp"
          multiple
          hidden
          onChange={handleInput}
        />
      </div>

      {images.length > 0 && (
        <div className="gallery">
          {images.map((img, i) => (
            <button
              key={i}
              className={`gallery-thumb ${i === activeIndex ? "active" : ""} status-${img.status}`}
              onClick={() => setActiveIndex(i)}
            >
              <img src={img.preview} alt={`Upload ${i + 1}`} />
              <span className="thumb-remove" onClick={(e) => { e.stopPropagation(); removeImage(i); }}>
                <CloseIcon width={14} height={14} />
              </span>
              {img.status === "analyzing" && <span className="thumb-spinner" />}
              {img.status === "done" && (
                <span className="thumb-badge ok">
                  <CheckIcon width={12} height={12} />
                </span>
              )}
              {img.status === "error" && (
                <span className="thumb-badge err">
                  <AlertIcon width={12} height={12} />
                </span>
              )}
            </button>
          ))}
        </div>
      )}

      {error && <div className="alert error animate-fade-in">{error}</div>}

      {toast && (
        <div className="toast animate-slide-up">
          <CheckIcon width={16} height={16} />
          <span>{toast}</span>
        </div>
      )}

      {active && !analyzing && (
        <div className="detection-layout">
          <div className="panel preview-panel">
            <div className="panel-head">
              <h3>Image Preview</h3>
              <button
                className="ghost-btn"
                onClick={() => setZoomed(true)}
                aria-label="Zoom image"
              >
                <ZoomIcon width={16} height={16} />
                Zoom
              </button>
            </div>
            <div
              className={`preview-stage ${zoomed ? "zoomed" : ""}`}
              onClick={() => setZoomed(true)}
            >
              <img src={active.preview} alt="Selected leaf" />
            </div>
            <p className="preview-name">{active.file.name}</p>
            <div className="preview-actions">
              <button className="primary-btn" onClick={analyze} disabled={!active}>
                Analyze This Image
              </button>
            </div>
          </div>

          <div className="panel result-panel">
            <div className="panel-head">
              <h3>Diagnosis</h3>
              {active.result && (
                <div className="head-actions">
                  <button
                    className="ghost-btn"
                    onClick={() => {
                      setReported(true);
                      setToast("Thank you. Your feedback helps improve the model.");
                    }}
                    disabled={reported}
                  >
                    <AlertIcon width={15} height={15} />
                    {reported ? "Reported" : "Report Incorrect"}
                  </button>
                  <button className="ghost-btn" onClick={downloadReport}>
                    <DownloadIcon width={15} height={15} />
                    Download Report
                  </button>
                </div>
              )}
            </div>

            {active.status === "analyzing" || analyzing ? (
              <div className="progress-steps">
                {STEPS.map((label, i) => (
                  <div
                    key={label}
                    className={`step ${i < stepIndex ? "done" : ""} ${i === stepIndex ? "current" : ""}`}
                  >
                    <span className="step-dot">
                      {i < stepIndex ? (
                        <CheckIcon width={14} height={14} />
                      ) : (
                        i + 1
                      )}
                    </span>
                    <span className="step-label">{label}</span>
                  </div>
                ))}
              </div>
            ) : active.result ? (
              <DiagnosisResult
                result={active.result}
                similar={similarDiseases}
                circumference={circumference}
                gaugeRadius={gaugeRadius}
              />
            ) : active.status === "error" ? (
              <div className="empty-hint">
                <AlertIcon width={36} height={36} />
                <p>Analysis failed for this image. Try a clearer, well-lit photo.</p>
              </div>
            ) : (
              <div className="empty-hint">
                <LeafIcon width={36} height={36} />
                <p>Click "Analyze This Image" to run disease detection.</p>
              </div>
            )}
          </div>
        </div>
      )}

      {zoomed && active && (
        <div className="lightbox" onClick={() => setZoomed(false)}>
          <button className="lightbox-close" aria-label="Close zoomed view">
            <CloseIcon width={20} height={20} />
          </button>
          <img
            src={active.preview}
            alt="Zoomed leaf"
            className="lightbox-img"
            onClick={(e) => e.stopPropagation()}
          />
          <span className="lightbox-hint">Click anywhere to close</span>
        </div>
      )}
    </div>
  );
}

function DiagnosisResult({
  result,
  similar,
  circumference,
  gaugeRadius,
}: {
  result: Prediction;
  similar: [string, number][];
  circumference: number;
  gaugeRadius: number;
}) {
  const [expanded, setExpanded] = useState(false);
  const offset = circumference * (1 - result.confidence);
  const color = confidenceColor(result.confidence);

  return (
    <div className="diagnosis animate-fade-in">
      <div className="diagnosis-top">
        <div className="gauge-wrap">
          <svg viewBox="0 0 120 120" className="gauge">
            <circle
              cx="60"
              cy="60"
              r={gaugeRadius}
              fill="none"
              stroke="#21262d"
              strokeWidth="10"
            />
            <circle
              cx="60"
              cy="60"
              r={gaugeRadius}
              fill="none"
              stroke={color}
              strokeWidth="10"
              strokeLinecap="round"
              strokeDasharray={circumference}
              strokeDashoffset={offset}
              transform="rotate(-90 60 60)"
              className="gauge-arc"
            />
          </svg>
          <div className="gauge-label">
            <strong style={{ color }}>
              {(result.confidence * 100).toFixed(1)}%
            </strong>
            <span>confidence</span>
          </div>
        </div>
        <div className="diagnosis-title">
          <span className={`severity-badge severity-${severityClass(result.severity)}`}>
            {result.severity.toUpperCase()}
          </span>
          <h4>{result.disease.replace(/_/g, " ")}</h4>
          <p className="desc">{result.description}</p>
        </div>
      </div>

      <div className="treatment-card">
        <button className="treatment-head" onClick={() => setExpanded((e) => !e)}>
          <h4>
            <LeafIcon width={16} height={16} />
            Recommended Treatment
          </h4>
          <ChevronDownIcon
            width={16}
            height={16}
            className={`chev ${expanded ? "up" : ""}`}
          />
        </button>
        <div className={`treatment-body ${expanded ? "expanded" : ""}`}>
          <p>{result.treatment}</p>
          {expanded && (
            <div className="treatment-extra animate-fade-in">
              <div className="extra-row">
                <span className="extra-label">Application</span>
                <span>Apply during early morning or late evening for best absorption.</span>
              </div>
              <div className="extra-row">
                <span className="extra-label">Frequency</span>
                <span>Repeat every 7-10 days until symptoms subside.</span>
              </div>
              <div className="extra-row">
                <span className="extra-label">Safety</span>
                <span>Wear protective gear. Keep away from children and water sources.</span>
              </div>
            </div>
          )}
        </div>
      </div>

      {similar.length > 0 && (
        <div className="similar-section">
          <h4>Similar Diseases to Rule Out</h4>
          <div className="similar-list">
            {similar.map(([d, p]) => (
              <div key={d} className="similar-row">
                <span className="prob-label">{d.replace(/_/g, " ")}</span>
                <div className="prob-bar">
                  <div
                    className="prob-fill"
                    style={{ width: `${p * 100}%` }}
                  />
                </div>
                <span className="prob-value">{(p * 100).toFixed(1)}%</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
