import pytest

from app.core.recommendations import (
    calculate_fertilizer,
    generate_seasonal_calendar,
    get_pest_lifecycle,
    get_weather_alerts,
    plan_crop_rotation,
    predict_yield,
)


class TestCropRotation:
    def test_rice_rotation(self):
        plan = plan_crop_rotation("rice")
        assert plan.current_crop == "rice"
        assert len(plan.recommended_next_crops) > 0
        assert plan.rotation_benefit is not None

    def test_cotton_rotation(self):
        plan = plan_crop_rotation("cotton")
        assert plan.current_crop == "cotton"
        assert len(plan.recommended_next_crops) > 0

    def test_invalid_crop_raises(self):
        with pytest.raises(ValueError):
            plan_crop_rotation("invalid_crop_xyz")

    def test_rotation_has_soil_impact(self):
        plan = plan_crop_rotation("rice")
        assert plan.soil_impact is not None
        assert len(plan.soil_impact) > 0


class TestFertilizerCalculator:
    def test_rice_fertilizer(self):
        result = calculate_fertilizer("rice", "clay loam", 1.0)
        assert result.crop == "rice"
        assert result.urea_kg > 0
        assert result.dap_kg > 0
        assert result.mop_kg > 0
        assert result.organic_manure_kg > 0

    def test_fertilizer_scales_with_area(self):
        result_1acre = calculate_fertilizer("rice", "clay loam", 1.0)
        result_2acre = calculate_fertilizer("rice", "clay loam", 2.0)
        assert result_2acre.urea_kg > result_1acre.urea_kg

    def test_fertilizer_cost_positive(self):
        result = calculate_fertilizer("wheat", "loam", 1.0)
        assert result.estimated_cost_inr > 0

    def test_fertilizer_schedule(self):
        result = calculate_fertilizer("rice", "clay loam", 1.0)
        assert len(result.application_schedule) >= 2

    def test_invalid_crop_raises(self):
        with pytest.raises(ValueError):
            calculate_fertilizer("invalid_crop", "loam", 1.0)


class TestPestLifecycle:
    def test_aphid_lifecycle(self):
        result = get_pest_lifecycle("aphid")
        assert result is not None
        assert result.pest_name == "aphid"
        assert len(result.control_measures) > 0

    def test_bollworm_lifecycle(self):
        result = get_pest_lifecycle("bollworm")
        assert result is not None
        assert result.scientific_name is not None

    def test_invalid_pest_returns_none(self):
        result = get_pest_lifecycle("nonexistent_pest")
        assert result is None


class TestSeasonalCalendar:
    def test_rice_calendar(self):
        cal = generate_seasonal_calendar("rice")
        assert cal.crop == "rice"
        assert len(cal.entries) > 0
        assert cal.planting_window is not None

    def test_wheat_calendar(self):
        cal = generate_seasonal_calendar("wheat")
        assert cal.crop == "wheat"
        assert "Rabi" in cal.planting_window

    def test_invalid_crop_raises(self):
        with pytest.raises(ValueError):
            generate_seasonal_calendar("invalid_crop")


class TestYieldPrediction:
    def test_rice_yield(self):
        result = predict_yield("rice", 1.0, "clay loam", "kharif")
        assert result.crop == "rice"
        assert result.predicted_yield_quintals > 0
        assert result.yield_range_low < result.predicted_yield_quintals
        assert result.yield_range_high > result.predicted_yield_quintals

    def test_yield_scales_with_area(self):
        result_1 = predict_yield("rice", 1.0, "clay loam", "kharif")
        result_5 = predict_yield("rice", 5.0, "clay loam", "kharif")
        assert result_5.predicted_yield_quintals > result_1.predicted_yield_quintals

    def test_yield_has_suggestions(self):
        result = predict_yield("rice", 1.0, "sandy loam", "kharif")
        assert len(result.improvement_suggestions) > 0

    def test_invalid_crop_raises(self):
        with pytest.raises(ValueError):
            predict_yield("invalid_crop", 1.0, "loam", "kharif")


class TestWeatherAlerts:
    def test_high_temperature_alert(self):
        alerts = get_weather_alerts(40.0, 50.0, 0.0)
        assert any(a.alert_type == "heat_stress" for a in alerts)

    def test_high_humidity_alert(self):
        alerts = get_weather_alerts(30.0, 90.0, 0.0)
        assert any(a.alert_type == "disease_favorable" for a in alerts)

    def test_heavy_rain_alert(self):
        alerts = get_weather_alerts(28.0, 70.0, 90.0)
        assert any(a.alert_type == "heavy_rain" for a in alerts)

    def test_favorable_conditions(self):
        alerts = get_weather_alerts(25.0, 50.0, 10.0)
        assert any(a.alert_type == "favorable" for a in alerts)

    def test_alerts_have_recommendations(self):
        alerts = get_weather_alerts(40.0, 90.0, 90.0)
        for alert in alerts:
            assert alert.recommended_action is not None
            assert len(alert.recommended_action) > 0
