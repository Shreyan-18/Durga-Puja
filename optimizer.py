"""
Core Optimization Engine for Durga Puja Hopping Itineraries.
Features:
- Route-Aware Restaurant Selection (finds eateries directly on the path with minimal detour).
- Multi-Meal Scheduling (Evening snacks, Dinner, Midnight chai).
- Gateway Transit Hub Guidance (Entry Metro/Station & Return Home station).
- Clear Movement Mode Tracking for every leg of the journey.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Tuple, Optional
import math
import random
import copy

from data import (
    Pandal, SAMPLE_PANDALS, FOOD_CATALOG, FoodOption,
    Restaurant, ICONIC_RESTAURANTS, TransitHub, MAJOR_TRANSIT_HUBS,
    get_transition_details, TransitionInfo, get_queue_wait_time, haversine_km,
    find_nearest_restaurant_along_route
)

@dataclass
class MealSlot:
    title: str                    # e.g., "Evening Snacks & Rolls", "Dinner", "Midnight Chai"
    target_hour: float            # 24h float, e.g. 20.5 (8:30 PM), 23.5 (11:30 PM), 2.5 (2:30 AM)
    food_category: str            # 'street_food', 'biryani', 'bengali_thali', 'chai_snacks', 'vegetarian'
    specific_restaurant_id: Optional[str] = "auto_along_route" # 'auto_along_route', specific ID, or 'street_stall'
    duration_mins: int = 35

@dataclass
class UserPreference:
    home_name: str
    home_lat: float
    home_lon: float
    start_hour: float
    end_hour: float
    preferred_zones: List[str]
    tithi: str = "Ashtami"
    theme_preference: float = 1.0
    traditional_pref: float = 1.0
    patience_factor: float = 1.0
    has_vip_pass: bool = False
    meals: List[MealSlot] = field(default_factory=list)
    max_budget_inr: Optional[int] = None
    max_meal_cost: Optional[int] = None
    planning_mode: str = "auto"
    custom_pandal_ids: List[str] = field(default_factory=list)
    include_on_route_pandals: bool = True

    @property
    def total_budget_minutes(self) -> float:
        if self.end_hour <= self.start_hour:
            duration_hours = (24.0 - self.start_hour) + self.end_hour
        else:
            duration_hours = self.end_hour - self.start_hour
        return duration_hours * 60.0

@dataclass
class ItineraryStop:
    stop_number: int
    pandal_id: str
    name: str
    zone: str
    arrival_time_str: str
    departure_time_str: str
    queue_wait_mins: float
    visit_mins: float
    nearest_metro: str
    description: str
    
    # Mode of movement from previous stop
    movement_mode: str = "Origin"
    transition: Optional[TransitionInfo] = None
    is_home_stop: bool = False
    is_food_stop: bool = False
    is_bonus_stop: bool = False
    food_cost_min: int = 0
    food_cost_max: int = 0
    lat: float = 0.0
    lon: float = 0.0

@dataclass
class CostingSummary:
    transit_cost_min_inr: int
    transit_cost_max_inr: int
    food_cost_min_inr: int
    food_cost_max_inr: int
    total_cost_min_inr: int
    total_cost_max_inr: int
    max_budget_inr: Optional[int] = None
    is_within_budget: bool = True

@dataclass
class GatewayGuidance:
    entry_gateway_name: str
    entry_gateway_line: str
    entry_instructions: str
    return_gateway_name: str
    return_gateway_line: str
    return_instructions: str

@dataclass
class ItineraryResult:
    home_name: str
    start_time_str: str
    end_time_str: str
    actual_return_time_str: str
    total_pandals_visited: int
    total_budget_mins: float
    total_elapsed_mins: float
    total_queue_mins: float
    total_travel_mins: float
    total_distance_km: float
    total_score: float
    costing: CostingSummary
    gateway: GatewayGuidance
    schedule: List[ItineraryStop]
    summary_notes: List[str]
    planning_mode: str = "auto"
    selected_pandal_count: int = 0
    unvisited_custom_pandals: List[str] = field(default_factory=list)
    bonus_pandals_added: List[str] = field(default_factory=list)

def format_hour_to_time_str(hour_float: float) -> str:
    normalized_hour = hour_float % 24.0
    h = int(normalized_hour)
    m = int(round((normalized_hour - h) * 60))
    if m >= 60:
        h = (h + 1) % 24
        m = 0
    period = "AM" if h < 12 else "PM"
    display_h = h if h in (0, 12) else (h % 12)
    if display_h == 0:
        display_h = 12
    return f"{display_h:02d}:{m:02d} {period}"

def parse_time_str_to_float(time_str: str) -> float:
    parts = time_str.strip().split(":")
    h = int(parts[0])
    m = int(parts[1]) if len(parts) > 1 else 0
    return h + (m / 60.0)

def normalize_elapsed_hours_from_start(hour: float, start_hour: float) -> float:
    if hour >= start_hour:
        return hour - start_hour
    return (24.0 - start_hour) + hour

class PujaHopperOptimizer:
    def __init__(self, pandal_pool: Optional[List[Pandal]] = None):
        self.pandal_pool = pandal_pool or SAMPLE_PANDALS

    def filter_candidates(self, prefs: UserPreference) -> List[Pandal]:
        if prefs.planning_mode == "custom_selection" and prefs.custom_pandal_ids:
            pandal_map = {p.id: p for p in self.pandal_pool}
            selected = [pandal_map[pid] for pid in prefs.custom_pandal_ids if pid in pandal_map]
            if selected:
                return selected

        if not prefs.preferred_zones:
            return self.pandal_pool
        return [p for p in self.pandal_pool if p.zone in prefs.preferred_zones]

    def calculate_stop_utility(self, pandal: Pandal, prefs: UserPreference) -> float:
        score = pandal.base_rating
        if pandal.theme_type == "Theme":
            score *= prefs.theme_preference
        elif pandal.theme_type in ("Traditional", "Bonedi_Bari"):
            score *= prefs.traditional_pref
        return score

    def determine_gateway_guidance(self, prefs: UserPreference, first_pandal: Optional[Pandal], last_pandal: Optional[Pandal]) -> GatewayGuidance:
        """Determines best entry metro/train gateway and return gateway."""
        is_south_suburb = ("baruipur" in prefs.home_name.lower() or "sonarpur" in prefs.home_name.lower())
        
        if is_south_suburb:
            entry_name = "Ballygunge Railway Junction / Kavi Subhash Metro"
            entry_line = "Sealdah South EMU Line & Blue Line Metro"
            entry_ins = "Take EMU local train from Baruipur Jn directly to Ballygunge Jn (28-35 mins, ₹10). Alight at Ballygunge to access South Kolkata pandals immediately."
            
            return_name = "Ballygunge Railway Junction (Puja Night Special EMU)"
            return_line = "Eastern Railway All-Night Puja Special"
            return_ins = "Head to Ballygunge Jn to board Eastern Railway's All-Night Puja Special EMU train directly back to Baruipur. Trains operate throughout the night on Saptami, Ashtami, and Nabami."
        else:
            first_metro = first_pandal.nearest_metro if first_pandal else "Central Kolkata"
            entry_name = f"{first_metro}"
            entry_line = "Kolkata Metro Blue Line / Suburban Network"
            entry_ins = f"Take Kolkata Metro Blue line and deboard at {first_metro} to bypass festive surface road jams."

            last_metro = last_pandal.nearest_metro if last_pandal else "Central Kolkata"
            return_name = f"{last_metro}"
            return_line = "Kolkata Metro / Taxi Stand"
            return_ins = f"Board returning metro service or hailed cab from {last_metro} directly back towards {prefs.home_name}."

        return GatewayGuidance(
            entry_gateway_name=entry_name,
            entry_gateway_line=entry_line,
            entry_instructions=entry_ins,
            return_gateway_name=return_name,
            return_gateway_line=return_line,
            return_instructions=return_ins
        )

    def find_on_route_pandal(
        self,
        current_lat: float,
        current_lon: float,
        target_lat: float,
        target_lon: float,
        visited_ids: Set[str],
        max_detour_km: float = 0.75,
        min_rating: float = 8.9
    ) -> Optional[Tuple[Pandal, float]]:
        """
        Finds a top-rated unvisited pandal directly along the corridor between
        current location and target pandal with minimal detour.
        """
        direct_dist = haversine_km(current_lat, current_lon, target_lat, target_lon)
        best_candidate: Optional[Pandal] = None
        min_detour = 999.0

        for candidate in self.pandal_pool:
            if candidate.id in visited_ids:
                continue
            if candidate.base_rating < min_rating:
                continue

            dist1 = haversine_km(current_lat, current_lon, candidate.lat, candidate.lon)
            dist2 = haversine_km(candidate.lat, candidate.lon, target_lat, target_lon)
            detour = (dist1 + dist2) - direct_dist

            # Must lie in forward progression corridor with minimal detour
            if detour <= max_detour_km and dist1 < (direct_dist + 0.3) and dist2 < (direct_dist + 0.3):
                if detour < min_detour:
                    min_detour = detour
                    best_candidate = candidate

        if best_candidate:
            return best_candidate, min_detour
        return None

    def simulate_itinerary(self, route: List[Pandal], prefs: UserPreference) -> Tuple[List[ItineraryStop], Dict[str, Any]]:
        home_lat = prefs.home_lat
        home_lon = prefs.home_lon
        current_lat = home_lat
        current_lon = home_lon
        current_location_name = prefs.home_name
        current_hour = prefs.start_hour

        total_budget = prefs.total_budget_minutes
        elapsed_mins = 0.0
        total_queue_mins = 0.0
        total_travel_mins = 0.0
        total_dist_km = 0.0
        total_transit_cost_min = 0
        total_transit_cost_max = 0
        total_food_cost_min = 0
        total_food_cost_max = 0

        sorted_meals = sorted(
            prefs.meals,
            key=lambda m: normalize_elapsed_hours_from_start(m.target_hour, prefs.start_hour)
        )
        remaining_meals = list(sorted_meals)

        stops: List[ItineraryStop] = []

        # 1. Depart from Origin
        stops.append(ItineraryStop(
            stop_number=1,
            pandal_id="home_depart",
            name=f"🏠 Depart from Origin ({prefs.home_name})",
            zone="Origin",
            arrival_time_str=format_hour_to_time_str(current_hour),
            departure_time_str=format_hour_to_time_str(current_hour),
            queue_wait_mins=0.0,
            visit_mins=0.0,
            nearest_metro="-",
            description=f"Beginning Durga Puja journey from {prefs.home_name}.",
            movement_mode="🚩 Start of Journey",
            transition=None,
            is_home_stop=True,
            lat=home_lat,
            lon=home_lon
        ))

        visited_pandals: List[Pandal] = []
        bonus_pandal_names: List[str] = []
        visited_ids: Set[str] = {p.id for p in route}

        for pandal in route:
            # Check if any scheduled meal is due BEFORE visiting this pandal
            if remaining_meals:
                next_meal = remaining_meals[0]
                curr_elapsed_hours = normalize_elapsed_hours_from_start(current_hour, prefs.start_hour)
                target_elapsed_hours = normalize_elapsed_hours_from_start(next_meal.target_hour, prefs.start_hour)

                if curr_elapsed_hours >= (target_elapsed_hours - 0.6):
                    # Smart Route-Aware Restaurant Selection
                    chosen_rest: Optional[Restaurant] = None
                    if next_meal.specific_restaurant_id and next_meal.specific_restaurant_id in ICONIC_RESTAURANTS:
                        chosen_rest = ICONIC_RESTAURANTS[next_meal.specific_restaurant_id]
                    elif next_meal.specific_restaurant_id == "auto_along_route":
                        chosen_rest, _ = find_nearest_restaurant_along_route(
                            current_lat, current_lon, pandal.lat, pandal.lon, next_meal.food_category,
                            max_cost=prefs.max_meal_cost
                        )

                    if chosen_rest:
                        m_trans = get_transition_details(
                            current_lat, current_lon, chosen_rest.lat, chosen_rest.lon,
                            current_hour, current_location_name, chosen_rest.name
                        )
                        m_arrival = current_hour + (m_trans.travel_time_mins / 60.0)
                        m_dep = m_arrival + (next_meal.duration_mins / 60.0)
                        ret_check = get_transition_details(
                            chosen_rest.lat, chosen_rest.lon, home_lat, home_lon,
                            m_dep, chosen_rest.name, prefs.home_name
                        )

                        if elapsed_mins + m_trans.travel_time_mins + next_meal.duration_mins + ret_check.travel_time_mins <= total_budget:
                            elapsed_mins += (m_trans.travel_time_mins + next_meal.duration_mins)
                            total_travel_mins += m_trans.travel_time_mins
                            total_dist_km += m_trans.distance_km
                            total_transit_cost_min += m_trans.cost_min_inr
                            total_transit_cost_max += m_trans.cost_max_inr
                            total_food_cost_min += chosen_rest.cost_min_inr
                            total_food_cost_max += chosen_rest.cost_max_inr

                            stops.append(ItineraryStop(
                                stop_number=len(stops) + 1,
                                pandal_id=f"rest_{chosen_rest.id}",
                                name=f"🍽️ {next_meal.title}: {chosen_rest.name}",
                                zone=chosen_rest.zone,
                                arrival_time_str=format_hour_to_time_str(m_arrival),
                                departure_time_str=format_hour_to_time_str(m_dep),
                                queue_wait_mins=0.0,
                                visit_mins=next_meal.duration_mins,
                                nearest_metro=chosen_rest.nearest_landmark,
                                description=f"On-route dining: {chosen_rest.description} (Specialty: {chosen_rest.specialty}).",
                                movement_mode=m_trans.mode,
                                transition=m_trans,
                                is_food_stop=True,
                                food_cost_min=chosen_rest.cost_min_inr,
                                food_cost_max=chosen_rest.cost_max_inr,
                                lat=chosen_rest.lat,
                                lon=chosen_rest.lon
                            ))
                            current_lat = chosen_rest.lat
                            current_lon = chosen_rest.lon
                            current_location_name = chosen_rest.name
                            current_hour = m_dep
                            remaining_meals.pop(0)
                    else:
                        # Street Food Stalls near current pandal
                        f_opt = FOOD_CATALOG.get(next_meal.food_category, FOOD_CATALOG["street_food"])
                        m_arrival = current_hour
                        m_dep = current_hour + (next_meal.duration_mins / 60.0)
                        ret_check = get_transition_details(
                            current_lat, current_lon, home_lat, home_lon,
                            m_dep, current_location_name, prefs.home_name
                        )
                        if elapsed_mins + next_meal.duration_mins + ret_check.travel_time_mins <= total_budget:
                            elapsed_mins += next_meal.duration_mins
                            total_food_cost_min += f_opt.cost_min_inr
                            total_food_cost_max += f_opt.cost_max_inr

                            stops.append(ItineraryStop(
                                stop_number=len(stops) + 1,
                                pandal_id=f"street_food_{len(stops)}",
                                name=f"🍽️ {next_meal.title}: {f_opt.name}",
                                zone="Local Street",
                                arrival_time_str=format_hour_to_time_str(m_arrival),
                                departure_time_str=format_hour_to_time_str(m_dep),
                                queue_wait_mins=0.0,
                                visit_mins=next_meal.duration_mins,
                                nearest_metro="-",
                                description=f"{f_opt.description} (Near {current_location_name}).",
                                movement_mode="🚶 Walking (Food Stalls)",
                                transition=TransitionInfo(
                                    mode="🚶 Immediate Walk",
                                    instructions=f"Walk to the festive food stalls and food street around {current_location_name}.",
                                    distance_km=0.1,
                                    travel_time_mins=0.0,
                                    cost_min_inr=0,
                                    cost_max_inr=0
                                ),
                                is_food_stop=True,
                                food_cost_min=f_opt.cost_min_inr,
                                food_cost_max=f_opt.cost_max_inr,
                                lat=current_lat,
                                lon=current_lon
                            ))
                            current_hour = m_dep
                            remaining_meals.pop(0)

            # Check for high-rated on-route bonus pandal opportunity between current location and pandal
            if prefs.include_on_route_pandals and len(visited_pandals) > 0:
                candidate_info = self.find_on_route_pandal(
                    current_lat, current_lon, pandal.lat, pandal.lon,
                    visited_ids=visited_ids,
                    max_detour_km=0.75,
                    min_rating=8.9
                )
                if candidate_info:
                    bonus_pandal, detour_km = candidate_info
                    b_trans = get_transition_details(
                        current_lat, current_lon, bonus_pandal.lat, bonus_pandal.lon,
                        current_hour, current_location_name, bonus_pandal.name
                    )
                    b_arr = current_hour + (b_trans.travel_time_mins / 60.0)
                    b_queue = get_queue_wait_time(
                        bonus_pandal, b_arr % 24.0, tithi=prefs.tithi, has_vip_pass=prefs.has_vip_pass
                    )
                    b_visit = bonus_pandal.avg_visit_mins
                    b_dep = b_arr + ((b_queue + b_visit) / 60.0)

                    # Next leg from bonus_pandal to the planned pandal
                    leg2_trans = get_transition_details(
                        bonus_pandal.lat, bonus_pandal.lon, pandal.lat, pandal.lon,
                        b_dep, bonus_pandal.name, pandal.name
                    )
                    leg2_arr = b_dep + (leg2_trans.travel_time_mins / 60.0)
                    leg2_queue = get_queue_wait_time(
                        pandal, leg2_arr % 24.0, tithi=prefs.tithi, has_vip_pass=prefs.has_vip_pass
                    )
                    leg2_dep = leg2_arr + ((leg2_queue + pandal.avg_visit_mins) / 60.0)
                    leg2_ret = get_transition_details(
                        pandal.lat, pandal.lon, home_lat, home_lon,
                        leg2_dep, pandal.name, prefs.home_name
                    )

                    time_with_bonus = (
                        elapsed_mins +
                        b_trans.travel_time_mins + b_queue + b_visit +
                        leg2_trans.travel_time_mins + leg2_queue + pandal.avg_visit_mins +
                        leg2_ret.travel_time_mins
                    )

                    # Only insert bonus pandal if both bonus pandal AND planned pandal + safe return fit within curfew
                    if time_with_bonus <= total_budget:
                        elapsed_mins += (b_trans.travel_time_mins + b_queue + b_visit)
                        total_travel_mins += b_trans.travel_time_mins
                        total_queue_mins += b_queue
                        total_dist_km += b_trans.distance_km
                        total_transit_cost_min += b_trans.cost_min_inr
                        total_transit_cost_max += b_trans.cost_max_inr

                        visited_pandals.append(bonus_pandal)
                        visited_ids.add(bonus_pandal.id)
                        bonus_pandal_names.append(bonus_pandal.name)

                        stops.append(ItineraryStop(
                            stop_number=len(stops) + 1,
                            pandal_id=bonus_pandal.id,
                            name=f"✨ {bonus_pandal.name} (On-Route Discovery)",
                            zone=bonus_pandal.zone,
                            arrival_time_str=format_hour_to_time_str(b_arr),
                            departure_time_str=format_hour_to_time_str(b_dep),
                            queue_wait_mins=round(b_queue, 1),
                            visit_mins=round(b_visit, 1),
                            nearest_metro=bonus_pandal.nearest_metro,
                            description=f"Direct on-route opportunity (~{detour_km:.2f} km detour): {bonus_pandal.description}",
                            movement_mode=b_trans.mode,
                            transition=b_trans,
                            is_home_stop=False,
                            is_bonus_stop=True,
                            lat=bonus_pandal.lat,
                            lon=bonus_pandal.lon
                        ))

                        current_lat = bonus_pandal.lat
                        current_lon = bonus_pandal.lon
                        current_location_name = bonus_pandal.name
                        current_hour = b_dep

            # Move to Pandal
            transition = get_transition_details(
                current_lat, current_lon, pandal.lat, pandal.lon,
                current_hour, current_location_name, pandal.name
            )

            arrival_hour = current_hour + (transition.travel_time_mins / 60.0)
            queue_wait = get_queue_wait_time(
                pandal, arrival_hour % 24.0, tithi=prefs.tithi, has_vip_pass=prefs.has_vip_pass
            )
            visit_time = pandal.avg_visit_mins
            dep_hour = arrival_hour + ((queue_wait + visit_time) / 60.0)

            return_transition = get_transition_details(
                pandal.lat, pandal.lon, home_lat, home_lon,
                dep_hour, pandal.name, prefs.home_name
            )

            projected_elapsed = elapsed_mins + transition.travel_time_mins + queue_wait + visit_time + return_transition.travel_time_mins

            if projected_elapsed > total_budget:
                break

            elapsed_mins += (transition.travel_time_mins + queue_wait + visit_time)
            total_travel_mins += transition.travel_time_mins
            total_queue_mins += queue_wait
            total_dist_km += transition.distance_km
            total_transit_cost_min += transition.cost_min_inr
            total_transit_cost_max += transition.cost_max_inr

            visited_pandals.append(pandal)

            stops.append(ItineraryStop(
                stop_number=len(stops) + 1,
                pandal_id=pandal.id,
                name=pandal.name,
                zone=pandal.zone,
                arrival_time_str=format_hour_to_time_str(arrival_hour),
                departure_time_str=format_hour_to_time_str(dep_hour),
                queue_wait_mins=round(queue_wait, 1),
                visit_mins=round(visit_time, 1),
                nearest_metro=pandal.nearest_metro,
                description=pandal.description,
                movement_mode=transition.mode,
                transition=transition,
                is_home_stop=False,
                is_bonus_stop=False,
                lat=pandal.lat,
                lon=pandal.lon
            ))

            current_lat = pandal.lat
            current_lon = pandal.lon
            current_location_name = pandal.name
            current_hour = dep_hour

        # Check any remaining scheduled meals before final return
        while remaining_meals:
            next_meal = remaining_meals[0]
            chosen_rest: Optional[Restaurant] = None
            if next_meal.specific_restaurant_id and next_meal.specific_restaurant_id in ICONIC_RESTAURANTS:
                chosen_rest = ICONIC_RESTAURANTS[next_meal.specific_restaurant_id]
            elif next_meal.specific_restaurant_id == "auto_along_route":
                chosen_rest, _ = find_nearest_restaurant_along_route(
                    current_lat, current_lon, home_lat, home_lon, next_meal.food_category,
                    max_cost=prefs.max_meal_cost
                )

            if chosen_rest:
                m_trans = get_transition_details(
                    current_lat, current_lon, chosen_rest.lat, chosen_rest.lon,
                    current_hour, current_location_name, chosen_rest.name
                )
                m_arrival = current_hour + (m_trans.travel_time_mins / 60.0)
                m_dep = m_arrival + (next_meal.duration_mins / 60.0)
                ret_check = get_transition_details(
                    chosen_rest.lat, chosen_rest.lon, home_lat, home_lon,
                    m_dep, chosen_rest.name, prefs.home_name
                )
                if elapsed_mins + m_trans.travel_time_mins + next_meal.duration_mins + ret_check.travel_time_mins <= total_budget:
                    elapsed_mins += (m_trans.travel_time_mins + next_meal.duration_mins)
                    total_travel_mins += m_trans.travel_time_mins
                    total_dist_km += m_trans.distance_km
                    total_transit_cost_min += m_trans.cost_min_inr
                    total_transit_cost_max += m_trans.cost_max_inr
                    total_food_cost_min += chosen_rest.cost_min_inr
                    total_food_cost_max += chosen_rest.cost_max_inr

                    stops.append(ItineraryStop(
                        stop_number=len(stops) + 1,
                        pandal_id=f"rest_{chosen_rest.id}",
                        name=f"🍽️ {next_meal.title}: {chosen_rest.name}",
                        zone=chosen_rest.zone,
                        arrival_time_str=format_hour_to_time_str(m_arrival),
                        departure_time_str=format_hour_to_time_str(m_dep),
                        queue_wait_mins=0.0,
                        visit_mins=next_meal.duration_mins,
                        nearest_metro=chosen_rest.nearest_landmark,
                        description=f"On-route dining: {chosen_rest.description} (Specialty: {chosen_rest.specialty}).",
                        movement_mode=m_trans.mode,
                        transition=m_trans,
                        is_food_stop=True,
                        food_cost_min=chosen_rest.cost_min_inr,
                        food_cost_max=chosen_rest.cost_max_inr,
                        lat=chosen_rest.lat,
                        lon=chosen_rest.lon
                    ))
                    current_lat = chosen_rest.lat
                    current_lon = chosen_rest.lon
                    current_location_name = chosen_rest.name
                    current_hour = m_dep
                    remaining_meals.pop(0)
                else:
                    break
            else:
                f_opt = FOOD_CATALOG.get(next_meal.food_category, list(FOOD_CATALOG.values())[0])
                m_arrival = current_hour
                m_dep = current_hour + (next_meal.duration_mins / 60.0)
                ret_check = get_transition_details(
                    current_lat, current_lon, home_lat, home_lon,
                    m_dep, current_location_name, prefs.home_name
                )
                if elapsed_mins + next_meal.duration_mins + ret_check.travel_time_mins <= total_budget:
                    elapsed_mins += next_meal.duration_mins
                    total_food_cost_min += f_opt.cost_min_inr
                    total_food_cost_max += f_opt.cost_max_inr

                    stops.append(ItineraryStop(
                        stop_number=len(stops) + 1,
                        pandal_id=f"street_food_{len(stops)}",
                        name=f"🍽️ {next_meal.title}: {f_opt.name}",
                        zone="Local Street",
                        arrival_time_str=format_hour_to_time_str(m_arrival),
                        departure_time_str=format_hour_to_time_str(m_dep),
                        queue_wait_mins=0.0,
                        visit_mins=next_meal.duration_mins,
                        nearest_metro="-",
                        description=f"{f_opt.description} (Near {current_location_name}).",
                        movement_mode="🚶 Walking (Food Stalls)",
                        transition=TransitionInfo(
                            mode="🚶 Immediate Walk",
                            instructions=f"Walk to the festive food stalls around {current_location_name}.",
                            distance_km=0.1,
                            travel_time_mins=0.0,
                            cost_min_inr=0,
                            cost_max_inr=0
                        ),
                        is_food_stop=True,
                        food_cost_min=f_opt.cost_min_inr,
                        food_cost_max=f_opt.cost_max_inr,
                        lat=current_lat,
                        lon=current_lon
                    ))
                    current_hour = m_dep
                    remaining_meals.pop(0)
                else:
                    break

        # Final Return Journey back to Origin/Home
        if len(visited_pandals) > 0:
            return_transition = get_transition_details(
                current_lat, current_lon, home_lat, home_lon,
                current_hour, current_location_name, f"Home ({prefs.home_name})"
            )
            elapsed_mins += return_transition.travel_time_mins
            total_travel_mins += return_transition.travel_time_mins
            total_dist_km += return_transition.distance_km
            total_transit_cost_min += return_transition.cost_min_inr
            total_transit_cost_max += return_transition.cost_max_inr
            return_hour = current_hour + (return_transition.travel_time_mins / 60.0)

            stops.append(ItineraryStop(
                stop_number=len(stops) + 1,
                pandal_id="home_return",
                name=f"🏡 Return Safe at Origin ({prefs.home_name})",
                zone="Destination",
                arrival_time_str=format_hour_to_time_str(return_hour),
                departure_time_str=format_hour_to_time_str(return_hour),
                queue_wait_mins=0.0,
                visit_mins=0.0,
                nearest_metro="-",
                description=f"Journey completed comfortably within your target window. Rest well!",
                movement_mode=return_transition.mode,
                transition=return_transition,
                is_home_stop=True,
                lat=home_lat,
                lon=home_lon
            ))

        is_within_budget = True
        if prefs.max_budget_inr and prefs.max_budget_inr > 0:
            is_within_budget = (total_transit_cost_min + total_food_cost_min) <= prefs.max_budget_inr

        costing = CostingSummary(
            transit_cost_min_inr=total_transit_cost_min,
            transit_cost_max_inr=total_transit_cost_max,
            food_cost_min_inr=total_food_cost_min,
            food_cost_max_inr=total_food_cost_max,
            total_cost_min_inr=total_transit_cost_min + total_food_cost_min,
            total_cost_max_inr=total_transit_cost_max + total_food_cost_max,
            max_budget_inr=prefs.max_budget_inr,
            is_within_budget=is_within_budget
        )

        gateway = self.determine_gateway_guidance(
            prefs,
            visited_pandals[0] if visited_pandals else None,
            visited_pandals[-1] if visited_pandals else None
        )

        stats = {
            "elapsed_mins": round(elapsed_mins, 1),
            "total_queue_mins": round(total_queue_mins, 1),
            "total_travel_mins": round(total_travel_mins, 1),
            "total_distance_km": round(total_dist_km, 1),
            "pandal_count": len(visited_pandals),
            "bonus_pandals": bonus_pandal_names,
            "costing": costing,
            "gateway": gateway
        }
        return stops, stats

    def evaluate_route_objective(self, route: List[Pandal], prefs: UserPreference, candidate_count: int = 0) -> float:
        stops, stats = self.simulate_itinerary(route, prefs)
        if stats["pandal_count"] == 0:
            return -9999.0

        pandal_stops = [s for s in stops if not s.is_home_stop and not s.is_food_stop]
        visited_ids = {s.pandal_id for s in pandal_stops}
        visited_pandals = [p for p in route if p.id in visited_ids]

        if prefs.planning_mode == "custom_selection" and prefs.custom_pandal_ids:
            total_target = candidate_count if candidate_count > 0 else len(prefs.custom_pandal_ids)
            coverage_reward = len(visited_pandals) * 250.0
            unvisited_penalty = (total_target - len(visited_pandals)) * 350.0
            queue_penalty = stats["total_queue_mins"] * (0.40 / max(prefs.patience_factor, 0.2))
            travel_penalty = stats["total_travel_mins"] * 0.45
            return coverage_reward - unvisited_penalty - queue_penalty - travel_penalty

        total_utility = sum(self.calculate_stop_utility(p, prefs) * 10.0 for p in visited_pandals)

        queue_penalty_weight = 0.55 / max(prefs.patience_factor, 0.2)
        queue_penalty = stats["total_queue_mins"] * queue_penalty_weight
        travel_penalty = stats["total_travel_mins"] * 0.40
        quantity_bonus = len(pandal_stops) * 16.0

        return total_utility - queue_penalty - travel_penalty + quantity_bonus

    def optimize_itinerary(self, prefs: UserPreference, max_iterations: int = 1400) -> ItineraryResult:
        candidates = self.filter_candidates(prefs)
        if not candidates:
            candidates = self.pandal_pool

        def init_sort_key(p: Pandal):
            dist = haversine_km(prefs.home_lat, prefs.home_lon, p.lat, p.lon)
            return (dist / max(p.base_rating, 1.0))

        cand_count = len(candidates)
        initial_route = sorted(candidates, key=init_sort_key)
        best_route = copy.copy(initial_route)
        best_score = self.evaluate_route_objective(best_route, prefs, candidate_count=cand_count)

        current_route = copy.copy(best_route)
        current_score = best_score

        temperature = 100.0
        cooling_rate = 0.995

        for i in range(max_iterations):
            neighbor = copy.copy(current_route)
            move_type = random.choice(["swap", "2opt", "shuffle_sub"])

            if move_type == "swap" and len(neighbor) >= 2:
                idx1, idx2 = random.sample(range(len(neighbor)), 2)
                neighbor[idx1], neighbor[idx2] = neighbor[idx2], neighbor[idx1]
            elif move_type == "2opt" and len(neighbor) >= 4:
                idx1 = random.randint(0, len(neighbor) - 3)
                idx2 = random.randint(idx1 + 2, len(neighbor) - 1)
                neighbor[idx1:idx2] = reversed(neighbor[idx1:idx2])
            elif move_type == "shuffle_sub" and len(neighbor) >= 3:
                idx1 = random.randint(0, len(neighbor) - 3)
                sub = neighbor[idx1:idx1+3]
                random.shuffle(sub)
                neighbor[idx1:idx1+3] = sub

            neighbor_score = self.evaluate_route_objective(neighbor, prefs, candidate_count=cand_count)
            delta = neighbor_score - current_score

            if delta > 0 or math.exp(delta / max(temperature, 1e-4)) > random.random():
                current_route = neighbor
                current_score = neighbor_score
                if neighbor_score > best_score:
                    best_route = copy.copy(neighbor)
                    best_score = neighbor_score

            temperature *= cooling_rate

        final_stops, final_stats = self.simulate_itinerary(best_route, prefs)

        start_time_str = format_hour_to_time_str(prefs.start_hour)
        end_time_str = format_hour_to_time_str(prefs.end_hour)
        actual_return_time_str = final_stops[-1].arrival_time_str if final_stops else end_time_str

        notes = []
        costing = final_stats["costing"]
        gateway = final_stats["gateway"]
        bonus_pandals = final_stats.get("bonus_pandals", [])
        notes.append(f"💰 Total Estimated Budget: ₹{costing.total_cost_min_inr} - ₹{costing.total_cost_max_inr} per person (Transit: ₹{costing.transit_cost_min_inr}-₹{costing.transit_cost_max_inr}, Food & Meals: ₹{costing.food_cost_min_inr}-₹{costing.food_cost_max_inr}).")
        notes.append(f"🚉 Entry Transit Gateway: {gateway.entry_gateway_name} ({gateway.entry_gateway_line}).")
        notes.append(f"🏡 Return Transit Gateway: {gateway.return_gateway_name}.")
        
        if bonus_pandals:
            notes.append(f"✨ On-Route Discovery Bonus: Added {len(bonus_pandals)} top-rated pandal(s) directly along your walking corridor ({', '.join(bonus_pandals)}) without causing any detour delay!")
        if len(prefs.meals) > 1:
            notes.append(f"🍽️ Multi-Meal Schedule: Successfully placed {len(prefs.meals)} culinary stops directly along your path.")
        if prefs.start_hour >= 23.0 or prefs.start_hour < 4.0:
            notes.append("🌙 Midnight Hopping: Queues drop by ~60% after 2:30 AM; roads open up for faster connections.")

        pandal_stops = [s for s in final_stops if not s.is_home_stop and not s.is_food_stop]
        visited_ids = {s.pandal_id for s in pandal_stops}
        unvisited_names = []
        if prefs.planning_mode == "custom_selection" and prefs.custom_pandal_ids:
            unvisited_names = [p.name for p in candidates if p.id not in visited_ids]
            if len(unvisited_names) == 0:
                notes.insert(0, f"🎯 Perfect Custom Route: Successfully planned the optimal sequence for all {len(candidates)} of your chosen pandals!")
            else:
                notes.insert(0, f"⏱️ Time Window Advisory: Fitted {len(visited_ids)} of your {len(candidates)} chosen pandals within the {prefs.total_budget_minutes/60:.1f}-hr window. Remaining: {', '.join(unvisited_names[:3])}{'...' if len(unvisited_names)>3 else ''}.")

        return ItineraryResult(
            home_name=prefs.home_name,
            start_time_str=start_time_str,
            end_time_str=end_time_str,
            actual_return_time_str=actual_return_time_str,
            total_pandals_visited=final_stats["pandal_count"],
            total_budget_mins=prefs.total_budget_minutes,
            total_elapsed_mins=final_stats["elapsed_mins"],
            total_queue_mins=final_stats["total_queue_mins"],
            total_travel_mins=final_stats["total_travel_mins"],
            total_distance_km=final_stats["total_distance_km"],
            total_score=round(best_score, 1),
            costing=costing,
            gateway=gateway,
            schedule=final_stops,
            summary_notes=notes,
            planning_mode=prefs.planning_mode,
            selected_pandal_count=len(prefs.custom_pandal_ids) if prefs.planning_mode == "custom_selection" else 0,
            unvisited_custom_pandals=unvisited_names,
            bonus_pandals_added=bonus_pandals
        )
