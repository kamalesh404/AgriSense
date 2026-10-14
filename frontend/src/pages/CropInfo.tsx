import { useEffect, useState } from "react";
import { getCrops, type Crop } from "../api/client";

export default function CropInfo() {
  const [crops, setCrops] = useState<Crop[]>([]);

  useEffect(() => {
    getCrops().then(setCrops);
  }, []);

  return (
    <div className="page">
      <h2>Crop Information</h2>
      <p className="subtitle">
        Essential farming information for major crops grown in Tamil Nadu
      </p>
      <div className="crop-grid">
        {crops.map((crop) => (
          <div key={crop.name} className="card crop-card">
            <h3>{crop.name}</h3>
            <div className="crop-detail">
              <span className="label">Soil Type:</span>
              <span>{crop.soil_type}</span>
            </div>
            <div className="crop-detail">
              <span className="label">Water Needs:</span>
              <span>{crop.water_requirement}</span>
            </div>
            <div className="crop-detail">
              <span className="label">Season:</span>
              <span>{crop.growing_season}</span>
            </div>
            <div className="crop-detail">
              <span className="label">Common Diseases:</span>
              <div className="disease-tags">
                {crop.common_diseases.map((d) => (
                  <span key={d} className="tag">
                    {d.replace(/_/g, " ")}
                  </span>
                ))}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
