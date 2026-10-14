import { BrowserRouter, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import Dashboard from "./pages/Dashboard";
import DiseaseDetection from "./pages/DiseaseDetection";
import CropInfo from "./pages/CropInfo";
import WeatherAdvice from "./pages/WeatherAdvice";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="detect" element={<DiseaseDetection />} />
          <Route path="crops" element={<CropInfo />} />
          <Route path="weather" element={<WeatherAdvice />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
