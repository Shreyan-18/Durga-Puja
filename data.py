"""
Data definitions for Kolkata Durga Puja Pandals, Crowd Profiles, Transit Modes,
Metro Stations, and Route-Aware Iconic Restaurants.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import math

from pandals_data import Pandal, SAMPLE_PANDALS
from restaurants_data import Restaurant, FoodOption, FOOD_CATALOG, ICONIC_RESTAURANTS

@dataclass
class TransitHub:
    id: str
    name: str
    hub_type: str  # 'Metro Station', 'Suburban Railway Jn'
    line: str      # 'Blue Line', 'Green Line', 'Sealdah South Line'
    lat: float
    lon: float
    description: str

# Major Kolkata Metro & Railway Transit Gateways
MAJOR_TRANSIT_HUBS: List[TransitHub] = [
    TransitHub("kavi_subhash", "Kavi Subhash (New Garia)", "Metro Station", "Blue Line / Local Train Interchange", 22.4716, 88.3976, "Key terminal interchange connecting South 24 Pgs local trains (Baruipur/Sonarpur) to Kolkata Metro."),
    TransitHub("ballygunge_jn", "Ballygunge Railway Junction", "Suburban Railway Jn", "Sealdah South Line", 22.5235, 88.3670, "Prime gateway for South Kolkata pandals (Ekdalia, Singhi Park, Ballygunge Cultural, Tridhara). All-night trains."),
    TransitHub("kalighat_metro", "Kalighat Metro Station", "Metro Station", "Blue Line", 22.5178, 88.3468, "Direct walking access to Chetla Agrani, Deshapriya Park, and Rashbehari corridors."),
    TransitHub("jatin_das_park", "Jatin Das Park Metro Station", "Metro Station", "Blue Line", 22.5218, 88.3495, "Gateways to Tridhara Sammilani and Ballygunge Cultural."),
    TransitHub("rabindra_sarobar", "Rabindra Sarobar Metro Station", "Metro Station", "Blue Line", 22.5125, 88.3465, "Direct access to Mudiali Club and Shiv Mandir."),
    TransitHub("netaji_bhavan", "Netaji Bhavan Metro Station", "Metro Station", "Blue Line", 22.5325, 88.3485, "Direct gateway to Maddox Square and Bhowanipore pujas."),
    TransitHub("sovabazar_metro", "Sovabazar Sutanuti Metro", "Metro Station", "Blue Line", 22.5975, 88.3650, "Historic North Kolkata gateway to Sovabazar Rajbari, Kumartuli Park, and Ahiritola."),
    TransitHub("shyambazar_metro", "Shyambazar Metro Station", "Metro Station", "Blue Line", 22.6025, 88.3710, "Direct gateway to Bagbazar Sarbojanin, Hatibagan, and Shyambazar 5-Point."),
    TransitHub("mg_road_metro", "MG Road Metro Station", "Metro Station", "Blue Line", 22.5786, 88.3630, "Gateway to College Square and Mohammad Ali Park."),
    TransitHub("sealdah_station", "Sealdah Railway Station / Metro", "Suburban Railway Jn", "Sealdah Division / Green Line", 22.5675, 88.3712, "Major suburban rail terminal with all-night Puja special EMU services across Bengal."),
    TransitHub("behala_chowrasta", "Behala Chowrasta Gateway", "Metro / Arterial Hub", "Purple Line / DH Road", 22.4930, 88.3130, "Major gateway to Behala pandals (Barisha Club, Nutan Dal, Behala Club)."),
]

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def find_nearest_restaurant_along_route(
    current_lat: float,
    current_lon: float,
    next_lat: float,
    next_lon: float,
    preferred_category: Optional[str] = None,
    max_cost: Optional[int] = None
) -> Tuple[Restaurant, float]:
    """
    Finds the iconic restaurant that causes minimal detour between current location and next destination,
    respecting cuisine preference and optional maximum cost constraint.
    """
    best_rest = None
    best_detour = 99999.0

    direct_dist = haversine_km(current_lat, current_lon, next_lat, next_lon)

    cat_keywords = {
        "biryani": ["biryani", "mughlai", "awadhi"],
        "bengali_heritage": ["bengali", "zamindari", "thali", "ilish", "paturi", "kosha"],
        "bengali_thali": ["bengali", "thali", "zamindari"],
        "street_rolls_cutlets": ["rolls", "cutlets", "kathi", "fry", "cabin"],
        "street_food": ["rolls", "cutlets", "kathi", "fry", "street"],
        "tangra_chinese": ["chinese", "tangra", "hakka", "noodles", "dim sum", "wonton"],
        "park_street_continental": ["continental", "grills", "chelo", "sizzler", "kebab"],
        "chai_dhaba": ["dhaba", "chai", "tea", "paratha", "doodh", "snacks", "sherbets"],
        "chai_snacks": ["chai", "dhaba", "tea", "snacks", "sherbets"],
        "bengali_sweets": ["mishti", "sweets", "rosogolla", "sandesh", "doi"],
        "kolkata_chaat": ["chaat", "phuchka", "kachori", "dhaba", "snacks"],
        "pure_veg_jain": ["pure vegetarian", "marwari", "kachori", "jain", "sweets", "thali"],
        "vegetarian": ["pure vegetarian", "marwari", "chaat", "veg"],
        "cafe_bakery": ["cafe", "bakery", "breakfast", "confectionery", "coffee", "tea"],
        "south_indian": ["south indian", "dosa", "idli", "tiffin"],
        "tibetan_momos": ["momo", "chinese", "thukpa", "dim sum"]
    }

    candidates = list(ICONIC_RESTAURANTS.values())
    if max_cost is not None and max_cost > 0:
        budget_candidates = [r for r in candidates if r.cost_min_inr <= max_cost]
        if budget_candidates:
            candidates = budget_candidates

    for rest in candidates:
        if preferred_category and preferred_category not in ("any", "restaurant", "auto_along_route"):
            keywords = cat_keywords.get(preferred_category, [])
            if keywords and not any(k in rest.specialty.lower() or k in rest.description.lower() for k in keywords):
                continue

        dist1 = haversine_km(current_lat, current_lon, rest.lat, rest.lon)
        dist2 = haversine_km(rest.lat, rest.lon, next_lat, next_lon)
        detour = (dist1 + dist2) - direct_dist

        if detour < best_detour:
            best_detour = detour
            best_rest = rest

    if not best_rest:
        # Fallback to closest candidate
        best_rest = min(candidates, key=lambda r: haversine_km(current_lat, current_lon, r.lat, r.lon))
        best_detour = haversine_km(current_lat, current_lon, best_rest.lat, best_rest.lon)

    return best_rest, round(best_detour, 2)

@dataclass
class TransitionInfo:
    mode: str
    instructions: str
    distance_km: float
    travel_time_mins: float
    cost_min_inr: int
    cost_max_inr: int

def get_transition_details(lat1: float, lon1: float, lat2: float, lon2: float, hour: float, from_name: str, to_name: str) -> TransitionInfo:
    dist_km = haversine_km(lat1, lon1, lat2, lon2)
    
    is_suburban_commute = (dist_km >= 11.0)
    is_south_suburb = ("baruipur" in from_name.lower() or "sonarpur" in from_name.lower() or 
                       "baruipur" in to_name.lower() or "sonarpur" in to_name.lower())

    if is_suburban_commute:
        if is_south_suburb:
            train_mins = 28.0 + (dist_km * 0.4)
            return TransitionInfo(
                mode="🚆 Suburban EMU Local Train (Sealdah South Line)",
                instructions=f"Take Sealdah South local train between {from_name} and Ballygunge Jn / Kavi Subhash Metro (~{dist_km:.1f} km). Eastern Railway operates All-Night Puja Special EMU Trains. Very fast and beats road traffic!",
                distance_km=round(dist_km, 2),
                travel_time_mins=round(train_mins, 1),
                cost_min_inr=10,
                cost_max_inr=15
            )
        else:
            train_mins = 35.0 + (dist_km * 0.5)
            return TransitionInfo(
                mode="🚆 Suburban Local Train / Metro Link",
                instructions=f"Take suburban railway or arterial connector towards {to_name} (~{dist_km:.1f} km). Connect via Metro for central pandals.",
                distance_km=round(dist_km, 2),
                travel_time_mins=round(train_mins, 1),
                cost_min_inr=10,
                cost_max_inr=25
            )

    if dist_km <= 0.8:
        mins = max(2.0, (dist_km / 3.2) * 60.0)
        return TransitionInfo(
            mode="🚶 Walking",
            instructions=f"Walk ~{dist_km*1000:.0f}m along the decorated pedestrian corridor from {from_name} to {to_name}. Avoid vehicles due to police barricades.",
            distance_km=round(dist_km, 2),
            travel_time_mins=round(mins, 1),
            cost_min_inr=0,
            cost_max_inr=0
        )
    
    if dist_km <= 2.5:
        mins = 8.0 + (dist_km / 12.0) * 60.0
        return TransitionInfo(
            mode="🛺 Shared Auto / E-Rickshaw (Toto)",
            instructions=f"Take a shared auto route or Toto towards {to_name} (~{dist_km:.1f} km). Drop off at the nearest barricade choke point and walk the final 200m.",
            distance_km=round(dist_km, 2),
            travel_time_mins=round(mins, 1),
            cost_min_inr=15,
            cost_max_inr=30
        )
    
    is_late_night = (1.5 <= (hour % 24.0) <= 5.5)
    
    if not is_late_night and dist_km >= 3.5:
        mins = 14.0 + (dist_km / 22.0) * 60.0
        return TransitionInfo(
            mode="🚇 Kolkata Metro + Short Walk",
            instructions=f"Board the Kolkata Metro towards {to_name}. Fast and bypasses major surface road blockades. Final 500m walk via designated pedestrian gates.",
            distance_km=round(dist_km, 2),
            travel_time_mins=round(mins, 1),
            cost_min_inr=10,
            cost_max_inr=25
        )
    else:
        traffic_mult = 1.3 if is_late_night else 2.2
        mins = 7.0 + (dist_km / (20.0 / traffic_mult)) * 60.0
        fare_min = int(80 + dist_km * 18)
        fare_max = int(120 + dist_km * 28)
        return TransitionInfo(
            mode="🚖 Yellow Taxi / Ride-Hail Cab",
            instructions=f"Take a yellow taxi or app cab towards {to_name}. Note: Vehicles will be diverted at major street crossings by Kolkata Police.",
            distance_km=round(dist_km, 2),
            travel_time_mins=round(mins, 1),
            cost_min_inr=fare_min,
            cost_max_inr=fare_max
        )

def estimate_travel_time_minutes(lat1: float, lon1: float, lat2: float, lon2: float, hour: float) -> float:
    t = get_transition_details(lat1, lon1, lat2, lon2, hour, "Origin", "Dest")
    return t.travel_time_mins

def get_queue_wait_time(pandal: Pandal, hour: float, tithi: str = "Ashtami", has_vip_pass: bool = False) -> float:
    if has_vip_pass:
        return max(5.0, pandal.crowd_tier * 4.0)

    base_tier_wait = {1: 15.0, 2: 35.0, 3: 75.0}.get(pandal.crowd_tier, 25.0)

    tithi_mult = {
        "Chaturthi": 0.4,
        "Panchami": 0.6,
        "Sasthi": 0.8,
        "Saptami": 1.1,
        "Ashtami": 1.35,
        "Nabami": 1.35,
        "Dashami": 0.7
    }.get(tithi, 1.0)

    if 0.0 <= hour < 2.0:
        hour_factor = 1.0
    elif 2.0 <= hour < 5.0:
        hour_factor = 0.4
    elif 5.0 <= hour < 10.0:
        hour_factor = 0.25
    elif 10.0 <= hour < 16.0:
        hour_factor = 0.5
    elif 16.0 <= hour < 19.0:
        hour_factor = 0.95
    elif 19.0 <= hour < 24.0:
        hour_factor = 1.4
    else:
        hour_factor = 1.0

    return round(base_tier_wait * tithi_mult * hour_factor, 1)
