from pydantic import BaseModel


class PredictionResponse(BaseModel):
    disease: str
    confidence: float
    probabilities: dict[str, float]
    treatment: str
    description: str
    severity: str
    organic_treatment: str
    features: dict
    image_stats: dict
    model_loaded: bool


class WeatherAdvice(BaseModel):
    temperature: float
    humidity: float
    condition: str
    irrigation_advice: str
    disease_risk: str
    recommendation: str


class CropInfo(BaseModel):
    name: str
    soil_type: str
    water_requirement: str
    growing_season: str
    common_diseases: list[str]


class DiseaseInfo(BaseModel):
    name: str
    display_name: str
    description: str
    symptoms: list[str]
    treatment: str
    organic_treatment: str
    severity: str
    favorable_conditions: str
    affected_crops: list[str]


class PesticideInfo(BaseModel):
    name: str
    chemical_name: str
    target_diseases: list[str]
    dosage_per_litre: str
    safety_interval_days: int
    toxicity_level: str
    organic_alternative: str


CROP_DB: dict[str, CropInfo] = {
    "rice": CropInfo(
        name="Rice",
        soil_type="Clay loam",
        water_requirement="High (flooded fields)",
        growing_season="Kharif (June-November)",
        common_diseases=["leaf_blight", "leaf_spot", "bacterial_blight", "wilt"],
    ),
    "wheat": CropInfo(
        name="Wheat",
        soil_type="Loam",
        water_requirement="Medium",
        growing_season="Rabi (October-March)",
        common_diseases=["rust", "powdery_mildew", "wilt"],
    ),
    "cotton": CropInfo(
        name="Cotton",
        soil_type="Black soil",
        water_requirement="Low-Medium",
        growing_season="Kharif (May-November)",
        common_diseases=["leaf_spot", "wilt", "root_rot", "anthracnose"],
    ),
    "tomato": CropInfo(
        name="Tomato",
        soil_type="Sandy loam",
        water_requirement="Medium",
        growing_season="Year-round",
        common_diseases=["leaf_blight", "leaf_spot", "wilt", "anthracnose"],
    ),
    "banana": CropInfo(
        name="Banana",
        soil_type="Loam",
        water_requirement="High",
        growing_season="Year-round",
        common_diseases=["leaf_blight", "leaf_spot", "wilt", "anthracnose"],
    ),
    "sugarcane": CropInfo(
        name="Sugarcane",
        soil_type="Clay loam",
        water_requirement="High",
        growing_season="Year-round (12-18 months)",
        common_diseases=["rust", "leaf_blight", "wilt", "red_rot"],
    ),
    "maize": CropInfo(
        name="Maize",
        soil_type="Sandy loam",
        water_requirement="Medium",
        growing_season="Kharif and Rabi",
        common_diseases=["leaf_blight", "rust", "wilt"],
    ),
    "groundnut": CropInfo(
        name="Groundnut",
        soil_type="Sandy loam",
        water_requirement="Low-Medium",
        growing_season="Kharif (June-October)",
        common_diseases=["leaf_spot", "rust", "wilt", "root_rot"],
    ),
    "mango": CropInfo(
        name="Mango",
        soil_type="Loam",
        water_requirement="Medium",
        common_diseases=["anthracnose", "powdery_mildew", "leaf_blight"],
        growing_season="Year-round (perennial)",
    ),
    "coconut": CropInfo(
        name="Coconut",
        soil_type="Sandy loam",
        water_requirement="Medium",
        common_diseases=["root_rot", "leaf_blight", "wilt"],
        growing_season="Year-round (perennial)",
    ),
    "chili": CropInfo(
        name="Chili",
        soil_type="Loam",
        water_requirement="Medium",
        growing_season="Year-round",
        common_diseases=["leaf_spot", "anthracnose", "powdery_mildew", "wilt"],
    ),
    "brinjal": CropInfo(
        name="Brinjal",
        soil_type="Sandy loam",
        water_requirement="Medium",
        growing_season="Year-round",
        common_diseases=["leaf_spot", "wilt", "root_rot"],
    ),
    "onion": CropInfo(
        name="Onion",
        soil_type="Sandy loam",
        water_requirement="Medium",
        growing_season="Rabi (October-March)",
        common_diseases=["leaf_blight", "downy_mildew", "rust"],
    ),
    "potato": CropInfo(
        name="Potato",
        soil_type="Sandy loam",
        water_requirement="Medium",
        growing_season="Rabi (October-March)",
        common_diseases=["late_blight", "early_blight", "leaf_spot", "wilt"],
    ),
    "soybean": CropInfo(
        name="Soybean",
        soil_type="Clay loam",
        water_requirement="Medium",
        growing_season="Kharif (June-October)",
        common_diseases=["rust", "leaf_spot", "powdery_mildew"],
    ),
    "turmeric": CropInfo(
        name="Turmeric",
        soil_type="Sandy loam",
        water_requirement="Medium",
        growing_season="Kharif (May-November)",
        common_diseases=["leaf_blight", "leaf_spot", "rhizome_rot"],
    ),
    "ginger": CropInfo(
        name="Ginger",
        soil_type="Sandy loam",
        water_requirement="Medium-High",
        growing_season="Kharif (April-October)",
        common_diseases=["leaf_blight", "rhizome_rot", "wilt"],
    ),
    "pigeon_pea": CropInfo(
        name="Pigeon Pea (Toor Dal)",
        soil_type="Loam",
        water_requirement="Low-Medium",
        growing_season="Kharif (June-November)",
        common_diseases=["wilt", "leaf_spot", "powdery_mildew"],
    ),
    "black_gram": CropInfo(
        name="Black Gram (Urad Dal)",
        soil_type="Loam",
        water_requirement="Low",
        growing_season="Kharif (June-September)",
        common_diseases=["leaf_spot", "powdery_mildew", "rust"],
    ),
    "green_gram": CropInfo(
        name="Green Gram (Moong Dal)",
        soil_type="Loam",
        water_requirement="Low",
        growing_season="Kharif (June-September)",
        common_diseases=["leaf_spot", "powdery_mildew", "rust"],
    ),
}


DISEASE_DB: dict[str, DiseaseInfo] = {
    "healthy": DiseaseInfo(
        name="healthy",
        display_name="Healthy",
        description="No disease detected. Plant appears healthy with normal green coloration and no visible lesions.",
        symptoms=["Normal green leaf color", "No visible spots or lesions", "Normal leaf texture"],
        treatment="Continue regular monitoring and good agricultural practices.",
        organic_treatment="No treatment needed. Use neem oil as preventive measure.",
        severity="none",
        favorable_conditions="Well-drained soil, proper spacing, adequate sunlight",
        affected_crops=["all"],
    ),
    "leaf_blight": DiseaseInfo(
        name="leaf_blight",
        display_name="Leaf Blight",
        description="Caused by fungal pathogens (Helminthosporium, Alternaria). Appears as brown to dark brown lesions with concentric rings on leaves. Spreads rapidly in humid conditions.",
        symptoms=["Brown to dark brown lesions", "Concentric rings on leaves", "Lesions expand and merge", "Leaf yellowing around lesions", "Premature leaf drop"],
        treatment="Apply copper-based fungicide (Bordeaux mixture). Remove and destroy infected leaves. Improve air circulation.",
        organic_treatment="Spray neem oil (5ml/L) or garlic extract. Apply compost tea to boost plant immunity.",
        severity="high",
        favorable_conditions="High humidity (above 70%), warm temperature (25-35 C), dense planting",
        affected_crops=["rice", "wheat", "maize", "tomato", "banana", "turmeric", "ginger"],
    ),
    "leaf_spot": DiseaseInfo(
        name="leaf_spot",
        display_name="Leaf Spot",
        description="Bacterial or fungal infection causing dark brown to black spots with yellow halos on leaves. Common in vegetables and field crops.",
        symptoms=["Dark brown to black spots", "Yellow halo around spots", "Spots may merge causing blighting", "Premature leaf drop"],
        treatment="Apply copper oxychloride fungicide. Avoid overhead watering. Use disease-resistant varieties.",
        organic_treatment="Spray baking soda solution (1 tsp/L with neem oil). Remove infected leaves and destroy them.",
        severity="medium",
        favorable_conditions="Wet foliage, high humidity, warm temperature, poor air circulation",
        affected_crops=["rice", "cotton", "tomato", "groundnut", "banana", "turmeric", "ginger"],
    ),
    "powdery_mildew": DiseaseInfo(
        name="powdery_mildew",
        display_name="Powdery Mildew",
        description="White powdery coating on leaf surfaces caused by fungal infection (Erysiphe, Sphaerotheca). Reduces photosynthesis and yield.",
        symptoms=["White powdery coating on leaves", "Leaf curling and distortion", "Stunted growth", "Yellowing of affected leaves"],
        treatment="Apply sulfur-based fungicide or tridemorph. Increase spacing between plants. Reduce humidity.",
        organic_treatment="Spray milk solution (1:9 milk to water ratio). Apply potassium bicarbonate solution.",
        severity="medium",
        favorable_conditions="Dry foliage with high humidity, warm days and cool nights, dense canopy",
        affected_crops=["wheat", "mango", "chili", "brinjal", "soybean", "pigeon_pea", "black_gram"],
    ),
    "root_rot": DiseaseInfo(
        name="root_rot",
        display_name="Root Rot",
        description="Fungal infection of roots (Fusarium, Pythium) causing wilting, yellowing, and root browning. Often fatal if not treated early.",
        symptoms=["Yellowing and wilting of leaves", "Brown and decayed roots", "Stunted growth", "Plant collapse in severe cases"],
        treatment="Improve field drainage. Apply Trichoderma viride to soil. Remove severely infected plants immediately.",
        organic_treatment="Apply Pseudomonas fluorescens to soil. Use mustard cake as soil amendment.",
        severity="high",
        favorable_conditions="Waterlogged soil, poor drainage, high soil moisture, warm temperature",
        affected_crops=["cotton", "brinjal", "groundnut", "coconut", "tomato"],
    ),
    "rust": DiseaseInfo(
        name="rust",
        display_name="Rust",
        description="Orange, yellow, or brown pustules on leaf surfaces caused by rust fungi (Puccinia species). Significantly reduces yield.",
        symptoms=["Orange or brown pustules on leaves", "Yellow spots on upper leaf surface", "Premature leaf drop", "Reduced plant vigor"],
        treatment="Apply triazole fungicide (propiconazole). Remove infected plant debris. Practice crop rotation.",
        organic_treatment="Spray sulfur dust or sulfur-based organic fungicide. Apply wood ash solution.",
        severity="high",
        favorable_conditions="High humidity, moderate temperature (15-25 C), heavy dew, dense planting",
        affected_crops=["wheat", "sugarcane", "groundnut", "maize", "soybean", "onion", "black_gram"],
    ),
    "wilt": DiseaseInfo(
        name="wilt",
        display_name="Wilt",
        description="Bacterial or fungal infection (Fusarium oxysporum, Ralstonia) causing sudden wilting and vascular discoloration. Often fatal.",
        symptoms=["Sudden wilting of leaves", "Vascular discoloration (brown streaks)", "Yellowing of lower leaves", "Plant death in severe cases"],
        treatment="Use resistant varieties. Solarize soil before planting. Apply biocontrol agents (Trichoderma, Pseudomonas).",
        organic_treatment="Apply Trichoderma harzianum as soil treatment. Use biogas slurry as soil amendment.",
        severity="high",
        favorable_conditions="Warm soil temperature (25-35 C), acidic soil, continuous cropping of susceptible varieties",
        affected_crops=["cotton", "tomato", "banana", "maize", "chili", "brinjal", "pigeon_pea", "ginger"],
    ),
    "bacterial_blight": DiseaseInfo(
        name="bacterial_blight",
        display_name="Bacterial Blight",
        description="Xanthomonas infection causing water-soaked lesions that turn brown/black with yellow margins. Common in rice.",
        symptoms=["Water-soaked lesions on leaf edges", "Lesions turn brown/black", "Yellow margins around lesions", "Wilting of young leaves"],
        treatment="Apply copper-based bactericide. Avoid working in wet fields. Use certified disease-free seeds.",
        organic_treatment="Apply copper oxychloride with streptomycin. Use botanical extracts from neem and turmeric.",
        severity="high",
        favorable_conditions="High humidity, warm temperature (25-35 C), rain splash, excessive nitrogen fertilization",
        affected_crops=["rice", "tomato", "chili"],
    ),
    "anthracnose": DiseaseInfo(
        name="anthracnose",
        display_name="Anthracnose",
        description="Fungal disease (Colletotrichum) causing dark sunken lesions on leaves, stems, and fruits. Affects many vegetable crops.",
        symptoms=["Dark sunken lesions on fruits and leaves", "Pinkish spore masses in lesions", "Leaf browning and drop", "Fruit rot"],
        treatment="Apply chlorothalonil or mancozeb fungicide. Remove infected plant parts. Maintain field sanitation.",
        organic_treatment="Spray copper-based organic fungicide. Apply Trichoderma-based biocontrol.",
        severity="high",
        favorable_conditions="Warm temperature (25-30 C), high humidity, rain splash, wounds on plant tissue",
        affected_crops=["cotton", "tomato", "banana", "chili", "mango", "groundnut"],
    ),
    "downy_mildew": DiseaseInfo(
        name="downy_mildew",
        display_name="Downy Mildew",
        description="Oomycete infection causing yellow patches on upper leaf surface and grayish growth on underside. Reduces photosynthesis.",
        symptoms=["Yellow angular patches on upper leaf surface", "Grayish fuzzy growth on lower leaf surface", "Leaf browning and death", "Stunted growth"],
        treatment="Apply metalaxyl or mancozeb fungicide. Ensure good drainage. Reduce canopy humidity.",
        organic_treatment="Spray copper hydroxide solution. Apply compost extract as foliar spray.",
        severity="medium",
        favorable_conditions="Cool nights with heavy dew, warm days (15-25 C), high humidity, poor air circulation",
        affected_crops=["onion", "ginger", "turmeric", "cucumber", "grape"],
    ),
}


PESTICIDE_DB: dict[str, PesticideInfo] = {
    "copper_oxychloride": PesticideInfo(
        name="Copper Oxychloride",
        chemical_name="Cu2(OH)3Cl",
        target_diseases=["leaf_blight", "leaf_spot", "bacterial_blight", "anthracnose", "downy_mildew"],
        dosage_per_litre="3g per litre of water",
        safety_interval_days=15,
        toxicity_level="low",
        organic_alternative="Neem oil solution (5ml/L)",
    ),
    "bordeaux_mixture": PesticideInfo(
        name="Bordeaux Mixture",
        chemical_name="CuSO4 + Ca(OH)2",
        target_diseases=["leaf_blight", "downy_mildew", "anthracnose"],
        dosage_per_litre="10g CuSO4 + 10g Ca(OH)2 per litre",
        safety_interval_days=20,
        toxicity_level="low",
        organic_alternative="Garlic and chili extract spray",
    ),
    "carbendazim": PesticideInfo(
        name="Carbendazim",
        chemical_name="Methyl benzimidazol-2-ylcarbamate",
        target_diseases=["leaf_blight", "powdery_mildew", "anthracnose", "wilt"],
        dosage_per_litre="1g per litre of water",
        safety_interval_days=21,
        toxicity_level="moderate",
        organic_alternative="Trichoderma viride soil application",
    ),
    "mancozeb": PesticideInfo(
        name="Mancozeb",
        chemical_name="Manganese ethylenebis(dithiocarbamate)",
        target_diseases=["leaf_spot", "downy_mildew", "rust", "anthracnose"],
        dosage_per_litre="2.5g per litre of water",
        safety_interval_days=15,
        toxicity_level="low",
        organic_alternative="Copper hydroxide spray",
    ),
    "propiconazole": PesticideInfo(
        name="Propiconazole",
        chemical_name="1-[[2-(2,4-dichlorophenyl)-4-propyl-1,3-dioxolan-2-yl]methyl]-1H-1,2,4-triazole",
        target_diseases=["rust", "powdery_mildew", "leaf_blight"],
        dosage_per_litre="1ml per litre of water",
        safety_interval_days=30,
        toxicity_level="moderate",
        organic_alternative="Sulfur-based dust",
    ),
    "chlorothalonil": PesticideInfo(
        name="Chlorothalonil",
        chemical_name="Tetrachloroisophthalonitrile",
        target_diseases=["anthracnose", "leaf_spot", "downy_mildew"],
        dosage_per_litre="2g per litre of water",
        safety_interval_days=14,
        toxicity_level="low",
        organic_alternative="Baking soda + neem oil solution",
    ),
    "trichoderma": PesticideInfo(
        name="Trichoderma viride (Biofungicide)",
        chemical_name="Trichoderma viride spores",
        target_diseases=["root_rot", "wilt", "leaf_blight"],
        dosage_per_litre="5g per litre of water (soil drenching)",
        safety_interval_days=0,
        toxicity_level="none",
        organic_alternative="Already organic. Use Pseudomonas fluorescens as alternative.",
    ),
    "neem_oil": PesticideInfo(
        name="Neem Oil (Azadirachtin)",
        chemical_name="Azadirachtin 0.03%",
        target_diseases=["leaf_spot", "powdery_mildew", "rust", "healthy"],
        dosage_per_litre="5ml per litre of water",
        safety_interval_days=0,
        toxicity_level="none",
        organic_alternative="Already organic. Can be combined with other botanicals.",
    ),
    "sulfur": PesticideInfo(
        name="Wettable Sulfur",
        chemical_name="Sulfur",
        target_diseases=["powdery_mildew", "rust", "leaf_spot"],
        dosage_per_litre="3g per litre of water",
        safety_interval_days=10,
        toxicity_level="low",
        organic_alternative="Already organic. Standard organic treatment for fungal diseases.",
    ),
    "metalaxyl": PesticideInfo(
        name="Metalaxyl",
        chemical_name="Methyl N-(methoxyacetyl)-N-(2,6-xylyl)-DL-alaninate",
        target_diseases=["downy_mildew", "root_rot"],
        dosage_per_litre="2g per litre of water",
        safety_interval_days=21,
        toxicity_level="moderate",
        organic_alternative="Copper hydroxide for downy mildew prevention",
    ),
}


DISEASE_LIFECYCLE: dict[str, dict] = {
    "leaf_blight": {
        "pathogen_type": "Fungal",
        "survival": "Crop debris, soil, infected seeds",
        "spread": "Wind, rain splash, irrigation water",
        "incubation_days": "4-7 days",
        "peak_season": "June-October (monsoon)",
        "stages": ["Initial infection on lower leaves", "Lesion expansion with concentric rings", "Spore production and spread", "Complete leaf blighting"],
    },
    "leaf_spot": {
        "pathogen_type": "Bacterial/Fungal",
        "survival": "Infected seeds, crop debris, soil",
        "spread": "Rain splash, wind, contaminated tools",
        "incubation_days": "3-5 days",
        "peak_season": "May-November",
        "stages": ["Small water-soaked spots appear", "Spots enlarge with yellow halos", "Spots turn brown/black", "Coalescence and blighting"],
    },
    "powdery_mildew": {
        "pathogen_type": "Fungal",
        "survival": "Infected plant debris, alternate hosts",
        "spread": "Wind-borne spores",
        "incubation_days": "3-7 days",
        "peak_season": "October-February (cool season)",
        "stages": ["White powdery spots appear", "Spots spread and merge", "Complete leaf coverage", "Leaf distortion and drop"],
    },
    "root_rot": {
        "pathogen_type": "Fungal",
        "survival": "Soil (survives for years), infected roots",
        "spread": "Soil water, tools, infected transplants",
        "incubation_days": "7-14 days",
        "peak_season": "Throughout growing season",
        "stages": ["Root tips turn brown", "Root decay progresses", "Vascular discoloration", "Above-ground wilting and death"],
    },
    "rust": {
        "pathogen_type": "Fungal",
        "survival": "Volunteer plants, crop debris, alternate hosts",
        "spread": "Wind-borne urediniospores",
        "incubation_days": "7-14 days",
        "peak_season": "November-February",
        "stages": ["Small yellow spots", "Orange/brown pustules form", "Pustules release spores", "Secondary infection cycles"],
    },
    "wilt": {
        "pathogen_type": "Fungal/Bacterial",
        "survival": "Soil, infected plant material, seeds",
        "spread": "Soil water, tools, infected transplants",
        "incubation_days": "5-10 days",
        "peak_season": "Throughout growing season",
        "stages": ["Vascular colonization", "Vessel blockage and wilting", "Yellowing of lower leaves", "Systemic collapse and death"],
    },
    "bacterial_blight": {
        "pathogen_type": "Bacterial",
        "survival": "Infected seeds, crop residue, irrigation water",
        "spread": "Rain splash, irrigation, wind-driven rain",
        "incubation_days": "3-5 days",
        "peak_season": "June-September",
        "stages": ["Water-soaked lesions on leaf tips", "Lesions extend along leaf margins", "Yellowing and wilting of leaves", "Kreef stage (complete wilting)"],
    },
    "anthracnose": {
        "pathogen_type": "Fungal",
        "survival": "Infected seeds, crop debris, soil",
        "spread": "Rain splash, wind, irrigation",
        "incubation_days": "4-7 days",
        "peak_season": "May-October",
        "stages": ["Small water-soaked lesions", "Dark sunken lesions form", "Pink spore masses in lesions", "Tissue death and fruit rot"],
    },
    "downy_mildew": {
        "pathogen_type": "Oomycete",
        "survival": "Oospores in soil, infected plant debris",
        "spread": "Wind, rain splash, irrigation",
        "incubation_days": "5-7 days",
        "peak_season": "October-February",
        "stages": ["Yellow patches on upper surface", "Grayish growth on lower surface", "Leaf browning", "Complete leaf death"],
    },
}


CROP_ROTATION_DB: dict[str, list[str]] = {
    "rice": ["black_gram", "green_gram", "groundnut", "sesame", "wheat"],
    "wheat": ["chickpea", "lentil", "mustard", "pea", "gram"],
    "cotton": ["black_gram", "green_gram", "groundnut", "maize", "wheat"],
    "tomato": ["cabbage", "cauliflower", "onion", "garlic", "beans"],
    "banana": ["pineapple", "turmeric", "ginger", "black_gram", "green_gram"],
    "sugarcane": ["black_gram", "green_gram", "chili", "tomato", "groundnut"],
    "maize": ["soybean", "groundnut", "black_gram", "sunhorse", "pigeon_pea"],
    "groundnut": ["maize", "sorghum", "cotton", "sunflower", "black_gram"],
    "chili": ["onion", "garlic", "tomato", "brinjal", "cabbage"],
    "brinjal": ["onion", "tomato", "okra", "chili", "beans"],
    "onion": ["carrot", "tomato", "beetroot", "cabbage", "lettuce"],
    "potato": ["maize", "beans", "cabbage", "onion", "garlic"],
    "soybean": ["wheat", "maize", "chickpea", "sorghum", "groundnut"],
    "turmeric": ["ginger", "black_gram", "green_gram", "maize", "chili"],
    "ginger": ["turmeric", "black_gram", "green_gram", "maize", "chili"],
    "pigeon_pea": ["black_gram", "green_gram", "groundnut", "sorghum", "wheat"],
    "black_gram": ["wheat", "rice", "mustard", "sunflower", "groundnut"],
    "green_gram": ["wheat", "rice", "mustard", "sunflower", "groundnut"],
}


MARKET_PRICE_DB: dict[str, dict[str, float]] = {
    "rice": {"msP_quintal": 2100, "modal_quintal": 2000, "unit": "quintal"},
    "wheat": {"msP_quintal": 2300, "modal_quintal": 2200, "unit": "quintal"},
    "cotton": {"msP_quintal": 6500, "modal_quintal": 6200, "unit": "quintal"},
    "tomato": {"msP_quintal": 1500, "modal_quintal": 1200, "unit": "quintal"},
    "banana": {"msP_quintal": 2500, "modal_quintal": 2200, "unit": "quintal"},
    "sugarcane": {"msP_quintal": 350, "modal_quintal": 310, "unit": "tonne"},
    "maize": {"msP_quintal": 2000, "modal_quintal": 1900, "unit": "quintal"},
    "groundnut": {"msP_quintal": 5500, "modal_quintal": 5200, "unit": "quintal"},
    "mango": {"msP_quintal": 4000, "modal_quintal": 3500, "unit": "quintal"},
    "coconut": {"msP_quintal": 3000, "modal_quintal": 2800, "unit": "quintal"},
    "chili": {"msP_quintal": 8000, "modal_quintal": 7500, "unit": "quintal"},
    "brinjal": {"msP_quintal": 2000, "modal_quintal": 1800, "unit": "quintal"},
    "onion": {"msP_quintal": 2500, "modal_quintal": 2200, "unit": "quintal"},
    "potato": {"msP_quintal": 1500, "modal_quintal": 1300, "unit": "quintal"},
    "soybean": {"msP_quintal": 4000, "modal_quintal": 3800, "unit": "quintal"},
    "turmeric": {"msP_quintal": 7000, "modal_quintal": 6500, "unit": "quintal"},
    "ginger": {"msP_quintal": 9000, "modal_quintal": 8500, "unit": "quintal"},
    "pigeon_pea": {"msP_quintal": 6000, "modal_quintal": 5500, "unit": "quintal"},
    "black_gram": {"msP_quintal": 6500, "modal_quintal": 6000, "unit": "quintal"},
    "green_gram": {"msP_quintal": 7000, "modal_quintal": 6500, "unit": "quintal"},
}


FERTILIZER_DB: dict[str, dict[str, dict[str, float]]] = {
    "rice": {
        "clay_loam": {"N_kg_per_acre": 40, "P_kg_per_acre": 20, "K_kg_per_acre": 20, "organic_matter_kg": 2000},
        "sandy_loam": {"N_kg_per_acre": 50, "P_kg_per_acre": 25, "K_kg_per_acre": 25, "organic_matter_kg": 2500},
        "loam": {"N_kg_per_acre": 45, "P_kg_per_acre": 22, "K_kg_per_acre": 22, "organic_matter_kg": 2200},
    },
    "wheat": {
        "clay_loam": {"N_kg_per_acre": 50, "P_kg_per_acre": 25, "K_kg_per_acre": 12, "organic_matter_kg": 1500},
        "sandy_loam": {"N_kg_per_acre": 60, "P_kg_per_acre": 30, "K_kg_per_acre": 15, "organic_matter_kg": 2000},
        "loam": {"N_kg_per_acre": 55, "P_kg_per_acre": 27, "K_kg_per_acre": 13, "organic_matter_kg": 1800},
    },
    "cotton": {
        "black_soil": {"N_kg_per_acre": 40, "P_kg_per_acre": 20, "K_kg_per_acre": 20, "organic_matter_kg": 2000},
        "sandy_loam": {"N_kg_per_acre": 50, "P_kg_per_acre": 25, "K_kg_per_acre": 25, "organic_matter_kg": 2500},
        "loam": {"N_kg_per_acre": 45, "P_kg_per_acre": 22, "K_kg_per_acre": 22, "organic_matter_kg": 2200},
    },
    "tomato": {
        "sandy_loam": {"N_kg_per_acre": 30, "P_kg_per_acre": 30, "K_kg_per_acre": 30, "organic_matter_kg": 3000},
        "loam": {"N_kg_per_acre": 35, "P_kg_per_acre": 30, "K_kg_per_acre": 35, "organic_matter_kg": 2500},
        "clay_loam": {"N_kg_per_acre": 40, "P_kg_per_acre": 35, "K_kg_per_acre": 40, "organic_matter_kg": 2000},
    },
    "banana": {
        "loam": {"N_kg_per_acre": 200, "P_kg_per_acre": 60, "K_kg_per_acre": 200, "organic_matter_kg": 5000},
        "sandy_loam": {"N_kg_per_acre": 220, "P_kg_per_acre": 70, "K_kg_per_acre": 220, "organic_matter_kg": 5500},
        "clay_loam": {"N_kg_per_acre": 180, "P_kg_per_acre": 55, "K_kg_per_acre": 180, "organic_matter_kg": 4500},
    },
    "sugarcane": {
        "clay_loam": {"N_kg_per_acre": 150, "P_kg_per_acre": 60, "K_kg_per_acre": 80, "organic_matter_kg": 5000},
        "sandy_loam": {"N_kg_per_acre": 170, "P_kg_per_acre": 70, "K_kg_per_acre": 90, "organic_matter_kg": 5500},
        "loam": {"N_kg_per_acre": 160, "P_kg_per_acre": 65, "K_kg_per_acre": 85, "organic_matter_kg": 5200},
    },
    "maize": {
        "sandy_loam": {"N_kg_per_acre": 60, "P_kg_per_acre": 30, "K_kg_per_acre": 30, "organic_matter_kg": 2500},
        "loam": {"N_kg_per_acre": 55, "P_kg_per_acre": 27, "K_kg_per_acre": 27, "organic_matter_kg": 2200},
        "clay_loam": {"N_kg_per_acre": 65, "P_kg_per_acre": 32, "K_kg_per_acre": 32, "organic_matter_kg": 2000},
    },
    "groundnut": {
        "sandy_loam": {"N_kg_per_acre": 15, "P_kg_per_acre": 30, "K_kg_per_acre": 25, "organic_matter_kg": 2000},
        "loam": {"N_kg_per_acre": 20, "P_kg_per_acre": 35, "K_kg_per_acre": 30, "organic_matter_kg": 2200},
    },
    "chili": {
        "sandy_loam": {"N_kg_per_acre": 40, "P_kg_per_acre": 40, "K_kg_per_acre": 40, "organic_matter_kg": 3000},
        "loam": {"N_kg_per_acre": 45, "P_kg_per_acre": 45, "K_kg_per_acre": 45, "organic_matter_kg": 2800},
    },
    "brinjal": {
        "sandy_loam": {"N_kg_per_acre": 40, "P_kg_per_acre": 35, "K_kg_per_acre": 40, "organic_matter_kg": 3000},
        "loam": {"N_kg_per_acre": 45, "P_kg_per_acre": 40, "K_kg_per_acre": 45, "organic_matter_kg": 2800},
    },
    "onion": {
        "sandy_loam": {"N_kg_per_acre": 35, "P_kg_per_acre": 35, "K_kg_per_acre": 35, "organic_matter_kg": 2500},
        "loam": {"N_kg_per_acre": 40, "P_kg_per_acre": 40, "K_kg_per_acre": 40, "organic_matter_kg": 2200},
    },
    "potato": {
        "sandy_loam": {"N_kg_per_acre": 60, "P_kg_per_acre": 40, "K_kg_per_acre": 60, "organic_matter_kg": 4000},
        "loam": {"N_kg_per_acre": 65, "P_kg_per_acre": 45, "K_kg_per_acre": 65, "organic_matter_kg": 3800},
    },
    "soybean": {
        "clay_loam": {"N_kg_per_acre": 10, "P_kg_per_acre": 40, "K_kg_per_acre": 20, "organic_matter_kg": 1500},
        "loam": {"N_kg_per_acre": 15, "P_kg_per_acre": 45, "K_kg_per_acre": 25, "organic_matter_kg": 1800},
    },
    "turmeric": {
        "sandy_loam": {"N_kg_per_acre": 30, "P_kg_per_acre": 30, "K_kg_per_acre": 50, "organic_matter_kg": 4000},
        "loam": {"N_kg_per_acre": 35, "P_kg_per_acre": 35, "K_kg_per_acre": 55, "organic_matter_kg": 3800},
    },
    "ginger": {
        "sandy_loam": {"N_kg_per_acre": 30, "P_kg_per_acre": 30, "K_kg_per_acre": 50, "organic_matter_kg": 4000},
        "loam": {"N_kg_per_acre": 35, "P_kg_per_acre": 35, "K_kg_per_acre": 55, "organic_matter_kg": 3800},
    },
    "pigeon_pea": {
        "loam": {"N_kg_per_acre": 15, "P_kg_per_acre": 30, "K_kg_per_acre": 15, "organic_matter_kg": 1500},
        "sandy_loam": {"N_kg_per_acre": 20, "P_kg_per_acre": 35, "K_kg_per_acre": 20, "organic_matter_kg": 1800},
    },
    "black_gram": {
        "loam": {"N_kg_per_acre": 10, "P_kg_per_acre": 25, "K_kg_per_acre": 12, "organic_matter_kg": 1200},
        "sandy_loam": {"N_kg_per_acre": 15, "P_kg_per_acre": 30, "K_kg_per_acre": 15, "organic_matter_kg": 1500},
    },
    "green_gram": {
        "loam": {"N_kg_per_acre": 10, "P_kg_per_acre": 25, "K_kg_per_acre": 12, "organic_matter_kg": 1200},
        "sandy_loam": {"N_kg_per_acre": 15, "P_kg_per_acre": 30, "K_kg_per_acre": 15, "organic_matter_kg": 1500},
    },
    "mango": {
        "loam": {"N_kg_per_acre": 500, "P_kg_per_acre": 250, "K_kg_per_acre": 500, "organic_matter_kg": 10000},
        "sandy_loam": {"N_kg_per_acre": 550, "P_kg_per_acre": 275, "K_kg_per_acre": 550, "organic_matter_kg": 12000},
    },
    "coconut": {
        "sandy_loam": {"N_kg_per_acre": 300, "P_kg_per_acre": 150, "K_kg_per_acre": 400, "organic_matter_kg": 8000},
        "loam": {"N_kg_per_acre": 350, "P_kg_per_acre": 175, "K_kg_per_acre": 450, "organic_matter_kg": 9000},
    },
}


FARMING_CALENDAR: dict[str, list[dict[str, str]]] = {
    "rice": [
        {"month": "June", "activity": "Nursery preparation and sowing", "priority": "high"},
        {"month": "July", "activity": "Transplanting and basal fertilizer application", "priority": "high"},
        {"month": "August", "activity": "Top dressing (urea) and weed management", "priority": "high"},
        {"month": "September", "activity": "Pest monitoring and disease surveillance", "priority": "medium"},
        {"month": "October", "activity": "Grain filling stage - monitor for blast disease", "priority": "high"},
        {"month": "November", "activity": "Harvesting and post-harvest processing", "priority": "high"},
    ],
    "wheat": [
        {"month": "October", "activity": "Field preparation and sowing", "priority": "high"},
        {"month": "November", "activity": "First irrigation and weed control", "priority": "high"},
        {"month": "December", "activity": "Top dressing and rust monitoring", "priority": "medium"},
        {"month": "January", "activity": "Second irrigation and disease surveillance", "priority": "high"},
        {"month": "February", "activity": "Grain filling - monitor for rust and blight", "priority": "high"},
        {"month": "March", "activity": "Harvesting and threshing", "priority": "high"},
    ],
    "cotton": [
        {"month": "May", "activity": "Field preparation and sowing", "priority": "high"},
        {"month": "June", "activity": "Thinning and intercultural operations", "priority": "medium"},
        {"month": "July", "activity": "Fertilizer application and pest monitoring", "priority": "high"},
        {"month": "August", "activity": "Boll formation stage - monitor for bollworm", "priority": "high"},
        {"month": "September", "activity": "Irrigation management and disease control", "priority": "high"},
        {"month": "October", "activity": "First picking and continue monitoring", "priority": "high"},
        {"month": "November", "activity": "Second picking and final harvest", "priority": "high"},
    ],
    "tomato": [
        {"month": "June", "activity": "Nursery preparation", "priority": "high"},
        {"month": "July", "activity": "Transplanting and staking", "priority": "high"},
        {"month": "August", "activity": "Fertilizer application and pruning", "priority": "medium"},
        {"month": "September", "activity": "Flowering and fruit setting stage", "priority": "high"},
        {"month": "October", "activity": "First harvest and continued care", "priority": "high"},
        {"month": "November", "activity": "Second harvest and disease monitoring", "priority": "medium"},
    ],
    "banana": [
        {"month": "April", "activity": "Pit planting and basal manure application", "priority": "high"},
        {"month": "May", "activity": "Regular irrigation and gap filling", "priority": "medium"},
        {"month": "June", "activity": "Fertilizer application (NPK)", "priority": "high"},
        {"month": "July", "activity": "Desuckering and propping", "priority": "medium"},
        {"month": "August", "activity": "Bunch emergence stage management", "priority": "high"},
        {"month": "September", "activity": "Bunch covering and pest monitoring", "priority": "high"},
        {"month": "October", "activity": "Harvesting of mature bunches", "priority": "high"},
    ],
    "chili": [
        {"month": "July", "activity": "Nursery preparation and sowing", "priority": "high"},
        {"month": "August", "activity": "Transplanting and irrigation setup", "priority": "high"},
        {"month": "September", "activity": "Fertilizer application and weeding", "priority": "medium"},
        {"month": "October", "activity": "Flowering and fruit setting - monitor for anthracnose", "priority": "high"},
        {"month": "November", "activity": "First harvest and continued care", "priority": "high"},
        {"month": "December", "activity": "Second harvest and pest control", "priority": "medium"},
    ],
    "onion": [
        {"month": "October", "activity": "Field preparation and nursery sowing", "priority": "high"},
        {"month": "November", "activity": "Transplanting and basal fertilizer", "priority": "high"},
        {"month": "December", "activity": "Irrigation and weed management", "priority": "medium"},
        {"month": "January", "activity": "Bulb formation stage - monitor for downy mildew", "priority": "high"},
        {"month": "February", "activity": "Top dressing and disease control", "priority": "high"},
        {"month": "March", "activity": "Harvesting and curing", "priority": "high"},
    ],
    "potato": [
        {"month": "October", "activity": "Field preparation and seed treatment", "priority": "high"},
        {"month": "November", "activity": "Planting and irrigation setup", "priority": "high"},
        {"month": "December", "activity": "Earthing up and fertilizer application", "priority": "high"},
        {"month": "January", "activity": "Tuber formation - monitor for late blight", "priority": "high"},
        {"month": "February", "activity": "Irrigation and disease management", "priority": "high"},
        {"month": "March", "activity": "Harvesting and storage", "priority": "high"},
    ],
    "soybean": [
        {"month": "June", "activity": "Field preparation and sowing", "priority": "high"},
        {"month": "July", "activity": "Thinning and weed management", "priority": "medium"},
        {"month": "August", "activity": "Fertilizer and pest management", "priority": "high"},
        {"month": "September", "activity": "Pod formation - monitor for rust", "priority": "high"},
        {"month": "October", "activity": "Grain filling and harvest preparation", "priority": "high"},
    ],
}


PEST_LIFECYCLE_DB: dict[str, dict] = {
    "aphid": {
        "scientific_name": "Aphidoidea",
        "crops_affected": ["cotton", "chili", "brinjal", "tomato", "potato"],
        "life_cycle_days": "7-14 days",
        "reproduction": "Parthenogenesis (live birth)",
        "peak_activity": "Cool season (October-February)",
        "damage_type": "Sucking pest - causes leaf curling and virus transmission",
        "control_measures": ["Yellow sticky traps", "Neem oil spray", "Release ladybird beetles", "Imidacloprid (chemical)"],
        "economic_threshold": "20 aphids per leaf",
    },
    "bollworm": {
        "scientific_name": "Helicoverpa armigera",
        "crops_affected": ["cotton", "tomato", "chili", "pigeon_pea", "maize"],
        "life_cycle_days": "25-35 days",
        "reproduction": "Egg laying on leaves and flowers",
        "peak_activity": "October-December",
        "damage_type": "Chewing pest - damages bolls, fruits, and pods",
        "control_measures": ["Pheromone traps", "Release Trichogramma wasps", "NPV virus spray", "Emamectin benzoate"],
        "economic_threshold": "5% damaged fruits",
    },
    "whitefly": {
        "scientific_name": "Bemisia tabaci",
        "crops_affected": ["cotton", "tomato", "chili", "brinjal", "onion"],
        "life_cycle_days": "15-30 days",
        "reproduction": "Egg laying on leaf undersides",
        "peak_activity": "Warm dry season (March-June)",
        "damage_type": "Sucking pest - causes yellowing and virus transmission",
        "control_measures": ["Yellow sticky traps", "Neem oil spray", "Release Encarsia wasps", "Insecticidal soaps"],
        "economic_threshold": "5 whiteflies per leaf",
    },
    "stem_borer": {
        "scientific_name": "Scirpophaga incertulas",
        "crops_affected": ["rice", "sugarcane", "maize"],
        "life_cycle_days": "30-50 days",
        "reproduction": "Egg masses on leaf surfaces",
        "peak_activity": "July-September (monsoon)",
        "damage_type": "Boring pest - causes dead heart and white ear",
        "control_measures": ["Light traps", "Release Trichogramma", "Remove affected tillers", "Cartap hydrochloride"],
        "economic_threshold": "5% dead hearts",
    },
    "fruit_borer": {
        "scientific_name": "Leucinodes orbonalis",
        "crops_affected": ["brinjal", "tomato", "chili"],
        "life_cycle_days": "20-30 days",
        "reproduction": "Egg laying on leaves and stems",
        "peak_activity": "Year-round in warm climate",
        "damage_type": "Boring pest - damages fruits and shoots",
        "control_measures": ["Remove affected fruits", "Pheromone traps", "B.t. spray", "Spinosad"],
        "economic_threshold": "10% damaged fruits",
    },
    "red_spider_mite": {
        "scientific_name": "Tetranychus urticae",
        "crops_affected": ["cotton", "tomato", "chili", "brinjal", "groundnut"],
        "life_cycle_days": "7-10 days",
        "reproduction": "Egg laying on leaf undersides",
        "peak_activity": "Dry season (February-May)",
        "damage_type": "Sucking pest - causes bronzing and webbing",
        "control_measures": ["Spray water to increase humidity", "Release predatory mites", "Sulfur-based spray", "Abamectin"],
        "economic_threshold": "5 mites per leaf",
    },
    "leaf_folder": {
        "scientific_name": "Cnaphalocrocis medinalis",
        "crops_affected": ["rice"],
        "life_cycle_days": "20-30 days",
        "reproduction": "Egg laying on leaf surfaces",
        "peak_activity": "July-September",
        "damage_type": "Leaf folding and scraping",
        "control_measures": ["Remove folded leaves", "Release Trichogramma", "Light traps", "Chlorantraniliprole"],
        "economic_threshold": "5% folded leaves",
    },
    "thrips": {
        "scientific_name": "Thysanoptera",
        "crops_affected": ["cotton", "onion", "chili", "tomato", "groundnut"],
        "life_cycle_days": "10-20 days",
        "reproduction": "Egg laying in plant tissue",
        "peak_activity": "Dry warm season (March-June)",
        "damage_type": "Scraping pest - causes silver streaks and distorted growth",
        "control_measures": ["Blue sticky traps", "Neem oil spray", "Release predatory bugs", "Spinosad"],
        "economic_threshold": "10 thrips per plant",
    },
}


def get_crop_info(crop_name: str) -> CropInfo | None:
    return CROP_DB.get(crop_name.lower())


def get_disease_info(disease_name: str) -> DiseaseInfo | None:
    return DISEASE_DB.get(disease_name.lower())


def get_pesticide_info(pesticide_name: str) -> PesticideInfo | None:
    return PESTICIDE_DB.get(pesticide_name.lower())


def get_disease_lifecycle(disease_name: str) -> dict | None:
    return DISEASE_LIFECYCLE.get(disease_name.lower())


def get_rotation_recommendations(current_crop: str) -> list[str]:
    return CROP_ROTATION_DB.get(current_crop.lower(), [])


def get_market_price(crop_name: str) -> dict | None:
    return MARKET_PRICE_DB.get(crop_name.lower())


def get_fertilizer_recommendation(crop_name: str, soil_type: str) -> dict | None:
    crop_data = FERTILIZER_DB.get(crop_name.lower())
    if not crop_data:
        return None
    return crop_data.get(soil_type.lower().replace(" ", "_"), crop_data.get("loam"))


def get_farming_calendar(crop_name: str) -> list[dict[str, str]]:
    return FARMING_CALENDAR.get(crop_name.lower(), [])


def get_all_crops() -> list[CropInfo]:
    return list(CROP_DB.values())


def get_all_diseases() -> list[DiseaseInfo]:
    return list(DISEASE_DB.values())


def get_all_pesticides() -> list[PesticideInfo]:
    return list(PESTICIDE_DB.values())


def search_diseases_by_crop(crop_name: str) -> list[DiseaseInfo]:
    crop = CROP_DB.get(crop_name.lower())
    if not crop:
        return []
    result = []
    for disease_name in crop.common_diseases:
        disease = DISEASE_DB.get(disease_name)
        if disease:
            result.append(disease)
    return result
