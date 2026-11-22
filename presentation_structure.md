# 📊 MARSBOUND: Project Presentation PPT Structure
## Compulsory Presentation Slide Deck (100-Point Evaluation Rubric)
### ASTRA 2026 Space Hackathon — VIT Bhopal University

---

### Slide 1: Title & Overview
* **Project Title:** MARSBOUND: Unified ISRO Launch Telemetry, Ascent Trajectory & On-Orbit Mission Operations Platform
* **Event:** ASTRA 2026 Space Hackathon (ANTERIX Club, VIT Bhopal University)
* **Team Members:** [Your Team Names & Registration Numbers]
* **Core Domains:**
  * 01 | Indian Space Missions & Space Data
  * 02 | Earth Observation & Satellite Applications
  * 03 | Space-Based Disaster Management
  * 06 | Sustainable Space & Space Environment
* **Designated Portals Integrated:** Bhuvan • MOSDAC • Bhoonidhi • VEDAS / NEDAS

---

### Slide 2: The Core Problem & Motivation
* **The Aerospace Challenge:**
  * Launch decisions for multi-million dollar satellite missions require **100% deterministic, explainable, and zero-failure criteria**.
  * Data across ISRO's primary hubs (**MOSDAC** for weather, **Bhuvan** for GIS maps, **Bhoonidhi** for raw sensor data, **VEDAS** for environmental indicators) currently exist in separate portals, creating coordination lag during launch windows and disaster response.
* **Our Solution:**
  * An end-to-end mission intelligence system that unifies pre-launch Go/No-Go verification, ascent trajectory flight physics, orbital insertion, and on-orbit scientific data acquisition into a single interactive command center.

---

### Slide 3: Why Deterministic Physics Engine? (No Black-Box AI)
* **Aerospace Rationale (10 Marks - Innovation & Creativity):**
  * In actual space agencies (ISRO SDSC-SHAR, NASA, ESA), Automated Launch Sequences (ALS) **never use black-box machine learning models** for life-or-death launch decisions.
  * A single hallucinated probability in ML can cause catastrophic vehicle breakup during Max-Q.
* **The Deterministic Advantage:**
  * 100% mathematically verifiable Launch Commit Criteria (LCC).
  * Real-time aerodynamic shock heating ($T_{\text{skin}}$), barometric falloff ($\rho(h)$), dynamic pressure ($Q$), Tsiolkovsky $\Delta v$, and Friis communication link budgets.
  * Instant, transparent root-cause fault logging when safety thresholds are breached.

---

### Slide 4: System Architecture & Data Flow
* **Architecture Diagram:**
  * **Input Layer:** Real-world environmental variables from MOSDAC (INSAT-3D CTT, wind shear), Bhoonidhi (orbital debris catalog, multi-spectral bands), Bhuvan (launch azimuth, flood hazard zones), and VEDAS (geomagnetic Kp, drought index).
  * **Core Engine:** Deterministic LCC rule evaluator, 3-stage ascent physics integrator, and spectral index computer.
  * **Interactive UI:** Aerospace glassmorphism dashboard, real-time 2D ascent canvas, Leaflet.js orbital ground tracker, and Chart.js telemetry telemetry feeds.
  * **Output Layer:** Live Go/No-Go status, active milestone ticker, and downloadable ISRO Mission Verification Dossier.

---

### Slide 5: Phase 1 — Pre-Launch Go / No-Go Decision Console
* **4 Core Subsystems Monitored Against Strict LCC Limits:**
  1. **MOSDAC Weather:** Surface winds $< 15\text{ m/s}$, upper shear $< 25\text{ m/s}$, cloud top temp $> -25^\circ\text{C}$, zero lightning.
  2. **Propulsion & Cryo Tanks:** LOX ($-183.1^\circ\text{C}$), LH2 ($-253^\circ\text{C}$), C25 tank ullage pressure (2.0–2.6 bar).
  3. **Deep Space Network:** IDSN Byalalu 32m antenna lock, link SNR margin $> 14\text{ dB}$, VEDAS geomagnetic $\text{Kp} < 5.0$.
  4. **Orbital Corridor:** Bhoonidhi debris clearance $> 25\text{ km}$, collision probability $P_c < 10^{-6}$.
* **Interactive Anomaly Sandbox:**
  * Judges can test live edge cases (e.g. trigger high wind shear or cryo leaks) and watch the master state immediately trip from **`GO FOR LAUNCH`** to **`HOLD / NO-GO`**.

---

### Slide 6: Phase 2 — Ascent Trajectory & Flight Dynamics
* **Vehicle Architecture (ISRO LVM3 Heavy Lift Profile):**
  * Stage 1: Twin S200 Solid Strap-ons (High initial thrust, $T-0$ to $T+110\text{s}$)
  * Stage 2: Vikas L110 Liquid Core ($T+110\text{s}$ to $T+200\text{s}$)
  * Stage 3: C25 Cryogenic Upper Stage ($T+200\text{s}$ to $T+320\text{s}$)
* **Key Aerodynamic Milestones Simulated:**
  * Gravity turn downrange trajectory over the Bay of Bengal.
  * **Max-Q Region ($T+60\text{s}$ at 12–14 km):** Dynamic pressure peaks at 38.4 kPa (safely below 45 kPa limit).
  * Transonic shock barrier ($M=1.0$) and hypersonic ascent ($M>5.0$).
  * Fairing separation ($>115\text{ km}$) exposing payload in vacuum.
  * Continuous tracking handover: SDSC SHAR $\to$ Port Blair $\to$ IDSN Byalalu.

---

### Slide 7: Phase 3 — Orbital Trajectory & Ground Track Map
* **Orbital Mechanics & Sun-Synchronous Orbit (SSO):**
  * Altitude: 450 km LEO | Velocity: 27,480 km/h (7.63 km/s) | Orbital Period: 93.6 minutes.
* **Interactive Geospatial Visualization:**
  * Real-time sine-wave ground track over India on an interactive Leaflet dark map.
  * Dynamic satellite marker with animated 400 km sensor swath footprint circle.
  * Satellite bus telemetry: 2,400W solar panel array power generation, day/night eclipse cycle monitoring, and battery state of charge.

---

### Slide 8: Phase 4 — On-Orbit Satellite Work (The 4 ISRO Portals)
* **What the Satellite Actually Does in Orbit:**
  * 🌾 **Bhoonidhi Remote Sensing Lab:** Live multi-spectral band sliders (NIR, Red, Green) computing **NDVI** (crop stress/biomass health) and **NDWI** (flood inundation).
  * 🌪️ **MOSDAC Meteorology:** Thermal Infrared sounder tracking Bay of Bengal cyclonic storms, central barometric pressure, SST anomalies, and precipitation rates.
  * 🗺️ **Bhuvan Geospatial Disaster:** High-resolution SAR flood hazard mapping (41,200 ha inundated in Odisha/Andhra) with safe evacuation corridors and 1-click emergency dispatch.
  * ☀️ **VEDAS Environmental Analytics:** Multi-year Drought Vulnerability Index (DVI) anomaly mapping and solar insolation potential (5.82 kWh/m²/day).

---

### Slide 9: Phase 5 — Mars Orbital Payloads Suite (MENCA • MCC • MSM • TIS)
* **Astrodynamics & MARSBOUND Interplanetary Cruise:**
  * Exact 297-day Lambert heliocentric transfer covering 680 million km, one-way light delay ($12.5 - 21\text{ min}$), SEP solar conjunction blackout alerts, and retrograde MOI burn ($1,098.7\text{ m/s}$).
* **Full Suite of 4 Science Payloads Operationalized:**
  * 🔬 **MENCA (Mass Spectrometer):** Quadrupole neutral species profiling ($CO_2, Ar\text{-}40, N_2/CO, O, H_2O$) from $350\text{ km}$ to $2,000\text{ km}$, documenting barometric falloff and exospheric pressure.
  * 📸 **MCC (Colour Camera):** Dynamic Ground Sampling Distance ($22\text{ m/px}$ periapsis to $4,000\text{ m/px}$ apoapsis), atmospheric dust optical depth ($\tau$) attenuation via Beer-Lambert law, and high-res terrain viewports.
  * 💨 **MSM (Methane Sensor for Mars):** Differential absorption in $3.3\,\mu\text{m}$ band, columnar abundance in ppb, active plume anomaly trigger ($> 10\text{ ppb}$), and serpentinization (abiotic mantle olivine hydration) vs biogenic classification.
  * 🌡️ **TIS (Thermal Infrared Spectrometer):** Diurnal temperature range ($145\text{ K}$ to $286\text{ K}$), Apparent Thermal Inertia ($\text{ATI}$), regolith wheel trafficability classification, and mineralogical decomposition (clays, carbonates, sulfates, olivine).

---

### Slide 10: Candidate Spots for Exploration & Rover Route Decision Engine
* **Candidate Site Selection (Multi-Criteria Decision Analysis — MCDA):**
  * Evaluates 6 high-priority landing zones: **Jezero Crater** (ancient delta), **Gale Crater** (layered lake strata), **Oxia Planum** (vast Noachian clay plains), **Nili Fossae** (peak methane anomaly grabens), **Valles Marineris** (deep canyon stratigraphy), and **Elysium Planitia** (flat volcanic plain).
  * Synthesizes Science Value Score ($S_{\text{sci}}$) and Landing & Engineering Safety Score ($S_{\text{safe}}$) into the **Exploration Viability Index ($EVI$)**.
* **Lower-Risk Autonomous Rover Route Planning:**
  * Computes landing ellipse to primary science waypoint traverse path: distance (km), maximum slope encounter, bearing capacity from TIS ATI, daily solar energy budget ($kWh/\text{sol}$), and estimated duration in Sols.
  * Direct integration into the downloadable official ISRO mission report dossier.

---

### Slide 11: Technical Implementation & Code Quality (25 Marks)
* **Modern, Modular Engineering:**
  * **Frontend:** High-performance single-page web app with Tailwind CSS, Lucide icons, Chart.js, and Leaflet.js.
  * **Aerospace Backend:** Standalone Python engine (`launch_physics_engine.py`) containing numerical integration, LCC verification, and unit tests.
  * **Zero Setup Friction:** Runs locally in seconds or deploys globally on Vercel / GitHub Pages with 100% uptime and zero server crashes.
  * **Automated Reporting:** Generates downloadable official `.txt` mission summary dossiers.

---

### Slide 12: Scalability, Real-World Impact & Conclusion (10 Marks)
* **Scalability Potential:**
  * Can ingest live open REST APIs from Bhuvan WMS, MOSDAC FTP, and Bhoonidhi catalogs.
  * Extensible to interplanetary trajectories (Chandrayaan lunar South Pole, Gaganyaan crew escape abort criteria).
* **Summary of Mandatory Deliverables:**
  1. ✅ **GitHub Repository:** [https://github.com/Keshav4916/MARSBOUND](https://github.com/Keshav4916/MARSBOUND)
  2. ✅ **Compulsory Presentation PPT:** Slide deck aligned with the 100-mark rubric (`presentation_structure.md`).
  3. ✅ **Demo Video:** Crisp recorded voiceover demonstration script (`demo_video_script.md`).
  4. ✅ **Deployed Project Link:** [https://keshav4916.github.io/MARSBOUND/](https://keshav4916.github.io/MARSBOUND/)

---
