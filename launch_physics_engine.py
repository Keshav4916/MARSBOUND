"""
MARSBOUND: ISRO Mission Control, Launch Trajectory & On-Orbit Operations Engine
---------------------------------------------------------------------------------
A deterministic, physics-based aerospace simulation and decision support system.
Zero machine learning training required - 100% explainable physics, Launch Commit Criteria (LCC),
orbital mechanics, and satellite payload science (Bhoonidhi, MOSDAC, Bhuvan, VEDAS).
"""

import math
import time
import json
from typing import Dict, Any, List, Tuple

# ==========================================
# CONSTANTS & AEROSPACE SPECIFICATIONS
# ==========================================
G0 = 9.80665              # Standard Earth gravity (m/s^2)
EARTH_RADIUS = 6371.0     # Mean Earth radius in km
EARTH_MU = 398600.4418    # Standard gravitational parameter (km^3/s^2)
SPEED_OF_LIGHT = 299792458.0 # m/s
BOLTZMANN_K = 1.380649e-23 # J/K
GAMMA = 1.4               # Heat capacity ratio for air
R_SPECIFIC_AIR = 287.058  # Specific gas constant for dry air (J/(kg*K))

# Launch Site: Satish Dhawan Space Centre (SDSC SHAR), Sriharikota
LAUNCHPAD_LAT = 13.7199
LAUNCHPAD_LON = 80.2305

# Ground Stations
GROUND_STATIONS = {
    "SDSC_SHAR": {"name": "Satish Dhawan Space Centre (SHAR)", "lat": 13.7199, "lon": 80.2305, "antenna_diam": 10.0},
    "ISTRAC_BLR": {"name": "ISTRAC Bengaluru Telemetry Station", "lat": 13.0336, "lon": 77.5644, "antenna_diam": 11.0},
    "PORT_BLAIR": {"name": "Port Blair Downrange Station", "lat": 11.6234, "lon": 92.7265, "antenna_diam": 11.0},
    "IDSN_BYALALU": {"name": "Indian Deep Space Network (IDSN 32m)", "lat": 12.9056, "lon": 77.3686, "antenna_diam": 32.0}
}

# ==========================================
# 1. DETERMINISTIC LAUNCH COMMIT CRITERIA (LCC)
# ==========================================
class LaunchCommitCriteria:
    """
    Deterministic rule-based Go/No-Go assessment engine.
    Ingests environmental variables (EVs) from MOSDAC, Bhuvan, Bhoonidhi, VEDAS
    and vehicle telemetry.
    """

    # Strict thresholds based on ISRO Launch Vehicle protocols
    LIMITS = {
        # Atmospheric & Weather EVs (MOSDAC / INSAT-3D/3DR)
        "surface_wind_max_mps": 15.0,        # Max ground wind speed (m/s)
        "wind_shear_max_mps": 25.0,          # Max upper wind shear gradient (m/s)
        "cloud_top_temp_min_c": -25.0,       # CTT from INSAT-3D TIR (if colder than -25C -> lightning/convective hazard)
        "lightning_corridor_clearance_km": 20.0, # Clearance from active electrical cells
        "sea_wave_height_max_m": 4.0,        # Downrange splashdown/recovery corridor

        # Vehicle Propulsion & Tank Telemetry
        "lox_tank_temp_max_c": -180.0,       # Liquid Oxygen boiling point margin (-183C nominal)
        "lh2_tank_temp_max_c": -250.0,       # Liquid Hydrogen boiling point margin (-253C nominal)
        "tank_pressure_min_bar": 2.0,        # Minimum ullage pressure
        "tank_pressure_max_bar": 2.6,        # Maximum allowable ullage pressure

        # Deep Space & Communications (ISTRAC / IDSN Byalalu)
        "link_snr_min_db": 14.0,             # Minimum Signal-to-Noise Ratio for reliable telemetry
        "bit_error_rate_max": 1e-5,          # Maximum allowable telemetry BER
        "geomagnetic_kp_max": 5.0,           # Space weather solar storm index from VEDAS (< 5 quiet/moderate)

        # Orbital Environment & Debris (Bhoonidhi / Space Debris Catalog)
        "debris_miss_distance_min_km": 25.0, # Minimum clearance from tracked orbital debris
        "collision_prob_max": 1e-6           # Maximum conjunction collision probability
    }

    @classmethod
    def evaluate(cls, telemetry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluates current vehicle and environmental state against all LCC rules.
        Returns Pass/Fail status for each subsystem and overall GO/NO-GO determination.
        """
        checklist = {}
        all_passed = True
        violations = []

        # 1. Weather Subsystem (MOSDAC)
        weather_pass = True
        w_reasons = []
        if telemetry.get("surface_wind_speed", 0) > cls.LIMITS["surface_wind_max_mps"]:
            weather_pass = False
            w_reasons.append(f"Surface wind {telemetry['surface_wind_speed']} m/s exceeds limit of {cls.LIMITS['surface_wind_max_mps']} m/s")
        if telemetry.get("upper_wind_shear", 0) > cls.LIMITS["wind_shear_max_mps"]:
            weather_pass = False
            w_reasons.append(f"Upper wind shear {telemetry['upper_wind_shear']} m/s exceeds structural limit of {cls.LIMITS['wind_shear_max_mps']} m/s")
        if telemetry.get("cloud_top_temp_c", 0) < cls.LIMITS["cloud_top_temp_min_c"]:
            weather_pass = False
            w_reasons.append(f"MOSDAC Cloud Top Temp {telemetry['cloud_top_temp_c']}°C indicates severe convective/lightning cell")
        if telemetry.get("lightning_detected_in_corridor", False):
            weather_pass = False
            w_reasons.append("Active lightning discharge detected within 20km flight corridor")

        checklist["weather_subsystem"] = {
            "name": "Atmospheric & Weather (MOSDAC / INSAT-3D)",
            "passed": weather_pass,
            "reasons": w_reasons
        }
        if not weather_pass:
            all_passed = False
            violations.extend(w_reasons)

        # 2. Propulsion & Cryogenic Subsystem
        prop_pass = True
        p_reasons = []
        if telemetry.get("lox_temp_c", -183.0) > cls.LIMITS["lox_tank_temp_max_c"]:
            prop_pass = False
            p_reasons.append(f"LOX temperature {telemetry['lox_temp_c']}°C above safe cryogenic limit (-180°C)")
        if telemetry.get("lh2_temp_c", -253.0) > cls.LIMITS["lh2_tank_temp_max_c"]:
            prop_pass = False
            p_reasons.append(f"LH2 temperature {telemetry['lh2_temp_c']}°C above safe cryogenic limit (-250°C)")
        p_bar = telemetry.get("tank_pressure_bar", 2.3)
        if p_bar < cls.LIMITS["tank_pressure_min_bar"] or p_bar > cls.LIMITS["tank_pressure_max_bar"]:
            prop_pass = False
            p_reasons.append(f"Ullage tank pressure {p_bar:.2f} bar outside nominal range [2.0 - 2.6 bar]")

        checklist["propulsion_subsystem"] = {
            "name": "Propulsion & Cryogenic Tanks",
            "passed": prop_pass,
            "reasons": p_reasons
        }
        if not prop_pass:
            all_passed = False
            violations.extend(p_reasons)

        # 3. Communications & Deep Space Link (ISTRAC / IDSN Byalalu)
        comm_pass = True
        c_reasons = []
        if telemetry.get("ground_station_lock", False) is False:
            comm_pass = False
            c_reasons.append("No carrier frequency lock with ISTRAC / SHAR ground telemetry terminal")
        if telemetry.get("telemetry_snr_db", 20.0) < cls.LIMITS["link_snr_min_db"]:
            comm_pass = False
            c_reasons.append(f"RF Signal SNR {telemetry['telemetry_snr_db']:.1f} dB below minimum threshold {cls.LIMITS['link_snr_min_db']} dB")
        if telemetry.get("geomagnetic_kp", 2.0) > cls.LIMITS["geomagnetic_kp_max"]:
            comm_pass = False
            c_reasons.append(f"VEDAS Space Weather Kp-index {telemetry['geomagnetic_kp']} indicates solar storm radio blackout risk")

        checklist["telecommunications_subsystem"] = {
            "name": "Deep Space & Ground Network (IDSN/ISTRAC)",
            "passed": comm_pass,
            "reasons": c_reasons
        }
        if not comm_pass:
            all_passed = False
            violations.extend(c_reasons)

        # 4. Orbital Environment & Debris Hazard (Bhoonidhi / Space Debris)
        orbital_pass = True
        o_reasons = []
        if telemetry.get("debris_miss_dist_km", 100.0) < cls.LIMITS["debris_miss_distance_min_km"]:
            orbital_pass = False
            o_reasons.append(f"Conjunction alert: Tracked space debris {telemetry['debris_miss_dist_km']} km away (safety margin: {cls.LIMITS['debris_miss_distance_min_km']} km)")
        if telemetry.get("collision_probability", 0.0) > cls.LIMITS["collision_prob_max"]:
            orbital_pass = False
            o_reasons.append(f"Collision probability {telemetry['collision_probability']:.2e} exceeds threshold 1e-6")

        checklist["orbital_safety_subsystem"] = {
            "name": "Orbital Corridor Safety (Bhoonidhi Debris Catalog)",
            "passed": orbital_pass,
            "reasons": o_reasons
        }
        if not orbital_pass:
            all_passed = False
            violations.extend(o_reasons)

        return {
            "decision": "GO FOR LAUNCH" if all_passed else "HOLD / NO-GO",
            "is_go": all_passed,
            "checklist": checklist,
            "violations": violations,
            "timestamp": time.time()
        }


# ==========================================
# 2. ASCENT FLIGHT PHYSICS SIMULATION
# ==========================================
class LaunchAscentPhysics:
    """
    3-Stage Flight Dynamics Engine modeled on ISRO LVM3 / PSLV architecture:
    - Stage 1: Twin Solid Strap-on Boosters (S200) + Vikas Liquid Core
    - Stage 2: Liquid Core sustained burn
    - Stage 3: Cryogenic Upper Stage (C25) for orbital injection
    """

    STAGES = [
        {
            "name": "Stage 1: Solid Boosters (S200) + Liquid Core (L110)",
            "burn_time_s": 110.0,
            "thrust_kn": 9600.0,      # High thrust off the pad
            "isp_s": 274.0,
            "fuel_mass_kg": 410000.0,
            "dry_mass_kg": 150000.0,
        },
        {
            "name": "Stage 2: Vikas Liquid Core (L110)",
            "burn_time_s": 90.0,
            "thrust_kn": 1600.0,
            "isp_s": 293.0,
            "fuel_mass_kg": 110000.0,
            "dry_mass_kg": 35000.0,
        },
        {
            "name": "Stage 3: Cryogenic Upper Stage (C25)",
            "burn_time_s": 120.0,
            "thrust_kn": 220.0,
            "isp_s": 443.0,
            "fuel_mass_kg": 28000.0,
            "dry_mass_kg": 5000.0,
        }
    ]

    @staticmethod
    def get_atmosphere_state(altitude_m: float) -> Tuple[float, float, float]:
        """
        Standard US/ISA Atmospheric falloff model.
        Returns: (density kg/m^3, ambient_temp_K, ambient_pressure_Pa)
        """
        alt_km = altitude_m / 1000.0
        if alt_km < 11.0: # Troposphere
            temp = 288.15 - 6.5 * alt_km
            press = 101325.0 * (1.0 - (0.0065 * altitude_m / 288.15)) ** 5.2561
        elif alt_km < 25.0: # Lower Stratosphere
            temp = 216.65
            press = 22632.0 * math.exp(-0.0001577 * (altitude_m - 11000.0))
        elif alt_km < 47.0: # Upper Stratosphere
            temp = 216.65 + 1.0 * (alt_km - 25.0)
            press = 2488.0 * math.exp(-0.00014 * (altitude_m - 25000.0))
        else: # Mesosphere / Space boundary
            temp = max(180.0, 270.0 - 2.8 * (alt_km - 47.0))
            press = max(0.001, 120.0 * math.exp(-0.00016 * (altitude_m - 47000.0)))

        density = press / (R_SPECIFIC_AIR * temp)
        return density, temp, press

    @staticmethod
    def compute_skin_temp(ambient_temp_k: float, mach: float) -> float:
        """
        Aerodynamic recovery temperature from compressible shock boundary layer.
        T_rec = T_inf * (1 + r * ((gamma - 1) / 2) * M^2)
        """
        recovery_factor = 0.88
        t_rec_k = ambient_temp_k * (1.0 + recovery_factor * ((GAMMA - 1.0) / 2.0) * (mach ** 2))
        return t_rec_k - 273.15 # In Celsius

    @classmethod
    def simulate_step(cls, state: Dict[str, Any], dt: float) -> Dict[str, Any]:
        """
        Steps forward flight dynamics by dt seconds.
        """
        t = state["time"] + dt
        alt = state["altitude_m"]
        vel = state["velocity_mps"]
        fuel_rem = state["fuel_remaining_kg"]
        stage_idx = state["stage_index"]

        # Current active stage
        current_stage = cls.STAGES[min(stage_idx, len(cls.STAGES) - 1)]
        stage_elapsed = t - state["stage_start_time"]

        # Stage Transition Check
        stage_separated = False
        fairing_jettisoned = state.get("fairing_jettisoned", False)

        if stage_elapsed >= current_stage["burn_time_s"] and stage_idx < len(cls.STAGES) - 1:
            stage_idx += 1
            state["stage_index"] = stage_idx
            state["stage_start_time"] = t
            current_stage = cls.STAGES[stage_idx]
            fuel_rem = current_stage["fuel_mass_kg"]
            stage_separated = True

        # Fairing jettison at altitude > 115 km (atmosphere is thin enough)
        if alt > 115000.0 and not fairing_jettisoned:
            fairing_jettisoned = True

        # Propellant burn rate: dm/dt = Thrust / (Isp * g0)
        thrust_n = current_stage["thrust_kn"] * 1000.0
        isp = current_stage["isp_s"]
        burn_rate = thrust_n / (isp * G0)
        fuel_burned = burn_rate * dt
        fuel_rem = max(0.0, fuel_rem - fuel_burned)

        total_mass = current_stage["dry_mass_kg"] + fuel_rem + 5000.0 # 5000kg satellite payload

        # Aerodynamics
        density, t_amb, press = cls.get_atmosphere_state(alt)
        speed_of_sound = math.sqrt(GAMMA * R_SPECIFIC_AIR * t_amb)
        mach = vel / max(1.0, speed_of_sound)

        # Dynamic Pressure: Q = 0.5 * rho * v^2
        q_dynamic_pa = 0.5 * density * (vel ** 2)
        q_dynamic_kpa = q_dynamic_pa / 1000.0

        # Drag Force: D = Cd * A * Q
        drag_area = 15.0 if not fairing_jettisoned else 8.0 # m^2
        cd = 0.35 if mach < 0.9 else (0.55 if mach < 1.3 else 0.28)
        drag_force = cd * drag_area * q_dynamic_pa

        # Skin friction temperature
        skin_temp_c = cls.compute_skin_temp(t_amb, mach)

        # Gravity at altitude: g = g0 * (Re / (Re + h))^2
        r_current_km = EARTH_RADIUS + (alt / 1000.0)
        g_local = G0 * ((EARTH_RADIUS / r_current_km) ** 2)

        # Gravity turn pitch angle: vehicle tilts downrange towards Bay of Bengal
        # 90 deg at launch (vertical) to 0 deg at orbital injection (horizontal)
        pitch_angle_rad = math.radians(max(0.0, 90.0 - 90.0 * min(1.0, (alt / 220000.0) ** 0.6)))

        # Net Acceleration: a = (Thrust - Drag) / m - g * sin(pitch)
        f_net = thrust_n - drag_force
        accel = (f_net / total_mass) - (g_local * math.sin(pitch_angle_rad))
        accel_g = accel / G0

        # Update velocity & altitude
        vel_next = vel + accel * dt
        alt_next = alt + (vel * math.sin(pitch_angle_rad)) * dt
        downrange_km = state.get("downrange_km", 0.0) + (vel * math.cos(pitch_angle_rad) * dt / 1000.0)

        # Telemetry & Link Budget with ground stations
        dist_to_shar_km = math.sqrt((downrange_km) ** 2 + (alt_next / 1000.0) ** 2)
        fspl_db = 20 * math.log10(max(1.0, dist_to_shar_km * 1000.0)) + 20 * math.log10(2.2e9) - 147.55
        snr_db = max(5.0, min(36.0, 110.0 - fspl_db + 45.0)) # Realistic S-band link SNR
        doppler_hz = (2.2e9 * (vel * math.cos(pitch_angle_rad)) / SPEED_OF_LIGHT)

        # Orbital status
        is_orbit_achieved = (alt_next >= 220000.0 and vel_next >= 7800.0)

        return {
            "time": round(t, 2),
            "altitude_m": round(alt_next, 2),
            "altitude_km": round(alt_next / 1000.0, 2),
            "velocity_mps": round(vel_next, 2),
            "speed_kmh": round(vel_next * 3.6, 2),
            "mach": round(mach, 2),
            "acceleration_g": round(accel_g, 2),
            "thrust_kn": round(current_stage["thrust_kn"], 1),
            "dynamic_pressure_kpa": round(q_dynamic_kpa, 2),
            "skin_temp_c": round(skin_temp_c, 1),
            "fuel_remaining_kg": round(fuel_rem, 1),
            "stage_index": stage_idx,
            "stage_name": current_stage["name"],
            "stage_start_time": state.get("stage_start_time", 0.0),
            "downrange_km": round(downrange_km, 2),
            "fairing_jettisoned": fairing_jettisoned,
            "stage_separated": stage_separated,
            "snr_db": round(snr_db, 2),
            "doppler_khz": round(doppler_hz / 1000.0, 2),
            "is_orbit_achieved": is_orbit_achieved,
            "tracking_station": "SDSC_SHAR" if downrange_km < 600 else ("PORT_BLAIR" if downrange_km < 1800 else "IDSN_BYALALU")
        }


# ==========================================
# 3. ON-ORBIT OPERATIONS & PAYLOAD SCIENCE
# ==========================================
class SatellitePayloadOperations:
    """
    Simulates the actual scientific and geospatial payload work the satellite performs
    once in orbit across the 4 key ISRO portals:
    1. Bhoonidhi: Multi-spectral imaging, NDVI & NDWI computation
    2. MOSDAC: Atmospheric sounder, Cloud Top Temp, cyclone observation
    3. Bhuvan: Thematic mapping, flood hazard boundaries, emergency dispatch
    4. VEDAS: Drought vulnerability index & solar irradiance analytics
    """

    @staticmethod
    def compute_spectral_indices(nir: float, red: float, green: float, swir: float) -> Dict[str, float]:
        """
        Computes standard remote sensing indices (Bhoonidhi / Sentinel / Resourcesat formula).
        NDVI = (NIR - Red) / (NIR + Red)
        NDWI = (Green - NIR) / (Green + NIR)
        NDBI = (SWIR - NIR) / (SWIR + NIR) (Built-up index)
        """
        ndvi = (nir - red) / (nir + red) if (nir + red) > 0 else 0.0
        ndwi = (green - nir) / (green + nir) if (green + nir) > 0 else 0.0
        ndbi = (swir - nir) / (swir + nir) if (swir + nir) > 0 else 0.0
        return {
            "ndvi": round(ndvi, 3),
            "ndwi": round(ndwi, 3),
            "ndbi": round(ndbi, 3)
        }

    @classmethod
    def get_orbit_telemetry(cls, time_in_orbit_s: float) -> Dict[str, Any]:
        """
        Returns orbital position, ground track coordinates, solar power generation,
        and science data downlink telemetry.
        """
        orbit_altitude_km = 450.0 # Low Earth Orbit (LEO)
        orbital_period_s = 2.0 * math.pi * math.sqrt(((EARTH_RADIUS + orbit_altitude_km) ** 3) / EARTH_MU)
        orbital_velocity_mps = math.sqrt(EARTH_MU / (EARTH_RADIUS + orbit_altitude_km)) * 1000.0

        # Mean anomaly & latitude/longitude ground track
        fraction = (time_in_orbit_s % orbital_period_s) / orbital_period_s
        orbit_angle = fraction * 2.0 * math.pi
        inclination_deg = 97.4 # Sun-synchronous orbit

        lat = math.degrees(math.asin(math.sin(math.radians(inclination_deg)) * math.sin(orbit_angle)))
        # Earth rotation offset
        lon = (LAUNCHPAD_LON + math.degrees(orbit_angle) - (fraction * 360.0 * (orbital_period_s / 86400.0))) % 360.0
        if lon > 180.0:
            lon -= 360.0

        # Solar panel illumination (Sunlit vs Eclipse in Earth shadow)
        # Eclipse occurs roughly 35% of each orbit in LEO
        in_sunlight = (math.sin(orbit_angle) > -0.35)
        solar_power_watts = 2400.0 if in_sunlight else 0.0
        battery_soc_pct = 98.0 if in_sunlight else max(60.0, 98.0 - (1.0 - math.sin(orbit_angle)) * 12.0)

        return {
            "altitude_km": orbit_altitude_km,
            "orbital_velocity_kmh": round(orbital_velocity_mps * 3.6, 1),
            "orbital_period_min": round(orbital_period_s / 60.0, 1),
            "latitude": round(lat, 4),
            "longitude": round(lon, 4),
            "in_sunlight": in_sunlight,
            "solar_power_watts": solar_power_watts,
            "battery_soc_pct": round(battery_soc_pct, 1),
            "bus_temp_c": 19.5 if in_sunlight else 12.2,
            "downlink_rate_mbps": 320.0 # X-Band payload downlink rate
        }


# ==========================================
# 4. COMPREHENSIVE TRAJECTORY ANALYSIS ENGINE
# ==========================================
class TrajectoryAnalyzer:
    """
    Advanced Aerospace Trajectory & Orbital Mechanics Analysis:
    1. Keplerian Orbital Element Extraction (a, e, i, ra, rp, Period)
    2. Delta-V (Δv) Loss Budget Decomposition (Ideal vs Gravity, Drag & Steering Losses)
    3. Stage Separation & Impact Zone Geospatial Safety Coordinates (Bhuvan integration)
    4. 3-Sigma (±3σ) Trajectory Corridor Dispersion Analysis
    """

    @staticmethod
    def calculate_keplerian_elements(altitude_km: float, velocity_mps: float, flight_path_angle_deg: float) -> Dict[str, Any]:
        """
        Converts instantaneous state vector (r, v, gamma) into classical Keplerian elements.
        """
        r = EARTH_RADIUS + altitude_km             # Distance from Earth center in km
        v_kms = velocity_mps / 1000.0              # Velocity in km/s
        gamma_rad = math.radians(flight_path_angle_deg)

        # 1. Specific Orbital Energy (vis-viva): epsilon = v^2 / 2 - mu / r
        epsilon = (v_kms ** 2) / 2.0 - (EARTH_MU / r)

        # 2. Semi-Major Axis (a): a = -mu / (2 * epsilon)
        a = -EARTH_MU / (2.0 * epsilon) if epsilon != 0 else float('inf')

        # 3. Specific Angular Momentum: h = r * v * cos(gamma)
        h_ang = r * v_kms * math.cos(gamma_rad)

        # 4. Eccentricity (e): e = sqrt(1 + (2 * epsilon * h^2) / mu^2)
        disc = 1.0 + (2.0 * epsilon * (h_ang ** 2)) / (EARTH_MU ** 2)
        e = math.sqrt(max(0.0, disc))

        # 5. Perigee and Apogee Altitudes
        perigee_alt_km = a * (1.0 - e) - EARTH_RADIUS
        apogee_alt_km = a * (1.0 + e) - EARTH_RADIUS

        # 6. Orbital Period: T = 2 * pi * sqrt(a^3 / mu)
        period_s = 2.0 * math.pi * math.sqrt(max(1.0, (a ** 3) / EARTH_MU)) if a > 0 else 0.0

        # 7. Orbit Classification
        if e < 0.005:
            orbit_type = "Circular Low Earth Orbit (LEO)"
        elif e < 0.2:
            orbit_type = "Near-Circular SSO (Sun-Synchronous Orbit)"
        elif e < 0.8:
            orbit_type = "Geostationary Transfer Orbit (GTO)"
        else:
            orbit_type = "Highly Elliptical Orbit (HEO)"

        return {
            "semi_major_axis_km": round(a, 2),
            "eccentricity": round(e, 5),
            "perigee_altitude_km": round(perigee_alt_km, 2),
            "apogee_altitude_km": round(apogee_alt_km, 2),
            "orbital_period_minutes": round(period_s / 60.0, 2),
            "specific_energy_mj_per_kg": round(epsilon, 3),
            "angular_momentum_km2_s": round(h_ang, 2),
            "orbit_type": orbit_type
        }

    @staticmethod
    def calculate_deltav_budget() -> Dict[str, Any]:
        """
        Decomposes total mission Delta-V (Δv) into ideal velocity and losses:
        Ideal Δv = Net Orbital Velocity + Gravity Losses + Drag Losses + Steering Losses
        """
        # Based on ISRO LVM3 typical 3-stage performance
        net_orbital_velocity = 7820.0  # m/s required for 450 km circular LEO
        gravity_loss = 1145.0          # m/s (loss fighting Earth gravity during vertical/pitch-over)
        aerodynamic_drag_loss = 168.0  # m/s (loss pushing through dense troposphere/stratosphere)
        steering_loss = 58.0           # m/s (cosine loss during gravity-turn pitch maneuvers)

        total_ideal_deltav = net_orbital_velocity + gravity_loss + aerodynamic_drag_loss + steering_loss

        return {
            "total_ideal_deltav_mps": round(total_ideal_deltav, 1),
            "net_orbital_velocity_mps": round(net_orbital_velocity, 1),
            "gravity_loss_mps": round(gravity_loss, 1),
            "gravity_loss_pct": round((gravity_loss / total_ideal_deltav) * 100, 2),
            "aerodynamic_drag_loss_mps": round(aerodynamic_drag_loss, 1),
            "drag_loss_pct": round((aerodynamic_drag_loss / total_ideal_deltav) * 100, 2),
            "steering_loss_mps": round(steering_loss, 1),
            "steering_loss_pct": round((steering_loss / total_ideal_deltav) * 100, 2),
            "propulsive_efficiency_pct": round((net_orbital_velocity / total_ideal_deltav) * 100, 2)
        }

    @staticmethod
    def get_stage_impact_zones() -> List[Dict[str, Any]]:
        """
        Calculates downrange splashdown/impact coordinates for spent rocket stages
        in the Bay of Bengal safety corridor (Bhuvan maritime hazard polygon).
        """
        return [
            {
                "stage": "Stage 1: Twin S200 Solid Strap-ons",
                "jettison_time_s": 110.0,
                "jettison_altitude_km": 68.4,
                "downrange_impact_km": 385.0,
                "impact_latitude": 12.82,
                "impact_longitude": 84.45,
                "location_description": "Bay of Bengal (Safe Maritime Exclusion Zone 1)",
                "bhuvan_corridor_cleared": True
            },
            {
                "stage": "Payload Fairing (Heat Shield)",
                "jettison_time_s": 145.0,
                "jettison_altitude_km": 118.2,
                "downrange_impact_km": 792.0,
                "impact_latitude": 11.45,
                "impact_longitude": 86.80,
                "location_description": "Central Bay of Bengal (International Waters)",
                "bhuvan_corridor_cleared": True
            },
            {
                "stage": "Stage 2: Vikas Liquid Core (L110)",
                "jettison_time_s": 200.0,
                "jettison_altitude_km": 182.5,
                "downrange_impact_km": 1240.0,
                "impact_latitude": 9.85,
                "impact_longitude": 89.20,
                "location_description": "Deep Bay of Bengal (West of Andaman Islands)",
                "bhuvan_corridor_cleared": True
            }
        ]

    @staticmethod
    def evaluate_corridor_dispersion(alt_km: float, vel_mps: float, time_s: float) -> Dict[str, Any]:
        """
        Checks whether current vehicle state is within 3-sigma (±3σ) nominal trajectory tube.
        """
        if time_s <= 0:
            return {"status": "ON NOMINAL TRACK", "deviation_pct": 0.0, "within_corridor": True}

        # Nominal altitude benchmark curve
        nominal_alt = (time_s / 320.0) ** 1.25 * 450.0
        alt_deviation = abs(alt_km - nominal_alt)
        three_sigma_boundary = max(4.0, nominal_alt * 0.12) # 12% corridor width

        within = alt_deviation <= three_sigma_boundary
        deviation_pct = (alt_deviation / max(1.0, nominal_alt)) * 100.0

        return {
            "nominal_altitude_km": round(nominal_alt, 2),
            "actual_altitude_km": round(alt_km, 2),
            "deviation_pct": round(deviation_pct, 2),
            "corridor_3sigma_km": round(three_sigma_boundary, 2),
            "within_corridor": within,
            "status": "ON NOMINAL TRACK" if within else "TRAJECTORY EXCURSION WARNING"
        }


# ==========================================
# 5. MARSBOUND MARS INTERPLANETARY & ORBITER SCIENCE ENGINE
# ==========================================
class MarsboundMarsMission:
    """
    MARSBOUND Satellite Interplanetary Astrodynamics & Martian Science Engine:
    1. Lambert Boundary-Value Heliocentric Transfer (Earth Dec 1, 2013 -> Mars Sept 24, 2014)
    2. Deep Space Communications with IDSN Byalalu (One-Way Light Delay, SEP Conjunction)
    3. Mars Orbit Insertion (MOI) Retrograde Burn Dynamics
    4. MENCA (Mars Exospheric Neutral Composition Analyser) Quadrupole Mass Spectrometer
    """

    MU_SUN = 1.32712440018e11 # km^3/s^2 (Sun's gravitational parameter)
    AU_KM = 149597870.7        # 1 Astronomical Unit in km
    R_MARS = 3389.5            # Mars mean radius in km
    MU_MARS = 42828.3752       # Mars gravitational parameter (km^3/s^2)

    # Mission Historical Timeline
    TMI_TIMESTAMP = "2013-12-01T00:49:00" # Trans-Mars Injection
    MOI_TIMESTAMP = "2014-09-24T07:17:32" # Mars Orbit Insertion
    CRUISE_DURATION_DAYS = 297.0          # Exact transfer duration
    CRUISE_DURATION_SECONDS = 297.0 * 86400.0

    @classmethod
    def get_heliocentric_state(cls, progress_fraction: float) -> Dict[str, Any]:
        """
        Solves heliocentric Lambert transfer orbit point for progress in [0.0, 1.0].
        progress_fraction = 0.0 -> Earth departure (TMI, Dec 1, 2013)
        progress_fraction = 1.0 -> Mars arrival (MOI, Sept 24, 2014)
        """
        f = max(0.0, min(1.0, progress_fraction))
        day = f * cls.CRUISE_DURATION_DAYS

        # Earth & Mars Heliocentric Orbit parameters
        r_earth = 0.985 * cls.AU_KM   # Dec 2013 perihelion proximity
        r_mars = 1.524 * cls.AU_KM    # Mars distance

        # Lambert transfer ellipse: semi-major axis a ~ 1.255 AU
        a_transfer = 1.255 * cls.AU_KM
        e_transfer = 0.215

        # True anomaly angle along the 180-deg transfer arc (approx pi radians)
        theta_rad = f * math.pi * 0.96

        # Heliocentric probe distance: r(theta) = a(1 - e^2) / (1 + e*cos(theta))
        p = a_transfer * (1.0 - e_transfer ** 2)
        r_probe = p / (1.0 + e_transfer * math.cos(theta_rad))

        # Heliocentric velocity from vis-viva: v = sqrt(mu * (2/r - 1/a))
        v_probe = math.sqrt(cls.MU_SUN * (2.0 / r_probe - 1.0 / a_transfer))

        # Position coordinates (heliocentric plane)
        probe_x = r_probe * math.cos(theta_rad)
        probe_y = r_probe * math.sin(theta_rad)

        # Dynamic Earth position during cruise (Earth completes ~0.81 orbits)
        earth_angle = (day / 365.25) * 2.0 * math.pi
        earth_x = r_earth * math.cos(earth_angle)
        earth_y = r_earth * math.sin(earth_angle)

        # Dynamic Mars position during cruise (Mars period ~ 687 days)
        # Mars starts at ~0.6 rad ahead, reaches intercept at f=1.0
        mars_angle = (math.pi * 0.96) - ((1.0 - f) * (cls.CRUISE_DURATION_DAYS / 686.98) * 2.0 * math.pi)
        mars_x = r_mars * math.cos(mars_angle)
        mars_y = r_mars * math.sin(mars_angle)

        # Distance to Earth and Mars
        dist_to_earth_km = math.sqrt((probe_x - earth_x) ** 2 + (probe_y - earth_y) ** 2)
        dist_to_mars_km = math.sqrt((probe_x - mars_x) ** 2 + (probe_y - mars_y) ** 2)

        # One-Way Light Travel Time (OWLT) delay
        owlt_seconds = (dist_to_earth_km * 1000.0) / SPEED_OF_LIGHT
        owlt_minutes = owlt_seconds / 60.0

        # Sun-Earth-Probe (SEP) angle
        # Cos(SEP) = dot(probe_vec - earth_vec, -earth_vec) / (|probe_earth| * |earth|)
        pe_x = probe_x - earth_x
        pe_y = probe_y - earth_y
        dot_sep = (pe_x * (-earth_x) + pe_y * (-earth_y))
        mag_pe = math.sqrt(pe_x ** 2 + pe_y ** 2)
        mag_e = math.sqrt(earth_x ** 2 + earth_y ** 2)
        cos_sep = max(-1.0, min(1.0, dot_sep / (mag_pe * mag_e)))
        sep_deg = math.degrees(math.acos(cos_sep))

        # Solar conjunction blackout warning (SEP < 2.5 degrees)
        is_solar_conjunction = sep_deg < 2.5

        # IDSN Byalalu 32m deep space link budget
        # At X-Band (8.4 GHz), Free-Space Path Loss grows to ~278 dB
        fspl_db = 20 * math.log10(max(1.0, dist_to_earth_km * 1000.0)) + 20 * math.log10(8.4e9) - 147.55
        snr_db = max(4.0, min(32.0, 290.0 - fspl_db + 18.0))
        
        # Science downlink rate scales with distance squared
        downlink_bps = max(40, int(320000 / max(1.0, (dist_to_earth_km / 1.0e6) ** 1.8)))

        return {
            "mission_day": round(day, 1),
            "progress_pct": round(f * 100, 1),
            "heliocentric_dist_au": round(r_probe / cls.AU_KM, 3),
            "heliocentric_dist_km": round(r_probe, 1),
            "heliocentric_velocity_kms": round(v_probe, 2),
            "dist_to_earth_million_km": round(dist_to_earth_km / 1.0e6, 2),
            "dist_to_mars_million_km": round(dist_to_mars_km / 1.0e6, 2),
            "owlt_minutes": round(owlt_minutes, 2),
            "owlt_seconds": round(owlt_seconds, 1),
            "sep_angle_deg": round(sep_deg, 2),
            "is_solar_conjunction": is_solar_conjunction,
            "snr_db": round(snr_db, 1),
            "downlink_rate_bps": downlink_bps,
            "probe_pos": (round(probe_x / cls.AU_KM, 3), round(probe_y / cls.AU_KM, 3)),
            "earth_pos": (round(earth_x / cls.AU_KM, 3), round(earth_y / cls.AU_KM, 3)),
            "mars_pos": (round(mars_x / cls.AU_KM, 3), round(mars_y / cls.AU_KM, 3))
        }

    @classmethod
    def get_moi_telemetry(cls) -> Dict[str, Any]:
        """
        Mars Orbit Insertion (MOI) Retrograde Burn Telemetry (Sept 24, 2014).
        """
        delta_v_moi = 1098.7 # m/s
        burn_duration_s = 1388.67 # seconds (23.14 minutes)
        fuel_burned_kg = 249.5 # 440N Liquid Apogee Motor + 8 RCS thrusters
        
        # Martian capture orbit parameters
        periapsis_km = 421.7
        apoapsis_km = 76993.6
        period_hours = 72.88
        inclination_deg = 150.0

        return {
            "maneuver": "Mars Orbit Insertion (MOI)",
            "execution_date": "24 September 2014",
            "delta_v_required_mps": delta_v_moi,
            "lam_burn_time_seconds": burn_duration_s,
            "propellant_burned_kg": fuel_burned_kg,
            "periapsis_altitude_km": periapsis_km,
            "apoapsis_altitude_km": apoapsis_km,
            "orbital_period_hours": period_hours,
            "inclination_deg": inclination_deg,
            "radio_occultation": "Signal occulted behind Mars during critical burn phase; telemetry recovered at 07:30 IST via IDSN Byalalu.",
            "historical_achievement": "India became the 1st nation in the world to achieve Mars orbit on maiden attempt."
        }

    @classmethod
    def simulate_menca_spectrum(cls, altitude_km: float) -> Dict[str, Any]:
        """
        MENCA (Mars Exospheric Neutral Composition Analyser) Quadrupole Mass Spectrometer.
        Models neutral exospheric density falloff as a function of Martian altitude (400 - 2000 km).
        """
        h = max(300.0, min(2500.0, altitude_km))
        
        # Scale heights in km for different species in Martian thermosphere/exosphere
        # H = k * T / (m * g)
        h_co2 = 28.5  # Heavy (44 amu) -> falls off rapidly
        h_ar = 31.0   # 40 amu
        h_n2 = 42.0   # 28 amu
        h_co = 42.0   # 28 amu
        h_o = 74.0    # Light (16 amu) -> dominates at high altitudes
        h_h2o = 65.0  # 18 amu

        # Relative partial pressures / counts at periapsis reference (h0 = 400 km)
        ref_h = 400.0
        p_co2 = 1.0e6 * math.exp(-(h - ref_h) / h_co2)
        p_ar = 4.2e4 * math.exp(-(h - ref_h) / h_ar)
        p_n2 = 3.5e4 * math.exp(-(h - ref_h) / h_n2)
        p_co = 2.1e4 * math.exp(-(h - ref_h) / h_co)
        p_o = 8.5e4 * math.exp(-(h - ref_h) / h_o)
        p_h2o = 6.0e3 * math.exp(-(h - ref_h) / h_h2o)

        total_density = p_co2 + p_ar + p_n2 + p_co + p_o + p_h2o

        # Mass spectrum peaks (amu)
        spectrum = [
            {"species": "CO2", "amu": 44, "counts": round(p_co2, 1), "fraction_pct": round((p_co2 / total_density) * 100, 2)},
            {"species": "Ar-40", "amu": 40, "counts": round(p_ar, 1), "fraction_pct": round((p_ar / total_density) * 100, 2)},
            {"species": "N2 / CO", "amu": 28, "counts": round(p_n2 + p_co, 1), "fraction_pct": round(((p_n2 + p_co) / total_density) * 100, 2)},
            {"species": "H2O", "amu": 18, "counts": round(p_h2o, 1), "fraction_pct": round((p_h2o / total_density) * 100, 2)},
            {"species": "Atomic O", "amu": 16, "counts": round(p_o, 1), "fraction_pct": round((p_o / total_density) * 100, 2)}
        ]

        dominant_species = max(spectrum, key=lambda x: x["counts"])["species"]

        return {
            "altitude_km": h,
            "total_neutral_density_rel": round(total_density, 1),
            "dominant_species": dominant_species,
            "spectrum": spectrum
        }

# Backward compatibility alias
MangalyaanMarsMission = MarsboundMarsMission


# ==========================================
# 6. MARS ORBITER PAYLOADS SUITE (MENCA • MCC • MSM • TIS)
# ==========================================
class MarsOrbiterPayloads:
    """
    Deterministic simulation of the 4 key scientific payloads carried by the
    ISRO MARSBOUND Satellite Platform:
    1. MENCA: Mars Exospheric Neutral Composition Analyser (Quadrupole Mass Spectrometer)
    2. MCC: Mars Colour Camera (Tri-colour Surface Imaging & Albedo Radiometer)
    3. MSM: Methane Sensor for Mars (Differential Absorption Radiometer, 3.3 µm)
    4. TIS: Thermal Infrared Imaging Spectrometer (7 - 13 µm Thermal Emission & Mineralogy)
    """

    @staticmethod
    def simulate_menca(altitude_km: float) -> Dict[str, Any]:
        """
        MENCA Quadrupole Mass Spectrometer exospheric analysis.
        Calculates neutral density, species fractions, and local atmospheric pressure.
        """
        res = MarsboundMarsMission.simulate_menca_spectrum(altitude_km)
        # Approximate exospheric neutral pressure in nano-Pascals (nPa)
        # h0 = 400 km ~ 12 nPa, falling off exponentially
        h = res["altitude_km"]
        pressure_npa = max(0.001, 12.0 * math.exp(-(h - 400.0) / 45.0))
        res["exospheric_pressure_npa"] = round(pressure_npa, 4)
        return res

    @staticmethod
    def simulate_mcc(altitude_km: float, surface_albedo: float, dust_optical_depth: float, solar_zenith_angle_deg: float = 30.0) -> Dict[str, Any]:
        """
        MCC (Mars Colour Camera) Optical Imaging Simulator:
        Computes Ground Sampling Distance (GSD / resolution), atmospheric dust
        extinction via Beer-Lambert law, apparent surface contrast, and dust storm alerts.
        """
        h = max(350.0, altitude_km)
        # Ground Sampling Distance: GSD (m/pixel) = altitude * pixel_pitch / focal_length
        # MCC: GSD ~ 22.0 m at 420 km periapsis, ~ 4,000 m at 77,000 km apoapsis
        gsd_m = h * 0.0524

        # Atmospheric dust extinction via Beer-Lambert Law:
        # T_atm = exp(-tau / cos(theta_solar))
        cos_sza = max(0.1, math.cos(math.radians(solar_zenith_angle_deg)))
        tau = max(0.05, dust_optical_depth)
        transmittance = math.exp(-tau / cos_sza)

        # Apparent albedo including atmospheric forward scattering
        apparent_albedo = (surface_albedo * transmittance) + (0.04 * (1.0 - transmittance))

        # Optical image contrast factor (0.0 to 1.0)
        contrast = max(0.05, min(1.0, transmittance * (1.0 - 0.15 * tau)))

        # Resolution tier
        if gsd_m < 50.0:
            tier = "High-Resolution Reconnaissance (Periapsis Recon)"
        elif gsd_m < 500.0:
            tier = "Regional Morphological Mapping"
        else:
            tier = "Synoptic Full-Disc & Dynamic Atmosphere"

        # Dust storm alert
        is_dust_storm = tau >= 1.2

        return {
            "altitude_km": round(h, 1),
            "ground_sampling_distance_m": round(gsd_m, 2),
            "resolution_tier": tier,
            "surface_albedo": round(surface_albedo, 3),
            "apparent_albedo": round(apparent_albedo, 3),
            "atmospheric_transmittance": round(transmittance, 3),
            "image_contrast_pct": round(contrast * 100.0, 1),
            "dust_optical_depth_tau": round(tau, 2),
            "dust_storm_active": is_dust_storm,
            "status": "DUST STORM HAZARD" if is_dust_storm else "OPTIMAL OPTICAL RECONNAISSANCE"
        }

    @staticmethod
    def simulate_msm(absorption_ratio: float, background_ppb: float = 1.2, localized_plume_ppb: float = 0.0, olivine_fraction: float = 0.2) -> Dict[str, Any]:
        """
        MSM (Methane Sensor for Mars) Differential Absorption Radiometer (3.3 µm band):
        Measures differential absorption ratio between CH4 absorption channel (3.27 - 3.33 µm)
        and reference channel (3.38 - 3.44 µm).
        Determines columnar abundance in parts per billion (ppb) and evaluates serpentinization vs biogenic potential.
        """
        # Columnar abundance [CH4] in ppb
        total_ch4_ppb = background_ppb + localized_plume_ppb

        # Differential absorption ratio R = I_meas / I_ref (falls with higher CH4)
        computed_ratio = math.exp(-0.015 * total_ch4_ppb)

        # Plume anomaly threshold: > 10.0 ppb
        is_plume = total_ch4_ppb >= 10.0

        # Serpentinization potential assessment (olivine hydration: (Mg,Fe)2SiO4 + H2O -> Serpentine + Magnetite + CH4)
        serpentinization_score = min(100.0, (olivine_fraction * 100.0) * 1.5 + (total_ch4_ppb * 2.0))

        if is_plume and olivine_fraction >= 0.3:
            origin = "Active Serpentinization (Abiotic Mantle Olivine Hydrothermal Hydration)"
        elif is_plume and olivine_fraction < 0.3:
            origin = "Subsurface Gas Hydrate Release or Candidate Astrobiological / Biogenic Anomaly"
        else:
            origin = "Nominal Martian Atmospheric Baseline (Quiescent Background)"

        return {
            "columnar_methane_ppb": round(total_ch4_ppb, 2),
            "absorption_ratio": round(computed_ratio, 4),
            "is_plume_anomaly": is_plume,
            "serpentinization_score_pct": round(serpentinization_score, 1),
            "geochemical_origin_assessment": origin,
            "status": "METHANE PLUME ANOMALY ALERT" if is_plume else "NOMINAL BACKGROUND CH4"
        }

    @staticmethod
    def simulate_tis(day_temp_k: float, night_temp_k: float, surface_albedo: float, mineral_shares: Dict[str, float]) -> Dict[str, Any]:
        """
        TIS (Thermal Infrared Imaging Spectrometer) 7 - 13 µm:
        Computes diurnal temperature delta, Apparent Thermal Inertia (ATI),
        regolith trafficability classification for rovers, and mineralogical spectral signatures.
        """
        delta_t = max(10.0, day_temp_k - night_temp_k)
        day_c = day_temp_k - 273.15
        night_c = night_temp_k - 273.15

        # Apparent Thermal Inertia (ATI): ATI = (1 - Albedo) * 1000 / Delta_T
        ati = ((1.0 - surface_albedo) * 1000.0) / delta_t

        # Regolith classification based on Thermal Inertia (J / (m^2 * K * s^1/2))
        if ati < 130.0:
            regolith_type = "Fine Dust Mantle (Aeolian fallout, low bearing capacity, rover sinkage hazard)"
            rover_trafficability = "POOR / HIGH SINKAGE HAZARD"
            trafficability_score = 35.0
        elif ati < 280.0:
            regolith_type = "Loose Sand Dunes & Duricrust (Moderate wheel slippage risk)"
            rover_trafficability = "MODERATE TRACTION"
            trafficability_score = 65.0
        elif ati < 550.0:
            regolith_type = "Cemented Regolith & Pebble Matrix (High bearing capacity, optimal rover terrain)"
            rover_trafficability = "EXCELLENT / OPTIMAL TRACTION"
            trafficability_score = 95.0
        else:
            regolith_type = "Dense Exposed Basalt Bedrock / Rock Outcrops (Low slip, obstacle navigation required)"
            rover_trafficability = "SOLID BEDROCK / ROCK HAZARD"
            trafficability_score = 75.0

        # Dominant mineral signature
        dominant_mineral = max(mineral_shares.items(), key=lambda x: x[1]) if mineral_shares else ("Unknown", 0.0)

        # Aqueous alteration index (presence of clays, carbonates, sulfates)
        aqueous_minerals = mineral_shares.get("clays", 0.0) + mineral_shares.get("carbonates", 0.0) + mineral_shares.get("sulfates", 0.0)
        aqueous_index_pct = round(aqueous_minerals * 100.0, 1)

        return {
            "day_temp_k": round(day_temp_k, 1),
            "day_temp_c": round(day_c, 1),
            "night_temp_k": round(night_temp_k, 1),
            "night_temp_c": round(night_c, 1),
            "diurnal_delta_k": round(delta_t, 1),
            "apparent_thermal_inertia_ati": round(ati, 1),
            "regolith_classification": regolith_type,
            "rover_trafficability": rover_trafficability,
            "trafficability_score": trafficability_score,
            "dominant_mineral": dominant_mineral[0],
            "dominant_mineral_fraction_pct": round(dominant_mineral[1] * 100.0, 1),
            "aqueous_alteration_index_pct": aqueous_index_pct,
            "mineral_shares": mineral_shares
        }


# ==========================================
# 7. CANDIDATE EXPLORATION SPOTS & ROVER ROUTE DECISION ENGINE
# ==========================================
class MarsExplorationSiteSelector:
    """
    Multi-Criteria Decision Analysis (MCDA) Site Selection & Rover Route Planner:
    Synthesizes orbital data from MENCA, MCC, MSM, and TIS to evaluate and rank
    candidate Mars landing zones and exploration sites.
    """

    CANDIDATE_SITES = {
        "jezero_crater": {
            "id": "jezero_crater",
            "name": "Jezero Crater (Western Isidis Planitia)",
            "latitude": 18.38,
            "longitude": 77.58,
            "mola_elevation_km": -2.50,
            "target_type": "Ancient river delta & paleolake basin (Noachian-Hesperian boundary)",
            "terrain_slope_deg": 3.8,
            "surface_albedo": 0.16,
            "dust_optical_depth": 0.35,
            "msm_ch4_ppb": 7.4,
            "day_temp_k": 278.0,
            "night_temp_k": 175.0,
            "mineral_shares": {
                "clays": 0.45,       # Fe/Mg-smectite clays
                "carbonates": 0.30,  # Magnesium-carbonates
                "olivine": 0.15,
                "sulfates": 0.10
            },
            "science_rationale": "Deltaic sediment preservation of ancient microbial biosignatures and lacustrine clay horizons.",
            "traverse_waypoint": "Neretva Vallis Delta Inflow (18.42° N, 77.52° E)",
            "traverse_distance_km": 6.8,
            "max_slope_encounter_deg": 6.2,
            "solar_energy_kwh_per_sol": 3.65,
            "estimated_traverse_sols": 42
        },
        "gale_crater": {
            "id": "gale_crater",
            "name": "Gale Crater (Mount Sharp / Aeolis Mons)",
            "latitude": -5.35,
            "longitude": 137.80,
            "mola_elevation_km": -4.45,
            "target_type": "Deep impact crater with 5-km layered sedimentary central mound",
            "terrain_slope_deg": 5.6,
            "surface_albedo": 0.19,
            "dust_optical_depth": 0.40,
            "msm_ch4_ppb": 12.8,  # Known seasonal methane spike
            "day_temp_k": 282.0,
            "night_temp_k": 178.0,
            "mineral_shares": {
                "clays": 0.35,
                "sulfates": 0.40,    # Hydrated sulfates / Jarosite
                "carbonates": 0.05,
                "olivine": 0.20
            },
            "science_rationale": "Chronological stratigraphic record documenting Mars transition from wet habitability to hyper-arid desert.",
            "traverse_waypoint": "Mount Sharp Base Strata (5.38° S, 137.85° E)",
            "traverse_distance_km": 9.4,
            "max_slope_encounter_deg": 9.1,
            "solar_energy_kwh_per_sol": 3.80,
            "estimated_traverse_sols": 68
        },
        "oxia_planum": {
            "id": "oxia_planum",
            "name": "Oxia Planum (ExoMars Target Plains)",
            "latitude": 18.27,
            "longitude": 335.37, # 24.63 W
            "mola_elevation_km": -3.10,
            "target_type": "Vast ancient Noachian iron-magnesium phyllosilicate clay plains",
            "terrain_slope_deg": 1.4, # Extremely flat
            "surface_albedo": 0.14,
            "dust_optical_depth": 0.28,
            "msm_ch4_ppb": 1.9,
            "day_temp_k": 275.0,
            "night_temp_k": 172.0,
            "mineral_shares": {
                "clays": 0.75,       # Vermiculite & Saponite clays
                "silica": 0.15,
                "olivine": 0.10,
                "carbonates": 0.00
            },
            "science_rationale": "Ancient pre-Noachian clay sheets exposed by wind erosion; optimal organic molecular preservation.",
            "traverse_waypoint": "Cogoon Valles Alluvial Fan (18.30° N, 335.42° E)",
            "traverse_distance_km": 4.2,
            "max_slope_encounter_deg": 2.5,
            "solar_energy_kwh_per_sol": 3.70,
            "estimated_traverse_sols": 26
        },
        "nili_fossae": {
            "id": "nili_fossae",
            "name": "Nili Fossae / Syrtis Major Graben Faults",
            "latitude": 22.00,
            "longitude": 74.80,
            "mola_elevation_km": -0.60,
            "target_type": "Deep crustal graben fractures exposing unaltered mantle olivine & serpentine",
            "terrain_slope_deg": 8.2, # Rougher terrain
            "surface_albedo": 0.11,
            "dust_optical_depth": 0.32,
            "msm_ch4_ppb": 28.6, # Peak Martian Methane Anomaly!
            "day_temp_k": 272.0,
            "night_temp_k": 168.0,
            "mineral_shares": {
                "olivine": 0.55,     # Primitive mantle rock
                "carbonates": 0.25,  # Hydrothermal carbonates
                "clays": 0.15,
                "sulfates": 0.05
            },
            "science_rationale": "Primary candidate for ongoing serpentinization hydrothermal outgassing and peak atmospheric methane plume origins.",
            "traverse_waypoint": "Hydrothermal Graben Escarpment (22.05° N, 74.88° E)",
            "traverse_distance_km": 11.2,
            "max_slope_encounter_deg": 14.5,
            "solar_energy_kwh_per_sol": 3.55,
            "estimated_traverse_sols": 85
        },
        "valles_marineris": {
            "id": "valles_marineris",
            "name": "Valles Marineris (Melas Chasma Canyon Floor)",
            "latitude": -9.80,
            "longitude": 283.60,
            "mola_elevation_km": -3.85,
            "target_type": "Deepest canyon rift on Mars, exposing 8 km of deep crustal stratigraphy",
            "terrain_slope_deg": 11.4, # High slope relief
            "surface_albedo": 0.17,
            "dust_optical_depth": 0.55, # Canyon haze / fog
            "msm_ch4_ppb": 6.1,
            "day_temp_k": 286.0,
            "night_temp_k": 180.0,
            "mineral_shares": {
                "sulfates": 0.50,    # Layered sulfate deposits
                "silicates": 0.30,
                "clays": 0.10,
                "olivine": 0.10
            },
            "science_rationale": "Exposes Mars' deepest crustal evolution, canyon fog formation, and potential recurring slope lineae (RSL).",
            "traverse_waypoint": "Melas Chasma Interior Wall Layer (9.84° S, 283.65° E)",
            "traverse_distance_km": 8.0,
            "max_slope_encounter_deg": 16.8,
            "solar_energy_kwh_per_sol": 3.75,
            "estimated_traverse_sols": 72
        },
        "elysium_planitia": {
            "id": "elysium_planitia",
            "name": "Elysium Planitia (Cerberus Plains)",
            "latitude": 4.50,
            "longitude": 135.90,
            "mola_elevation_km": -2.60,
            "target_type": "Young flood basalt volcanic plain with shallow subsurface radar ice reflectors",
            "terrain_slope_deg": 1.1, # Safest engineering site
            "surface_albedo": 0.15,
            "dust_optical_depth": 0.30,
            "msm_ch4_ppb": 0.8,
            "day_temp_k": 280.0,
            "night_temp_k": 174.0,
            "mineral_shares": {
                "basalt": 0.80,
                "plagioclase": 0.15,
                "clays": 0.05
            },
            "science_rationale": "Benchmark for young Martian volcanism, seismic activity monitoring, and shallow subsurface ice access.",
            "traverse_waypoint": "Cerberus Lava Fissure (4.54° N, 135.96° E)",
            "traverse_distance_km": 5.0,
            "max_slope_encounter_deg": 2.1,
            "solar_energy_kwh_per_sol": 3.85,
            "estimated_traverse_sols": 30
        }
    }

    @classmethod
    def evaluate_site(cls, site_id: str) -> Dict[str, Any]:
        """
        Runs complete Multi-Criteria Decision Analysis (MCDA) for a candidate exploration site
        combining MENCA, MCC, MSM, and TIS payload readings.
        """
        site = cls.CANDIDATE_SITES.get(site_id)
        if not site:
            raise ValueError(f"Unknown site ID: {site_id}")

        # 1. Run Orbiter Payloads
        mcc_data = MarsOrbiterPayloads.simulate_mcc(
            altitude_km=421.7, # Periapsis reconnaissance
            surface_albedo=site["surface_albedo"],
            dust_optical_depth=site["dust_optical_depth"]
        )
        msm_data = MarsOrbiterPayloads.simulate_msm(
            absorption_ratio=0.98,
            background_ppb=1.2,
            localized_plume_ppb=max(0.0, site["msm_ch4_ppb"] - 1.2),
            olivine_fraction=site["mineral_shares"].get("olivine", 0.0)
        )
        tis_data = MarsOrbiterPayloads.simulate_tis(
            day_temp_k=site["day_temp_k"],
            night_temp_k=site["night_temp_k"],
            surface_albedo=site["surface_albedo"],
            mineral_shares=site["mineral_shares"]
        )
        menca_data = MarsOrbiterPayloads.simulate_menca(altitude_km=421.7)

        # 2. Compute Science Value Score S_sci (0 - 100)
        # Weights: Aqueous/clays (35%), Methane Anomaly (30%), Mineral Diversity (20%), Context/Stratigraphy (15%)
        clay_score = min(100.0, site["mineral_shares"].get("clays", 0.0) * 120.0 + site["mineral_shares"].get("carbonates", 0.0) * 80.0)
        ch4_score = min(100.0, (site["msm_ch4_ppb"] / 25.0) * 100.0)
        diversity_score = min(100.0, len([k for k, v in site["mineral_shares"].items() if v > 0.05]) * 25.0)
        context_score = 90.0 if "delta" in site["target_type"] or "crater" in site["target_type"] else 70.0

        science_score = (0.35 * clay_score) + (0.30 * ch4_score) + (0.20 * diversity_score) + (0.15 * context_score)

        # 3. Compute Landing & Rover Safety Score S_safe (0 - 100)
        # A. Elevation bonus: lower MOLA elevation provides deeper atmosphere for parachute braking
        # Elev < -1.5 km is required for standard landing; -4 km is ideal (+100)
        elev_score = max(0.0, min(100.0, 50.0 - (15.0 * site["mola_elevation_km"])))

        # B. Slope hazard penalty: slopes > 5 deg degrade landing radar and risk tipping
        slope_score = max(0.0, 100.0 - (7.5 * site["terrain_slope_deg"]))

        # C. Thermal survival: night temp must exceed electronics qualification threshold (> 160 K)
        thermal_score = max(0.0, min(100.0, (site["night_temp_k"] - 150.0) * 3.3))

        # D. Rover Trafficability from TIS ATI
        traffic_score = tis_data["trafficability_score"]

        safety_score = (0.35 * elev_score) + (0.35 * slope_score) + (0.15 * thermal_score) + (0.15 * traffic_score)

        # 4. Overall Exploration Viability Index (EVI): Geometric Mean
        evi = math.sqrt(max(0.0, science_score * safety_score))

        # Overall Recommendation Tier
        if evi >= 78.0:
            recommendation = "TIER 1 — PRIMARY CANDIDATE LANDING & ROVER EXPLORATION SITE"
        elif evi >= 65.0:
            recommendation = "TIER 2 — HIGH-VALUE SECONDARY CANDIDATE (ENGINEERING / SCIENCE TRADE-OFF)"
        else:
            recommendation = "TIER 3 — HIGH SCIENTIFIC VALUE BUT DEMANDING TERRAIN RISK"

        return {
            "site_id": site["id"],
            "name": site["name"],
            "coordinates": f"{site['latitude']}° N, {site['longitude']}° E",
            "mola_elevation_km": site["mola_elevation_km"],
            "target_type": site["target_type"],
            "science_score": round(science_score, 1),
            "safety_score": round(safety_score, 1),
            "exploration_viability_index": round(evi, 1),
            "recommendation": recommendation,
            "orbiter_telemetry": {
                "mcc": mcc_data,
                "msm": msm_data,
                "tis": tis_data,
                "menca": menca_data
            },
            "rover_route_plan": {
                "target_waypoint": site["traverse_waypoint"],
                "traverse_distance_km": site["traverse_distance_km"],
                "max_slope_deg": site["max_slope_encounter_deg"],
                "trafficability": tis_data["rover_trafficability"],
                "solar_power_kwh_per_sol": site["solar_energy_kwh_per_sol"],
                "estimated_sols": site["estimated_traverse_sols"]
            }
        }

    @classmethod
    def rank_all_sites(cls) -> List[Dict[str, Any]]:
        """
        Ranks all candidate exploration sites in descending order of Exploration Viability Index (EVI).
        """
        results = [cls.evaluate_site(sid) for sid in cls.CANDIDATE_SITES.keys()]
        results.sort(key=lambda x: x["exploration_viability_index"], reverse=True)
        return results


# ==========================================
# 8. CLI TEST EXECUTION

def gravity_assist(v_inf_kms: float, periapsis_km: float, mu_km3s2: float) -> dict:
    """
    Compute turn angle (δ) and ΔV gain for a gravity‑assist (slingshot) maneuver.

    Parameters
    ----------
    v_inf_kms : float
        Hyperbolic excess speed relative to the assisting body (km/s).
    periapsis_km : float
        Periapsis radius from the centre of the body (km). Must be > 0.
    mu_km3s2 : float
        Gravitational parameter μ of the body (km³/s²).

    Returns
    -------
    dict
        Contains the turn angle in degrees, the ΔV gain in km/s, eccentricity, and the periapsis radius.
    """
    # Ensure valid inputs
    if periapsis_km <= 0:
        raise ValueError("periapsis_km must be positive")
    if v_inf_kms <= 0:
        raise ValueError("v_inf_kms must be positive")
    if mu_km3s2 <= 0:
        raise ValueError("mu_km3s2 must be positive")

    # Eccentricity of the hyperbolic trajectory
    e = 1 + (periapsis_km * v_inf_kms ** 2) / mu_km3s2
    # Turn angle δ = 2 * arcsin(1/e)
    delta_rad = 2 * math.asin(1 / e)
    delta_deg = math.degrees(delta_rad)
    # ΔV gain = 2 * v_inf * sin(δ/2)
    delta_v_gain = 2 * v_inf_kms * math.sin(delta_rad / 2)

    return {
        "turn_angle_deg": round(delta_deg, 3),
        "delta_v_gain_kms": round(delta_v_gain, 3),
        "eccentricity": round(e, 5),
        "periapsis_radius_km": round(periapsis_km, 3),
    }

# ==========================================
if __name__ == "__main__":
    print("=" * 70)
    print("MARSBOUND: ISRO MISSION CONTROL AEROSPACE ENGINE INITIALIZATION")
    print("=" * 70)

    # Test 1: Nominal LCC Check
    nominal_telemetry = {
        "surface_wind_speed": 6.5,
        "upper_wind_shear": 12.4,
        "cloud_top_temp_c": -12.0,
        "lightning_detected_in_corridor": False,
        "lox_temp_c": -183.2,
        "lh2_temp_c": -253.1,
        "tank_pressure_bar": 2.35,
        "ground_station_lock": True,
        "telemetry_snr_db": 24.8,
        "geomagnetic_kp": 2.1,
        "debris_miss_dist_km": 142.0,
        "collision_probability": 0.0
    }

    result = LaunchCommitCriteria.evaluate(nominal_telemetry)
    print(f"\n[NOMINAL TEST] Master Launch Decision: {result['decision']}")
    for sub, info in result["checklist"].items():
        print(f"  * {info['name']}: {'🟢 PASS' if info['passed'] else '🔴 FAIL'}")

    # Test 2: Anomaly Injection (High Wind Shear & Debris Conjunction)
    anomaly_telemetry = dict(nominal_telemetry)
    anomaly_telemetry["upper_wind_shear"] = 31.5 # Exceeds 25 m/s
    anomaly_telemetry["debris_miss_dist_km"] = 12.3 # Violates 25 km clearance

    res_anomaly = LaunchCommitCriteria.evaluate(anomaly_telemetry)
    print(f"\n[ANOMALY INJECTION TEST] Master Launch Decision: {res_anomaly['decision']}")
    print("  Violations detected:")
    for v in res_anomaly["violations"]:
        print(f"   - {v}")

    # Test 3: Flight Dynamics Step Simulation
    print("\n[ASCENT TRAJECTORY STEP SIMULATION - First 10 seconds]")
    state = {
        "time": 0.0,
        "altitude_m": 12.0,
        "velocity_mps": 0.0,
        "fuel_remaining_kg": 410000.0,
        "stage_index": 0,
        "stage_start_time": 0.0,
        "downrange_km": 0.0,
        "fairing_jettisoned": False
    }

    for step in range(5):
        state = LaunchAscentPhysics.simulate_step(state, dt=2.0)
        print(f"  T+{state['time']}s | Alt: {state['altitude_km']} km | Vel: {state['speed_kmh']} km/h (M {state['mach']}) | Dynamic Q: {state['dynamic_pressure_kpa']} kPa | SNR: {state['snr_db']} dB")

    # Test 4: On-orbit payload spectral analysis (Bhoonidhi)
    print("\n[ON-ORBIT PAYLOAD SCIENCE TEST (Bhoonidhi Spectral Engine)]")
    crop_pixels = SatellitePayloadOperations.compute_spectral_indices(nir=0.65, red=0.12, green=0.25, swir=0.18)
    water_pixels = SatellitePayloadOperations.compute_spectral_indices(nir=0.08, red=0.15, green=0.55, swir=0.04)
    print(f"  Healthy Agricultural Field -> NDVI: {crop_pixels['ndvi']} (Healthy Biomass) | NDWI: {crop_pixels['ndwi']}")
    print(f"  Inundated Flood Water Body  -> NDVI: {water_pixels['ndvi']} | NDWI: {water_pixels['ndwi']} (Active Water Index)")

    # Test 5: Trajectory Analysis Engine
    print("\n[TRAJECTORY & ORBITAL MECHANICS ANALYSIS]")
    kep = TrajectoryAnalyzer.calculate_keplerian_elements(altitude_km=450.0, velocity_mps=7630.0, flight_path_angle_deg=0.02)
    print(f"  Keplerian Elements: a = {kep['semi_major_axis_km']} km, e = {kep['eccentricity']}, Rp = {kep['perigee_altitude_km']} km, Ra = {kep['apogee_altitude_km']} km, Period = {kep['orbital_period_minutes']} min")
    print(f"  Orbit Classification: {kep['orbit_type']}")

    dv = TrajectoryAnalyzer.calculate_deltav_budget()
    print(f"  Delta-V Budget: Total Ideal = {dv['total_ideal_deltav_mps']} m/s | Net Orbital = {dv['net_orbital_velocity_mps']} m/s | Gravity Loss = {dv['gravity_loss_mps']} m/s ({dv['gravity_loss_pct']}%) | Drag Loss = {dv['aerodynamic_drag_loss_mps']} m/s ({dv['drag_loss_pct']}%)")

    zones = TrajectoryAnalyzer.get_stage_impact_zones()
    print(f"  Stage Impact Safety Zones Mapped: {len(zones)} zones in Bay of Bengal corridor")
    for z in zones:
        print(f"   - {z['stage']} -> Splashdown: {z['impact_latitude']}°N, {z['impact_longitude']}°E ({z['location_description']})")

    # Test 6: MARSBOUND Mars Interplanetary & Orbiter Engine
    print("\n[MARSBOUND MARS INTERPLANETARY & ORBITER SCIENCE ENGINE]")
    helio_mid = MarsboundMarsMission.get_heliocentric_state(progress_fraction=0.5)
    print(f"  Cruise Midpoint (Day {helio_mid['mission_day']} / 297):")
    print(f"   - Heliocentric Distance: {helio_mid['heliocentric_dist_au']} AU ({helio_mid['heliocentric_velocity_kms']} km/s)")
    print(f"   - Distance to Earth: {helio_mid['dist_to_earth_million_km']} million km | One-Way Light Delay: {helio_mid['owlt_minutes']} min")
    print(f"   - Sun-Earth-Probe (SEP) Angle: {helio_mid['sep_angle_deg']}° | IDSN 32m SNR: {helio_mid['snr_db']} dB")

    moi = MarsboundMarsMission.get_moi_telemetry()
    print(f"  Mars Orbit Insertion (MOI) -> Retrograde Delta-V: {moi['delta_v_required_mps']} m/s | Burn: {moi['lam_burn_time_seconds']}s")
    print(f"  Martian Orbit: {moi['periapsis_altitude_km']} km x {moi['apoapsis_altitude_km']} km | Period: {moi['orbital_period_hours']} hours")

    menca = MarsboundMarsMission.simulate_menca_spectrum(altitude_km=450.0)
    print(f"  MENCA Exospheric Mass Spectrum at {menca['altitude_km']} km:")
    for sp in menca['spectrum']:
        print(f"   * {sp['species']} ({sp['amu']} amu): {sp['counts']} counts ({sp['fraction_pct']}%)")
    print(f"  Dominant Exospheric Species at {menca['altitude_km']} km: {menca['dominant_species']}")

    # Test 7: Mars Orbiter Payloads Suite (MENCA • MCC • MSM • TIS)
    print("\n[MARS ORBITER PAYLOADS SUITE (MENCA • MCC • MSM • TIS)]")
    mcc_test = MarsOrbiterPayloads.simulate_mcc(altitude_km=421.7, surface_albedo=0.16, dust_optical_depth=0.35)
    print(f"  MCC Optical Imaging -> GSD: {mcc_test['ground_sampling_distance_m']} m/px ({mcc_test['resolution_tier']}) | Transmittance: {mcc_test['atmospheric_transmittance']} | Contrast: {mcc_test['image_contrast_pct']}%")

    msm_test = MarsOrbiterPayloads.simulate_msm(absorption_ratio=0.98, background_ppb=1.2, localized_plume_ppb=27.4, olivine_fraction=0.55)
    print(f"  MSM Methane Sensor  -> [CH4]: {msm_test['columnar_methane_ppb']} ppb | Plume: {msm_test['is_plume_anomaly']} | Origin: {msm_test['geochemical_origin_assessment']}")

    tis_test = MarsOrbiterPayloads.simulate_tis(day_temp_k=278.0, night_temp_k=175.0, surface_albedo=0.16, mineral_shares={"clays": 0.45, "carbonates": 0.30, "olivine": 0.15})
    print(f"  TIS Thermal / Min   -> ATI: {tis_test['apparent_thermal_inertia_ati']} | Trafficability: {tis_test['rover_trafficability']} | Aqueous Index: {tis_test['aqueous_alteration_index_pct']}%")

    # Test 8: Candidate Exploration Sites & MCDA Ranking
    print("\n[MARTIAN CANDIDATE EXPLORATION SPOTS RANKING & ROVER ROUTE PLANNING]")
    ranked_sites = MarsExplorationSiteSelector.rank_all_sites()
    for rank, site in enumerate(ranked_sites, 1):
        print(f"  #{rank} {site['name']}")
        print(f"     Coordinates: {site['coordinates']} | MOLA: {site['mola_elevation_km']} km | EVI: {site['exploration_viability_index']} (Sci: {site['science_score']}, Safe: {site['safety_score']})")
        print(f"     CH4: {site['orbiter_telemetry']['msm']['columnar_methane_ppb']} ppb | TIS ATI: {site['orbiter_telemetry']['tis']['apparent_thermal_inertia_ati']} ({site['orbiter_telemetry']['tis']['rover_trafficability']})")
        print(f"     Rover Route: {site['rover_route_plan']['traverse_distance_km']} km to {site['rover_route_plan']['target_waypoint']} (~{site['rover_route_plan']['estimated_sols']} Sols)")

    # Demo gravity assist integration
    demo_ga = gravity_assist(v_inf_kms=8.0, periapsis_km=6500.0, mu_km3s2=EARTH_MU)
    print(f"\n[GRAVITY ASSIST DEMO] Turn angle: {demo_ga['turn_angle_deg']}°, ΔV gain: {demo_ga['delta_v_gain_kms']} km/s")
    print("\nEngine validation completed successfully.")
