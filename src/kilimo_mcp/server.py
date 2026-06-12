"""KilimoMCP — Kenya Precision Agriculture Tools (6 tools). All data DEMO."""
from __future__ import annotations
from typing import Optional
from fastmcp import FastMCP
mcp = FastMCP(name="kilimo-mcp", description="Kenya precision agriculture tools. DEMO data only.")

CALENDARS = {
    "maize": {
        "highland": {"plant": "Mar-Apr (long rains), Oct-Nov (short rains)", "harvest": "Jul-Aug, Feb-Mar", "days_to_maturity": "90-120"},
        "lowland":  {"plant": "Mar-Apr", "harvest": "Jul-Aug", "days_to_maturity": "80-90"},
    },
    "beans":   {"highland": {"plant": "Mar-Apr, Oct-Nov", "harvest": "Jun-Jul, Jan-Feb", "days_to_maturity": "60-90"}},
    "tea":     {"highland": {"plant": "Any season (perennial)", "harvest": "Year-round (peak Apr-Jun, Oct-Dec)", "days_to_maturity": "3 years to full production"}},
    "coffee":  {"highland": {"plant": "Apr-Jun", "harvest": "Oct-Jan (main), Mar-May (fly)", "days_to_maturity": "3-4 years to production"}},
    "potato":  {"highland": {"plant": "Mar-Apr, Sep-Oct", "harvest": "Jun-Jul, Jan-Feb", "days_to_maturity": "90-100"}},
    "tomato":  {"highland": {"plant": "Any season with irrigation", "harvest": "60-80 days after transplant", "days_to_maturity": "60-80"}},
    "sukuma_wiki": {"all": {"plant": "Any season", "harvest": "6 weeks after planting (continuous)", "days_to_maturity": "42"}},
}

@mcp.tool(name="crop_calendar", description="Kenya crop planting and harvesting calendar by region. DEMO.")
def crop_calendar(crop: str, region: Optional[str] = "highland") -> dict:
    c = crop.lower().replace(" ","_")
    data = CALENDARS.get(c, {})
    r_data = data.get(region.lower() if region else "highland") or data.get("all") or {"note": "Crop not in sample dataset"}
    return {"source": "DEMO — KALRO and Ministry of Agriculture", "crop": crop, "region": region,
            **r_data, "long_rains": "March–May (main planting)", "short_rains": "October–December",
            "kalro": "kalro.org for official crop recommendations"}

@mcp.tool(name="fertilizer_guide", description="Fertilizer recommendations by Kenya crop and soil type. DEMO.")
def fertilizer_guide(crop: str, soil_type: Optional[str] = "medium") -> dict:
    GUIDE = {
        "maize":  {"basal": "DAP 50kg/acre at planting", "top_dress": "CAN 50kg/acre 6 weeks after planting",
                   "organic": "2–3 tons/acre well-composted manure before planting"},
        "beans":  {"basal": "DAP 25kg/acre (beans fix nitrogen)", "top_dress": "None usually needed",
                   "organic": "Compost improves yield significantly"},
        "tomato": {"basal": "NPK 17:17:17 at 50kg/acre", "top_dress": "CAN 25kg/acre weekly foliar",
                   "organic": "Heavy manure user — 5 tons/acre recommended"},
        "potato": {"basal": "DSP or NPK 23:23:0 at 200kg/acre", "top_dress": "CAN 50kg/acre at 6 weeks",
                   "organic": "Potato responds well to manure + inorganic combo"},
    }
    c = crop.lower()
    rec = GUIDE.get(c, {"general": "Apply DAP at planting, CAN at 6 weeks. Get soil test from KARI/KALRO lab."})
    return {"source": "DEMO — KALRO Fertilizer Use Recommendations", "crop": crop, "soil_type": soil_type,
            **rec, "soil_test": "Get soil test at KALRO soil lab: kalro.org (costs ~KES 1,000/sample)",
            "subsidy": "Kenya fertilizer subsidy scheme: check county agriculture office"}

@mcp.tool(name="pest_disease_alert", description="Kenya crop pest and disease management guide. DEMO.")
def pest_disease_alert(crop: str, symptom: Optional[str] = None) -> dict:
    PESTS = {
        "maize": [{"name": "Fall Armyworm", "symptom": "Ragged holes in leaves, frass in whorls",
                   "management": "Emamectin benzoate or chlorpyrifos. Early morning application. Report to county pest control."},
                  {"name": "Maize Lethal Necrosis", "symptom": "Yellow streaking, premature drying",
                   "management": "No cure. Remove and destroy affected plants. Use certified seed."}],
        "tomato": [{"name": "Late Blight", "symptom": "Brown lesions on leaves and fruit",
                    "management": "Mancozeb or metalaxyl fungicide. Remove affected leaves."},
                   {"name": "Tuta absoluta", "symptom": "Mines in leaves, bored fruit",
                    "management": "Pheromone traps, spinosad, cyantraniliprole"}],
        "beans":  [{"name": "Bean fly", "symptom": "Yellowing, wilting seedlings",
                    "management": "Seed treatment with thiamethoxam. Early planting."},
                   {"name": "Angular leaf spot", "symptom": "Brown angular lesions",
                    "management": "Copper-based fungicide. Use resistant varieties."}],
    }
    c = crop.lower()
    pests = PESTS.get(c, [{"name": "General", "symptom": "Multiple", "management": "Consult county extension officer"}])
    if symptom:
        pests = [p for p in pests if symptom.lower() in p["symptom"].lower()] or pests
    return {"source": "DEMO — KEPHIS and county extension services", "crop": crop,
            "common_pests_diseases": pests, "emergency": "Pest outbreak: call KEPHIS 020-3597481",
            "fall_armyworm_hotline": "0800720553 (Kenya FAO FAW reporting)"}

@mcp.tool(name="market_timing_guide", description="Best timing to sell Kenya produce based on price cycles. DEMO.")
def market_timing_guide(commodity: str, county: Optional[str] = None) -> dict:
    TIMING = {
        "maize":    {"best_sell_months": ["Aug","Sep","Oct","Feb","Mar"],
                     "low_price_months": ["May","Jun"] ,
                     "tip": "Store 2-3 months after harvest to capture price recovery. Avoid selling in Jun-Jul (harvest glut)."},
        "tomatoes": {"best_sell_months": ["Jan","Feb","Jul","Aug"],
                     "low_price_months": ["Apr","May","Oct","Nov"],
                     "tip": "Seasonal gluts in Apr-May (long rains) and Oct-Nov (short rains). Consider processing to paste."},
        "beans":    {"best_sell_months": ["Sep","Oct","Mar","Apr"],
                     "low_price_months": ["Jul","Aug","Jan"],
                     "tip": "Dry beans store well — hold 1-2 months after harvest for 20-40% price premium."},
    }
    c = commodity.lower()
    timing = TIMING.get(c, {"tip": "Monitor WFP Kenya market prices at vam.wfp.org"})
    return {"source": "DEMO — WFP VAM Kenya Market Monitor", "commodity": commodity, "county": county,
            **timing, "real_time_prices": "vam.wfp.org | soko-mcp for current market prices"}

@mcp.tool(name="kalro_varieties", description="KALRO improved crop variety recommendations for Kenya. DEMO.")
def kalro_varieties(crop: str, condition: Optional[str] = None) -> dict:
    VARIETIES = {
        "maize": [
            {"variety": "H614D", "days": 120, "condition": "highland, 1500-2100m", "yield": "30-40 bags/acre"},
            {"variety": "DK8031", "days": 90, "condition": "lowland, drought-tolerant", "yield": "20-30 bags/acre"},
            {"variety": "WEMA (drought-tolerant)", "days": 85, "condition": "ASAL, drought stress", "yield": "15-25 bags/acre"},
        ],
        "beans": [
            {"variety": "Fahari", "days": 65, "condition": "highland, root rot resistant", "yield": "600-800kg/acre"},
            {"variety": "Lyamungu 85", "days": 75, "condition": "medium altitude", "yield": "500-700kg/acre"},
        ],
        "potato": [
            {"variety": "Dutch Robjin", "days": 90, "condition": "highland, all-purpose", "yield": "8-12 tons/acre"},
            {"variety": "Shangi", "days": 90, "condition": "highland, late blight resistant", "yield": "10-15 tons/acre"},
        ],
    }
    c = crop.lower()
    varieties = VARIETIES.get(c, [{"note": f"Varieties for {crop} not in sample dataset — visit kalro.org"}])
    if condition:
        filtered = [v for v in varieties if condition.lower() in v.get("condition","").lower()]
        varieties = filtered or varieties
    return {"source": "DEMO — KALRO Kenya", "crop": crop, "condition": condition,
            "recommended_varieties": varieties, "certified_seed": "Obtain from KEPHIS-registered agrodealers",
            "kalro": "kalro.org | 0722206986"}

@mcp.tool(name="input_cost_calculator", description="Kenya farm input cost calculator and comparison. DEMO.")
def input_cost_calculator(crop: str, acreage: float = 1.0) -> dict:
    COSTS = {
        "maize":  {"seed_kg": 10, "seed_cost": 600, "dap_kg": 50, "dap_cost": 5500,
                   "can_kg": 50, "can_cost": 4500, "labour_kes": 8000, "other_kes": 2000},
        "tomato": {"seedlings": 2000, "seedling_cost": 4000, "fertilizer_kes": 12000,
                   "pesticides_kes": 8000, "irrigation_kes": 5000, "labour_kes": 15000},
        "beans":  {"seed_kg": 20, "seed_cost": 3000, "dap_kg": 25, "dap_cost": 2750,
                   "pesticide_kes": 2000, "labour_kes": 5000},
    }
    c = crop.lower()
    base = COSTS.get(c, {"note": "Crop not in sample — estimate KES 30,000-80,000/acre for most crops"})
    total = sum(v for k, v in base.items() if k.endswith("_kes") or k.endswith("_cost"))
    total_scaled = round(total * acreage, 0)
    return {"source": "DEMO — Kenya agrovet prices indicative 2025", "crop": crop, "acreage": acreage,
            "input_costs_per_acre_kes": base, "estimated_total_kes": total_scaled,
            "subsidy": "Fertilizer subsidy may reduce DAP/CAN costs — check county agriculture office",
            "disclaimer": "Prices vary by region and season. Get current quotes from your local agrodealer."}
