"""
Streamlit Web App: Interactive Kolkata Durga Puja Hopping Scheduler.
Features:
- Route-Aware Restaurants: Automatically matches iconic eateries directly along the route with minimal detour.
- Interactive Route Lines: Connected visual paths connecting every stop on the map.
- Metro & Railway Gateways: Clear instructions for entering the pandal cluster and returning home safely.
- Explicit Movement Modes: Visual tags for Walking, Shared Auto, Metro, Local Train, and Cabs between pandals.
- Privacy-First Baruipur & Bengal suburb support.
"""

import streamlit as st
import pandas as pd
import pydeck as pdk
from collections import Counter

from data import SAMPLE_PANDALS, FOOD_CATALOG, ICONIC_RESTAURANTS, MAJOR_TRANSIT_HUBS
from geocoder import geocode_location
from optimizer import PujaHopperOptimizer, UserPreference, MealSlot, format_hour_to_time_str

st.set_page_config(
    page_title="Durga Puja Pandal Hopping Optimizer",
    page_icon="🪔",
    layout="wide"
)

st.title("🪔 Durga Puja Pandal Hopping Optimizer")
st.markdown(
    """
    Plan a complete **door-to-door** Durga Puja hopping journey across Kolkata.
    Features **on-route restaurant matching**, **interactive visual route lines**, 
    **Metro & Suburban rail gateway guidance**, and **step-by-step movement modes**.
    """
)

st.info(
    "🛡️ **Privacy Assured**: You never need to enter your personal house number or street! "
    "Simply enter your **Town name** (e.g., *Baruipur*), **Local Railway Station**, or **PIN code**."
)

# ----------------- SIDEBAR CONTROLS -----------------
st.sidebar.header("🏠 1. Starting Location (Privacy-First)")

input_mode = st.sidebar.radio(
    "How would you like to set your location?",
    ["✍️ Type Town / Station / Area", "📮 6-Digit PIN Code", "🚉 Bengal Suburbs & Hubs Presets"]
)

if input_mode == "✍️ Type Town / Station / Area":
    home_query = st.sidebar.text_input(
        "Enter Town, Station or Area",
        value="Baruipur",
        help="E.g., Baruipur, Sonarpur Junction, Behala Chowrasta, Barasat, Serampore, Garia, etc."
    )
elif input_mode == "📮 6-Digit PIN Code":
    pin_input = st.sidebar.text_input(
        "Enter 6-Digit PIN Code",
        value="743302",
        help="E.g., 743302 (Baruipur), 700084 (Garia), 700034 (Behala), 711101 (Howrah)"
    )
    home_query = pin_input
else:
    preset_choices = [
        "Baruipur (South 24 Parganas)",
        "Sonarpur Junction (South 24 Parganas)",
        "Garia / Kavi Subhash (South Kolkata)",
        "Behala Chowrasta (South West Kolkata)",
        "Gariahat Crossing (South Kolkata)",
        "Howrah Station (Howrah)",
        "Barasat Junction (North 24 Parganas)",
        "Barrackpore (North 24 Parganas)",
        "Shyambazar 5-Point (North Kolkata)",
        "Salt Lake Sector 5 (East Kolkata)",
        "Serampore (Hooghly)",
        "Chandannagar (Hooghly)"
    ]
    selected_preset = st.sidebar.selectbox("Choose a Suburban / City Hub", preset_choices)
    home_query = selected_preset.split("(")[0].strip()

# Geocode location
home_lat, home_lon, resolved_home_name = geocode_location(home_query)
st.sidebar.success(f"📍 **Origin Set:** {resolved_home_name}\n\nCoords: `({home_lat:.4f}, {home_lon:.4f})`")

st.sidebar.subheader("⏰ 2. Hopping Window")

time_options = []
for h in range(24):
    for m in (0, 30):
        t_str = f"{h:02d}:{m:02d}"
        period = "AM" if h < 12 else "PM"
        dh = h if h in (0, 12) else (h % 12)
        if dh == 0:
            dh = 12
        label = f"{dh:02d}:{m:02d} {period}"
        val = h + (m / 60.0)
        time_options.append((label, val))

time_labels = [opt[0] for opt in time_options]
time_values = [opt[1] for opt in time_options]

start_choice_idx = st.sidebar.selectbox(
    "Start Time (Depart from Town)",
    range(len(time_labels)),
    index=39, # 7:30 PM
    format_func=lambda i: time_labels[i]
)
end_choice_idx = st.sidebar.selectbox(
    "End Time (Return Home by)",
    range(len(time_labels)),
    index=8, # 4:00 AM next morning
    format_func=lambda i: time_labels[i]
)

start_hour = time_values[start_choice_idx]
end_hour = time_values[end_choice_idx]

# ----------------- ROUTE-AWARE MULTI-MEAL PLANNING -----------------
st.sidebar.subheader("🍽️ 3. Meals & On-Route Dining")

num_meals = st.sidebar.selectbox("How many meals/food stops?", [1, 2, 3, 4, 5, 6], index=1) # Supports up to 6 meals

configured_meals: List[MealSlot] = []

rest_keys = list(ICONIC_RESTAURANTS.keys())
venue_options = [
    ("✨ Auto-Match Restaurants On Route (Recommended)", "auto_along_route"),
    ("🎪 Festive Street Food Stalls near Current Pandal", "street_stall"),
] + [(f"🍴 {ICONIC_RESTAURANTS[k].name} ({ICONIC_RESTAURANTS[k].zone})", k) for k in rest_keys]

default_meal_types = ["Lunch", "Dinner", "Midnight Chai & Adda", "Evening Snacks", "Early Morning Bites", "Breakfast"]
common_types = ["Lunch", "Dinner", "Evening Snacks", "Midnight Chai & Adda", "Early Morning Bites", "Breakfast", "Brunch", "Afternoon Tea", "Custom..."]
default_times = [28, 46, 5, 38, 12, 18] # 2:00 PM, 11:00 PM, 2:30 AM, 7:00 PM, 6:00 AM, 9:00 AM

for m_idx in range(num_meals):
    saved_label = st.session_state.get(f"mlabel_{m_idx}", default_meal_types[m_idx % len(default_meal_types)])
    
    with st.sidebar.expander(f"🍴 Meal {m_idx + 1}", expanded=(m_idx < 2)):
        type_choice = st.selectbox(
            f"Meal {m_idx+1} Type",
            common_types,
            index=common_types.index(saved_label) if saved_label in common_types else 0,
            key=f"mtype_select_{m_idx}"
        )
        
        if type_choice == "Custom...":
            m_label = st.text_input(
                f"Enter Custom Name for Meal {m_idx+1}",
                value=saved_label if saved_label not in common_types else f"Meal {m_idx+1}",
                key=f"mlabel_{m_idx}"
            )
        else:
            m_label = type_choice
            st.session_state[f"mlabel_{m_idx}"] = type_choice
        
        # Smart default time based on type
        if "lunch" in m_label.lower():
            suggested_time_idx = 28 # 02:00 PM
        elif "dinner" in m_label.lower():
            suggested_time_idx = 46 # 11:00 PM
        elif "chai" in m_label.lower() or "midnight" in m_label.lower():
            suggested_time_idx = 5  # 02:30 AM
        elif "snack" in m_label.lower():
            suggested_time_idx = 39 # 07:30 PM
        elif "breakfast" in m_label.lower():
            suggested_time_idx = 18 # 09:00 AM
        elif "morning" in m_label.lower():
            suggested_time_idx = 12 # 06:00 AM
        else:
            suggested_time_idx = default_times[m_idx % len(default_times)]

        m_time_idx = st.selectbox(
            f"Preferred Time for {m_label}",
            range(len(time_labels)),
            index=suggested_time_idx,
            format_func=lambda i: f"Around {time_labels[i]}",
            key=f"mtime_{m_idx}"
        )
        m_target_hour = time_values[m_time_idx]
        
        venue_choice = st.selectbox(
            f"Venue Choice for {m_label}",
            range(len(venue_options)),
            index=0,
            format_func=lambda i: venue_options[i][0],
            key=f"mvenue_{m_idx}"
        )
        venue_id = venue_options[venue_choice][1]
        
        food_cat_keys = list(FOOD_CATALOG.keys())
        food_cat = st.selectbox(
            f"Cuisine Preference for {m_label}",
            food_cat_keys,
            index=m_idx % len(food_cat_keys),
            format_func=lambda k: FOOD_CATALOG[k].name,
            key=f"mfoodcat_{m_idx}"
        )
            
        configured_meals.append(MealSlot(
            title=m_label,
            target_hour=m_target_hour,
            food_category=food_cat,
            specific_restaurant_id=venue_id,
            duration_mins=40
        ))

# ----------------- HOPPING PREFERENCES -----------------
st.sidebar.subheader("🎪 4. Pandal Preferences")
tithi = st.sidebar.selectbox(
    "Puja Tithi",
    ["Chaturthi", "Panchami", "Sasthi", "Saptami", "Ashtami", "Nabami", "Dashami"],
    index=4 # Ashtami
)

selected_zones = st.sidebar.multiselect(
    "Target Pandal Zones",
    options=["South", "North", "Central", "East_VIP", "East_SaltLake", "Howrah"],
    default=["South"]
)

col_p1, col_p2 = st.sidebar.columns(2)
theme_weight = col_p1.slider("Theme Art", 0.5, 2.0, 1.2, 0.1)
trad_weight = col_p2.slider("Heritage", 0.5, 2.0, 1.0, 0.1)
patience = st.sidebar.slider("Queue Patience", 0.5, 1.5, 1.0, 0.1)
has_vip = st.sidebar.checkbox("VIP Passes", value=False)

# ----------------- BUDGET & COST LIMITATIONS -----------------
st.sidebar.subheader("💰 5. Budget & Cost Limits")
enable_budget = st.sidebar.checkbox("Enforce Maximum Budget Limit", value=False)
max_budget_val = None
max_meal_spend_val = None
if enable_budget:
    max_budget_val = st.sidebar.slider(
        "Max Total Trip Budget (₹ per person)",
        min_value=200,
        max_value=4000,
        value=1200,
        step=50,
        help="Caps combined transit fares (train/metro/cab) and dining expenses."
    )
    spend_tier = st.sidebar.selectbox(
        "Max Spend per Restaurant Meal",
        ["No Cap on Dining", "Budget Friendly (Max ₹250)", "Moderate (Max ₹500)", "Heritage / Fine Dining (Max ₹850)"],
        index=0
    )
    tier_map = {
        "Budget Friendly (Max ₹250)": 250,
        "Moderate (Max ₹500)": 500,
        "Heritage / Fine Dining (Max ₹850)": 850
    }
    max_meal_spend_val = tier_map.get(spend_tier)

# ----------------- RUN OPTIMIZATION -----------------
prefs = UserPreference(
    home_name=resolved_home_name,
    home_lat=home_lat,
    home_lon=home_lon,
    start_hour=start_hour,
    end_hour=end_hour,
    preferred_zones=selected_zones,
    tithi=tithi,
    theme_preference=theme_weight,
    traditional_pref=trad_weight,
    patience_factor=patience,
    has_vip_pass=has_vip,
    meals=configured_meals,
    max_budget_inr=max_budget_val,
    max_meal_cost=max_meal_spend_val
)

optimizer = PujaHopperOptimizer()
result = optimizer.optimize_itinerary(prefs)
c = result.costing
gw = result.gateway

# ----------------- GATEWAY GUIDANCE BANNER -----------------
st.subheader("🚉 Recommended Transit & Metro Gateways")
col_gw1, col_gw2 = st.columns(2)
with col_gw1:
    st.info(f"👉 **Entry Gateway to Pandals:**\n\n**{gw.entry_gateway_name}** ({gw.entry_gateway_line})\n\n_{gw.entry_instructions}_")
with col_gw2:
    st.success(f"🏡 **Safe Return Home Gateway:**\n\n**{gw.return_gateway_name}** ({gw.return_gateway_line})\n\n_{gw.return_instructions}_")

# ----------------- TOP METRICS & COSTING BANNER -----------------
st.subheader("💰 Estimated Trip Budget & Overview")

if c.max_budget_inr:
    if c.is_within_budget:
        buffer_val = c.max_budget_inr - c.total_cost_min_inr
        st.success(f"🎯 **Budget Compliance: WITHIN BUDGET!** Estimated Total: ₹{c.total_cost_min_inr} - ₹{c.total_cost_max_inr} per person (Budget Cap: ₹{c.max_budget_inr} | Remaining Buffer: ~₹{buffer_val})")
    else:
        overage = c.total_cost_min_inr - c.max_budget_inr
        st.warning(f"⚠️ **Budget Alert:** Estimated Total ₹{c.total_cost_min_inr} - ₹{c.total_cost_max_inr} exceeds your ₹{c.max_budget_inr} budget cap by ₹{overage}. Consider choosing street food stalls or closer zones.")

col_c1, col_c2, col_c3, col_c4 = st.columns(4)

col_c1.metric(
    "Total Cost Range",
    f"₹{c.total_cost_min_inr} - ₹{c.total_cost_max_inr}",
    "Per Person Total"
)
col_c2.metric(
    "Transit & Fares",
    f"₹{c.transit_cost_min_inr} - ₹{c.transit_cost_max_inr}",
    f"{result.total_distance_km} km total"
)
col_c3.metric(
    f"Meals ({len(configured_meals)} stops)",
    f"₹{c.food_cost_min_inr} - ₹{c.food_cost_max_inr}",
    f"{len(configured_meals)} culinary stops"
)
col_c4.metric(
    "Safe Home Return",
    f"{result.actual_return_time_str}",
    f"Target: {result.end_time_str}"
)

# Secondary Quick Metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("Pandals Visited", f"{result.total_pandals_visited} pandals")
m2.metric("Trip Duration", f"{result.total_elapsed_mins / 60.0:.1f} hours", f"Depart {result.start_time_str}")
m3.metric("Queue Wait Time", f"{result.total_queue_mins:.0f} mins")
m4.metric("In-Transit Time", f"{result.total_travel_mins:.0f} mins")

if result.summary_notes:
    with st.expander("💡 Tactical Puja Advisory & Route Tips", expanded=True):
        for note in result.summary_notes:
            st.write(f"• {note}")

# ----------------- TABS -----------------
tab_map, tab_sched, tab_transitions, tab_pandals, tab_restaurants = st.tabs([
    "🗺️ Interactive Route Map (With Route Lines)",
    "📋 Door-to-Door Plan",
    "🚶 Movement Modes & Transitions",
    "🏛️ Pandal Directory",
    "🍴 On-Route Restaurants Directory"
])

with tab_map:
    st.subheader("Geographic Hopping Sequence with Connected Path Lines")
    st.caption("Lines represent your journey path from Origin $\\rightarrow$ Pandals & On-Route Dining $\\rightarrow$ Return Origin.")

    # 1. Point data
    point_items = []
    
    # Origin
    point_items.append({
        "name": f"Home / Origin: {resolved_home_name}",
        "lat": home_lat,
        "lon": home_lon,
        "color": [0, 200, 80, 255], # Bright Green
        "size": 320,
        "type": "Origin"
    })
    
    # Scheduled stops
    for s in result.schedule:
        if not s.is_home_stop:
            if s.is_food_stop:
                point_items.append({
                    "name": f"🍴 Stop {s.stop_number}: {s.name}",
                    "lat": s.lat,
                    "lon": s.lon,
                    "color": [255, 150, 0, 240], # Vibrant Orange
                    "size": 240,
                    "type": "Dining"
                })
            else:
                point_items.append({
                    "name": f"🚩 Stop {s.stop_number}: {s.name} ({s.zone})",
                    "lat": s.lat,
                    "lon": s.lon,
                    "color": [230, 40, 40, 230], # Crimson Red
                    "size": 210,
                    "type": "Pandal"
                })

    # Transit Hubs on Map (Metro / Rail)
    for hub in MAJOR_TRANSIT_HUBS:
        point_items.append({
            "name": f"🚇 {hub.name} ({hub.line})",
            "lat": hub.lat,
            "lon": hub.lon,
            "color": [30, 144, 255, 200], # Dodger Blue
            "size": 140,
            "type": "Transit Hub"
        })

    df_points = pd.DataFrame(point_items)

    # 2. Path data connecting the sequential stops
    path_coords = []
    for s in result.schedule:
        if s.lat != 0.0 and s.lon != 0.0:
            path_coords.append([s.lon, s.lat])

    df_path = pd.DataFrame([{
        "path": path_coords,
        "color": [255, 110, 0, 220] # Festive Glowing Saffron Line
    }])

    view_state = pdk.ViewState(
        latitude=df_points["lat"].mean(),
        longitude=df_points["lon"].mean(),
        zoom=11.4,
        pitch=35
    )

    # Layers
    path_layer = pdk.Layer(
        "PathLayer",
        data=df_path,
        get_path="path",
        get_color="color",
        width_scale=20,
        width_min_pixels=4,
        rounded=True,
        pickable=False
    )

    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=df_points,
        get_position=["lon", "lat"],
        get_color="color",
        get_radius="size",
        pickable=True,
    )

    deck = pdk.Deck(
        layers=[path_layer, scatter_layer],
        initial_view_state=view_state,
        tooltip={"text": "{name}"}
    )
    st.pydeck_chart(deck)
    st.markdown("🟢 **Green**: Home/Origin | 🔴 **Red**: Pandals | 🟠 **Orange**: Food / Restaurant | 🔵 **Blue**: Key Metro & Train Stations")

with tab_sched:
    st.subheader(f"Minute-by-Minute Timeline ({result.start_time_str} → {result.actual_return_time_str})")
    
    table_data = []
    for s in result.schedule:
        table_data.append({
            "Step": s.stop_number,
            "Time Window": f"{s.arrival_time_str} - {s.departure_time_str}",
            "Stop / Activity": s.name,
            "Movement Mode": s.movement_mode,
            "Transit Time": f"{s.transition.travel_time_mins} min" if s.transition else "-",
            "Queue Wait": f"{s.queue_wait_mins} min" if not s.is_home_stop and not s.is_food_stop else "-",
            "Cost": f"₹{s.food_cost_min}-₹{s.food_cost_max}" if s.is_food_stop else (
                f"₹{s.transition.cost_min_inr}-₹{s.transition.cost_max_inr}" if s.transition and s.transition.cost_max_inr > 0 else "Free"
            )
        })
    df_sched = pd.DataFrame(table_data)
    st.dataframe(df_sched, use_container_width=True)

with tab_transitions:
    st.subheader("How to Move from One Stop to the Next (Modes & Directions)")
    st.caption("Detailed navigation modes, pedestrian corridor advice, train/metro lines, and estimated fares.")
    
    for s in result.schedule:
        if s.transition:
            t = s.transition
            with st.container():
                st.markdown(f"#### ➡️ Movement to Step {s.stop_number}: {s.name}")
                col_t1, col_t2, col_t3 = st.columns(3)
                col_t1.info(f"**Movement Mode:** {t.mode}")
                col_t2.write(f"**Distance & Time:** ~{t.distance_km} km ({t.travel_time_mins} mins)")
                fare_txt = f"₹{t.cost_min_inr} - ₹{t.cost_max_inr}" if t.cost_max_inr > 0 else "Free (Walking)"
                col_t3.write(f"**Estimated Fare:** {fare_txt}")
                st.write(f"🧭 **Directions & Police Advisory:** {t.instructions}")
                st.write("")
        
        # Stop details
        if s.is_food_stop:
            st.success(f"### 🍽️ {s.name} ({s.arrival_time_str} - {s.departure_time_str})\n\n{s.description}\n\n**Budget:** ₹{s.food_cost_min} - ₹{s.food_cost_max} per person")
        elif s.is_home_stop:
            st.warning(f"### {s.name} ({s.arrival_time_str})\n\n{s.description}")
        else:
            st.markdown(f"### 🚩 Step {s.stop_number}: **{s.name}** ({s.arrival_time_str} - {s.departure_time_str})")
            st.write(f"**Zone:** {s.zone} | **Metro:** {s.nearest_metro} | **Expected Queue:** ~{s.queue_wait_mins} mins | **Darshan:** ~{s.visit_mins} mins")
            st.write(f"_{s.description}_")
        st.divider()

with tab_pandals:
    st.subheader(f"🏛️ Comprehensive Bengal Durga Puja Directory ({len(SAMPLE_PANDALS)} Pandals)")
    st.caption("Browse, search, and filter celebrated Sharad Samman winners, Bonedi Bari mansions, and community Pujas.")
    zc = Counter(p.zone for p in SAMPLE_PANDALS)
    st.markdown(f"🌐 **Coverage Across Bengal ({len(SAMPLE_PANDALS)} Total):** 🔴 **{zc.get('South', 0)}** South Kolkata | 🔵 **{zc.get('North', 0)}** North Kolkata | 🟡 **{zc.get('Central', 0)}** Central Kolkata | 🟢 **{zc.get('East_SaltLake', 0)}** Salt Lake & New Town | 🟣 **{zc.get('East_VIP', 0)}** VIP Rd & Dum Dum | 🟠 **{zc.get('Howrah', 0)}** Howrah & Hooghly")

    # Search & Filter Controls
    col_f1, col_f2, col_f3, col_f4 = st.columns([2.5, 1.5, 1.5, 1.5])
    search_q = col_f1.text_input("🔍 Search Pandals", placeholder="Type name, metro, street, or theme keyword...").strip().lower()
    
    zone_filter = col_f2.selectbox("Filter Zone", ["All Zones", "South", "North", "Central", "East_VIP", "East_SaltLake", "Howrah"])
    type_filter = col_f3.selectbox("Filter Style", ["All Styles", "Theme", "Traditional", "Bonedi_Bari"])
    crowd_filter = col_f4.selectbox("Filter Crowd Tier", ["All Tiers", "🔥 Tier 1 (Moderate)", "🔥🔥 Tier 2 (High)", "🔥🔥🔥 Tier 3 (Mega)"])

    # Filtering Logic
    filtered_pandals = []
    for p in SAMPLE_PANDALS:
        if search_q:
            match_str = f"{p.name} {p.zone} {p.theme_type} {p.nearest_metro} {p.key_street} {p.description}".lower()
            if search_q not in match_str:
                continue
        if zone_filter != "All Zones" and p.zone != zone_filter:
            continue
        if type_filter != "All Styles" and p.theme_type != type_filter:
            continue
        if crowd_filter != "All Tiers":
            t_num = int(crowd_filter[1]) if crowd_filter[1].isdigit() else (3 if "Tier 3" in crowd_filter else (2 if "Tier 2" in crowd_filter else 1))
            if p.crowd_tier != t_num:
                continue
        filtered_pandals.append(p)

    st.write(f"**Showing {len(filtered_pandals)} of {len(SAMPLE_PANDALS)} pandals**")

    # Table View
    p_data = [{
        "Pandal Name": p.name,
        "Zone": p.zone,
        "Style": p.theme_type,
        "Rating": f"⭐ {p.base_rating}/10",
        "Crowd Rush": "🔥🔥🔥 Mega" if p.crowd_tier == 3 else ("🔥🔥 High" if p.crowd_tier == 2 else "🔥 Moderate"),
        "Nearest Metro / Rail": p.nearest_metro,
        "Key Street / Landmark": p.key_street,
        "Art & Heritage Highlights": p.description
    } for p in filtered_pandals]
    st.dataframe(pd.DataFrame(p_data), use_container_width=True)

    # Detailed Cards
    with st.expander("📖 View Detailed Pandal Guide Cards", expanded=False):
        for p in filtered_pandals:
            with st.container():
                st.markdown(f"### {p.name} (⭐ {p.base_rating}/10)")
                c1, c2, c3 = st.columns(3)
                c1.write(f"📍 **Zone & Street:** {p.zone} ({p.key_street})")
                c2.write(f"🚇 **Nearest Metro:** {p.nearest_metro}")
                crowd_label = "🔥🔥🔥 Mega Crowd (Queue 60-90m)" if p.crowd_tier == 3 else ("🔥🔥 High Crowd (Queue 35-50m)" if p.crowd_tier == 2 else "🔥 Moderate Queue (15-25m)")
                c3.write(f"👥 **Crowd Level:** {crowd_label}")
                st.write(f"_{p.description}_")
                st.divider()

with tab_restaurants:
    st.subheader(f"🍴 Iconic Kolkata Restaurants Directory ({len(ICONIC_RESTAURANTS)} Legendary Spots)")
    st.caption("Curated heritage cabins, biryani dynasties, Tangra Chinese institutions, midnight dhaba stops, and sweets.")

    col_r1, col_r2, col_r3 = st.columns([2.5, 1.5, 1.5])
    r_search = col_r1.text_input("🔍 Search Restaurants", placeholder="Search by name, cuisine, landmark...").strip().lower()
    r_zone = col_r2.selectbox("Filter Restaurant Zone", ["All Zones", "South", "North", "Central", "East_VIP", "East_SaltLake", "Howrah"])
    r_max_cost = col_r3.number_input("Max Budget Filter (₹)", min_value=0, max_value=2000, value=0, step=50, help="0 means no price filter")

    filtered_rests = []
    for r in ICONIC_RESTAURANTS.values():
        if r_search:
            m_text = f"{r.name} {r.specialty} {r.zone} {r.nearest_landmark} {r.description}".lower()
            if r_search not in m_text:
                continue
        if r_zone != "All Zones" and r.zone != r_zone:
            continue
        if r_max_cost > 0 and r.cost_min_inr > r_max_cost:
            continue
        filtered_rests.append(r)

    st.write(f"**Showing {len(filtered_rests)} of {len(ICONIC_RESTAURANTS)} restaurants**")
    r_data = [{
        "Restaurant Name": r.name,
        "Specialty": r.specialty,
        "Zone": r.zone,
        "Price Range": f"₹{r.cost_min_inr} - ₹{r.cost_max_inr}",
        "Nearest Landmark": r.nearest_landmark,
        "Signature Highlights": r.description
    } for r in filtered_rests]
    st.dataframe(pd.DataFrame(r_data), use_container_width=True)
