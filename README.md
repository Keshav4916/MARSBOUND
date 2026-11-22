# 🛰️ MARSBOUND: ISRO Launch Decision, Flight Trajectory & On-Orbit Mission Operations Platform

> **VIT Bhopal University — ASTRA 2026 Space Hackathon**  
> *Central Theme: Space Science, Indian Space Missions & Satellite Technologies*  
> *Aligned Core Domains: 01 (Indian Space Missions & Data), 02 (Earth Observation), 03 (Disaster Management), 06 (Sustainable Space)*

---

## 📌 Executive Summary

**MARSBOUND** is a deterministic, physics-based aerospace mission control and Earth observation intelligence system. It manages the complete lifecycle of an Indian satellite mission:

1. **Pre-Launch Go/No-Go Decision Matrix:** Rigorous evaluation of vehicle telemetry and environmental variables against ISRO Launch Commit Criteria (LCC) — with zero black-box AI dependencies.
2. **Ascent Flight Dynamics Simulator:** 3-stage rocket ascent (modeled on ISRO LVM3), real-time gravity turn over the Bay of Bengal, Max-Q dynamic pressure calculation, and stage separations.
3. **Orbital Trajectory & Ground Track:** Real-time 2D/3D geospatial tracking of the satellite in Sun-Synchronous Low Earth Orbit (SSO/LEO), line-of-sight tracking by ISTRAC and the Indian Deep Space Network (IDSN Byalalu 32m antenna).
4. **On-Orbit Scientific Mission Operations:** Live simulation of the scientific work the satellite executes using data feeds across all four designated ISRO platforms: **Bhuvan**, **MOSDAC**, **Bhoonidhi**, and **VEDAS**.
5. **Interplanetary Mars Transfer & Payloads Science (MARSBOUND Orbiter):** Exact historical boundary value Lambert transfer from Earth (TMI: Dec 1, 2013) to Mars (MOI: Sept 24, 2014), IDSN Byalalu 32m deep-space link tracking, light delay calculations, solar conjunction blackout alerts, and live multi-instrument science via the **MENCA**, **MCC**, **MSM**, and **TIS** payloads.
6. **Automated Mission & Hazard Bulletin:** One-click generation and export of official aerospace flight readiness and disaster mitigation reports.

---

## 🏛️ Integration Across the 4 ISRO Portals

| ISRO Platform | Managing Center | Operational Role in MARSBOUND |
|---|---|---|
| **Bhuvan** | **NRSC / ISRO** | **National Geoportal:** Provides launchpad geospatial coordinates (SDSC SHAR Sriharikota: 13.7199° N, 80.2305° E), downrange azimuth safety corridor, district flood hazard zonation polygons, and emergency rescue vectors. |
| **MOSDAC** | **SAC / ISRO** | **Meteorology & Oceanography:** Real-time INSAT-3D/3DR Thermal Infrared (TIR) Cloud Top Temperature (CTT), upper-atmosphere wind shear gradients, Sea Surface Temperature (SST) anomalies, and active Bay of Bengal cyclone tracking. |
| **Bhoonidhi** | **NRSC / ISRO** | **Earth Observation Data Hub:** High-resolution optical & SAR radar data catalog. Computes real-time **NDVI** (crop stress/drought index) and **NDWI** (flood inundation index) from multi-spectral bands (NIR, Red, Green). Tracks orbital debris conjunction hazards. |
| **VEDAS / NEDAS** | **SAC & NESAC / ISRO** | **Geo-Analytics & Climate Monitoring:** Spatio-temporal environmental indicators, Drought Vulnerability Index (DVI) trends, solar insolation atlas (kWh/m²/day), and space weather geomagnetic Kp-index monitoring. |

---

## 📐 Deterministic Aerospace Physics (Zero Machine Learning)

In high-stakes aerospace operations, mission-critical launch decisions rely on deterministic physics equations, thermodynamic limits, and link-budget mathematics rather than unverified machine learning models:

### 1. Tsiolkovsky Rocket Dynamics & Net Acceleration
$$F_{\text{net}}(t) = T(t) - D(t) - m(t) \cdot g(h) \sin(\theta)$$
$$a(t) = \frac{F_{\text{net}}(t)}{m(t)}, \quad \dot{m} = \frac{T}{I_{sp} \cdot g_0}$$
$$\Delta v = I_{sp} \cdot g_0 \cdot \ln\left(\frac{m_0}{m_f}\right)$$

### 2. Aerodynamic Drag & Dynamic Pressure (Max-Q)
$$\rho(h) = \rho_0 \cdot e^{-h / H}$$
$$Q(t) = \frac{1}{2} \rho(h) \cdot v(t)^2, \quad D(t) = C_d \cdot A \cdot Q(t)$$
*Structural limit threshold: $Q \le 45.0 \text{ kPa}$.*

### 3. Aerodynamic Compressible Shock Recovery Temperature
$$T_{\text{skin}} = T_{\text{ambient}}(h) \cdot \left[1 + r \cdot \frac{\gamma - 1}{2} M^2\right]$$
*Where $M$ is Mach number, recovery factor $r \approx 0.88$, and specific heat ratio $\gamma = 1.4$.*

### 4. Deep Space Communications & Link Margin (IDSN Byalalu / ISTRAC)
$$\text{FSPL (dB)} = 20\log_{10}(d) + 20\log_{10}(f) + 20\log_{10}\left(\frac{4\pi}{c}\right)$$
$$\text{SNR (dB)} = P_{tx} + G_{tx} + G_{rx} - \text{FSPL} - L_{\text{atm}} - L_{\text{ion}} - 10\log_{10}(k \cdot T_{\text{sys}} \cdot B)$$
$$\Delta f = f_0 \cdot \frac{v_{\text{LOS}}}{c}$$

### 5. Multi-Spectral Remote Sensing Indices (Bhoonidhi Engine)
$$\text{NDVI} = \frac{\text{NIR} - \text{Red}}{\text{NIR} + \text{Red}} \quad (\text{Vegetation health / Crop canopy})$$
$$\text{NDWI} = \frac{\text{Green} - \text{NIR}}{\text{Green} + \text{NIR}} \quad (\text{Surface water inundation / Flood mapping})$$

### 6. Mars Orbiter Payloads Physics & Mineralogy (MARSBOUND Engine)
- **MCC Beer-Lambert Optical Extinction & Resolution:**
  $$\text{GSD} = h \cdot \frac{p}{f}, \quad T_{\text{atm}} = e^{-\tau / \cos(\theta_{\text{sza}})}$$
- **MSM Differential Absorption & Columnar Methane (ppb):**
  $$R_{\text{abs}} = \frac{I_{3.3\mu\text{m}}}{I_{\text{ref}}}, \quad [\text{CH}_4]_{\text{col}} = -\frac{1}{\alpha \cdot L} \ln(R_{\text{abs}})$$
- **TIS Apparent Thermal Inertia (ATI) & Diurnal Range:**
  $$\Delta T = T_{\text{day}} - T_{\text{night}}, \quad \text{ATI} = \frac{(1 - \rho) \cdot 1000}{\Delta T}$$
- **MCDA Exploration Viability Index (EVI):**
  $$S_{\text{sci}} = 0.35 \cdot C_{\text{clays}} + 0.30 \cdot M_{\text{CH}_4} + 0.20 \cdot D_{\text{min}} + 0.15 \cdot K_{\text{context}}$$
  $$S_{\text{safe}} = 0.35 \cdot E_{\text{elev}} + 0.35 \cdot \theta_{\text{slope}} + 0.15 \cdot T_{\text{therm}} + 0.15 \cdot \text{ATI}_{\text{traffic}}$$
  $$\text{EVI} = \sqrt{S_{\text{sci}} \cdot S_{\text{safe}}}$$

---

## 🚀 Key Modules in the Application

### 1. Pre-Launch Go / No-Go Decision Console
* Live evaluation of the 4 critical subsystems:
  * **MOSDAC Weather:** Surface winds $< 15\text{ m/s}$, upper-air shear $< 25\text{ m/s}$, cloud top temp $> -25^\circ\text{C}$, zero lightning.
  * **Propulsion & Cryo Tanks:** Liquid Oxygen ($-183.1^\circ\text{C}$), Liquid Hydrogen ($-253^\circ\text{C}$), ullage pressure (2.0–2.6 bar).
  * **Deep Space Network:** IDSN Byalalu 32m lock, telemetry SNR $> 14\text{ dB}$, VEDAS geomagnetic $\text{Kp} < 5.0$.
  * **Orbital Safety:** Bhoonidhi debris clearance $> 25\text{ km}$, collision probability $P_c < 10^{-6}$.
* **Interactive Anomaly Sandbox for Judges:** Click buttons like *"Inject High Wind Shear"*, *"Inject Cryo Ullage Drop"*, or *"Spawn Orbital Debris Hazard"* to watch the system trip into **HOLD/NO-GO** in real time with an automated telemetry violation breakdown.

### 2. Ascent & Flight Dynamics Simulator
* Automated launch countdown sequence ($T-10\text{s} \to T-0 \to$ Lift-off).
* Real-time 2D canvas trajectory animation showing vehicle gravity turn over the Bay of Bengal, exhaust plume, Max-Q aerodynamic condensation cloud, stage separations, and payload fairing jettison ($> 115\text{ km}$).
* Live telemetry dials: Speed (km/h & Mach), G-force, Dynamic Pressure $Q$, Fuel Depletion, and Skin Temperature.
* Dynamic Chart.js telemetry graphs (Velocity vs. Time, Altitude vs. Time).

### 3. Orbital Trajectory & Ground Track Map
* Full-screen interactive Leaflet.js dark geospatial map.
* Real-time Sun-Synchronous Orbit (SSO) ground track with animated satellite position marker and sensor swath coverage circle over India.
* Ground tracking station markers: SDSC SHAR, ISTRAC Bengaluru, Port Blair, and IDSN Byalalu.
* Satellite bus telemetry: 2,400W solar array power, daylight/eclipse transitions, battery SOC %, and attitude control.

### 4. On-Orbit Satellite Work (Bhuvan • MOSDAC • Bhoonidhi • VEDAS)
* **Bhoonidhi Lab:** Interactive multi-spectral band sliders (NIR, Red, Green) with real-time computation of **NDVI** (crop stress) and **NDWI** (flood bodies) with quick presets.
* **MOSDAC Radar:** Live tracking of Bay of Bengal cyclonic storms, central barometric pressure, SST thermal anomalies, and rainfall rate.
* **Bhuvan GIS Disaster:** District-level flood risk mapping (41,200 ha inundated, safe evacuation corridors), with one-click emergency vector dispatch.
* **VEDAS Climate Analytics:** Drought Vulnerability Index (DVI) anomaly graphs, solar insolation atlas (5.82 kWh/m²/day), and air quality (AOD).

### 5. Mars Mission: Payloads Suite (MENCA • MCC • MSM • TIS) & Candidate Spot Exploration
* **Astrodynamics Cruise & Orbit Insertion:** Exact 297-day Lambert heliocentric transfer (Dec 1, 2013 to Sept 24, 2014), light travel delay ($> 14\text{ min}$), solar conjunction blackout alerts, and MOI retrograde burn ($1,098.7\text{ m/s}$).
* **MENCA (Mass Spectrometer):** Quadrupole neutral species spectrum ($CO_2, Ar\text{-}40, N_2/CO, O, H_2O$) and local exospheric pressure falloff.
* **MCC (Mars Colour Camera):** Reconnaissance zoom ($420\text{ km}$ periapsis at $22\text{ m/px}$ to $77,000\text{ km}$ apoapsis), atmospheric dust optical depth ($\tau$) slider with dust storm warnings, and simulated optical surface viewports.
* **MSM (Methane Sensor for Mars):** Differential absorption in $3.3\,\mu\text{m}$ band, columnar methane abundance in ppb, and active plume alert ($> 10\text{ ppb}$) with serpentinization vs biogenic classifier.
* **TIS (Thermal Infrared Spectrometer):** Day/night diurnal temperatures, Apparent Thermal Inertia ($\text{ATI}$), regolith bearing trafficability classification, and mineralogical decomposition (smectite clays, carbonates, sulfates, olivine).
* **Candidate Spots & Rover Route Decision Engine:** Multi-Criteria Decision Analysis (MCDA) evaluating 6 high-priority exploration targets: **Jezero Crater**, **Gale Crater**, **Oxia Planum**, **Nili Fossae**, **Valles Marineris**, and **Elysium Planitia**. Computes Exploration Viability Index ($EVI$) and lower-risk rover traverse routes with waypoint coordinates, distances, slope limits, and solar energy generation.

### 6. Feedback Loop 6: Mars Target Rover Position Map & Operational Risk Summary
* **Interactive Mars Surface Maps:** Dual-mode visualization featuring a high-definition tactical elevation topography radar HUD (with elevation isolines from -2,800m to -1,800m, landing ellipse, safe traverse route waypoints, and hazard polygons) and an interactive geospatial Leaflet map.
* **Target Rover Position Telemetry:** Real-time Martian coordinates (Latitude, Longitude, MOLA datum elevation, local surface gradient, azimuth heading, and distance to goal waypoint) synchronized across candidate landing sites. Includes manual coordinate fine-tuning and click-to-reposition capabilities.
* **Closed-Loop Feedback Controller:** 10 Hz closed-loop guidance architecture coupling Terrain-Relative Navigation (TRN) and visual odometry. Real-time error comparator tracks cross-track error ($\epsilon_{\text{cross}}$), along-track error ($\epsilon_{\text{along}}$), and heading drift, with one-click injection of navigation drift (+2.5m obstacle perturbation) and automated closed-loop PID re-centering convergence.
* **Multi-Parametric Risk Summary:** Real-time operational risk dashboard evaluating 6 core domains: Terrain Slope & Rollover risk, Boulder Strike risk, Wheel Slip & Regolith Sinkage risk, Dust Storm Obscuration risk, Diurnal Thermal Stress risk, and Communication Occultation risk. Features an interactive composite mission risk meter and hazard injection sandbox.

### 7. Rover Surface Science Timeline (Sol 0 to Sol 120)
* **Chronological Surface Exploration:** Sol-by-sol time-evolution scrubber detailing touchdown (Sol 0), Chandrayaan-3 Pragyan-heritage APXS/LIBS soil geochemistry (Sol 10), Neretva Vallis delta traverse (Sol 25), subsurface water ice horizon discovery at 1.2m depth (Sol 42), dust storm survival (Sol 60), and extended astrobiology survey (Sol 90-120).
* **Python Streamlit & Plotly Integration:** One-click generation and download of complete `marsbound_streamlit_rover_dashboard.py` source code.

### 8. Automated Official Mission Report
* Formatted aerospace verification summary covering all flight parameters, LCC safety pass/fail checks, downlinked science data, selected Martian exploration landing site, and rover traverse route plan.
* One-click download of the official `.txt` mission dossier.

---

## 🛠️ Quickstart & Local Setup

### Option 1: Direct Browser Launch (Zero Dependencies)
Simply double-click or open `index.html` in any modern web browser (Chrome, Edge, Firefox, Safari). All styling and visualization libraries are loaded dynamically via lightweight CDN.

### Option 2: Local Python Server
```bash
# Clone the repository
git clone https://github.com/Keshav4916/MARSBOUND.git
cd MARSBOUND

# Start local server
python -m http.server 8080
```
Open your browser at `http://localhost:8080`.

### Option 3: Run the Deterministic Python Aerospace Engine
```bash
python launch_physics_engine.py
```
This runs the standalone Python test harness, evaluating nominal vs. anomalous LCC criteria, running numerical integration steps for flight dynamics, and computing multi-spectral reflectance indices.

---

## 🌐 Live Deployed Project Link (GitHub Pages)

The project is deployed and accessible globally at:
> 🔗 **Live Deployed Web Application:** [https://keshav4916.github.io/MARSBOUND/](https://keshav4916.github.io/MARSBOUND/)

### How GitHub Pages is Configured:
1. Repository: [https://github.com/Keshav4916/MARSBOUND](https://github.com/Keshav4916/MARSBOUND)
2. In **Settings** $\to$ **Pages**:
   * **Source**: `Deploy from a branch`
   * **Branch**: `main` / `/ (root)`
3. Live production link: **`https://keshav4916.github.io/MARSBOUND/`**

---

## 👥 Hackathon Submission Checklist

- [x] **01 | GitHub Repository:** [https://github.com/Keshav4916/MARSBOUND](https://github.com/Keshav4916/MARSBOUND)
- [x] **02 | Project Presentation PPT:** Full slide-by-slide structure documented in `presentation_structure.md`.
- [x] **03 | Demo Video Script:** Crisp recorded demo script provided in `demo_video_script.md`.
- [x] **04 | Deployed Project Link:** [https://keshav4916.github.io/MARSBOUND/](https://keshav4916.github.io/MARSBOUND/)

---

*Developed for ASTRA 2026 — ANTERIX Club, VIT Bhopal University.*

