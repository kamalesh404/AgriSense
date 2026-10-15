import { BrowserRouter, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import DiseaseDetection from "./pages/DiseaseDetection";
import DiseaseEncyclopedia from "./pages/DiseaseEncyclopedia";
import CropInfo from "./pages/CropInfo";
import SmartRecommendations from "./pages/SmartRecommendations";
import WeatherDashboard from "./pages/WeatherDashboard";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="detect" element={<DiseaseDetection />} />
          <Route path="diseases" element={<DiseaseEncyclopedia />} />
          <Route path="crops" element={<CropInfo />} />
          <Route path="recommendations" element={<SmartRecommendations />} />
          <Route path="weather" element={<WeatherDashboard />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
