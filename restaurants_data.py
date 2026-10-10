"""
Curated Catalog of 45+ Iconic Kolkata & Bengal Heritage Restaurants,
Street Food Legends, Mid-Night Cafes, and Cuisine Categorization.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

@dataclass
class Restaurant:
    id: str
    name: str
    specialty: str
    zone: str  # 'South', 'North', 'Central', 'East_VIP', 'East_SaltLake', 'Howrah'
    lat: float
    lon: float
    nearest_landmark: str
    cost_min_inr: int
    cost_max_inr: int
    description: str

@dataclass
class FoodOption:
    id: str
    category: str
    name: str
    description: str
    cost_min_inr: int
    cost_max_inr: int
    typical_duration_mins: int

# -------------------------------------------------------------------------
# 12 RICH CUISINE PREFERENCE TIERS
# -------------------------------------------------------------------------
FOOD_CATALOG: Dict[str, FoodOption] = {
    "biryani": FoodOption(
        id="biryani",
        category="Kolkata Biryani / Mughlai",
        name="👑 Royal Kolkata Biryani & Chaap (Arsalan, Shiraz, Aminia, Royal)",
        description="Aromatic long-grain basmati, succulent meat, iconic melt-in-mouth aloo, chicken chaap, and firni.",
        cost_min_inr=350,
        cost_max_inr=650,
        typical_duration_mins=45
    ),
    "bengali_heritage": FoodOption(
        id="bengali_heritage",
        category="Bengali Cuisine / Zamindari Thali",
        name="🐟 Authentic Bengali Zamindari Feast (Ilish, Paturi, Kosha Mangsho)",
        description="Basanti pulao, bhetki paturi, daab chingri, kosha mangsho, luchi, chholar dal, followed by mishti doi.",
        cost_min_inr=450,
        cost_max_inr=950,
        typical_duration_mins=50
    ),
    "street_rolls_cutlets": FoodOption(
        id="street_rolls_cutlets",
        category="Cabin Cutlets & Kathi Rolls",
        name="🌯 Kolkata Kathi Rolls, Kabiraji & Cabin Cutlets (Nizam's, Kusum, Mitra Cafe)",
        description="Crispy paratha rolls (egg-chicken/paneer), Diamond fish fry, mutton kabiraji with fiery kasundi.",
        cost_min_inr=140,
        cost_max_inr=280,
        typical_duration_mins=30
    ),
    "tangra_chinese": FoodOption(
        id="tangra_chinese",
        category="Tangra Chinatown & Indo-Chinese",
        name="🥢 Tangra Chinatown Indo-Chinese Feast (Golden Joy, Beijing, Chowman)",
        description="Wok-tossed Hakka noodles, chilli chicken, golden fried prawns, crispy konjee lamb, and momos.",
        cost_min_inr=300,
        cost_max_inr=650,
        typical_duration_mins=45
    ),
    "park_street_continental": FoodOption(
        id="park_street_continental",
        category="Continental & Heritage Grills",
        name="🥩 Park Street Heritage Continental & Grills (Peter Cat, Mocambo)",
        description="Legendary Chelo Kebab, sizzlers, devilled crab, chicken tetrazzini, and vintage Park Street charm.",
        cost_min_inr=550,
        cost_max_inr=1100,
        typical_duration_mins=55
    ),
    "chai_dhaba": FoodOption(
        id="chai_dhaba",
        category="Midnight Dhaba & Bharer Cha",
        name="☕ Midnight Bharer Cha, Club Kochuri & Dhaba Parathas (Balwant Singh, Sharma)",
        description="Clay cup (bhar) piping hot kesar tea, doodh-cola, club kachoris, tandoori parathas, and tadka.",
        cost_min_inr=70,
        cost_max_inr=200,
        typical_duration_mins=25
    ),
    "bengali_sweets": FoodOption(
        id="bengali_sweets",
        category="Bengal Mishti Pilgrimage",
        name="🍨 Heritage Bengal Mishti Pilgrimage (Balaram Mullick, Nobin Das, Chittaranjan)",
        description="Baked rosogolla, nolen gur sandesh, hot pantua, mishti doi, kacha golla, and radhaballabhi.",
        cost_min_inr=80,
        cost_max_inr=220,
        typical_duration_mins=25
    ),
    "kolkata_chaat": FoodOption(
        id="kolkata_chaat",
        category="Street Chaat & Phuchka Trail",
        name="🌶️ Kolkata Street Phuchka & Spicy Chaat Trail",
        description="Crispy gondhoraj phuchka, churmur, dahi phuchka, aloo dum, ghugni, and festive roadside chaat.",
        cost_min_inr=60,
        cost_max_inr=150,
        typical_duration_mins=20
    ),
    "pure_veg_jain": FoodOption(
        id="pure_veg_jain",
        category="Pure Vegetarian & Marwari Delights",
        name="🌿 Pure Vegetarian Delights & Marwari Tiffin (Maharaja, Haldiram's, Tewari)",
        description="Fluffy hing kochuri, chilla, dal baati churma, pav bhaji, paneer tikka, and pure ghee sweets.",
        cost_min_inr=150,
        cost_max_inr=350,
        typical_duration_mins=35
    ),
    "cafe_bakery": FoodOption(
        id="cafe_bakery",
        category="Heritage European Cafe & Bakery",
        name="🥐 European Cafe, Confectionery & Coffee (Flurys, Coffee House)",
        description="English breakfast, rum balls, cream horns, darjeeling tea, and intellectual adda coffee.",
        cost_min_inr=150,
        cost_max_inr=450,
        typical_duration_mins=35
    ),
    "south_indian": FoodOption(
        id="south_indian",
        category="South Indian Tiffin",
        name="🥞 South Indian Quick Tiffin (Ghee Roast Dosa, Idli-Vada)",
        description="Crispy Mysore masala dosa, piping hot sambar-vada, and filter coffee.",
        cost_min_inr=120,
        cost_max_inr=250,
        typical_duration_mins=30
    ),
    "tibetan_momos": FoodOption(
        id="tibetan_momos",
        category="Momos & Himalayan Bites",
        name="🥟 Steamed Momos, Wonton & Thukpa",
        description="Juicy steamed pork/chicken/veg momos with spicy red chilli dip and piping hot soup.",
        cost_min_inr=100,
        cost_max_inr=220,
        typical_duration_mins=25
    )
}

# -------------------------------------------------------------------------
# MASTER CATALOG OF 45+ ICONIC RESTAURANTS
# -------------------------------------------------------------------------
ICONIC_RESTAURANTS: Dict[str, Restaurant] = {
    # --- SOUTH KOLKATA: BALLYGUNGE, GARIAHAT, KALIGHAT, BHOWANIPORE ---
    "arsalan_gariahat": Restaurant(
        id="arsalan_gariahat",
        name="Arsalan (Gariahat / 7-Point)",
        specialty="Kolkata Biryani / Mughlai",
        zone="South",
        lat=22.5195,
        lon=88.3660,
        nearest_landmark="Gariahat Crossing / Ekdalia",
        cost_min_inr=380,
        cost_max_inr=650,
        description="The quintessential Kolkata mutton/chicken biryani with melt-in-mouth aloo, chaap, and firni."
    ),
    "six_ballygunge_place": Restaurant(
        id="six_ballygunge_place",
        name="6 Ballygunge Place (Ballygunge)",
        specialty="Bengali Cuisine / Zamindari Thali",
        zone="South",
        lat=22.5255,
        lon=88.3648,
        nearest_landmark="Ballygunge / Ekdalia",
        cost_min_inr=650,
        cost_max_inr=1100,
        description="Premier heritage bungalow serving Daab Chingri, Kosha Mangsho, Bhetki Paturi, and Chhanar Malpoa."
    ),
    "bhojohori_manna_ekdalia": Restaurant(
        id="bhojohori_manna_ekdalia",
        name="Bhojohori Manna (Ekdalia / Gariahat)",
        specialty="Bengali Cuisine / Zamindari Thali",
        zone="South",
        lat=22.5210,
        lon=88.3650,
        nearest_landmark="Ekdalia Evergreen Club",
        cost_min_inr=350,
        cost_max_inr=650,
        description="Authentic homestyle Bengali food: Ilish bhapa, Goalondo steamer curry, basanti pulao, and mishti doi."
    ),
    "kasturi_hindustan_park": Restaurant(
        id="kasturi_hindustan_park",
        name="Kasturi Restaurant (Hindustan Park)",
        specialty="Bengali Cuisine / Zamindari Thali",
        zone="South",
        lat=22.5190,
        lon=88.3615,
        nearest_landmark="Hindustan Park / Tridhara",
        cost_min_inr=350,
        cost_max_inr=650,
        description="Pioneers of Dhakai Bengali cuisine: legendary Kochu Pata Chingri, Bhetki Bhapa, and Mutton Kasha."
    ),
    "aminia_golpark": Restaurant(
        id="aminia_golpark",
        name="Aminia (Golpark / Gariahat)",
        specialty="Kolkata Biryani / Mughlai",
        zone="South",
        lat=22.5140,
        lon=88.3685,
        nearest_landmark="Golpark Ramakrishna Mission",
        cost_min_inr=350,
        cost_max_inr=600,
        description="Classic Awadhi-Kolkata biryani, pasinda kebab, and rich gravies."
    ),
    "oudh_1590_deshapriya": Restaurant(
        id="oudh_1590_deshapriya",
        name="Oudh 1590 (Deshapriya Park)",
        specialty="Kolkata Biryani / Mughlai",
        zone="South",
        lat=22.5180,
        lon=88.3550,
        nearest_landmark="Deshapriya Park / Tridhara",
        cost_min_inr=500,
        cost_max_inr=850,
        description="Period dining ambiance offering Raan Biryani, Galawati Kebab, and Shahi Tukda."
    ),
    "campari_gariahat": Restaurant(
        id="campari_gariahat",
        name="Campari (Gariahat)",
        specialty="Cabin Cutlets & Kathi Rolls",
        zone="South",
        lat=22.5190,
        lon=88.3640,
        nearest_landmark="Gariahat Crossing",
        cost_min_inr=140,
        cost_max_inr=260,
        description="Legendary fry stop: Crunchy Fish Roll, Devilled Crab, and Chicken Cutlet with spicy Kasundi."
    ),
    "beduin_gariahat": Restaurant(
        id="beduin_gariahat",
        name="Beduin Rolls (Gariahat)",
        specialty="Cabin Cutlets & Kathi Rolls",
        zone="South",
        lat=22.5200,
        lon=88.3645,
        nearest_landmark="Gariahat Market",
        cost_min_inr=110,
        cost_max_inr=220,
        description="Crisp parathas loaded with succulent chicken tikka, eggs, and freshly sliced onions."
    ),
    "bhoj_company_gariahat": Restaurant(
        id="bhoj_company_gariahat",
        name="The Bhoj Company (Gariahat)",
        specialty="Bengali Cuisine / Zamindari Thali",
        zone="South",
        lat=22.5208,
        lon=88.3642,
        nearest_landmark="Gariahat Pantaloons",
        cost_min_inr=380,
        cost_max_inr=700,
        description="Traditional Bengali feast: Chingri Malaikari, Bhetki Gondhoraj, and Aloo Posto."
    ),
    "hatari_triangular_park": Restaurant(
        id="hatari_triangular_park",
        name="Hatari (Triangular Park)",
        specialty="Tangra Chinatown & Indo-Chinese",
        zone="South",
        lat=22.5175,
        lon=88.3565,
        nearest_landmark="Triangular Park / Deshapriya",
        cost_min_inr=320,
        cost_max_inr=580,
        description="Popular dining institution for Kolkata-style Chilli Chicken, Hakka Chowmein, and Crispy Pepper Fish."
    ),
    "balwant_singh_dhaba": Restaurant(
        id="balwant_singh_dhaba",
        name="Balwant Singh Dhaba (Bhowanipore)",
        specialty="Midnight Dhaba & Bharer Cha",
        zone="South",
        lat=22.5320,
        lon=88.3450,
        nearest_landmark="Netaji Bhavan Metro / Harish Mukherjee Rd",
        cost_min_inr=90,
        cost_max_inr=240,
        description="Iconic midnight haven famous for 'Doodh-Cola', piping hot clay-cup kesar tea, club kachori, and aloo paratha."
    ),
    "sharma_tea_stall": Restaurant(
        id="sharma_tea_stall",
        name="Sharma Tea House (Ashutosh Mukherjee Rd)",
        specialty="Midnight Dhaba & Bharer Cha",
        zone="South",
        lat=22.5340,
        lon=88.3510,
        nearest_landmark="Netaji Bhavan Metro",
        cost_min_inr=60,
        cost_max_inr=160,
        description="24-hour hotspot for piping hot masala bharer cha, hing kachori, jalebi, and gulab jamun."
    ),
    "maharaja_maharani": Restaurant(
        id="maharaja_maharani",
        name="Maharaja & Maharani (Sarat Bose Road)",
        specialty="Pure Vegetarian & Marwari Delights",
        zone="South",
        lat=22.5230,
        lon=88.3520,
        nearest_landmark="Sarat Bose Road / Lansdowne",
        cost_min_inr=80,
        cost_max_inr=180,
        description="Legendary breakfast & snack institution: piping hot hing kochuri, radhaballabhi, and syrupy jalebis."
    ),
    "bijoli_grill_bhawanipur": Restaurant(
        id="bijoli_grill_bhawanipur",
        name="Bijoli Grill (Bhowanipore)",
        specialty="Cabin Cutlets & Kathi Rolls",
        zone="South",
        lat=22.5280,
        lon=88.3470,
        nearest_landmark="Jatin Das Park Metro",
        cost_min_inr=200,
        cost_max_inr=450,
        description="Historic heritage catering titan: famous Fish Orly, Prawn Cutlet, and Diamond Fish Fry."
    ),
    "balaram_mullick_bhowanipore": Restaurant(
        id="balaram_mullick_bhowanipore",
        name="Balaram Mullick & Radharaman Mullick (Bhowanipore)",
        specialty="Bengal Mishti Pilgrimage",
        zone="South",
        lat=22.5310,
        lon=88.3470,
        nearest_landmark="Netaji Bhavan Metro",
        cost_min_inr=80,
        cost_max_inr=250,
        description="Legendary sweet innovators: Baked Rosogolla, Mishti Doi, Nolen Gur Soufflé, and Chhanar Jilapi."
    ),

    # --- BEHALA & DIAMOND HARBOUR ROAD ---
    "chowman_behala": Restaurant(
        id="chowman_behala",
        name="Chowman (Behala Chowrasta)",
        specialty="Tangra Chinatown & Indo-Chinese",
        zone="South",
        lat=22.4935,
        lon=88.3125,
        nearest_landmark="Behala Chowrasta / Tram Depot",
        cost_min_inr=320,
        cost_max_inr=600,
        description="Favorite neighborhood Chinese eatery: Wok-tossed noodles, Kung Pao chicken, and prawn balls."
    ),
    "royal_feast_behala": Restaurant(
        id="royal_feast_behala",
        name="Royal Feast Biryani (Behala Sakher Bazar)",
        specialty="Kolkata Biryani / Mughlai",
        zone="South",
        lat=22.4830,
        lon=88.3110,
        nearest_landmark="Sakher Bazar / Barisha Club",
        cost_min_inr=260,
        cost_max_inr=480,
        description="Popular South-West Kolkata biryani hotspot serving Dum Biryani with tender aloo and chicken chaap."
    ),
    "bhojohori_manna_taratala": Restaurant(
        id="bhojohori_manna_taratala",
        name="Bhojohori Manna (New Alipore / Taratala)",
        specialty="Bengali Cuisine / Zamindari Thali",
        zone="South",
        lat=22.5110,
        lon=88.3240,
        nearest_landmark="Taratala Crossing / Suruchi Sangha",
        cost_min_inr=350,
        cost_max_inr=650,
        description="Traditional Bengali dining right near Suruchi Sangha and Behala entry gates."
    ),

    # --- NORTH KOLKATA: SHYAMBAZAR, SOVABAZAR, BAGBAZAR, HATIBAGAN ---
    "mitra_cafe_sovabazar": Restaurant(
        id="mitra_cafe_sovabazar",
        name="Mitra Cafe (Sovabazar / North Kolkata)",
        specialty="Cabin Cutlets & Kathi Rolls",
        zone="North",
        lat=22.5970,
        lon=88.3660,
        nearest_landmark="Sovabazar Metro Station",
        cost_min_inr=180,
        cost_max_inr=350,
        description="Heritage culinary institution (1910): Diamond Fish Fry, Kabiraji cutlet, and Mutton Brain Chop."
    ),
    "golbari_shyambazar": Restaurant(
        id="golbari_shyambazar",
        name="Golbari (Shyambazar 5-Point)",
        specialty="Bengali Cuisine / Zamindari Thali",
        zone="North",
        lat=22.6020,
        lon=88.3710,
        nearest_landmark="Shyambazar 5-Point Crossing",
        cost_min_inr=220,
        cost_max_inr=420,
        description="90-year-old culinary institution famous for jet-black spicy Kosha Mangsho and soft luchi/parathas."
    ),
    "allen_kitchen_sovabazar": Restaurant(
        id="allen_kitchen_sovabazar",
        name="Allen Kitchen (Shobhabazar)",
        specialty="Cabin Cutlets & Kathi Rolls",
        zone="North",
        lat=22.5960,
        lon=88.3640,
        nearest_landmark="Shobhabazar Metro",
        cost_min_inr=190,
        cost_max_inr=380,
        description="135-year-old culinary monument famed for Pure Ghee Fried Prawn Cutlet and fish roll."
    ),
    "arsalan_hatibagan": Restaurant(
        id="arsalan_hatibagan",
        name="Arsalan (Hatibagan)",
        specialty="Kolkata Biryani / Mughlai",
        zone="North",
        lat=22.5950,
        lon=88.3730,
        nearest_landmark="Hatibagan Market / Star Theatre",
        cost_min_inr=380,
        cost_max_inr=650,
        description="Arsalan's bustling North Kolkata hub for aromatic Biryani and juicy reshmi kebabs."
    ),
    "bhojohori_manna_hatibagan": Restaurant(
        id="bhojohori_manna_hatibagan",
        name="Bhojohori Manna (Star Theatre / Hatibagan)",
        specialty="Bengali Cuisine / Zamindari Thali",
        zone="North",
        lat=22.5940,
        lon=88.3720,
        nearest_landmark="Star Theatre",
        cost_min_inr=350,
        cost_max_inr=650,
        description="Authentic homestyle Bengali delicacies right on the Hatibagan hopping corridor."
    ),
    "chittaranjan_mishti_sovabazar": Restaurant(
        id="chittaranjan_mishti_sovabazar",
        name="Chittaranjan Sweet Traders (Sovabazar)",
        specialty="Bengal Mishti Pilgrimage",
        zone="North",
        lat=22.5980,
        lon=88.3670,
        nearest_landmark="Sovabazar Metro",
        cost_min_inr=70,
        cost_max_inr=200,
        description="World-renowned for the fluffiest, spongiest white Rosogollas and authentic Madhuparka."
    ),
    "nobin_chandra_das_bagbazar": Restaurant(
        id="nobin_chandra_das_bagbazar",
        name="Nobin Chandra Das (Bagbazar)",
        specialty="Bengal Mishti Pilgrimage",
        zone="North",
        lat=22.6025,
        lon=88.3660,
        nearest_landmark="Bagbazar Sarbojanin Pandal",
        cost_min_inr=80,
        cost_max_inr=220,
        description="The legendary creator of the sponge Rosogolla (1868); landmark stop near Bagbazar ghats."
    ),
    "dada_boudi_barrackpore": Restaurant(
        id="dada_boudi_barrackpore",
        name="Dada Boudi Biryani (Barrackpore)",
        specialty="Kolkata Biryani / Mughlai",
        zone="North",
        lat=22.7660,
        lon=88.3680,
        nearest_landmark="Barrackpore Railway Station",
        cost_min_inr=450,
        cost_max_inr=750,
        description="Culinary pilgrimage for massive succulent mutton pieces, fragrant long-grain rice, and unlimited gravy."
    ),

    # --- CENTRAL KOLKATA: PARK STREET, COLLEGE STREET, BARA BAZAR ---
    "peter_cat_park_street": Restaurant(
        id="peter_cat_park_street",
        name="Peter Cat (Park Street)",
        specialty="Continental & Heritage Grills",
        zone="Central",
        lat=22.5530,
        lon=88.3535,
        nearest_landmark="Park Street Metro",
        cost_min_inr=600,
        cost_max_inr=1100,
        description="Legendary restaurant famous for the iconic Chelo Kebab with buttered rice, grilled tomatoes, and sizzlers."
    ),
    "mocambo_park_street": Restaurant(
        id="mocambo_park_street",
        name="Mocambo (Park Street)",
        specialty="Continental & Heritage Grills",
        zone="Central",
        lat=22.5525,
        lon=88.3530,
        nearest_landmark="Park Street Metro",
        cost_min_inr=650,
        cost_max_inr=1200,
        description="1950s Continental icon famed for Devilled Crab, Chicken Tetrazzini, Fish Florentine, and sizzling grills."
    ),
    "flurys_park_street": Restaurant(
        id="flurys_park_street",
        name="Flurys Tearoom (Park Street)",
        specialty="Heritage European Cafe & Bakery",
        zone="Central",
        lat=22.5535,
        lon=88.3525,
        nearest_landmark="Park Street",
        cost_min_inr=300,
        cost_max_inr=750,
        description="Quintessential European tearoom (1927): English Breakfast, legendary Rum Balls, baba cake, and Darjeeling tea."
    ),
    "kusum_rolls_park_street": Restaurant(
        id="kusum_rolls_park_street",
        name="Kusum Rolls (Park Street)",
        specialty="Cabin Cutlets & Kathi Rolls",
        zone="Central",
        lat=22.5510,
        lon=88.3525,
        nearest_landmark="Park Street Metro",
        cost_min_inr=120,
        cost_max_inr=240,
        description="The benchmark of Kolkata Kathi Rolls: flaky parathas wrapped with spiced double chicken, egg, and green chillies."
    ),
    "nizams_new_market": Restaurant(
        id="nizams_new_market",
        name="Nizam's (New Market / Esplanade)",
        specialty="Cabin Cutlets & Kathi Rolls",
        zone="Central",
        lat=22.5595,
        lon=88.3530,
        nearest_landmark="New Market / Esplanade Metro",
        cost_min_inr=130,
        cost_max_inr=260,
        description="The historic 1932 birthplace of the Kathi Roll: juicy beef/mutton/chicken kebabs rolled in roasted paratha."
    ),
    "shiraz_park_circus": Restaurant(
        id="shiraz_park_circus",
        name="Shiraz Golden Restaurant (Park Circus)",
        specialty="Kolkata Biryani / Mughlai",
        zone="Central",
        lat=22.5442,
        lon=88.3665,
        nearest_landmark="Park Circus 7-Point",
        cost_min_inr=380,
        cost_max_inr=650,
        description="Famed for legendary Kolkata mutton chaap, creamy rezala, and authentic Dum Biryani since decades."
    ),
    "arsalan_park_circus": Restaurant(
        id="arsalan_park_circus",
        name="Arsalan Flagship (Park Circus 7-Point)",
        specialty="Kolkata Biryani / Mughlai",
        zone="Central",
        lat=22.5435,
        lon=88.3670,
        nearest_landmark="Park Circus 7-Point",
        cost_min_inr=400,
        cost_max_inr=700,
        description="The mega flagship branch; high-capacity festive dining with piping hot Awadhi-Kolkata Biryani."
    ),
    "royal_indian_hotel_chitpur": Restaurant(
        id="royal_indian_hotel_chitpur",
        name="Royal Indian Hotel (Chitpur / Bara Bazar)",
        specialty="Kolkata Biryani / Mughlai",
        zone="Central",
        lat=22.5830,
        lon=88.3600,
        nearest_landmark="Nakhoda Masjid / Chitpur",
        cost_min_inr=320,
        cost_max_inr=580,
        description="1905 heritage culinary titan famous for royal Lucknowi Mutton Chaap and Potato-free Shahi Mutton Biryani."
    ),
    "anadi_cabin_dharmatala": Restaurant(
        id="anadi_cabin_dharmatala",
        name="Anadi Cabin (Esplanade)",
        specialty="Cabin Cutlets & Kathi Rolls",
        zone="Central",
        lat=22.5630,
        lon=88.3535,
        nearest_landmark="Esplanade Metro",
        cost_min_inr=120,
        cost_max_inr=220,
        description="Heritage snack cabin famous for authentic deep-fried Mughlai Parathas stuffed with minced duck egg and mutton."
    ),
    "paramount_sherbets": Restaurant(
        id="paramount_sherbets",
        name="Paramount Sherbets & Syrups (College Square)",
        specialty="Midnight Dhaba & Bharer Cha",
        zone="Central",
        lat=22.5740,
        lon=88.3630,
        nearest_landmark="College Square Pandal",
        cost_min_inr=90,
        cost_max_inr=180,
        description="Historic beverage shop established in 1918; world-famous Daab Sarbat (tender coconut) and Malai Sherbet."
    ),
    "indian_coffee_house_college_st": Restaurant(
        id="indian_coffee_house_college_st",
        name="Indian Coffee House (College Street)",
        specialty="Heritage European Cafe & Bakery",
        zone="Central",
        lat=22.5750,
        lon=88.3625,
        nearest_landmark="College Street Boipara",
        cost_min_inr=80,
        cost_max_inr=200,
        description="The intellectual sanctuary of Bengal: hot infusion coffee, mutton cutlets, and vintage adda vibe."
    ),
    "tewari_brothers_burrabazar": Restaurant(
        id="tewari_brothers_burrabazar",
        name="Tewari Brothers (Burrabazar)",
        specialty="Pure Vegetarian & Marwari Delights",
        zone="Central",
        lat=22.5800,
        lon=88.3550,
        nearest_landmark="MG Road Metro",
        cost_min_inr=90,
        cost_max_inr=200,
        description="Pure desi ghee samosas, hing kachori with aloo tarkari, and oversized syrupy gulab jamuns."
    ),
    "haldirams_exide": Restaurant(
        id="haldirams_exide",
        name="Haldiram's Food City (Exide / Rabindra Sadan)",
        specialty="Pure Vegetarian & Marwari Delights",
        zone="Central",
        lat=22.5410,
        lon=88.3490,
        nearest_landmark="Rabindra Sadan Metro",
        cost_min_inr=180,
        cost_max_inr=400,
        description="Spacious pure vegetarian multi-cuisine food court: Chole Bhature, Dahi Vada, Rajbhog, and Pav Bhaji."
    ),

    # --- TANGRA CHINATOWN & EAST KOLKATA ---
    "golden_joy_tangra": Restaurant(
        id="golden_joy_tangra",
        name="Golden Joy (Tangra Chinatown)",
        specialty="Tangra Chinatown & Indo-Chinese",
        zone="Central",
        lat=22.5480,
        lon=88.3880,
        nearest_landmark="Tangra Chinatown",
        cost_min_inr=400,
        cost_max_inr=800,
        description="The mecca of Indo-Chinese gastronomy: giant crispy pepper chicken, Golden fried prawns, and Hakka noodles."
    ),
    "beijing_tangra": Restaurant(
        id="beijing_tangra",
        name="Beijing Restaurant (Tangra Chinatown)",
        specialty="Tangra Chinatown & Indo-Chinese",
        zone="Central",
        lat=22.5475,
        lon=88.3890,
        nearest_landmark="Tangra Chinatown",
        cost_min_inr=420,
        cost_max_inr=850,
        description="Atmospheric Chinatown giant famous for Chilli Pork, Peking Chicken, and Manchow Soup."
    ),

    # --- SALT LAKE & NEW TOWN ---
    "oudh_1590_saltlake": Restaurant(
        id="oudh_1590_saltlake",
        name="Oudh 1590 (Salt Lake Sector 1)",
        specialty="Kolkata Biryani / Mughlai",
        zone="East_SaltLake",
        lat=22.5870,
        lon=88.4090,
        nearest_landmark="City Centre 1 Salt Lake",
        cost_min_inr=480,
        cost_max_inr=800,
        description="Awadhi biryani, Galawati Kebab, and Moti Biryani in royal Nawabi ambiance."
    ),
    "kaafila_saltlake_citycentre": Restaurant(
        id="kaafila_saltlake_citycentre",
        name="Kaafila (City Centre 1, Salt Lake)",
        specialty="Continental & Heritage Grills",
        zone="East_SaltLake",
        lat=22.5890,
        lon=88.4080,
        nearest_landmark="City Centre 1 Metro",
        cost_min_inr=500,
        cost_max_inr=950,
        description="North-West Frontier and Afghan tandoori delights with rich gravies and warm breads."
    ),

    # --- VIP ROAD & DUM DUM ---
    "arsalan_chinar_park": Restaurant(
        id="arsalan_chinar_park",
        name="Arsalan (Chinar Park / VIP Road)",
        specialty="Kolkata Biryani / Mughlai",
        zone="East_VIP",
        lat=22.6240,
        lon=88.4480,
        nearest_landmark="Chinar Park Crossing",
        cost_min_inr=380,
        cost_max_inr=650,
        description="Massive multi-storey Arsalan serving biryani for pandal hoppers on VIP Road and New Town."
    ),
    "aminia_chinar_park": Restaurant(
        id="aminia_chinar_park",
        name="Aminia (Chinar Park / VIP Road)",
        specialty="Kolkata Biryani / Mughlai",
        zone="East_VIP",
        lat=22.6230,
        lon=88.4470,
        nearest_landmark="Chinar Park Crossing",
        cost_min_inr=350,
        cost_max_inr=600,
        description="Classic biryani, tandoori kebabs, and firni along the VIP Road route."
    ),

    # --- HOWRAH ---
    "ganguram_howrah": Restaurant(
        id="ganguram_howrah",
        name="Ganguram Sweets & Tiffin (Howrah Station)",
        specialty="Bengal Mishti Pilgrimage",
        zone="Howrah",
        lat=22.5840,
        lon=88.3430,
        nearest_landmark="Howrah Railway Station",
        cost_min_inr=80,
        cost_max_inr=200,
        description="Century-old sweetmaker famous for thick Mishti Doi, Radhaballabhi, and Indrani."
    )
}
