"""
Geocoding module for resolving Home locations in West Bengal / Kolkata.
Privacy-first: Supports town names, railway stations, PIN codes, and landmarks
without requiring personal house addresses.
"""

import requests
from typing import Tuple, Optional
import urllib.parse
import re

# Comprehensive database of Bengal suburbs, district towns, and railway stations
BENGAL_LOCATIONS = {
    # --- South 24 Parganas ---
    "baruipur": (22.3663, 88.4313, "Baruipur, South 24 Parganas"),
    "baruipur junction": (22.3663, 88.4313, "Baruipur Junction Station, South 24 Parganas"),
    "baruipur station": (22.3663, 88.4313, "Baruipur Junction Station, South 24 Parganas"),
    "sonarpur": (22.4402, 88.4233, "Sonarpur, South 24 Parganas"),
    "sonarpur junction": (22.4402, 88.4233, "Sonarpur Junction Station, South 24 Parganas"),
    "subhasgram": (22.4085, 88.4290, "Subhasgram, South 24 Parganas"),
    "mallikpur": (22.3850, 88.4300, "Mallikpur, South 24 Parganas"),
    "canning": (22.3087, 88.6653, "Canning, South 24 Parganas"),
    "diamond harbour": (22.1953, 88.1965, "Diamond Harbour, South 24 Parganas"),
    "lakshmikantapur": (22.1764, 88.3182, "Lakshmikantapur, South 24 Parganas"),
    "amtala": (22.3833, 88.2667, "Amtala, South 24 Parganas"),
    "budge budge": (22.4825, 88.1812, "Budge Budge, South 24 Parganas"),
    "garia": (22.4645, 88.3900, "Garia, South 24 Parganas / Kolkata"),
    "kavi subhash": (22.4716, 88.3976, "Kavi Subhash (New Garia) Metro / Station"),
    "new garia": (22.4716, 88.3976, "New Garia / Kavi Subhash, South Kolkata"),
    "narendrapur": (22.4410, 88.3965, "Narendrapur, South 24 Parganas"),
    "behala chowrasta": (22.4874, 88.3134, "Behala Chowrasta, South West Kolkata"),
    "jadavpur": (22.4988, 88.3685, "Jadavpur 8B / Station, South Kolkata"),
    "jadavpur 8b": (22.4988, 88.3685, "Jadavpur 8B Bus Stand, South Kolkata"),

    # --- North 24 Parganas ---
    "barasat": (22.7214, 88.4812, "Barasat, North 24 Parganas"),
    "barasat junction": (22.7214, 88.4812, "Barasat Junction Station, North 24 Parganas"),
    "madhyamgram": (22.7011, 88.4552, "Madhyamgram, North 24 Parganas"),
    "barrackpore": (22.7663, 88.3687, "Barrackpore, North 24 Parganas"),
    "dum dum junction": (22.6214, 88.3934, "Dum Dum Junction / Metro, North 24 Parganas"),
    "dum dum": (22.6214, 88.3934, "Dum Dum, North 24 Parganas"),
    "habra": (22.8398, 88.6578, "Habra, North 24 Parganas"),
    "bangaon": (23.0538, 88.8267, "Bangaon Junction, North 24 Parganas"),
    "naihati": (22.8988, 88.4262, "Naihati Junction, North 24 Parganas"),
    "sodepur": (22.6975, 88.3892, "Sodepur, North 24 Parganas"),
    "khardah": (22.7200, 88.3800, "Khardah, North 24 Parganas"),

    # --- Howrah & Hooghly ---
    "howrah station": (22.5838, 88.3426, "Howrah Railway Station, Howrah"),
    "howrah": (22.5838, 88.3426, "Howrah Central / Station"),
    "shibpur": (22.5645, 88.3150, "Shibpur, Howrah"),
    "bally": (22.6515, 88.3420, "Bally, Howrah"),
    "serampore": (22.7500, 88.3444, "Serampore, Hooghly"),
    "rishra": (22.7118, 88.3517, "Rishra, Hooghly"),
    "chandannagar": (22.8670, 88.3673, "Chandannagar Strand, Hooghly"),
    "bandel": (22.9238, 88.3758, "Bandel Junction, Hooghly"),
    "chinsurah": (22.9000, 88.3900, "Chinsurah, Hooghly"),
    "uttarpara": (22.6672, 88.3486, "Uttarpara, Hooghly"),

    # --- Kolkata Core Hubs ---
    "gariahat": (22.5186, 88.3644, "Gariahat Crossing, South Kolkata"),
    "shyambazar": (22.6022, 88.3719, "Shyambazar 5-Point Crossing, North Kolkata"),
    "park street": (22.5511, 88.3524, "Park Street, Central Kolkata"),
    "salt lake sector 5": (22.5867, 88.4312, "Sector V, Salt Lake, Kolkata"),
    "salt lake": (22.5867, 88.4312, "Salt Lake, Kolkata"),
    "new town": (22.5937, 88.4716, "Action Area 1, New Town, Kolkata"),
    "bhowanipore": (22.5312, 88.3475, "Bhowanipore, South Kolkata"),
    "sealdah": (22.5675, 88.3712, "Sealdah Railway Station, Central Kolkata"),
    "esplanade": (22.5645, 88.3522, "Esplanade / Dharmatala, Central Kolkata"),
    "kankurgachi": (22.5768, 88.3888, "Kankurgachi, East Kolkata"),
    "lake town": (22.6062, 88.4025, "Lake Town / VIP Road, Kolkata"),
}

# West Bengal PIN Codes mapping
WB_PIN_CODES = {
    "743302": (22.3663, 88.4313, "Baruipur (PIN 743302), South 24 Parganas"),
    "743387": (22.3663, 88.4313, "Baruipur Head Post Office (PIN 743387)"),
    "700144": (22.3663, 88.4313, "Baruipur Town (PIN 700144), South 24 Parganas"),
    "700150": (22.4402, 88.4233, "Sonarpur (PIN 700150), South 24 Parganas"),
    "743372": (22.4085, 88.4290, "Subhasgram (PIN 743372), South 24 Parganas"),
    "700084": (22.4645, 88.3900, "Garia (PIN 700084), Kolkata / South 24 Pgs"),
    "700103": (22.4410, 88.3965, "Narendrapur (PIN 700103), South 24 Parganas"),
    "700034": (22.4874, 88.3134, "Behala (PIN 700034), Kolkata"),
    "700019": (22.5186, 88.3644, "Gariahat / Ballygunge (PIN 700019), Kolkata"),
    "700004": (22.6022, 88.3719, "Shyambazar (PIN 700004), Kolkata"),
    "700091": (22.5867, 88.4312, "Salt Lake Sector V (PIN 700091), Kolkata"),
    "700156": (22.5937, 88.4716, "New Town (PIN 700156), Kolkata"),
    "700124": (22.7214, 88.4812, "Barasat (PIN 700124), North 24 Parganas"),
    "700120": (22.7663, 88.3687, "Barrackpore (PIN 700120), North 24 Parganas"),
    "711101": (22.5838, 88.3426, "Howrah (PIN 711101), Howrah"),
    "712201": (22.7500, 88.3444, "Serampore (PIN 712201), Hooghly"),
    "712136": (22.8670, 88.3673, "Chandannagar (PIN 712136), Hooghly"),
}

def geocode_location(location_query: str) -> Tuple[float, float, str]:
    """
    Resolves a town name, railway station, landmark, or PIN code into (lat, lon, display_name).
    Never requires personal street or house addresses.
    """
    clean_query = location_query.strip().lower()
    
    # 1. Check if the query contains a 6-digit Indian PIN Code
    pin_match = re.search(r'\b\d{6}\b', clean_query)
    if pin_match:
        pin = pin_match.group(0)
        if pin in WB_PIN_CODES:
            return WB_PIN_CODES[pin]

    # 2. Check offline Bengal database
    for key, (lat, lon, desc) in BENGAL_LOCATIONS.items():
        if key == clean_query or key in clean_query or clean_query in key:
            return lat, lon, desc

    # 3. Query OpenStreetMap Nominatim for any arbitrary West Bengal town/landmark
    search_term = location_query.strip()
    if not any(k in search_term.lower() for k in ["west bengal", "bengal", "kolkata", "24 parganas", "howrah", "hooghly"]):
        search_term += ", West Bengal, India"

    headers = {"User-Agent": "DurgaPujaHopperApp/2.5 (privacy_first_puja_planner)"}
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(search_term)}&format=json&limit=1"

    try:
        response = requests.get(url, headers=headers, timeout=6)
        if response.status_code == 200:
            data = response.json()
            if data and len(data) > 0:
                first = data[0]
                lat = float(first["lat"])
                lon = float(first["lon"])
                display_name = first.get("display_name", location_query)
                parts = [p.strip() for p in display_name.split(",")]
                short_name = ", ".join(parts[:3]) if len(parts) >= 3 else display_name
                return lat, lon, short_name
    except Exception:
        pass

    # Default fallback: Baruipur / South 24 Parganas if mentioned or general Kolkata
    if "baruipur" in clean_query:
        return 22.3663, 88.4313, "Baruipur, South 24 Parganas"
    
    return 22.5630, 88.3510, f"{location_query} (Estimated Location)"
