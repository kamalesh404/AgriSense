import { Link } from "react-router-dom";

export default function Dashboard() {
  return (
    <div className="page">
      <h2>AgriSense Dashboard</h2>
      <p className="subtitle">
        AI-powered crop disease detection and smart farming recommendations
      </p>
      <div className="grid">
        <Link to="/detect" className="card feature-card">
          <h3>Disease Detection</h3>
          <p>Upload a crop leaf image for instant AI diagnosis and treatment recommendations</p>
        </Link>
        <Link to="/crops" className="card feature-card">
          <h3>Crop Information</h3>
          <p>Database of crops with soil, water requirements, and common diseases</p>
        </Link>
        <Link to="/weather" className="card feature-card">
          <h3>Weather Advice</h3>
          <p>Smart irrigation and disease risk alerts based on weather conditions</p>
        </Link>
      </div>
      <div className="card info-card">
        <h3>How It Works</h3>
        <ol className="steps">
          <li>Upload a clear photo of the affected crop leaf</li>
          <li>AI model analyzes the image for disease patterns</li>
          <li>Get instant diagnosis with treatment recommendations</li>
          <li>Follow weather-based advice to prevent future outbreaks</li>
        </ol>
      </div>
    </div>
  );
}
