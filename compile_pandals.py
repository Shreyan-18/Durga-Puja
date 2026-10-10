"""
Generator script to compile the complete master catalog of 150+ Kolkata & Bengal Durga Puja Pandals.
"""

# Let's define the comprehensive raw list of 150+ pandals across all zones
PANDALS_RAW = [
    # =========================================================================
    # --- SOUTH KOLKATA (36 PANDALS) ---
    # =========================================================================
    ("ekdalia", "Ekdalia Evergreen Club", "South", 22.5204, 88.3653, 9.5, "Traditional", 15, 3, "Gariahat / Kalighat", "Famous for towering traditional chandeliers from Chandannagar and classical pratima.", "Gariahat Road"),
    ("singhi_park", "Singhi Park Sarbojanin", "South", 22.5188, 88.3638, 9.1, "Traditional", 15, 2, "Kalighat", "Across Ekdalia; magnificent architectural temple replica and artisanal craft.", "Dover Terrace"),
    ("tridhara", "Tridhara Sammilani", "South", 22.5172, 88.3585, 9.6, "Theme", 20, 3, "Jatin Das Park", "Pioneering conceptual socio-cultural art, environmental decor, and stunning lighting.", "Monoharpukur Road"),
    ("ballygunge_cultural", "Ballygunge Cultural Association", "South", 22.5228, 88.3614, 9.2, "Theme", 18, 2, "Jatin Das Park / Ballygunge Jn", "Celebrated eco-art, indigenous craft installations, and serene aesthetic ambiance.", "Lake Temple Road"),
    ("maddox_square", "Maddox Square", "South", 22.5284, 88.3575, 9.3, "Traditional", 30, 2, "Netaji Bhavan", "The ultimate adda and youth cultural hub; massive park with pure traditional Ekchala idol.", "Ritchie Road"),
    ("hindustan_park", "Hindustan Park Sarbojanin", "South", 22.5195, 88.3602, 9.0, "Theme", 18, 2, "Kalighat", "Refined contemporary visual art exploring folk traditions and societal themes.", "Hindustan Park Road"),
    ("samaj_sebi", "Samaj Sebi Sangha", "South", 22.5168, 88.3608, 9.1, "Theme", 20, 2, "Kalighat", "Socially-conscious conceptual art, famous for Braille and sensory inclusivity themes.", "Lake View Road"),
    ("deshapriya_park", "Deshapriya Park", "South", 22.5182, 88.3538, 9.4, "Theme", 22, 3, "Kalighat", "Monumental scale presentations in a grand park, famous for record-breaking structural replicas.", "Rashbehari Avenue"),
    ("badamtala_ashar_sangha", "Badamtala Ashar Sangha", "South", 22.5198, 88.3472, 9.3, "Theme", 20, 3, "Kalighat", "Kalighat hub pioneer; multiple Sharad Samman winner for profound spiritual motifs.", "Nepal Bhattacharjee Street"),
    ("sixty_six_pally", "66 Pally", "South", 22.5192, 88.3465, 9.1, "Theme", 18, 2, "Kalighat", "Adjacent to Badamtala; historic trailblazer that famously appointed female priestesses.", "Suren Tagore Road"),
    ("nepal_bhattacharjee", "Nepal Bhattacharjee Street Club", "South", 22.5205, 88.3460, 8.9, "Theme", 16, 2, "Kalighat", "Part of the tight Kalighat walking quad; intricate handcrafted bamboo and cane work.", "Rashbehari Crossing"),
    ("chetla_agrani", "Chetla Agrani Club", "South", 22.5160, 88.3415, 9.7, "Theme", 25, 3, "Kalighat", "Consistently ranks among Kolkata's top 3 mega art spectacles with mindblowing architecture.", "Peary Mohan Roy Road"),
    ("mudiali_club", "Mudiali Club", "South", 22.5103, 88.3508, 9.2, "Traditional", 18, 2, "Rabindra Sarobar", "Renowned for harmonious environmental decor, vibrant natural colors, and traditional Pratima.", "Southern Avenue"),
    ("shiv_mandir", "Shiv Mandir Sarbojanin", "South", 22.5115, 88.3512, 9.1, "Theme", 18, 2, "Rabindra Sarobar", "Next door to Mudiali; thoughtful conceptual themes and artistic lighting along the lake.", "Lake Road"),
    ("suruchi_sangha", "Suruchi Sangha (New Alipore)", "South", 22.5085, 88.3312, 9.8, "Theme", 25, 3, "Majerhat / Kalighat", "Massive Indian state-themed cultural immersion; one of the most attended pandals in Bengal.", "New Alipore Block M"),
    ("jodhpur_park", "Jodhpur Park Sarbojanin", "South", 22.5030, 88.3630, 9.3, "Theme", 20, 3, "Rabindra Sarobar / Dhakuria", "Sprawling open grounds with majestic architectural and conceptual installations.", "Jodhpur Park 4th Lane"),
    ("selimpur_pally", "Selimpur Pally", "South", 22.5045, 88.3670, 9.2, "Theme", 18, 2, "Dhakuria Railway Stn", "Celebrated for intricate rural crafts, terracotta, and thought-provoking social themes.", "Selimpur Road"),
    ("babubagan", "Babubagan Sarbojanin", "South", 22.5065, 88.3685, 9.1, "Traditional", 18, 2, "Dhakuria", "Historic temple replicas made with astonishing materials like genuine coins and stamps.", "Dhakuria Babubagan"),
    ("ninety_five_pally", "95 Pally (Jodhpur Park)", "South", 22.5015, 88.3620, 9.0, "Theme", 18, 2, "Dhakuria", "Artistic community hub in Jodhpur Park featuring innovative lighting and serene Pratima.", "Jodhpur Park"),
    ("naktala_udayan", "Naktala Udayan Sangha", "South", 22.4740, 88.3620, 9.7, "Theme", 25, 3, "Gitanjali (Naktala)", "South Kolkata's titan of high-concept contemporary art and moving installations.", "NSC Bose Road"),
    ("behala_nutan_dal", "Behala Nutan Dal", "South", 22.4985, 88.3120, 9.4, "Theme", 20, 3, "Tarabala / Behala Tram Depot", "Behala's flagship theme powerhouse featuring profound philosophical art installations.", "Bonomali Naskar Road"),
    ("behala_club", "Behala Club Sarbojanin", "South", 22.4930, 88.3150, 9.1, "Theme", 18, 2, "Behala Chowrasta", "Over 75 years old; celebrated for peaceful aesthetic craftsmanship and folk art.", "Roy Bahadur Road"),
    ("behala_buroshibtala", "Behala Buroshibtala Janakalyan", "South", 22.4960, 88.3180, 9.2, "Theme", 18, 2, "Behala Chowrasta", "Creative installations exploring rural traditions and experimental clay work.", "Buroshibtala Main Road"),
    ("behala_debdaru_fatak", "Behala Debdaru Fatak", "South", 22.4910, 88.3140, 9.0, "Theme", 18, 2, "Behala Chowrasta", "Known for unique architectural pavilions and festive carnival vibe.", "Arya Samiti Road"),
    ("barisha_club", "Barisha Club", "South", 22.4820, 88.3105, 9.3, "Theme", 20, 3, "Sakherbazar / Chowrasta", "Shot into global spotlight with poignant migrant-mother and emotional humanitarian themes.", "Diamond Harbour Road"),
    ("behala_friends_club", "Behala Friends Club", "South", 22.4975, 88.3145, 9.1, "Theme", 18, 2, "Behala Chowrasta", "Renowned for handcrafted clay, bamboo, and terracotta traditional folk motifs.", "Bonomali Naskar Road"),
    ("behala_players_corner", "Behala Players Corner", "South", 22.4960, 88.3130, 9.2, "Theme", 18, 2, "Behala Chowrasta", "Iconic community club associated with cricket legend Sourav Ganguly; vibrant cultural hub.", "Satyen Roy Road Behala"),
    ("barisha_sarbojanin", "Barisha Sarbojanin Durgotsav", "South", 22.4835, 88.3110, 9.3, "Traditional", 20, 2, "Sakherbazar", "Century-old heritage puja with majestic sabeki pratima and grand cultural traditions.", "Diamond Harbour Road"),
    ("barisha_yubak_brinda", "Barisha Yubak Brinda", "South", 22.4810, 88.3130, 9.0, "Theme", 18, 2, "Sakherbazar", "High-budget artistic theme installations and innovative lighting on James Long Sarani.", "James Long Sarani"),
    ("behala_adarsha_pally", "Behala Adarsha Pally", "South", 22.5030, 88.3070, 9.0, "Theme", 18, 2, "Taratala / Parnasree", "Artistic environmental themes and serene courtyard ambiance in Parnasree.", "Parnasree Pally Behala"),
    ("behala_srishti", "Behala Srishti", "South", 22.4920, 88.3160, 9.1, "Theme", 18, 2, "Behala Chowrasta", "Pioneering contemporary social and folk art themes near Chowrasta.", "Raja Rammohan Roy Road"),
    ("behala_unique_park", "Behala Unique Park", "South", 22.4895, 88.3185, 9.0, "Theme", 18, 2, "Behala Chowrasta", "Grand architectural mandap replicas and intricate artisan idol craftsmanship.", "James Long Sarani Behala"),
    ("behala_sarsuna_tarun", "Behala Sarsuna Tarun Sangha", "South", 22.4690, 88.2890, 8.9, "Theme", 16, 2, "Sarsuna / Behala", "Massive community turnout and vibrant pandal lighting in South-West Behala.", "Sarsuna Main Road"),
    ("parnasree_club", "Parnasree Club (Behala)", "South", 22.5010, 88.3040, 9.0, "Traditional", 18, 2, "Taratala / Parnasree", "Heritage South-Western Kolkata pandal celebrated for cultural harmony and sabeki murti.", "Parnasree Lake Behala"),
    ("behala_panchanantala", "Behala Panchanantala Sarbojanin", "South", 22.4880, 88.3110, 8.9, "Theme", 16, 2, "Sakherbazar", "Celebrated community puja right along the Diamond Harbour arterial corridor.", "Diamond Harbour Road Behala"),
    ("barisha_asram_sangha", "Barisha Asram Sangha", "South", 22.4790, 88.3090, 8.9, "Traditional", 16, 2, "Sakherbazar", "Classical heritage artwork and traditional Ekchala pratima with deep devotional atmosphere.", "Sakher Bazar Behala"),
    ("haridevpur_ajeya", "Haridevpur Ajeya Sanghati", "South", 22.4860, 88.3390, 9.2, "Theme", 20, 2, "Mahanayak Uttam Kumar", "Acclaimed artistic excellence and atmospheric experiential walking tunnels.", "Haridevpur Main Road"),
    ("forty_one_pally", "41 Pally (Haridevpur)", "South", 22.4840, 88.3370, 9.0, "Theme", 18, 2, "Mahanayak Uttam Kumar", "Intricate indigenous craftsmanship using bell metal, brass, and handloom fabrics.", "Haridevpur"),
    ("tollygunge_agragami", "Tollygunge Agragami", "South", 22.5020, 88.3440, 8.9, "Traditional", 16, 2, "Netaji / Tollygunge", "Community hub with classical Pratima, cultural functions, and authentic bhog.", "Mani Mukherjee Road"),
    ("lake_youth_club", "Lake Youth Club", "South", 22.5130, 88.3540, 8.9, "Theme", 16, 2, "Rabindra Sarobar", "Located right by Rabindra Sarobar lake; environmental aesthetics and cool breeze.", "Southern Avenue"),
    ("golf_green_sarbojanin", "Golf Green Sarbojanin", "South", 22.4950, 88.3610, 9.0, "Traditional", 18, 2, "Bikramgarh / Tollygunge", "Lush township green surroundings, peaceful darshan, and classical music evenings.", "Golf Green Phase 2"),
    ("bansdroni_anila", "Bansdroni Anila Smriti", "South", 22.4710, 88.3560, 8.9, "Theme", 16, 2, "Masterda Surya Sen", "Vibrant community theme with hand-carved terracotta and wood sculptures.", "Bansdroni Main Road"),
    ("garia_navapally", "Garia Navapally Sarbojanin", "South", 22.4620, 88.3880, 8.8, "Theme", 16, 2, "Kavi Nazrul (Garia)", "Famous neighborhood puja in Garia featuring creative environmental structures.", "Garia Station Road"),
    ("patuli_sarbojanin", "Baishnabghata Patuli Sarbojanin", "South", 22.4750, 88.3890, 9.1, "Theme", 18, 2, "Kavi Subhash", "Huge open grounds near Patuli floating market; grand illuminated pavilions.", "EM Bypass Patuli"),
    ("baruipur_roy_chowdhury", "Baruipur Roy Chowdhury Bari (300+ yrs)", "South", 22.3680, 88.4340, 9.5, "Bonedi_Bari", 25, 2, "Baruipur Junction Station", "300-year-old historic Zamindar Bonedi Bari of Baruipur; pure heritage Pratima, royal Dalan, and authentic Sandhi rituals.", "Baruipur Kacharibari Road"),
    ("baruipur_padmapukur", "Baruipur Padmapukur Sarbojanin", "South", 22.3640, 88.4300, 8.8, "Theme", 18, 2, "Baruipur Junction", "Baruipur's landmark community puja featuring grand illumination and social theme.", "Kulpi Road Baruipur"),
    ("sonarpur_sporting", "Sonarpur Sporting Club", "South", 22.4410, 88.4240, 8.8, "Theme", 18, 2, "Sonarpur Junction", "Prominent South 24 Parganas hub right off the suburban local train line.", "Station Road Sonarpur"),

    # =========================================================================
    # --- NORTH KOLKATA (38 PANDALS) ---
    # =========================================================================
    ("bagbazar", "Bagbazar Sarbojanin", "North", 22.6033, 88.3672, 9.8, "Traditional", 25, 3, "Shyambazar", "Over a century old; the crown jewel of traditional Pujas with iconic Daker Saaj idol, sindoor khela, and carnival.", "Bagbazar Street"),
    ("sovabazar_rajbari", "Sovabazar Rajbari (Boro Taraf)", "North", 22.5975, 88.3644, 9.7, "Bonedi_Bari", 20, 2, "Sovabazar Sutanuti", "Dating back to 1757 (Raja Nabakrishna Deb); grand courtyard puja with cannon salute and Kanak-Durga rituals.", "Raja Nabakrishna Street"),
    ("sovabazar_chhoto_rajbari", "Sovabazar Chhoto Rajbari", "North", 22.5970, 88.3640, 9.4, "Bonedi_Bari", 18, 2, "Sovabazar Sutanuti", "Across from Boro Rajbari; majestic colonnaded courtyard, classical ekchala pratima, and preserved family heritage.", "Raja Nabakrishna Street"),
    ("kumartuli_park", "Kumartuli Park", "North", 22.5996, 88.3651, 9.3, "Theme", 20, 3, "Sovabazar Sutanuti", "Located right in the idol-makers' heartland; dramatic theatrical grandeur and immersive architectural themes.", "Kumartuli Park"),
    ("kumartuli_sarbojanin", "Kumartuli Sarbojanin", "North", 22.5985, 88.3662, 9.1, "Traditional", 16, 2, "Sovabazar Sutanuti", "The original community puja run by the master sculptors themselves, showcasing pure sculpting mastery.", "Banamali Sarkar Street"),
    ("ahiritola", "Ahiritola Sarbojanin", "North", 22.5950, 88.3590, 9.2, "Theme", 20, 2, "Sovabazar Sutanuti", "Bold social awareness themes, riverbank breezes along the Hooghly ghats, and artistic illumination.", "BK Paul Avenue"),
    ("beniatola_sarbojanin", "Beniatola Sarbojanin", "North", 22.5942, 88.3620, 9.1, "Theme", 18, 2, "Sovabazar Sutanuti", "Renowned for deeply researched socio-artistic themes in intimate historic North Kolkata lanes.", "Beniatola Lane"),
    ("hatibagan_sarbojanin", "Hatibagan Sarbojanin", "North", 22.5962, 88.3725, 9.0, "Theme", 18, 2, "Shyambazar", "Vintage North Kolkata charm, heritage artistic motifs, and classical musical backdrop.", "Bidhan Sarani"),
    ("shikdar_bagan", "Shikdar Bagan Sadharan Durgotsav", "North", 22.5980, 88.3715, 9.2, "Theme", 18, 2, "Shyambazar", "One of the oldest in Kolkata (1913); famed for masterfully crafted cane, mud, and wooden themes.", "Shikdar Bagan Street"),
    ("kashi_bose_lane", "Kashi Bose Lane", "North", 22.5905, 88.3712, 9.6, "Theme", 22, 3, "Girish Park / Shyambazar", "North Kolkata's biggest thematic crowd magnet with award-winning architectural scale and experiential audio-visual walkthroughs.", "Bidhan Sarani"),
    ("nalin_sarkar_st", "Nalin Sarkar Street", "North", 22.5952, 88.3740, 9.2, "Theme", 18, 2, "Shyambazar", "Famed for folk art, natural earthenware, terracotta murals, and master artisan clay handicrafts.", "Nalin Sarkar Street"),
    ("tala_prattoy", "Tala Prattoy", "North", 22.6105, 88.3752, 9.7, "Theme", 25, 3, "Belgachia / Shyambazar", "Globally celebrated installation art; curated like a Venice Biennale contemporary pavilion by renowned visual artists.", "Tala Park"),
    ("jagat_mukherjee_park", "Jagat Mukherjee Park", "North", 22.6002, 88.3698, 9.1, "Theme", 18, 2, "Shyambazar", "Known for experiential engineering concepts (e.g. underwater submarine & aerospace replicas).", "Shyambazar Crossing"),
    ("telengabagan", "Telengabagan Sarbojanin", "North", 22.5890, 88.3845, 9.1, "Theme", 18, 2, "Ultadanga", "Pioneered the modern theme movement in North Kolkata since the late 1990s with deeply thought-out installations.", "Ultadanga Main Road"),
    ("ultadanga_pallyshree", "Ultadanga Pallyshree", "North", 22.5875, 88.3880, 8.9, "Theme", 16, 2, "Ultadanga", "Adjacent to Telengabagan; celebrated for harmonious woodcraft and traditional folk sculpture.", "Muraripukur Road"),
    ("chalta_bagan", "Maniktala Chaltabagan Lohapatty", "North", 22.5855, 88.3735, 9.3, "Traditional", 20, 3, "Girish Park", "World-famous for its spirited Dhunuchi Nach, glass and brass decor, and star-studded festive carnival.", "Raja Rammohan Sarani"),
    ("simla_bayam_samity", "Simla Bayam Samity", "North", 22.5878, 88.3690, 9.2, "Traditional", 18, 2, "Girish Park", "Centenary wrestling club steeped in freedom movement; majestic martial Durga pratima with weapons.", "Vivekananda Road"),
    ("gouribari_sarbojanin", "Gouribari Sarbojanin", "North", 22.5880, 88.3780, 9.0, "Theme", 18, 2, "Shyambazar / Ultadanga", "Celebrated centenary puja on APC Road featuring indigenous artisan craft and evocative lighting.", "APC Road"),
    ("pathuriaghata_ghosh", "Pathuriaghata Ghosh Bari", "North", 22.5880, 88.3580, 9.4, "Bonedi_Bari", 18, 2, "Girish Park", "Centuries-old aristocratic zamindar mansion puja famous for heritage Thakur Dalan and preserved rituals.", "Pathuriaghata Street"),
    ("dorjipara_mitra", "Dorjipara Mitra Bari", "North", 22.5910, 88.3630, 9.3, "Bonedi_Bari", 18, 2, "Sovabazar / Girish Park", "Historic Bonedi Bari puja where Durga sits on a majestic throne with Mahishasura in classic Dokhini style.", "Nilmani Mitra Street"),
    ("laha_bari", "Laha Bari Durga Puja", "North", 22.5840, 88.3610, 9.3, "Bonedi_Bari", 18, 2, "MG Road", "Historic aristocrat puja with a one-of-a-kind Shiva-seated idol (Haragouri) without weapons drawn.", "Bidhan Sarani / Thanthania"),
    ("thanthania_dutta", "Thanthania Dutta Bari (1788)", "North", 22.5825, 88.3635, 9.2, "Bonedi_Bari", 16, 2, "MG Road", "230+ years old; distinctive Durga idol made of Hara-Gouri without weapons drawn, famous for sweet offerings.", "College Street / Thanthania"),
    ("chorbagan_sarbojanin", "Chorbagan Sarbojanin", "North", 22.5845, 88.3670, 9.1, "Theme", 18, 2, "MG Road / Girish Park", "Renowned for intricate handloom, jute, and hand-embroidered environmental artistry.", "Muktarambabu Street"),
    ("shyampukur_pally", "Shyampukur Pally Durgotsav", "North", 22.6010, 88.3690, 8.9, "Traditional", 16, 2, "Shyambazar", "Close historical ties with Netaji Subhash Chandra Bose; traditional pratima with patriotic heritage.", "Shyampukur Street"),
    ("cossimbazar_rajbari", "Cossimbazar Rajbari (North)", "North", 22.6040, 88.3750, 9.2, "Bonedi_Bari", 18, 2, "Shyambazar", "Historic palatial mansion of the Maharaja of Cossimbazar, traditional chandimandap rituals.", "Cossimbazar House"),
    ("baranagar_netaji", "Baranagar Netaji Colony Sarbojanin", "North", 22.6350, 88.3790, 9.1, "Theme", 18, 2, "Noapara Metro", "North suburban powerhouse featuring grand innovative thematic pavilions.", "Netaji Colony Baranagar"),
    ("sinthee_friends", "Sinthee Friends Athletic Club", "North", 22.6240, 88.3780, 9.0, "Theme", 18, 2, "Dum Dum Metro", "Vibrant community hub along BT Road famous for thematic clay art and lights.", "Kalicharan Ghosh Road"),
    ("cossipore_sarbojanin", "Cossipore Sarbojanin", "North", 22.6210, 88.3690, 8.8, "Traditional", 16, 2, "Dum Dum Metro", "Historic riverbank community puja with traditional daker saaj pratima.", "Cossipore Road"),
    ("paikpara_sarbojanin", "Paikpara Sarbojanin (Tala)", "North", 22.6080, 88.3780, 9.0, "Theme", 18, 2, "Belgachia", "Grand pavilions featuring folk art from Bengal's rural artisan villages.", "Paikpara First Row"),
    ("belgachia_sadharan", "Belgachia Sadharan Durgotsav", "North", 22.6040, 88.3840, 8.9, "Theme", 16, 2, "Belgachia Metro", "Atmospheric theme decor right by Belgachia metro station.", "Belgachia Road"),
    ("hatibagan_nabin_pally", "Hatibagan Nabin Pally", "North", 22.5970, 88.3730, 9.1, "Theme", 18, 2, "Shyambazar", "Cozy, highly detailed conceptual themes in historic Hatibagan neighborhood.", "Bidhan Sarani"),
    ("nimtala_sarbojanin", "Nimtala Sarbojanin", "North", 22.5920, 88.3560, 8.8, "Traditional", 16, 2, "Sovabazar Sutanuti", "Riverside heritage puja near historic Nimtala Ghat with pure classic Pratima.", "Nimtala Ghat Street"),
    ("girish_park_five_star", "Girish Park Five Star Club", "North", 22.5860, 88.3630, 8.9, "Theme", 16, 2, "Girish Park Metro", "Conveniently located at Girish Park crossing; creative experimental artwork.", "CR Avenue Girish Park"),
    ("bagbazar_pally_samity", "Bagbazar Pally Samity", "North", 22.6020, 88.3650, 8.9, "Traditional", 16, 2, "Shyambazar", "Classic family-friendly North Kolkata adda hub with serene idol and prasad.", "Bagbazar Ghat"),
    ("maniktala_vivekananda", "Maniktala Vivekananda Sporting", "North", 22.5830, 88.3750, 8.9, "Theme", 16, 2, "Girish Park", "Famous for handcrafted bamboo and coconut shell sculptures.", "Vivekananda Road"),
    ("jorabagan_sarbojanin", "Jorabagan Sarbojanin", "North", 22.5900, 88.3570, 8.8, "Traditional", 16, 2, "Sovabazar Sutanuti", "Historic traditional merchant quarter puja with authentic brass utensils.", "Jorabagan Street"),
    ("kashi_mitra_ghat", "Kashi Mitra Ghat Durgotsav", "North", 22.6015, 88.3620, 8.8, "Traditional", 15, 2, "Shyambazar", "Overlooking the holy river Hooghly, peaceful darshan with evening Ganga aarti vibe.", "Strand Bank Road"),
    ("darpanarayan_tagore", "Darpanarayan Tagore Street Pally", "North", 22.5890, 88.3590, 8.9, "Bonedi_Bari", 16, 2, "Girish Park", "Historic merchant mansion lane with century-old family Pratima and customs.", "Darpanarayan Tagore St"),

    # =========================================================================
    # --- CENTRAL KOLKATA (22 PANDALS) ---
    # =========================================================================
    ("college_square", "College Square", "Central", 22.5765, 88.3648, 9.6, "Traditional", 25, 3, "Central / MG Road", "Spectacular illuminated palace replica mirrored in the swimming lake; world-famous Chandannagar lighting.", "College Street"),
    ("mohammad_ali_park", "Mohammad Ali Park", "Central", 22.5786, 88.3619, 9.4, "Traditional", 20, 3, "MG Road", "Monumental historical palace recreation inside a grand walled park setting on Central Avenue.", "CR Avenue"),
    ("santosh_mitra_sq", "Santosh Mitra Square (Lebutala)", "Central", 22.5695, 88.3695, 9.8, "Theme", 25, 3, "Central / Sealdah", "Kolkata's most sensational replication feats (Ayodhya Ram Mandir, Las Vegas Sphere, pure gold and silver idols).", "Bowbazar / Sealdah"),
    ("sealdah_athletic", "Sealdah Railway Athletic Club", "Central", 22.5670, 88.3730, 9.0, "Traditional", 18, 2, "Sealdah Station", "Located right by Sealdah terminal; grand temple pavilions and massive commuter crowd darshan.", "Kaiser Street"),
    ("rani_rashmoni_bari", "Janbazar Rani Rashmoni Bari (1790s)", "Central", 22.5615, 88.3565, 9.5, "Bonedi_Bari", 20, 2, "Esplanade", "Iconic heritage mansion where Sri Ramakrishna Paramahamsa himself worshiped; ancient traditions preserved.", "SN Banerjee Road Janbazar"),
    ("bowbazar_sarbojanin", "Bowbazar Sarbojanin", "Central", 22.5705, 88.3640, 8.9, "Traditional", 16, 2, "Central", "Historic central community puja with magnificent gold jewellery adornments on the Pratima.", "BB Ganguly Street"),
    ("muchipara_sarbojanin", "Muchipara Sarbojanin", "Central", 22.5680, 88.3660, 8.8, "Theme", 16, 2, "Central", "Popular neighborhood puja known for innovative theme work and lighting.", "Santosh Mitra Square Lane"),
    ("subodh_mullick_sq", "Subodh Mullick Square", "Central", 22.5645, 88.3605, 8.9, "Traditional", 16, 2, "Central / Chandni Chowk", "Pleasant open park setting with classical Pratima and community cultural programs.", "Wellington Square"),
    ("beliaghata_33_pally", "Beliaghata 33 Pally", "Central", 22.5660, 88.3880, 9.3, "Theme", 20, 3, "Phoolbagan / Sealdah", "Award-winning conceptual art pioneer (famous for antique yellow ambassador taxi installations).", "Subhas Sarobar Road"),
    ("beliaghata_sandhani", "Beliaghata Sandhani Club", "Central", 22.5690, 88.3850, 9.0, "Theme", 18, 2, "Sealdah / Phoolbagan", "Adjacent to 33 Pally; celebrated for creative eco-themes and community festivals.", "Beliaghata Main Road"),
    ("entally_sammilani", "Entally Sammilani", "Central", 22.5560, 88.3680, 8.8, "Theme", 16, 2, "Sealdah / Moulali", "Vibrant central community puja showcasing Bengali folk handicrafts.", "CIT Road Entally"),
    ("moulali_yubak_brinda", "Moulali Yubak Brinda", "Central", 22.5580, 88.3660, 8.8, "Traditional", 16, 2, "Sealdah", "Traditional pratima with sparkling lighting along the busy Moulali crossing.", "AJC Bose Road"),
    ("taltala_sarbojanin", "Taltala Sarbojanin", "Central", 22.5590, 88.3580, 8.9, "Theme", 16, 2, "Central / Park Street", "Historical central Kolkata neighborhood puja celebrating communal harmony.", "Taltala Lane"),
    ("chandni_chowk_pally", "Chandni Chowk Sarbojanin", "Central", 22.5650, 88.3540, 8.8, "Traditional", 15, 2, "Chandni Chowk Metro", "Located in the electronic market district; classic traditional puja with warm community adda.", "Chandni Chowk Street"),
    ("amherst_street_sarbojanin", "Amherst Street Sarbojanin", "Central", 22.5730, 88.3690, 8.9, "Traditional", 16, 2, "MG Road", "Historic collegiate area puja with classical Pratima and cultural shows.", "Amherst Street"),
    ("mirzapur_street", "Mirzapur City Club", "Central", 22.5740, 88.3660, 8.8, "Theme", 15, 2, "Central", "Close to College Street; creative installations by student art communities.", "Surya Sen Street"),
    ("patwarbagan_sarbojanin", "Patwarbagan Sarbojanin", "Central", 22.5720, 88.3710, 8.8, "Traditional", 15, 2, "Sealdah", "Traditional heritage decor with authentic daker saaj pratima.", "Patwarbagan Lane"),
    ("sealdah_baithakkhana", "Baithakkhana Sarbojanin", "Central", 22.5685, 88.3705, 8.9, "Traditional", 16, 2, "Sealdah Station", "Historic trading hub community puja dating back to nineteenth-century merchants.", "Baithakkhana Road"),
    ("park_circus_maidan", "Park Circus Maidan Durgotsav", "Central", 22.5410, 88.3670, 9.0, "Traditional", 18, 2, "Park Circus", "Spacious open maidan puja famous for communal solidarity and food fairs.", "Park Circus 7-Point"),
    ("bowbazar_bhattacharya", "Bowbazar Bhattacharya Bari", "Central", 22.5710, 88.3620, 9.1, "Bonedi_Bari", 16, 2, "Central", "Historic Bonedi Bari with unique traditional rituals and hereditary family pujas.", "Bowbazar Lane"),
    ("ganesh_chandra_avenue", "Ganesh Chandra Avenue Durgotsav", "Central", 22.5680, 88.3550, 8.8, "Traditional", 15, 2, "Chandni Chowk", "Commercial district puja with grand decorative chandeliers and illumination.", "GC Avenue"),
    ("dharmatala_sarbojanin", "Dharmatala Sarbojanin", "Central", 22.5630, 88.3530, 8.8, "Traditional", 15, 2, "Esplanade Metro", "Located in the heart of Kolkata; high transit commuter darshan and festival stalls.", "Lenin Sarani"),

    # =========================================================================
    # --- EAST KOLKATA & SALT LAKE & NEW TOWN (25 PANDALS) ---
    # =========================================================================
    ("fd_block_saltlake", "FD Block, Salt Lake", "East_SaltLake", 22.5862, 88.4143, 9.4, "Theme", 20, 3, "Salt Lake Karunamoyee", "Salt Lake's marquee flagship puja; grand palace structures and township festive carnival.", "Salt Lake Sector III"),
    ("bj_block_saltlake", "BJ Block, Salt Lake", "East_SaltLake", 22.5896, 88.4111, 9.0, "Theme", 18, 2, "Karunamoyee", "Spacious green township ambiance, innovative artistic decor, and peaceful family-friendly hopping.", "Salt Lake Sector II"),
    ("ak_block_saltlake", "AK Block, Salt Lake", "East_SaltLake", 22.5920, 88.4150, 9.0, "Theme", 18, 2, "City Centre 1", "Celebrated for grand architectural replicas, environmental themes, and spacious park layout.", "Salt Lake Sector I"),
    ("aj_block_saltlake", "AJ Block, Salt Lake", "East_SaltLake", 22.5910, 88.4120, 8.8, "Traditional", 16, 1, "City Centre 1", "Serene traditional ekchala idol with authentic rituals and cozy township warmth.", "Salt Lake Sector II"),
    ("cf_block_saltlake", "CF Block, Salt Lake", "East_SaltLake", 22.5870, 88.4080, 8.9, "Theme", 18, 2, "Salt Lake Stadium / Central Park", "Folk art and handloom decor, popular among township residents.", "Salt Lake Sector I"),
    ("bl_block_saltlake", "BL Block, Salt Lake", "East_SaltLake", 22.5880, 88.4160, 8.8, "Theme", 16, 1, "Karunamoyee", "Creative conceptual theme with artistic illumination around the neighborhood park.", "Salt Lake Sector II"),
    ("ee_block_saltlake", "EE Block, Salt Lake", "East_SaltLake", 22.5840, 88.4120, 8.9, "Theme", 18, 2, "Karunamoyee", "Renowned for experimental installations using natural fiber, brass, and wood.", "Salt Lake Sector II"),
    ("labony_estate", "Labony Estate, Salt Lake", "East_SaltLake", 22.5930, 88.4100, 8.8, "Traditional", 16, 2, "City Centre 1", "One of the earliest pujas of Salt Lake, famous for classical Pratima and community adda.", "Salt Lake Sector I"),
    ("ab_block_saltlake", "AB Block, Salt Lake", "East_SaltLake", 22.5940, 88.4080, 8.8, "Theme", 16, 1, "City Centre 1", "Peaceful residential park setting featuring delicate terracotta artwork.", "Salt Lake Sector I"),
    ("ac_block_saltlake", "AC Block, Salt Lake", "East_SaltLake", 22.5935, 88.4065, 8.8, "Traditional", 16, 1, "City Centre 1", "Traditional Pratima with community cultural plays and authentic bhog distribution.", "Salt Lake Sector I"),
    ("ad_block_saltlake", "AD Block, Salt Lake", "East_SaltLake", 22.5925, 88.4050, 8.8, "Theme", 16, 1, "City Centre 1", "Innovative lighting and eco-friendly themes along the quiet avenue.", "Salt Lake Sector I"),
    ("ae_block_saltlake", "AE Block (Part 1), Salt Lake", "East_SaltLake", 22.5900, 88.4060, 8.9, "Theme", 18, 2, "Central Park Metro", "Major Salt Lake crowd puller with grand thematic entry gates.", "Salt Lake Sector I"),
    ("ba_block_saltlake", "BA Block, Salt Lake", "East_SaltLake", 22.5950, 88.4120, 8.8, "Traditional", 16, 1, "City Centre 1", "Charming traditional puja with classical Dhaki music and adda.", "Salt Lake Sector I"),
    ("bb_block_saltlake", "BB Block, Salt Lake", "East_SaltLake", 22.5945, 88.4140, 8.8, "Theme", 16, 1, "City Centre 1", "Artistic wood and metal reliefs with peaceful crowd queues.", "Salt Lake Sector I"),
    ("bc_block_saltlake", "BC Block, Salt Lake", "East_SaltLake", 22.5940, 88.4160, 8.8, "Theme", 16, 1, "Karunamoyee", "Community park installation with creative rural handicrafts.", "Salt Lake Sector I"),
    ("ca_block_saltlake", "CA Block, Salt Lake", "East_SaltLake", 22.5890, 88.4050, 8.9, "Theme", 18, 2, "Central Park Metro", "Famous for elaborate terracotta temple replicas and family ambiance.", "Salt Lake Sector I"),
    ("gd_block_saltlake", "GD Block, Salt Lake", "East_SaltLake", 22.5810, 88.4100, 8.9, "Theme", 18, 2, "Karunamoyee", "Southern Salt Lake crowd favorite with grand lighting across the park.", "Salt Lake Sector III"),
    ("hb_block_saltlake", "HB Block, Salt Lake", "East_SaltLake", 22.5800, 88.4140, 8.8, "Theme", 16, 1, "Karunamoyee", "Artistic community installation using recycled environmental media.", "Salt Lake Sector III"),
    ("ib_block_saltlake", "IB Block, Salt Lake", "East_SaltLake", 22.5780, 88.4160, 8.8, "Traditional", 16, 1, "Salt Lake Stadium", "Cozy park setting with pure traditional Ekchala idol and festive adda.", "Salt Lake Sector III"),
    ("karunamoyee_housing", "Karunamoyee Housing Complex", "East_SaltLake", 22.5850, 88.4180, 8.9, "Traditional", 18, 2, "Karunamoyee Metro", "Massive residential colony puja with carnival rides, food stalls, and cultural nights.", "Karunamoyee Complex"),
    ("new_town_sarbojanin", "New Town Sarbojanin (Swapno Bhor)", "East_SaltLake", 22.5820, 88.4680, 9.3, "Theme", 22, 2, "Action Area 1 / Eco Park", "New Town's mega hub; grand futuristic installations with vast open manicured plazas.", "Major Arterial Road New Town"),
    ("new_town_balaka", "New Town Balaka Abasan", "East_SaltLake", 22.5840, 88.4620, 8.9, "Theme", 18, 2, "New Town Bus Stand", "Sprawling residential township puja featuring creative modern themes.", "Action Area 1D"),
    ("new_town_uniworld", "Uniworld City Durgotsav", "East_SaltLake", 22.5750, 88.4820, 9.0, "Theme", 20, 2, "Action Area 3", "Gated township extravaganza in Action Area 3 with international flair.", "Uniworld City New Town"),
    ("kankurgachi_mitali", "Kankurgachi Mitali Sangha", "East_SaltLake", 22.5775, 88.3895, 9.4, "Theme", 20, 3, "Phoolbagan", "Eastern corridor superstar; consistently creates monumental visual replicas drawing huge crowds.", "Kankurgachi VIP Market"),
    ("kankurgachi_swapnarbag", "Kankurgachi Swapnarbag", "East_SaltLake", 22.5790, 88.3910, 9.0, "Theme", 18, 2, "Phoolbagan", "Thoughtful eco-artistic installations just a short walk from Mitali Sangha.", "Maniktala Main Road"),

    # =========================================================================
    # --- VIP ROAD, LAKE TOWN, BANGUR & DUM DUM (18 PANDALS) ---
    # =========================================================================
    ("sreebhumi", "Sreebhumi Sporting Club", "East_VIP", 22.5995, 88.4042, 9.9, "Theme", 30, 3, "Ultadanga / VIP Road", "World-famous monumental wonder replicas (Burj Khalifa, Vatican, Disneyland, Tirupati). Massive crowd puller.", "VIP Road Lake Town"),
    ("lake_town_adhibasi", "Lake Town Adhibasi Brinda", "East_VIP", 22.6045, 88.4010, 9.2, "Theme", 18, 2, "VIP Road", "Just down the street from Sreebhumi; artistic eco-craft and peaceful aesthetic balance.", "Lake Town Block B"),
    ("lake_town_netaji", "Lake Town Netaji Sporting Club", "East_VIP", 22.6020, 88.4030, 9.0, "Theme", 18, 2, "VIP Road", "Popular Lake Town neighborhood hub featuring grand thematic lighting from Chandannagar.", "Lake Town Block A"),
    ("lake_town_block_a", "Lake Town Block A Sarbojanin", "East_VIP", 22.6010, 88.4000, 8.9, "Traditional", 16, 2, "VIP Road", "Serene traditional pratima with lovely neighborhood adda and cultural plays.", "Lake Town Main Road"),
    ("lake_town_kalindi", "Kalindi Housing Sarbojanin", "East_VIP", 22.6090, 88.3980, 8.9, "Theme", 16, 2, "Dum Dum Metro", "Popular housing estate puja near Jessore Road with creative theme decor.", "Kalindi Housing"),
    ("dum_dum_park_bharat", "Dum Dum Park Bharat Chakra", "East_VIP", 22.6080, 88.4080, 9.5, "Theme", 22, 3, "Nagerbazar / VIP Road", "High art conceptual powerhouse along the VIP Road canal strip; multiple major awards.", "Dum Dum Park"),
    ("dum_dum_tarun_sangha", "Dum Dum Park Tarun Sangha", "East_VIP", 22.6095, 88.4095, 9.4, "Theme", 20, 2, "Nagerbazar", "Famous for breathtaking experimental sculptures, hand-woven fabrics, and rural artisanal motifs.", "Dum Dum Park Tank 3"),
    ("dum_dum_tarun_dal", "Dum Dum Park Tarun Dal", "East_VIP", 22.6070, 88.4110, 9.2, "Theme", 18, 2, "Nagerbazar", "Completes the famous Dum Dum Park trio; known for vibrant folk artwork and metal craft.", "Dum Dum Park Tank 2"),
    ("dum_dum_park_yubak", "Dum Dum Park Yubak Brinda", "East_VIP", 22.6060, 88.4070, 8.9, "Theme", 16, 2, "VIP Road", "Adjacent neighborhood hub with delightful handcrafted terracotta and mud work.", "Dum Dum Park Tank 1"),
    ("bangur_pallimangal", "Bangur Avenue Pallimangal Samity", "East_VIP", 22.6050, 88.4120, 9.0, "Theme", 18, 2, "Dum Dum Metro / VIP Rd", "Bangur's top thematic presentation with vast manicured lawns and food stalls.", "Bangur Avenue Block B"),
    ("bangur_block_c", "Bangur Avenue Block C Sarbojanin", "East_VIP", 22.6070, 88.4140, 8.8, "Traditional", 16, 1, "VIP Road", "Peaceful residential puja with traditional Pratima and musical soirees.", "Bangur Avenue Block C"),
    ("dum_dum_cantonment", "Dum Dum Cantonment Sarbojanin", "East_VIP", 22.6280, 88.4150, 8.9, "Theme", 18, 2, "Dum Dum Cantonment Station", "Historical railway hub puja known for grand lighting and community adda.", "Subhas Nagar Road"),
    ("nagerbazar_sarbojanin", "Nagerbazar Sarbojanin", "East_VIP", 22.6150, 88.4180, 8.9, "Traditional", 16, 2, "Dum Dum Metro", "High-density transit hub puja on Jessore Road with glowing chandeliers.", "Jessore Road Nagerbazar"),
    ("baguiati_joramandir", "Baguiati Joramandir Sarbojanin", "East_VIP", 22.6180, 88.4230, 9.1, "Theme", 18, 2, "VIP Road Baguiati", "VIP Road favorite known for stunning thematic walkthroughs and festive lights.", "VIP Road Crossing"),
    ("baguiati_railpukur", "Baguiati Railpukur United Club", "East_VIP", 22.6190, 88.4280, 9.0, "Theme", 18, 2, "VIP Road", "Lake-adjacent installation with floating decor and glowing water reflections.", "Railpukur Road"),
    ("baguiati_arjunpur", "Arjunpur Amra Sabai Club", "East_VIP", 22.6220, 88.4260, 9.2, "Theme", 20, 2, "VIP Road / Airport", "Multiple award-winner for poignant social and philosophical installation art.", "Arjunpur Baguiati"),
    ("teghoria_sarbojanin", "Teghoria Sarbojanin", "East_VIP", 22.6240, 88.4320, 8.9, "Traditional", 16, 2, "VIP Road", "Busy VIP Road corridor stop with towering temple architecture replica.", "Teghoria Main Road"),
    ("kestopur_prafulla_kanan", "Kestopur Prafulla Kanan Paschim", "East_VIP", 22.6020, 88.4220, 9.1, "Theme", 18, 2, "Kestopur VIP Road", "Famous for intricate handloom and straw craft; huge crowd magnet along the canal.", "Prafulla Kanan Kestopur"),

    # =========================================================================
    # --- HOWRAH & HOOGHLY (14 PANDALS) ---
    # =========================================================================
    ("belur_math", "Belur Math (Ramakrishna Mission)", "Howrah", 22.6322, 88.3562, 9.9, "Traditional", 35, 3, "Belur / Dakshineswar Metro", "Spiritual epicenter founded by Swami Vivekananda; world-famous for its revered Ashtami Kumari Puja along the Ganga.", "Belur Math Road"),
    ("howrah_salkia_alapani", "Salkia Alapani Club", "Howrah", 22.6050, 88.3490, 9.3, "Theme", 20, 2, "Howrah Station", "Howrah's premiere thematic award-winner; innovative socio-artistic concepts.", "Aurobindo Road Salkia"),
    ("howrah_bantra", "Bantra Sammilani", "Howrah", 22.5930, 88.3320, 9.1, "Traditional", 18, 2, "Howrah Station", "Centenary traditional puja in central Howrah famous for majestic pratima and Chandannagar lights.", "Kadamtala / Bantra"),
    ("howrah_mandirtala", "Shibpur Mandirtala Sarbojanin", "Howrah", 22.5650, 88.3180, 9.2, "Theme", 20, 2, "Vidyasagar Setu Toll Plaza", "Located right at the foot of Vidyasagar Setu (2nd Hooghly Bridge); grand themes and easy transit.", "Mandirtala Shibpur"),
    ("howrah_olabibitola", "Olabibitola Sarbojanin", "Howrah", 22.5780, 88.3240, 9.0, "Theme", 18, 2, "Howrah Maidan Metro", "Adjacent to Green Line Metro terminal; acclaimed for eco-sculptures and folk art.", "Olabibitola Lane"),
    ("howrah_kadamtala", "Kadamtala Sarbojanin", "Howrah", 22.5870, 88.3280, 8.9, "Traditional", 16, 2, "Howrah Station", "Busy central Howrah hub with glowing illuminated archways and classic Pratima.", "Kadamtala Crossing"),
    ("howrah_ramrajatala", "Ramrajatala Sarbojanin", "Howrah", 22.5750, 88.3050, 9.0, "Traditional", 18, 2, "Ramrajatala Station", "Historic temple town puja adjacent to the celebrated Ram-Sita mandir.", "Ramrajatala Bazar"),
    ("howrah_santragachi", "Santragachi Lake Sarbojanin", "Howrah", 22.5810, 88.2880, 8.9, "Theme", 18, 2, "Santragachi Railway Jn", "Scenic lakeside setting; environmental and migratory bird conservation themes.", "Santragachi Station Rd"),
    ("howrah_chatterjeehat", "Chatterjeehat Sarbojanin", "Howrah", 22.5710, 88.3120, 8.8, "Traditional", 16, 2, "Shibpur", "Traditional neighborhood community puja with vibrant cultural evenings.", "Chatterjeehat Crossing"),
    ("howrah_kona_express", "Kona Express Durgotsav", "Howrah", 22.5890, 88.2950, 9.1, "Theme", 18, 2, "Kona Expressway", "Massive open highway space allowing monumental architecture and amusement parks.", "Kona Expressway"),
    ("belur_saptarshi", "Belur Saptarshi Sangha", "Howrah", 22.6280, 88.3510, 8.9, "Theme", 16, 2, "Belur Station", "Popular youth club near Belur Math featuring creative eco-friendly art.", "GT Road Belur"),
    ("bally_durgotsav", "Bally Durgotsav", "Howrah", 22.6510, 88.3440, 9.0, "Traditional", 18, 2, "Bally Railway Station", "Centenary traditional puja with authentic Daker Saaj idol and classical rituals.", "Bally Bazar GT Road"),
    ("uttarpara_sarbojanin", "Uttarpara Sarbojanin (Hooghly)", "Howrah", 22.6680, 88.3470, 9.1, "Traditional", 18, 2, "Uttarpara Station", "Historic Hooghly riverbank town puja near the legendary Joy Krishna Public Library.", "GT Road Uttarpara"),
    ("serampore_goswami_bari", "Serampore Goswami Bari (Hooghly)", "Howrah", 22.7520, 88.3450, 9.4, "Bonedi_Bari", 20, 2, "Serampore Station", "Centuries-old historic aristocratic Vaishnavite Bonedi Bari; majestic Thakur Dalan and preserved rituals.", "Goswami Street Serampore")
]

def generate_pandals_file():
    content = '''"""
Master Catalog of 150+ Curated Durga Puja Pandals across West Bengal.
"""

from dataclasses import dataclass

@dataclass
class Pandal:
    id: str
    name: str
    zone: str
    lat: float
    lon: float
    base_rating: float
    theme_type: str
    avg_visit_mins: int
    crowd_tier: int
    nearest_metro: str
    description: str
    key_street: str = ""

SAMPLE_PANDALS = [
'''
    for item in PANDALS_RAW:
        pid, name, zone, lat, lon, rating, theme, mins, crowd, metro, desc, street = item
        content += f"""    Pandal(
        id="{pid}",
        name="{name}",
        zone="{zone}",
        lat={lat},
        lon={lon},
        base_rating={rating},
        theme_type="{theme}",
        avg_visit_mins={mins},
        crowd_tier={crowd},
        nearest_metro="{metro}",
        description="{desc}",
        key_street="{street}"
    ),
"""
    content += "]\n"
    
    with open("pandals_data.py", "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated pandals_data.py successfully with {len(PANDALS_RAW)} pandals!")

if __name__ == "__main__":
    generate_pandals_file()
