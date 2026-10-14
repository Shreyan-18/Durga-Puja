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

- **🎯 Dual Planning Modes (Auto-Discover vs. Custom Bucket List)**:
  - **✨ Auto-Discover & Recommend**: Intelligently recommends the highest-rated pandals across selected zones based on art themes, tradition, and crowd tolerance.
  - **🎯 Custom Selection & Route Optimization**: Handpick your exact must-visit pandals (or add custom neighborhood pandals with live geocoding). The algorithm computes the globally optimal traveling sequence, avoiding traffic traps and minimizing queue times.
  - **✨ Intelligent On-Route Pandal Discovery**: If an unselected top-rated pandal (rating $\ge 8.9$) lies directly along your walking corridor between two chosen stops (detour $\le 0.75\text{ km}$) and time permits before your return curfew, the optimizer automatically schedules it as a bonus discovery stop without causing itinerary delays.

- **🏛️ 300+ Bengal Pandals Across All Major Hubs**:
  - **South Kolkata & Southern Suburbs (99)**: Ekdalia, Singhi Park, Tridhara, Ballygunge Cultural, Maddox Square, Chetla Agrani, Suruchi Sangha, Mudiali, Naktala Udayan, Jodhpur Park, Garia Mitali (Naba Durga), Kanungo Park Garia, Santoshpur Lake Pally, Jadavpur Sammilani, Ganguly Bagan Jadavpur, Bosepukur Sitala Mandir, Rajpur 9 Er Pally, Boral Sukanta Sangha, Ramchandrapur Narendrapur, Mallikpur Pragati Sangha, Baruipur Sasan Balak Sangha (Sasan Thakur), Baruipur Sahapara, Baruipur Dakshin Roy Pally, Baruipur Ajeya Sangha, Baruipur Bhai Bhai Sangha, Baruipur Fultala, Baruipur Roy Chowdhury Bari, Baruipur Padmapukur, Baruipur Madarat, Subhasgram Nabajiban & Kallol Sangha, Sonarpur Sporting, Diamond Harbour Town Sarbojanin, Canning Sonjoy Polli, Joynagar Majilpur, Lakshmikantapur Station, etc.
  - **Behala & South-Western Corridor**: Barisha Club, Barisha Sarbojanin, Behala Nutan Dal, Behala Club, Behala Friends Club, Behala Players Corner, Barisha Yubak Brinda, Behala Srishti, Behala Buroshibtala, Behala Debdaru Fatak, Parnasree Club, SB Park Sarbojanin (Thakurpukur), Behala Youngmens Association, Behala Siksha Ayatan, Behala Silpara, Behala Shibrampur, Joka Vivekananda Sangha, etc.
  - **North Kolkata & Northern Rail Corridors (60)**: Bagbazar Sarbojanin, Sovabazar Rajbari, Kumartuli Park, Ahiritola, Kashi Bose Lane, Hatibagan, Tala Prattoy, Sikdar Bagan, Nalin Sarkar St, Kalyani ITI More (Luminous Club), Kalyani Rathtala, Kalyani A-9 Square Park, Kalyani Boat Park, Kalyani Manimala B-12, Kanchrapara 16 Pally, Kanchrapara Viswanath Smriti, Naihati Baro Maa & Arabinda Road, Bhatpara Prabartak, Krishnanagar Rajbari, Krishnanagar Chashapara Barowari, Ghurni Putulpatty, etc.
  - **Bishnupur, Bankura, Burdwan, Durgapur, Raniganj & Medinipur (59)**: Bishnupur Maa Mrinmoyee Temple (997 AD), Malla Royal Palace (Pot Pujo), Dalmadal Para, Rasmancha Square, Bankura Machantala, Katjuridanga, Nutanganj, School Danga, Durgapur Agrani Sanskriti, Gopal Math, Marconi Dakshin Palli, Ambuja Urvashi, Raniganj Searsole Rajbari (cannons), Sishubagan, Tarun Sangha, Asansol Sen-Raleigh, Burdwan Sarbamangala Mandir, Curzon Gate, Medinipur Choto Bazar, Kharagpur Talbagicha Sabuj Sangha, Chandannagar Bagbazar, Chinsurah Sandeswartala, Bandel, Tribeni, etc.
  - **Central Kolkata (26)**: College Square, Mohammad Ali Park, Santosh Mitra Square, Simla Bayam Samity, Simla Sporting, Chorbagan, Chaltabagan Lohapatti, Sealdah Athletic, etc.
  - **East Kolkata & Salt Lake (28)**: Salt Lake FD, BJ, AK, AJ, CF, BA, BE, BL blocks, Labony Estate, New Town Sarbojanin, Uniworld City, etc.
  - **VIP Road & Dum Dum (28)**: Sreebhumi Sporting Club, Lake Town Adhibasi Brinda, Dum Dum Park Bharat Chakra, Dum Dum Park Tarun Dal, Dum Dum Park Tarun Tirtho, Bangur Avenue Pratigya & Pallishree, Kestopur Prafulla Kanan, Baguiati Railpukur, Teghoria Deshbandhu, Kaikhali, etc.
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
