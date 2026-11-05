"""KilimoMCP — Kenya Precision Agriculture Tools (6 tools). All data DEMO."""
from __future__ import annotations

import base64
import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import UTC, datetime, timedelta
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _pkg_version
from typing import Annotated, Optional

from fastmcp import FastMCP
from pydantic import Field

# Annotations tell clients which tools are safe to auto-approve (read-only, no side effects).
READ_ONLY = {"readOnlyHint": True, "idempotentHint": True, "openWorldHint": False}

try:
    _VERSION = _pkg_version("kilimo-mcp")
except PackageNotFoundError:  # a source tree that was never installed
    _VERSION = "0+unknown"


mcp = FastMCP(name="kilimo-mcp", instructions="Kenya precision agriculture tools. DEMO data only.", version=_VERSION)

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

@mcp.tool(name="crop_calendar", description="Planting calendar for a Kenyan crop by region, with the long and short rains seasons. Use when a farmer asks when to plant or harvest. Looks the crop up in a small sample table (spaces become underscores) and the region (default highland, falling back to an all-regions entry); a crop not in the table returns the note 'Crop not in sample dataset' with only the season dates. Returns the source label, crop, region, the calendar entry, long and short rains dates and a KALRO pointer. Sample data labelled DEMO: confirm with KALRO or the county agriculture office. Read-only; no side effects.", annotations=READ_ONLY)
def crop_calendar(crop: Annotated[str, Field(description="Crop name such as maize or beans; spaces become underscores.")], region: Annotated[str | None, Field(description="Region such as highland (default); falls back to an all-regions entry.")] = "highland") -> dict:
    c = crop.lower().replace(" ","_")
    data = CALENDARS.get(c, {})
    r_data = data.get(region.lower() if region else "highland") or data.get("all") or {"note": "Crop not in sample dataset"}
    return {"source": "DEMO — KALRO and Ministry of Agriculture", "crop": crop, "region": region,
            **r_data, "long_rains": "March–May (main planting)", "short_rains": "October–December",
            "kalro": "kalro.org for official crop recommendations"}

@mcp.tool(name="fertilizer_guide", description="Fertilizer recommendation for a crop: basal, top-dressing and organic options per acre. Use when a farmer asks what fertilizer to apply. Crops in the sample table get specific advice; any other crop gets a general note (DAP at planting, CAN at six weeks). soil_type is only echoed back. Returns the source label, crop, soil_type, the recommendation, a soil-test pointer (about KES 1,000 per sample) and a note on the fertilizer subsidy. Sample guidance labelled DEMO: confirm with a soil test and KALRO. Read-only; no side effects.", annotations=READ_ONLY)
def fertilizer_guide(crop: Annotated[str, Field(description="Crop name such as maize, beans or tomato.")], soil_type: Annotated[str | None, Field(description="Soil type; only echoed back (default medium).")] = "medium") -> dict:
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

@mcp.tool(name="pest_disease_alert", description="Common pests and diseases of a crop with their symptoms and management. Use when a farmer describes damage and asks what it might be. symptom filters the sample list by matching text; if nothing matches, ALL the crop's entries are returned. Returns the source label, crop, the pests or diseases, an emergency KEPHIS number and the fall armyworm reporting line. Sample data labelled DEMO and not a diagnosis: confirm with a county extension officer or KEPHIS. Read-only; no side effects.", annotations=READ_ONLY)
def pest_disease_alert(crop: Annotated[str, Field(description="Crop name such as maize or tomato.")], symptom: Annotated[str | None, Field(description="Optional symptom text to filter by, such as holes in leaves.")] = None) -> dict:
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

@mcp.tool(name="market_timing_guide", description="Best and worst months to sell a commodity, with a storage tip. Use when a farmer asks when to sell. Only commodities in the sample table (such as maize and tomatoes) have month lists; any other returns a pointer to WFP market monitoring. county is only echoed back. Returns the source label, commodity, county, the timing entry and pointers to vam.wfp.org and soko-mcp for current prices. Seasonal patterns labelled DEMO, not price forecasts. Read-only; no side effects.", annotations=READ_ONLY)
def market_timing_guide(commodity: Annotated[str, Field(description="Commodity such as maize or tomatoes.")], county: Annotated[str | None, Field(description="Optional county; only echoed back.")] = None) -> dict:
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

@mcp.tool(name="kalro_varieties", description="Recommended KALRO varieties for a crop and growing condition, with days to maturity, suited conditions and typical yield. Use when a farmer asks which variety to plant. condition filters by matching text; if nothing matches, ALL varieties for the crop are returned. Returns the source label, crop, condition, recommended_varieties, certified-seed advice (KEPHIS-registered agrodealers) and a KALRO contact. Sample data labelled DEMO: confirm with KALRO. Read-only; no side effects.", annotations=READ_ONLY)
def kalro_varieties(crop: Annotated[str, Field(description="Crop name such as maize.")], condition: Annotated[str | None, Field(description="Optional growing condition to filter by, such as highland or drought.")] = None) -> dict:
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

@mcp.tool(name="input_cost_calculator", description="Estimate the cost of growing a crop in KES per acre and in total for an acreage: seed, fertilizer, labour and other items. Use when a farmer is budgeting a season. Only crops in the sample table are costed; for any other crop the per-acre entry is a note and estimated_total_kes is null, never zero. Returns the source label, crop, acreage, input_costs_per_acre_kes, estimated_total_kes, a subsidy note and a prices disclaimer. Indicative 2025 agrovet prices labelled DEMO: get quotes from a local agrodealer. Read-only; no side effects.", annotations=READ_ONLY)
def input_cost_calculator(crop: Annotated[str, Field(description="Crop name such as maize, tomato or beans.")], acreage: Annotated[float, Field(description="Number of acres (default 1.0); the per-acre cost is multiplied by it.")] = 1.0) -> dict:
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
    total = sum(v for k, v in base.items() if k.endswith(("_kes", "_cost")))
    total_scaled = round(total * acreage, 0)
    return {"source": "DEMO — Kenya agrovet prices indicative 2025", "crop": crop, "acreage": acreage,
            "input_costs_per_acre_kes": base, "estimated_total_kes": total_scaled if "note" not in base else None,
            "subsidy": "Fertilizer subsidy may reduce DAP/CAN costs — check county agriculture office",
            "disclaimer": "Prices vary by region and season. Get current quotes from your local agrodealer."}


# ── Live data (free public services) ─────────────────────────────────
# Live tools change nothing anywhere, but they contact an outside service, and clients should know that.
LIVE_READ_ONLY = {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True}
LIVE_TOOLS = {"rainfall_forecast", "food_market_prices"}
_LIVE_UA = {"User-Agent": "kilimo-mcp (https://github.com/gabrielmahia/kilimo-mcp)", "Accept": "application/json"}
_LIVE_ERRORS = (urllib.error.URLError, TimeoutError, ValueError, KeyError, TypeError, IndexError)


def _live_get(url: str, params: dict | None = None, timeout: float = 20.0):
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=_LIVE_UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:  # fixed https endpoints only
        return json.loads(r.read().decode("utf-8"))


def _live_meta(source: str, attribution: str) -> dict:
    return {"source": source, "attribution": attribution, "retrieved_at": datetime.now(UTC).isoformat(timespec="seconds")}

@mcp.tool(name="rainfall_forecast", annotations=LIVE_READ_ONLY, description="Get the daily rainfall forecast for a location in Kenya (or anywhere) for up to 16 days, from the free Open-Meteo weather service: expected millimetres and the chance of rain each day. Use when someone is planning planting, irrigation, water storage, travel or flood preparation and needs the rain outlook for a place. Returns one row per day with rain in mm and the maximum chance of rain in percent, the total, the source, its attribution and the retrieval time; on a network or service failure it returns an error instead of a forecast. Read-only; contacts an external service.")
def rainfall_forecast(latitude: Annotated[float, Field(description="Latitude in decimal degrees, for example -1.29 for Nairobi or -0.09 for Kisumu; between -90 and 90.")],
                      longitude: Annotated[float, Field(description="Longitude in decimal degrees, for example 36.82 for Nairobi; between -180 and 180.")],
                      days: Annotated[int, Field(description="How many days ahead to forecast, between 1 and 16.")] = 7) -> dict:
    meta = _live_meta("LIVE — Open-Meteo weather forecast API (api.open-meteo.com)", "Weather data by Open-Meteo.com, CC BY 4.0. The free API is for non-commercial use.")
    if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
        return {"error": "latitude must be between -90 and 90 and longitude between -180 and 180", **meta}
    if not 1 <= days <= 16:
        return {"error": "days must be between 1 and 16", **meta}
    try:
        d = _live_get("https://api.open-meteo.com/v1/forecast", {"latitude": latitude, "longitude": longitude, "daily": "precipitation_sum,precipitation_probability_max", "forecast_days": days, "timezone": "Africa/Nairobi"})
        daily = d["daily"]
        rows = [{"date": t, "rain_mm": r, "chance_pct": p} for t, r, p in zip(daily["time"], daily["precipitation_sum"], daily["precipitation_probability_max"], strict=True)]
        if not rows:
            raise ValueError("empty forecast")
    except _LIVE_ERRORS as e:
        return {"error": f"Open-Meteo did not return a usable forecast ({type(e).__name__}); no forecast is given without it. Try again later.", **meta}
    return {"latitude": latitude, "longitude": longitude, "days": rows, "total_rain_mm": round(sum(r["rain_mm"] or 0 for r in rows), 1),
            "note": "A model forecast: confidence falls with each day ahead, and local storms can differ from the grid forecast.", **meta}

@mcp.tool(name="food_market_prices", annotations=LIVE_READ_ONLY, description="Get recent food prices in Kenyan markets for a commodity (for example maize, beans, rice, sorghum, milk or sugar), from the World Food Programme's market monitoring, served by the free Humanitarian Data Exchange API (HDX HAPI). Use when someone is deciding when or where to buy or sell, checking whether a price is fair, or tracking food costs in a county. Returns the latest price per market and unit with its date, the source, its licence and the retrieval time; on a network or service failure it returns an error instead of prices. Read-only; contacts an external service.")
def food_market_prices(commodity: Annotated[str, Field(description="Commodity name or part of it, for example maize, beans, rice, sorghum, milk or sugar.")],
                       county: Annotated[str | None, Field(description="Optional county name to filter on, for example Turkana or Marsabit (WFP monitors mainly arid and semi-arid counties).")] = None,
                       months: Annotated[int, Field(description="How far back to look for the latest prices, in months, between 1 and 60.")] = 12) -> dict:
    meta = _live_meta("LIVE — WFP market monitor via HDX HAPI (hapi.humdata.org)", "World Food Programme price data via the Humanitarian Data Exchange (HDX HAPI); WFP data licensed CC BY-IGO.")
    name = (commodity or "").strip()
    if not 1 <= len(name) <= 60:
        return {"error": "commodity must be between 1 and 60 characters", **meta}
    if not 1 <= months <= 60:
        return {"error": "months must be between 1 and 60", **meta}
    since = (datetime.now(UTC) - timedelta(days=31 * months)).date().isoformat()
    params = {"location_code": "KEN", "commodity_name": name, "reference_period_start_min": since, "limit": 1000, "output_format": "json",
              "app_identifier": base64.b64encode(b"kilimo-mcp:contact@aikungfu.dev").decode()}
    if county:
        params["admin1_name"] = county.strip()
    try:
        data = _live_get("https://hapi.humdata.org/api/v2/food-security-nutrition-poverty/food-prices-market-monitor", params)["data"]
    except _LIVE_ERRORS as e:
        return {"error": f"HDX HAPI did not return usable prices ({type(e).__name__}); no prices are given without it. Try again later.", **meta}
    latest = {}
    for row in data:
        key = (row.get("market_name"), row.get("commodity_name"), row.get("unit"), row.get("price_type"))
        if key not in latest or row["reference_period_start"] > latest[key]["reference_period_start"]:
            latest[key] = row
    out = sorted(latest.values(), key=lambda r: r["reference_period_start"], reverse=True)[:25]
    prices = [{"market": r.get("market_name"), "county": r.get("admin1_name"), "commodity": r.get("commodity_name"), "unit": r.get("unit"), "price": r.get("price"),
               "currency": r.get("currency_code"), "price_type": r.get("price_type"), "date": (r.get("reference_period_start") or "")[:10]} for r in out]
    return {"commodity": name, "county": county, "since": since, "prices": prices, "count": len(prices),
            "note": "WFP monitors selected markets, mostly in arid and semi-arid counties; an empty list means no observation in that window, not that the item is unavailable.", **meta}


def main() -> None:
    """Console entry point."""
    mcp.run()
