"""
System configuration parameters: operating constraints, disturbances, prices and action space.
Values are taken from sections 1, 2-3 and 2-4 of the Software Requirements Specification (SRS).
"""

from __future__ import annotations

# Length of each control decision step. Real SCADA sampling is every 1 second, but training
# the RL agent on that interval is impractical; therefore each environment step is
# considered equivalent to a 15-minute decision interval (control decision frequency, not monitoring frequency).
DECISION_STEP_MINUTES = 15
STEPS_PER_EPISODE = 96  # one full operating day (96 × 15 minutes = 24 hours)

# Operating constraints of state/disturbance variables (sections 1 and 2-3 of the SRS)
OPERATING_LIMITS = {
    "T_primary_reformer": (750.0, 850.0),      # °C
    "T_secondary_reformer": (950.0, 1050.0),   # °C
    "P_ammonia_reactor": (120.0, 250.0),       # bar
    "S_C_ratio": (2.5, 4.0),                   # mol/mol
    "feed_gas_flow": (80_000.0, 120_000.0),    # Nm3/h
    "air_flow": (40_000.0, 60_000.0),          # Nm3/h
    "steam_flow": (120.0, 200.0),              # ton/h
    "compressor_power": (15.0, 35.0),          # MW
    "cooling_water_temp": (25.0, 40.0),        # °C
    "cooling_water_flow": (8_000.0, 15_000.0), # m3/h
    "ambient_temp": (-5.0, 45.0),              # °C
    "ammonia_production": (30.0, 45.0),        # ton/h
    "urea_production": (45.0, 65.0),           # ton/h
    "melamine_production": (1.5, 3.0),         # ton/h
}

# Uncontrollable variables (process disturbances)
DISTURBANCE_RANGES = {
    "feed_composition_CH4": (0.85, 0.95),
    "feed_composition_C2H6": (0.02, 0.08),
    "feed_composition_C3H8": (0.01, 0.04),
    "feed_composition_N2": (0.01, 0.03),
    "feed_composition_CO2": (0.005, 0.02),
    "coking_factor": (0.0, 0.3),  # efficiency reduction factor due to reformer coil coking
}

# Price range (rials) - section 2-3-2 of the SRS
PRICE_RANGES = {
    "gas_price": (5_000.0, 8_000.0),          # IRR/Nm3
    "electricity_price": (800.0, 1_500.0),    # IRR/kWh
    "ammonia_price": (18_000.0, 25_000.0),    # IRR/ton
    "urea_price": (12_000.0, 18_000.0),       # IRR/ton
    "melamine_price": (45_000.0, 60_000.0),   # IRR/ton
    "carbon_credit_price": (500.0, 1_500.0),  # IRR/ton CO2
}

# Control action space (section 2-4-1 of the SRS) - 11 continuous actions.
# Names with *_APPROX mean the effect of this action on the physical model is modeled
# in a simplified way (a detailed model of this equipment is outside the scope of this repo); see
# simulator.py for details.
ACTION_SPACE = {
    "S_C_ratio": (2.5, 4.0),                  # mol/mol
    "T_primary_reformer": (750.0, 850.0),     # °C  (COT)
    "T_secondary_reformer": (950.0, 1050.0),  # °C
    "P_ammonia_reactor": (120.0, 250.0),      # bar
    "secondary_air_pct": (50.0, 100.0),       # % of air flow capacity to the secondary reformer
    "cooling_water_temp_target": (25.0, 40.0),# °C
    "cooling_water_flow_pct": (50.0, 100.0),  # % of cooling water circulation capacity
    "compressor_speed_pct": (60.0, 100.0),    # % of main compressors power
    "heat_recovery_ratio_pct": (50.0, 90.0),  # % APPROX - heat recovery ratio
    "aux_fuel_pct": (0.0, 100.0),             # % APPROX - auxiliary fuel flow
    "control_valve_pct": (0.0, 100.0),        # % APPROX - opening of key control valves
}
ACTION_KEYS = list(ACTION_SPACE.keys())

# Target specific energy consumption (SEC) indicator - section 1-2 of the SRS, basis for inefficiency detection
SEC_TARGET_AMMONIA_GJ_PER_TON = 62.61
SEC_TARGET_UREA_GJ_PER_TON = 4.52
SEC_ALERT_DEVIATION_PCT = 5.0  # deviation above this percentage from the target → preventive alert

RANDOM_SEED = 42
