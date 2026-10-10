"""
Demonstration runner for Durga Puja Hopping Scheduler.
Features:
- Multi-meal scheduling (Snacks, Main Dinner at Arsalan, Midnight Chai at Balwant Singh Dhaba).
- Specific iconic restaurant integration and geolocated routing.
- Privacy-first Baruipur commuter route.
"""

import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from geocoder import geocode_location
from optimizer import PujaHopperOptimizer, UserPreference, MealSlot, parse_time_str_to_float
from data import FOOD_CATALOG, ICONIC_RESTAURANTS

def print_full_plan(title: str, result):
    print("=" * 90)
    print(f"[*] {title}")
    print("=" * 90)
    print(f"Origin Base           : {result.home_name}")
    print(f"Target Time Window    : {result.start_time_str}  -->  {result.end_time_str} (Window: {result.total_budget_mins/60.0:.1f} hrs)")
    print(f"Actual Return Home    : {result.actual_return_time_str} (Completed safely before curfew)")
    print(f"Total Pandals Visited : {result.total_pandals_visited}")
    print(f"Total Trip Duration   : {result.total_elapsed_mins / 60.0:.1f} hours ({result.total_elapsed_mins} mins)")
    print(f"Total In-Transit Time : {result.total_travel_mins} mins across ~{result.total_distance_km} km")
    print("-" * 90)
    print("💵 ESTIMATED COSTING BREAKDOWN (Per Person):")
    c = result.costing
    print(f"  • Transit & Train   : ₹{c.transit_cost_min_inr} - ₹{c.transit_cost_max_inr}")
    print(f"  • Food & Dining     : ₹{c.food_cost_min_inr} - ₹{c.food_cost_max_inr}")
    print(f"  • TOTAL ESTIMATED   : ₹{c.total_cost_min_inr} - ₹{c.total_cost_max_inr}")
    print("-" * 90)
    print("🗺️ STEP-BY-STEP ITINERARY & TRANSITIONS:")
    print("-" * 90)

    for stop in result.schedule:
        if stop.transition:
            t = stop.transition
            print(f"\n  >>> MOVEMENT TO STEP {stop.stop_number}:")
            print(f"      Mode       : {t.mode} (~{t.travel_time_mins} mins, {t.distance_km} km)")
            cost_str = f"₹{t.cost_min_inr} - ₹{t.cost_max_inr}" if t.cost_max_inr > 0 else "Free"
            print(f"      Fare       : {cost_str}")
            print(f"      Guidance   : {t.instructions}\n")

        time_slot = f"{stop.arrival_time_str} - {stop.departure_time_str}"
        if stop.is_home_stop:
            print(f"[{stop.stop_number}] {stop.name} ({time_slot})")
            print(f"    ↳ {stop.description}")
        elif stop.is_food_stop:
            print(f"[{stop.stop_number}] {stop.name} ({time_slot})")
            print(f"    ↳ {stop.description}")
            print(f"    ↳ Cost Range: ₹{stop.food_cost_min} - ₹{stop.food_cost_max} per person")
        else:
            print(f"[{stop.stop_number}] PANDAL: {stop.name} ({time_slot}) | Zone: {stop.zone}")
            print(f"    ↳ Queue Wait: ~{stop.queue_wait_mins}m | Inside Darshan: ~{stop.visit_mins}m | Metro: {stop.nearest_metro}")
            print(f"    ↳ {stop.description}")

    if result.summary_notes:
        print("\n" + "-" * 90)
        print("[+] Tactical Puja Insights & Advisory:")
        for note in result.summary_notes:
            print(f"  * {note}")
    print("=" * 90 + "\n")

def main():
    optimizer = PujaHopperOptimizer()

    # User starting from Baruipur
    user_location = "Baruipur"
    lat, lon, resolved_name = geocode_location(user_location)

    # 2 distinct meals:
    # Meal 1: Main Dinner at legendary Arsalan Gariahat (Biryani) around 10:30 PM
    # Meal 2: Midnight Chai & Aloo Paratha at Balwant Singh Dhaba around 2:30 AM
    meals = [
        MealSlot(
            title="Main Dinner",
            target_hour=parse_time_str_to_float("22:30"), # 10:30 PM
            food_category="biryani",
            specific_restaurant_id="arsalan_gariahat",
            duration_mins=45
        ),
        MealSlot(
            title="Midnight Chai & Adda",
            target_hour=parse_time_str_to_float("02:30"), # 2:30 AM
            food_category="chai_snacks",
            specific_restaurant_id="balwant_singh_dhaba",
            duration_mins=30
        )
    ]

    pref = UserPreference(
        home_name=resolved_name,
        home_lat=lat,
        home_lon=lon,
        start_hour=parse_time_str_to_float("19:00"),  # 7:00 PM
        end_hour=parse_time_str_to_float("04:00"),    # 4:00 AM next morning
        preferred_zones=["South"],
        tithi="Ashtami",
        theme_preference=1.2,
        traditional_pref=1.0,
        patience_factor=1.0,
        meals=meals
    )

    res = optimizer.optimize_itinerary(pref)
    print_full_plan(
        "BARUIPUR COMMUTER WITH ARSALAN BIRYANI (10:30 PM) + BALWANT SINGH DHABA CHAI (2:30 AM)",
        res
    )

if __name__ == "__main__":
    main()
