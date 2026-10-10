# 🪔 Durga Puja Pandal Hopping Optimizer

An intelligent route optimization and scheduling application tailored for Kolkata & West Bengal Durga Puja pandal hopping.

---

## 🌟 Overview
Standard routing engines (Google Maps, simple TSP solvers) assume static travel times and miss the intricate realities of Kolkata Durga Puja:
1. **Dynamic Time-Dependent Queues**: A mega-tier pandal (e.g. Suruchi Sangha, Sreebhumi, or Chetla Agrani) can have a 90-minute queue at 9:00 PM on Ashtami, dropping to 20 minutes at 3:30 AM.
2. **Corridor Traps**: Crossing between North and South Kolkata takes over an hour during festive evenings; intelligent spatial clustering is vital.
3. **Multi-Meal Scheduling**: Hoppers need properly timed meals—from afternoon lunch to evening rolls, midnight biryani feasts, and early morning chai adda.
4. **On-Route Restaurant Matching**: Automatically detours to iconic culinary institutions along the path with minimal detour and budget compliance.
5. **Gateway Guidance & Multi-Modal Transit**: Tracks Suburban Local EMU Trains (e.g., Sealdah South line from Baruipur/Sonarpur), Kolkata Metro (Blue & Green lines), Shared Autos, and pedestrian barricades.

---

## 🏗️ Architecture

```
puja_hopper/
├── app.py                # Interactive Streamlit Web Application with PyDeck map & directory
├── optimizer.py          # Simulated Annealing + 2-Opt solver for Time-Dependent Orienteering
├── data.py               # Gateway definitions, transit models, crowd curves, and route-aware finder
├── pandals_data.py       # Master catalog of 164+ curated pandals across 6 Bengal zones
├── restaurants_data.py   # Catalog of 46 iconic restaurants & 12 authentic cuisine tiers
├── geocoder.py           # Privacy-first location geocoder (Baruipur & Bengal town cache + OSM fallback)
├── compile_pandals.py    # Compiler script to assemble and validate pandal metadata
├── run_demo.py           # CLI demonstration script with detailed door-to-door itinerary
├── requirements.txt      # Python dependencies
└── .gitignore            # Git exclusion rules
```

---

## ✨ Key Features

- **🏛️ 164+ Bengal Pandals Across 6 Zones**:
  - **South Kolkata (47)**: Ekdalia, Singhi Park, Tridhara, Ballygunge Cultural, Maddox Square, Chetla Agrani, Suruchi Sangha, Mudiali, Naktala Udayan, Jodhpur Park, Baruipur Roy Chowdhury Bari, etc.
  - **Behala & Sakher Bazar**: Barisha Club, Barisha Sarbojanin, Behala Nutan Dal, Behala Club, Behala Friends Club, Behala Players Corner, Barisha Yubak Brinda, Behala Srishti, Behala Buroshibtala, Behala Debdaru Fatak, Parnasree Club, etc.
  - **North Kolkata (38)**: Bagbazar Sarbojanin, Sovabazar Rajbari, Kumartuli Park, Ahiritola, Kashi Bose Lane, Hatibagan, Tala Prattoy, Sikdar Bagan, Nalin Sarkar St, etc.
  - **Central Kolkata (22)**: College Square, Mohammad Ali Park, Santosh Mitra Square, Simla Bayam Samity, Sealdah Athletic, etc.
  - **East Kolkata & Salt Lake (25)**: Salt Lake FD, BJ, AK, AJ, CF, BA blocks, New Town Sarbojanin, etc.
  - **VIP Road & Dum Dum (18)**: Sreebhumi Sporting Club, Lake Town Adhibasi Brinda, Dum Dum Park Bharat Chakra, Dum Dum Park Tarun Dal, etc.
  - **Howrah & Hooghly (14)**: Belur Math, Salkia Alapani, Shibpur Mandirtala, Serampore Goswami Bari, Uttarpara, etc.

- **🍴 46 Iconic Restaurants & 12 Cuisine Tiers**:
  - Biryani & Mughlai (Arsalan, Shiraz, Aminia, Royal Indian Hotel, Dada Boudi)
  - Bengali Zamindari Feast (6 Ballygunge Place, Bhojohori Manna, Kasturi, Golbari, The Bhoj Company)
  - Cabin Cutlets & Kathi Rolls (Mitra Cafe, Nizam's, Kusum Rolls, Campari, Allen Kitchen, Anadi Cabin)
  - Tangra Chinatown (Golden Joy, Beijing Restaurant, Chowman)
  - Continental Grills (Peter Cat, Mocambo)
  - Midnight Dhaba & Bharer Cha (Balwant Singh Dhaba, Sharma Tea House)
  - Bengal Mishti Pilgrimage (Balaram Mullick, Nobin Chandra Das, Chittaranjan Sweets, Ganguram)
  - European Bakery & Cafe (Flurys Tearoom, Indian Coffee House)
  - Pure Vegetarian & Marwari Delights (Maharaja & Maharani, Tewari Brothers, Haldiram's)

- **🍱 Multi-Meal Planning (Up to 6 Meals)**:
  - Configure up to 6 meals (Lunch, Dinner, Midnight Chai, Evening Snacks, Early Morning Bites, Breakfast).
  - Select specific iconic restaurants or auto-match on-route with minimal travel detour.

- **💰 Budget & Cost Limits**:
  - Enforce maximum total trip budget per person (₹200 - ₹4,000).
  - Cap individual restaurant spending tiers.
  - Real-time budget compliance alert and savings indicator.

- **🗺️ Interactive Map & Visual Route Lines**:
  - Connected `PathLayer` showing complete journey path from Origin $\rightarrow$ Pandals & Dining $\rightarrow$ Return Origin.
  - Color-coded pins for Origin (Green), Pandals (Red), Food/Dining (Orange), and Transit Gateways (Blue).

- **🚆 Gateway Guidance**:
  - Identifies entrance and exit gateways (e.g. Sealdah South Local Train, Ballygunge Junction, Kavi Subhash, Kalighat, Shyambazar).
  - Explicit movement modes (Suburban Local Train, Kolkata Metro, Shared Auto / Toto, Walking, Yellow Taxi).

---

## 🚀 Quickstart

### 1. Installation
```bash
git clone https://github.com/Shreyan-18/Durga-Puja.git
cd Durga-Puja
pip install -r requirements.txt
```

### 2. Run CLI Scenario
```bash
python run_demo.py
```

### 3. Launch Web Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501` (or `--server.port 8502`).
