# 📊 MARSBOUND: Exact 8-Slide Hackathon Presentation Deck
## ASTRA 2026 Space Hackathon — VIT Bhopal University
### Theme: Space Science, Indian Space Missions & Satellite Technologies
**Live Repository:** [https://github.com/Keshav4916/MARSBOUND](https://github.com/Keshav4916/MARSBOUND)  
**Live Deployed Web App:** [https://keshav4916.github.io/MARSBOUND/](https://keshav4916.github.io/MARSBOUND/)

---

### 🛰️ Slide 1: Mission Overview, Architecture & ISRO Portals Integration
* **Project Title:** MARSBOUND — Deterministic Aerospace Mission Control & Earth Observation Platform
* **Event & Alignment:** ASTRA 2026 Space Hackathon (ANTERIX Club, VIT Bhopal University)
  * Aligned Core Domains: 01 (Indian Space Missions & Data), 02 (Earth Observation), 03 (Disaster Management), 06 (Sustainable Space)
* **The Core Problem:**
  * Mission-critical launch and flight decisions require **100% deterministic, explainable, and zero-failure criteria**.
  * Data across ISRO's primary hubs (**MOSDAC** weather, **Bhuvan** GIS maps, **Bhoonidhi** EO catalog, **VEDAS** geo-analytics) currently operate in silos, creating coordination lag during launch windows and disaster response.
* **Our Solution:**
  * A unified, web-first mission intelligence system integrating pre-launch Go/No-Go checks, 3-stage ascent physics, orbital tracking, Mars interplanetary transfer, closed-loop rover target positioning, and multi-parametric risk analysis.
* **Designated Portals Integrated:**
  * **Bhuvan (NRSC):** Launchpad coordinates (SDSC SHAR: 13.7199° N, 80.2305° E), downrange azimuth corridor, flood risk zonation polygons.
  * **MOSDAC (SAC):** INSAT-3D/3DR TIR Cloud Top Temperature (CTT), upper wind shear, Sea Surface Temperature (SST), and Bay of Bengal cyclone tracking.
  * **Bhoonidhi (NRSC):** High-res optical & SAR radar catalog, real-time NDVI crop health, and NDWI flood mapping.
  * **VEDAS (SAC/NESAC):** Spatio-temporal Drought Vulnerability Index (DVI), solar insolation atlas, and geomagnetic Kp monitoring.

---

### 🛡️ Slide 2: Phase 1 — Pre-Launch Go / No-Go Decision Console (Zero Machine Learning)
* **Aerospace Rationale (Deterministic vs. Black-Box AI):**
  * Real-world space agencies (ISRO SDSC-SHAR, NASA, ESA) **never use black-box machine learning** for life-or-death launch commit decisions.
  * A single hallucinated probability in ML can cause catastrophic vehicle breakup during Max-Q.
  * MARSBOUND implements mathematically verifiable Launch Commit Criteria (LCC) based on physics equations and thermodynamic limits.
* **4 Core Subsystems Monitored Against Strict LCC Limits:**
  1. **MOSDAC Weather:** Surface winds $< 15\text{ m/s}$, upper shear $< 25\text{ m/s}$, cloud top temp $> -25^\circ\text{C}$, zero lightning.
  2. **Propulsion & Cryo Tanks:** LOX ($-183.1^\circ\text{C}$), LH2 ($-253^\circ\text{C}$), C25 tank ullage pressure (2.0–2.6 bar).
  3. **Deep Space Network:** IDSN Byalalu 32m antenna lock, link SNR margin $> 14\text{ dB}$, VEDAS geomagnetic $\text{Kp} < 5.0$.
  4. **Orbital Corridor:** Bhoonidhi debris clearance $> 25\text{ km}$, collision probability $P_c < 10^{-6}$.
* **Interactive Anomaly Sandbox for Judges:**
  * Live edge-case buttons (*"Inject High Wind Shear"*, *"Inject Cryo Ullage Drop"*, *"Spawn Debris Hazard"*).
  * System instantly trips master state from **`GO FOR LAUNCH`** to **`HOLD / NO-GO`** with automated root-cause telemetry violation logging.

---

### 🚀 Slide 3: Phase 2 — 3-Stage Ascent Trajectory & Flight Dynamics
* **Vehicle Profile (ISRO LVM3 Heavy Lift Configuration):**
  * **Stage 1 (Twin S200 Solid Boosters):** Initial thrust $2 \times 5,150\text{ kN}$, $T-0$ to $T+110\text{s}$.
  * **Stage 2 (Vikas L110 Liquid Core):** $1,598\text{ kN}$ thrust, $T+110\text{s}$ to $T+200\text{s}$.
  * **Stage 3 (C25 Cryogenic Upper Stage):** High-$I_{sp}$ ($443\text{s}$) CE-20 engine, $T+200\text{s}$ to orbital injection.
* **Deterministic Aerospace Aerodynamics Simulated:**
  * **Tsiolkovsky Net Acceleration:** $F_{\text{net}}(t) = T(t) - D(t) - m(t) \cdot g(h)\sin(\theta)$
  * **Max-Q Dynamic Pressure Region ($T+60\text{s}$ at 12–14 km):** Peaks at $38.4\text{ kPa}$ (safely within structural threshold $Q \le 45.0\text{ kPa}$).
  * **Compressible Shock Recovery Temperature:** $T_{\text{skin}} = T_{\text{ambient}}(h) \cdot \left[1 + 0.88 \cdot \frac{\gamma - 1}{2} M^2\right]$
  * **Gravity Turn & Sri Lanka Dogleg:** Pitch program smooths vehicle towards local horizon; $+14.2^\circ$ SE corridor offset avoids Sri Lankan airspace.
  * **Stage Splashdown Clearances:** S200 ($T+110\text{s}$, $385\text{ km}$ downrange), Fairing ($T+145\text{s}$, $118.2\text{ km}$ alt), Vikas ($T+200\text{s}$, $1,240\text{ km}$ downrange) into cleared Bay of Bengal maritime corridors.

---

### 🌍 Slide 4: Phase 3 — Orbital Trajectory & Ground Track Map
* **Orbital Mechanics & Sun-Synchronous Orbit (SSO):**
  * Altitude: $450\text{ km}$ circular LEO | Velocity: $27,480\text{ km/h}$ ($7.63\text{ km/s}$) | Period: $93.6\text{ minutes}$ ($15.4\text{ orbits/day}$).
  * Specific Orbital Energy: $\varepsilon = -29.33\text{ MJ/kg}$ (Bound gravitational Keplerian state).
* **Interactive Leaflet Geospatial Tracking Map:**
  * Real-time sine-wave ground track over the Indian subcontinent on Leaflet dark canvas basemap.
  * Animated satellite position marker with dynamic $400\text{ km}$ Earth observation sensor swath circle.
  * Ground Tracking Station Footprints: SDSC SHAR, ISTRAC Bengaluru, Port Blair, and IDSN Byalalu 32m deep-space dish.
* **Satellite Bus Telemetry & Link Budget:**
  * 2,400W solar panel array power generation, day/night eclipse transition timers, and battery state of charge ($98.4\%$).
  * Friis Link Budget Margin: $\text{SNR} = 24.6\text{ dB} > 14.0\text{ dB}$ minimum with active Doppler tracking.

---

### 🛰️ Slide 5: Phase 4 — On-Orbit Earth Science Lab (The 4 ISRO Portals)
* **What the Satellite Actually Does in Orbit:**
  * 🌾 **Bhoonidhi Remote Sensing Lab:**
    * Multi-spectral band sliders (NIR, Red, Green) computing real-time reflectance indices:
      $$\text{NDVI} = \frac{\text{NIR} - \text{Red}}{\text{NIR} + \text{Red}} \quad \text{(Crop biomass health / drought stress)}$$
      $$\text{NDWI} = \frac{\text{Green} - \text{NIR}}{\text{Green} + \text{NIR}} \quad \text{(Water body / flood inundation)}$$
    * Instant presets for Healthy Crop Canopy, Drought-Stressed Farmland, and Inundated Flood Water.
  * 🌪️ **MOSDAC Meteorology & Cyclone Tracker:**
    * Real-time INSAT-3D thermal infrared sounder tracking active Bay of Bengal cyclonic storms, central barometric pressure ($972\text{ hPa}$), Sea Surface Temperature anomalies, and rainfall rate ($32\text{ mm/hr}$).
  * 🗺️ **Bhuvan Geospatial Disaster Intelligence:**
    * District-level flood risk mapping ($41,200\text{ ha}$ inundated across coastal corridors).
    * One-click tactical emergency dispatch vector transmitting evacuation corridor polygons to NDRF and SDMA.
  * ☀️ **VEDAS Environmental & Climate Analytics:**
    * Multi-year Drought Vulnerability Index (DVI) trends, surface solar insolation atlas ($5.82\text{ kWh/m}^2/\text{day}$), and atmospheric optical depth (AOD).

---

### 🔴 Slide 6: Phase 5 — Mars Mission & Scientific Payloads Suite
* **Interplanetary Astrodynamics (MARSBOUND Orbiter):**
  * Exact 297-day Lambert heliocentric transfer covering $680\text{ million km}$ from Earth (TMI: Dec 1, 2013) to Mars (MOI: Sept 24, 2014).
  * Real-time light travel delay calculation ($12.5 - 21\text{ minutes}$ One-Way Light Time) with IDSN Byalalu 32m link.
  * Sun-Earth-Probe (SEP) angle tracking with automated solar conjunction radio blackout alerts ($SEP < 2.5^\circ$).
  * Mars Orbit Insertion (MOI) retrograde burn: $\Delta v = 1,098.7\text{ m/s}$ (1,388s burn duration via 440N LAM engine) achieving $421.7\text{ km} \times 76,993\text{ km}$ orbit.
* **Full Suite of 4 Science Payloads Operationalized:**
  * 🔬 **MENCA (Mass Spectrometer):** Quadrupole neutral species profiling ($CO_2, Ar\text{-}40, N_2/CO, O, H_2O$) from $350\text{ km}$ to $2,000\text{ km}$, documenting barometric falloff and exospheric scale height.
  * 📸 **MCC (Colour Camera):** Ground Sampling Distance ($22\text{ m/px}$ periapsis to $77,000\text{ km}$ apoapsis), atmospheric dust optical depth ($\tau$) attenuation via Beer-Lambert law ($T = e^{-\tau/\cos\theta}$), and simulated RGB optical surface viewports.
  * 💨 **MSM (Methane Sensor for Mars):** Differential absorption in $3.3\,\mu\text{m}$ band, columnar abundance in ppb, active plume anomaly trigger ($> 10\text{ ppb}$), and serpentinization (abiotic mantle olivine hydration) vs biogenic classification.
  * 🌡️ **TIS (Thermal Infrared Spectrometer):** Diurnal temperature range ($175\text{ K}$ to $278\text{ K}$), Apparent Thermal Inertia ($\text{ATI}$), regolith wheel trafficability classification, and mineralogical decomposition (smectite clays, carbonates, sulfates, olivine).

---

### 🎯 Slide 7: Phase 6 — Feedback Loop 6: Rover Target Position, Maps & Operational Risk Summary
* **Interactive Mars Surface Maps:**
  * **Tactical Topography Radar HUD (Canvas):** High-definition terrain elevation isolines ($-2,800\text{ m}$ to $-1,800\text{ m}$), $7.5\text{ km} \times 4.2\text{ km}$ landing ellipse, safe traverse route waypoints, hazard polygons, scale bar ($1.0\text{ km}$), and rotating radar sweep.
  * **Geospatial Leaflet Basemap:** Photorealistic satellite layer placing markers at Martian coordinate equivalents.
* **Target Rover Position Telemetry:**
  * Live Martian Geodesy: Latitude `18.3842° N`, Longitude `77.5819° E`, Elevation `-2,504 m MOLA`, Heading `294.5° NW`, Slope `6.2°`.
  * Multi-Site Selector: Synchronizes across 6 exploration sites (**Jezero Crater**, **Gale Crater**, **Oxia Planum**, **Nili Fossae**, **Valles Marineris**, **Elysium Planitia**). Includes manual coordinate fine-tuning and click-to-reposition.
* **Deterministic Closed-Loop Feedback Guidance Controller (10 Hz):**
  $$\text{Target Waypoint } r_{\text{target}}(t) \longrightarrow \text{NavCam/TRN } r_{\text{actual}}(t) \longrightarrow \text{Error Detector } e(t) \longrightarrow \text{Risk Weighting } w_{\text{risk}} \longrightarrow \text{Adaptive Control } u(t) \longrightarrow \text{Loop Closure}$$
  * Tracks cross-track error ($\epsilon_{\text{cross}} = \pm 0.24\text{ m}$), along-track error ($\epsilon_{\text{along}} = +0.18\text{ m}$), and heading drift ($0.04^\circ$).
  * Interactive Perturbation Simulator: Click *"Inject Position Drift (+2.5m)"* to observe the error vector arrow $\vec{e}$ and loop trip, then click *"Execute Autonomous Closed-Loop Re-centering"* to watch the PID controller converge back to $\pm 0.04\text{ m}$.
* **Multi-Parametric Operational Risk Summary:**
  * Composite Risk Meter: Evaluates overall mission risk ($18.4\%$ - LOW RISK).
  * 6 Core Risk Domains: Terrain Slope ($6.2^\circ$ vs $12^\circ$), Boulder Density ($2.1/\text{m}^2$ vs $5.0$), Wheel Slip ($3.8\%$ vs $15\%$), Dust Storm ($\tau = 0.35$ vs $0.85$), Thermal Extreme (Warm bay $+14.6^\circ\text{C}$), and Radio Link ($256\text{ kbps}$ locked).
  * Includes active hazard injection sandbox and one-click Risk Dossier export.

---

### 🏆 Slide 8: Surface Science Timeline (Sol 0–120), Tech Stack & Hackathon Deliverables
* **Chronological Martian Surface Science Timeline (Sol 0 to Sol 120):**
  * **Sol 0–5:** Sky-crane retro-propulsion touchdown in Jezero Crater delta, solar array deployment, and NavCam calibration.
  * **Sol 10–20 (Geochemistry - Chandrayaan-3 Pragyan Heritage):** APXS and LIBS laser spectroscopy confirms Sulfur ($10.2\%$), Iron ($18.5\%$), Titanium, Calcium, and hydrated smectite clays in lacustrine mudstone.
  * **Sol 25–40:** Autonomous Visual Odometry driving $120\text{ m/hr}$; catalogs 142 terrain hazards with 0 obstacles $>35\text{ cm}$.
  * **Sol 42–55 (Water Ice Discovery):** Subsurface hydrogen/water-ice layer detected at $1.2\text{ m}$ depth ($35\text{ wt}\%$ water equivalent) with hermetic sample caching in titanium tube #04.
  * **Sol 60–85:** Dust storm early warning survival; high-voltage electrostatic dust mitigation repeller preserves $94.2\%$ solar array efficiency; 3x 1W RHUs maintain $+14.6^\circ\text{C}$ bay during $-100^\circ\text{C}$ nights.
  * **Sol 90–120:** Biosignature macromolecule screening and certification of $250\text{ m}$ obstacle-free landing ellipse for future ISRO crewed landers.
* **Streamlit & Python Embed:** One-click generation of `marsbound_streamlit_rover_dashboard.py` deploying Plotly orbital trajectories into Streamlit.
* **Automated Official Mission Report:** One-click download of the complete aerospace flight and science verification `.txt` dossier.
* **Mandatory Hackathon Deliverables Summary:**
  1. ✅ **GitHub Repository:** [https://github.com/Keshav4916/MARSBOUND](https://github.com/Keshav4916/MARSBOUND)
  2. ✅ **Live Deployed Web Application:** [https://keshav4916.github.io/MARSBOUND/](https://keshav4916.github.io/MARSBOUND/)
  3. ✅ **Official Slide Deck:** Complete 8-slide structure covering all 8 tabs (`presentation_structure.md`).
  4. ✅ **Demo Video Script:** Crisp recorded demonstration walkthrough (`demo_video_script.md`).
