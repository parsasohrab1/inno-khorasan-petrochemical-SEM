# inno-khorasan-petrochemical-SEM

Smart Energy Management System for Khorasan Petrochemical Based on Reinforcement Learning
1. Study and Understanding of Khorasan Petrochemical
1-1. General Company Profile
Khorasan Petrochemical Company (KHPC) was established in 1371 [1992] in Bojnourd, the capital of North Khorasan Province, and its first phase was commissioned in 1375 [1996]. The complex covers an area of more than 204 hectares at kilometer 17 of the Bojnourd-Shirvan road.

Main products:

Ammonia (annual production capacity 330 thousand tons)

Urea prill (annual production capacity 495 thousand tons)

Melamine crystal (annual production capacity 20 thousand tons)

Liquid nitrogen

Ownership: Tamin Oil, Gas and Petrochemical Investment Company (TAPICO)

1-2. Production Processes and Energy Consumption
The production process is chained: natural gas feed enters the ammonia production unit, the produced ammonia is sent to the urea unit, and part of the ammonia and urea is consumed as feed for the melamine crystal production unit.

Key energy consumption:

Natural gas as the main feed and fuel

Electricity for rotating equipment and refrigeration systems

Process steam in the various units

Specific energy consumption (SEC) indicators:

Ammonia unit: 62.61 GJ per ton of product (5.5% below the national standard)

Urea unit: 4.52 GJ per ton of product (5.97% below the national standard)

Exergy destruction in the ammonia unit (based on an existing study):

Section	Exergy destruction (GJ/h)
Syngas production	42
Shift reactor	36
CO₂ separation	31
Ammonia synthesis	69
Refrigeration	12
Methanation	2
1-3. Greenhouse Gas Emissions
According to the studies conducted, the greatest adverse environmental impacts of the ammonia unit are related to human health and are mainly caused by the consumption of methane and steam and by emissions from the ammonia unit and natural gas. The petrochemical industry as a whole accounts for about 14% of total industrial energy consumption and nearly 1.5 gigatons of CO₂ emissions per year.

2. Software Requirements Specification (SRS)
2-1. System Purpose
Design, development and deployment of a Smart Energy Management System (SEMS) based on Reinforcement Learning for dynamic optimization of energy consumption, reduction of greenhouse gas emissions and improvement of economic productivity at the Khorasan Petrochemical complex.

2-2. System Scope
The system covers all production units, including:

Ammonia production unit

Urea production unit

Melamine crystal production unit

Utility unit (steam, electricity, cooling water, compressed air, liquid nitrogen production)

2-3. System Inputs
2-3-1. Real-time operational data (from SCADA and IoT)
No.	Data name	Unit	Source	Sampling rate
1	Primary reformer outlet temperature	°C	SCADA	1 second
2	Secondary reformer outlet temperature	°C	SCADA	1 second
3	Ammonia synthesis reactor pressure	bar	SCADA	1 second
4	Ammonia synthesis reactor temperature	°C	SCADA	1 second
5	Natural gas feed inlet flow	Nm³/h	Flow Meter	1 second
6	Air flow into the reformer	Nm³/h	Flow Meter	1 second
7	Steam flow into the process	ton/h	Flow Meter	1 second
8	Power consumption of main compressors	MW	Power Meter	1 second
9	Power consumption of main pumps	kW	Power Meter	1 second
10	Cooling water inlet/outlet temperature	°C	Temperature Sensor	5 seconds
11	Circulating cooling water flow	m³/h	Flow Meter	5 seconds
12	Utility steam pressure produced	bar	Pressure Sensor	1 second
13	Steam temperature produced	°C	Temperature Sensor	1 second
14	Feed gas composition (CH₄, C₂H₆, C₃H₈, N₂, CO₂)	%	GC Analyzer	15 minutes
15	Syngas outlet composition (H₂, N₂, CH₄, Ar)	%	GC Analyzer	15 minutes
16	Liquid ammonia production flow	ton/h	Flow Meter	1 minute
17	Urea production flow	ton/h	Flow Meter	1 minute
18	Melamine production flow	ton/h	Flow Meter	1 minute
19	Ambient temperature	°C	Weather Station	1 minute
20	Ambient relative humidity	%	Weather Station	1 minute
2-3-2. Economic data
No.	Data name	Unit	Source	Update rate
21	Natural gas feed price	IRR/Nm³	Financial system	Daily
22	Electricity price	IRR/kWh	Financial system	Daily
23	Ammonia selling price	IRR/ton	Financial system	Daily
24	Urea selling price	IRR/ton	Financial system	Daily
25	Melamine selling price	IRR/ton	Financial system	Daily
26	Reference exchange rate	IRR/USD	Financial system	Daily
27	Carbon emission reduction certificate price	IRR/ton CO₂	Financial system	Daily
2-3-3. Operational data and constraints
No.	Data name	Description
28	Equipment status (online/offline/maintenance)	Operational status of each key equipment
29	Preventive maintenance schedule	Planned maintenance scheduling
30	Operational safety constraints	Allowable temperature, pressure and flow limits
31	Reformer coil coking status	Estimated thermal resistance index
2-3-4. Environmental and sustainability data
No.	Data name	Unit	Source
32	Instantaneous CO₂ emission	ton/h	Calculated from fuel flow
33	NOx emission	ppm	Stack analyzer
34	Specific energy consumption (SEC) of ammonia	GJ/ton	Calculated
35	Specific energy consumption (SEC) of urea	GJ/ton	Calculated
2-4. System Outputs
2-4-1. Control outputs (Action Space)
No.	Control action	Range	Unit
1	Reformer steam-to-carbon ratio (S/C)	2.5 – 4.0	mol/mol
2	Primary reformer outlet temperature (COT)	750 – 850	°C
3	Secondary reformer outlet temperature	950 – 1050	°C
4	Ammonia synthesis operating pressure	120 – 250	bar
5	Air flow into the secondary reformer	50 – 100	% capacity
6	Target cooling water temperature	25 – 40	°C
7	Cooling water circulation flow	50 – 100	% capacity
8	Main compressors power (speed)	60 – 100	%
9	Heat recovery ratio	50 – 90	%
10	Auxiliary fuel flow (if needed)	0 – 100	% capacity
11	Key control valve settings	0 – 100	% opening
2-4-2. Prediction and reporting outputs
No.	Output	Description
12	Energy consumption forecast for the next 24 hours	Based on historical patterns and forecast conditions
13	CO₂ emission forecast	Based on different operational scenarios
14	Identification of energy inefficiencies	High-accuracy detection of energy loss points
15	Preventive alerts	Alert when deviating from optimal conditions
16	Energy management dashboard	Real-time display of key energy performance indicators
17	Periodic reports	Daily, weekly and monthly energy consumption reports
18	Optimization recommendations	Practical suggestions for improving energy efficiency
2-5. Non-Operational Requirements
2-5-1. Performance requirements
Control response latency of less than 500 milliseconds

Energy consumption prediction accuracy with an error of less than 5%

Output confidence factor ≥ 95%

Ability to run on industrial servers with 99.99% availability

2-5-2. Security requirements
Multi-step authentication for system access

Complete logging of operations

Communication encryption (TLS 1.3)

Automatic backup with a 6-hour cycle

2-5-3. Integration requirements
Compatibility with industrial protocols: OPC UA, Modbus TCP/IP, Profinet

Ability to connect to the existing DCS

API output for connecting to enterprise-level systems

3. Synthetic Data Generation for Training the Reinforcement Learning Agent
To achieve a high confidence factor (≥95%) and low error (≤5%), we need at least 100,000 data samples over different time intervals. The following code generates synthetic data using a Physics-Informed approach:

python
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from scipy.stats import norm, truncnorm
import random

class KhorasanPetrochemicalDataGenerator:
    """
    Synthetic data generator for Khorasan Petrochemical
    Based on physics-informed models and thermodynamic constraints
    """
    
    def __init__(self, seed=42):
        np.random.seed(seed)
        random.seed(seed)
        
        # Operational constraints based on real information
        self.limits = {
            'T_primary_reformer': (750, 850),      # °C
            'T_secondary_reformer': (950, 1050),    # °C
            'P_ammonia_reactor': (120, 250),        # bar
            'S_C_ratio': (2.5, 4.0),                # mol/mol
            'feed_gas_flow': (80000, 120000),       # Nm3/h
            'air_flow': (40000, 60000),             # Nm3/h
            'steam_flow': (120, 200),               # ton/h
            'compressor_power': (15, 35),           # MW
            'cooling_water_temp': (25, 40),         # °C
            'cooling_water_flow': (8000, 15000),    # m3/h
            'ambient_temp': (-5, 45),               # °C
            'ammonia_production': (30, 45),         # ton/h
            'urea_production': (45, 65),            # ton/h
            'melamine_production': (1.5, 3.0),      # ton/h
        }
        
        # Uncontrollable variables (disturbances)
        self.disturbances = {
            'feed_composition_CH4': (0.85, 0.95),
            'feed_composition_C2H6': (0.02, 0.08),
            'feed_composition_C3H8': (0.01, 0.04),
            'feed_composition_N2': (0.01, 0.03),
            'feed_composition_CO2': (0.005, 0.02),
            'coking_factor': (0.0, 0.3),  # efficiency reduction factor due to coking
        }
        
        # Costs and prices (IRR)
        self.prices = {
            'gas_price': (5000, 8000),      # IRR per Nm3
            'electricity_price': (800, 1500), # IRR per kWh
            'ammonia_price': (18000, 25000),  # IRR per ton
            'urea_price': (12000, 18000),     # IRR per ton
            'melamine_price': (45000, 60000), # IRR per ton
            'carbon_credit_price': (500, 1500) # IRR per ton CO2
        }
        
    def _generate_time_series(self, n_samples, start_time=None):
        """Generate a time series with 1-second sampling"""
        if start_time is None:
            start_time = datetime.now() - timedelta(days=30)
        
        timestamps = [start_time + timedelta(seconds=i) for i in range(n_samples)]
        return timestamps
    
    def _add_noise(self, value, noise_std, min_val=None, max_val=None):
        """Add Gaussian noise with limits"""
        noisy = value + np.random.normal(0, noise_std * abs(value))
        if min_val is not None:
            noisy = max(noisy, min_val)
        if max_val is not None:
            noisy = min(noisy, max_val)
        return noisy
    
    def _simulate_reformer(self, feed_flow, S_C_ratio, T_primary, T_secondary, 
                           feed_composition, coking_factor):
        """
        Reformer simulation based on mass and energy balance
        Returns: syngas flow, composition, energy consumption
        """
        # Calculate steam flow
        steam_flow = feed_flow * S_C_ratio * 0.012  # conversion approximation
        
        # Effect of coking on efficiency
        efficiency_factor = 1.0 - coking_factor * 0.3
        
        # Methane conversion efficiency based on temperature (simple Arrhenius model)
        k_primary = 0.85 * (1 + 0.003 * (T_primary - 800)) * efficiency_factor
        k_secondary = 0.92 * (1 + 0.002 * (T_secondary - 1000)) * efficiency_factor
        
        # Syngas composition
        H2_fraction = 0.60 + 0.02 * (T_primary - 800)/50 + 0.01 * (1 - coking_factor)
        N2_fraction = 0.20 + 0.01 * (feed_composition['N2'] - 0.02)/0.01
        CH4_fraction = 0.15 - 0.02 * (T_primary - 800)/50 - 0.01 * k_primary
        Ar_fraction = 0.02 + 0.01 * (feed_composition['N2'] - 0.02)/0.01
        
        # Normalization
        total = H2_fraction + N2_fraction + CH4_fraction + Ar_fraction
        H2_fraction /= total
        N2_fraction /= total
        CH4_fraction /= total
        Ar_fraction /= total
        
        # Reformer energy consumption
        energy_consumption = feed_flow * 2.5 * (1 - 0.1 * coking_factor)  # GJ/h
        
        return {
            'syngas_flow': feed_flow * 1.8 * efficiency_factor,
            'H2_fraction': H2_fraction,
            'N2_fraction': N2_fraction,
            'CH4_fraction': CH4_fraction,
            'Ar_fraction': Ar_fraction,
            'steam_flow': steam_flow,
            'energy_consumption': energy_consumption,
            'efficiency': k_primary * k_secondary
        }
    
    def _simulate_ammonia_synthesis(self, syngas_flow, H2_fraction, N2_fraction, 
                                    P_reactor, T_reactor):
        """
        Ammonia synthesis simulation with reaction kinetics
        Returns: ammonia production flow, energy consumption, conversion
        """
        # The optimal H2/N2 ratio is 3
        H2_N2_ratio = H2_fraction / N2_fraction if N2_fraction > 0 else 3.0
        
        # Conversion factor based on temperature and pressure (simple model)
        conversion = 0.85 * (1 + 0.005 * (P_reactor - 180)/10) * \
                    (1 - 0.008 * (T_reactor - 450)/10)
        conversion = max(0.4, min(0.98, conversion))
        
        # Ammonia production
        ammonia_flow = syngas_flow * 0.15 * conversion * (H2_N2_ratio / 3.0) * 0.8
        
        # Compressor energy consumption
        compressor_power = 20 * (P_reactor / 180) * (syngas_flow / 100000) * 0.9
        
        return {
            'ammonia_flow': max(20, min(55, ammonia_flow)),
            'conversion': conversion,
            'compressor_power': compressor_power,
            'H2_N2_ratio': H2_N2_ratio
        }
    
    def _simulate_urea_production(self, ammonia_flow, CO2_availability):
        """
        Urea production simulation from ammonia and CO2
        """
        # Stoichiometric ratio 2NH3 + CO2 → (NH2)2CO + H2O
        urea_flow = ammonia_flow * 0.75 * CO2_availability * 0.92
        return max(35, min(70, urea_flow))
    
    def _simulate_melamine_production(self, ammonia_flow, urea_flow):
        """
        Melamine production simulation from urea
        """
        # Urea consumed as melamine feed
        urea_for_melamine = min(urea_flow * 0.15, 3.5)
        melamine_flow = urea_for_melamine * 0.28  # approximate yield
        return max(0.5, min(3.5, melamine_flow))
    
    def _calculate_emissions(self, feed_flow, energy_consumption, efficiency):
        """
        Calculate CO2 emission based on fuel consumption and efficiency
        """
        # Emission from fuel combustion
        combustion_CO2 = feed_flow * 0.002 * (1 - efficiency * 0.1)  # ton/h
        
        # Process emission
        process_CO2 = feed_flow * 0.0005  # ton/h
        
        return combustion_CO2 + process_CO2
    
    def generate_sample(self, t):
        """
        Generate one complete data sample
        """
        # Uncontrollable variables (disturbances)
        feed_composition = {
            'CH4': np.random.uniform(*self.disturbances['feed_composition_CH4']),
            'C2H6': np.random.uniform(*self.disturbances['feed_composition_C2H6']),
            'C3H8': np.random.uniform(*self.disturbances['feed_composition_C3H8']),
            'N2': np.random.uniform(*self.disturbances['feed_composition_N2']),
            'CO2': np.random.uniform(*self.disturbances['feed_composition_CO2'])
        }
        
        # Feed composition normalization
        total = sum(feed_composition.values())
        for k in feed_composition:
            feed_composition[k] /= total
        
        coking_factor = np.random.uniform(*self.disturbances['coking_factor'])
        ambient_temp = np.random.uniform(*self.limits['ambient_temp'])
        
        # Decision variables (controllable by the agent)
        S_C_ratio = np.random.uniform(*self.limits['S_C_ratio'])
        T_primary = np.random.uniform(*self.limits['T_primary_reformer'])
        T_secondary = np.random.uniform(*self.limits['T_secondary_reformer'])
        P_reactor = np.random.uniform(*self.limits['P_ammonia_reactor'])
        T_reactor = 400 + 0.5 * (T_secondary - 950) + np.random.normal(0, 5)
        T_reactor = max(380, min(500, T_reactor))
        
        feed_flow = np.random.uniform(*self.limits['feed_gas_flow'])
        air_flow = np.random.uniform(*self.limits['air_flow'])
        
        cooling_water_temp = np.random.uniform(*self.limits['cooling_water_temp'])
        cooling_water_flow = np.random.uniform(*self.limits['cooling_water_flow'])
        
        # Reformer simulation
        reformer_result = self._simulate_reformer(
            feed_flow, S_C_ratio, T_primary, T_secondary,
            feed_composition, coking_factor
        )
        
        # Ammonia synthesis simulation
        ammonia_result = self._simulate_ammonia_synthesis(
            reformer_result['syngas_flow'],
            reformer_result['H2_fraction'],
            reformer_result['N2_fraction'],
            P_reactor, T_reactor
        )
        
        ammonia_flow = ammonia_result['ammonia_flow']
        
        # Urea production simulation
        CO2_availability = 0.85 + 0.1 * (feed_composition['CO2'] / 0.02)
        urea_flow = self._simulate_urea_production(ammonia_flow, CO2_availability)
        
        # Melamine production simulation
        melamine_flow = self._simulate_melamine_production(ammonia_flow, urea_flow)
        
        # Emission calculation
        total_emissions = self._calculate_emissions(
            feed_flow, 
            reformer_result['energy_consumption'],
            reformer_result['efficiency']
        )
        
        # Specific energy consumption (SEC) calculation
        SEC_ammonia = reformer_result['energy_consumption'] / ammonia_flow
        SEC_urea = (reformer_result['energy_consumption'] * 0.4) / urea_flow
        
        # Prices (with random daily variations)
        prices = {
            'gas': np.random.uniform(*self.prices['gas_price']),
            'electricity': np.random.uniform(*self.prices['electricity_price']),
            'ammonia': np.random.uniform(*self.prices['ammonia_price']),
            'urea': np.random.uniform(*self.prices['urea_price']),
            'melamine': np.random.uniform(*self.prices['melamine_price']),
            'carbon': np.random.uniform(*self.prices['carbon_credit_price'])
        }
        
        # Profitability calculation
        revenue = (ammonia_flow * prices['ammonia'] + 
                   urea_flow * prices['urea'] + 
                   melamine_flow * prices['melamine'])
        
        energy_cost = (feed_flow * prices['gas'] * 0.001 + 
                      ammonia_result['compressor_power'] * 1000 * prices['electricity'] * 0.001)
        
        carbon_cost = total_emissions * prices['carbon']
        
        profit = revenue - energy_cost - carbon_cost
        
        # Build the sample
        sample = {
            # Inputs (State)
            'timestamp': t,
            'feed_flow': feed_flow,
            'feed_CH4': feed_composition['CH4'],
            'feed_C2H6': feed_composition['C2H6'],
            'feed_C3H8': feed_composition['C3H8'],
            'feed_N2': feed_composition['N2'],
            'feed_CO2': feed_composition['CO2'],
            'coking_factor': coking_factor,
            'ambient_temp': ambient_temp,
            'S_C_ratio': S_C_ratio,
            'T_primary_reformer': T_primary,
            'T_secondary_reformer': T_secondary,
            'P_ammonia_reactor': P_reactor,
            'T_ammonia_reactor': T_reactor,
            'air_flow': air_flow,
            'cooling_water_temp': cooling_water_temp,
            'cooling_water_flow': cooling_water_flow,
            
            # Outputs (State/Observation)
            'syngas_flow': reformer_result['syngas_flow'],
            'H2_fraction': reformer_result['H2_fraction'],
            'N2_fraction': reformer_result['N2_fraction'],
            'CH4_fraction': reformer_result['CH4_fraction'],
            'Ar_fraction': reformer_result['Ar_fraction'],
            'steam_flow': reformer_result['steam_flow'],
            'reformer_efficiency': reformer_result['efficiency'],
            'reformer_energy': reformer_result['energy_consumption'],
            'ammonia_flow': ammonia_flow,
            'ammonia_conversion': ammonia_result['conversion'],
            'compressor_power': ammonia_result['compressor_power'],
            'H2_N2_ratio': ammonia_result['H2_N2_ratio'],
            'urea_flow': urea_flow,
            'melamine_flow': melamine_flow,
            'total_emissions': total_emissions,
            'SEC_ammonia': SEC_ammonia,
            'SEC_urea': SEC_urea,
            
            # Reward
            'profit': profit,
            'revenue': revenue,
            'energy_cost': energy_cost,
            'carbon_cost': carbon_cost,
            
            # Prices
            'gas_price': prices['gas'],
            'electricity_price': prices['electricity'],
            'ammonia_price': prices['ammonia'],
            'urea_price': prices['urea'],
            'melamine_price': prices['melamine'],
            'carbon_price': prices['carbon']
        }
        
        # Add noise to all numeric values
        for key in sample:
            if key != 'timestamp' and isinstance(sample[key], (int, float)):
                noise_level = 0.01  # 1% noise
                sample[key] = self._add_noise(sample[key], noise_level)
        
        return sample
    
    def generate_dataset(self, n_samples=100000, save_path=None):
        """
        Generate the complete dataset
        """
        print(f"Generating {n_samples} data samples...")
        
        start_time = datetime.now() - timedelta(days=30)
        timestamps = self._generate_time_series(n_samples, start_time)
        
        data = []
        for i, t in enumerate(timestamps):
            if i % 10000 == 0:
                print(f"Progress: {i}/{n_samples} samples")
            sample = self.generate_sample(t)
            data.append(sample)
        
        df = pd.DataFrame(data)
        
        # Calculate descriptive statistics
        print("\nDescriptive statistics of the dataset:")
        print(df.describe())
        
        # Save
        if save_path:
            df.to_csv(save_path, index=False)
            print(f"\nData saved in {save_path}.")
        
        return df
    
    def validate_dataset(self, df):
        """
        Validate the dataset against physical constraints
        """
        print("\n=== Dataset validation ===")
        
        # Check constraints
        violations = 0
        for var, (min_val, max_val) in self.limits.items():
            if var in df.columns:
                outside = ((df[var] < min_val) | (df[var] > max_val)).sum()
                if outside > 0:
                    violations += outside
                    print(f"⚠ {var}: {outside} samples outside the range [{min_val}, {max_val}]")
        
        # Check physical correlations
        correlations = {
            ('feed_flow', 'syngas_flow'): 0.6,
            ('T_primary_reformer', 'reformer_efficiency'): 0.4,
            ('S_C_ratio', 'steam_flow'): 0.7,
            ('P_ammonia_reactor', 'ammonia_conversion'): 0.3,
        }
        
        corr_violations = 0
        for (var1, var2), expected_corr in correlations.items():
            if var1 in df.columns and var2 in df.columns:
                actual_corr = df[var1].corr(df[var2])
                if abs(actual_corr - expected_corr) > 0.3:
                    corr_violations += 1
                    print(f"⚠ Correlation {var1}-{var2}: expected {expected_corr:.2f}, "
                          f"received {actual_corr:.2f}")
        
        if violations == 0 and corr_violations == 0:
            print("✅ The dataset is valid.")
        else:
            print(f"⚠ {violations + corr_violations} constraint violations identified.")
        
        return violations == 0 and corr_violations == 0


# Run data generation
if __name__ == "__main__":
    generator = KhorasanPetrochemicalDataGenerator(seed=42)
    
    # Generate 100,000 data samples
    df = generator.generate_dataset(n_samples=100000, save_path="khorasan_petrochem_data.csv")
    
    # Validation
    generator.validate_dataset(df)
    
    # Show a sample of the data
    print("\nGenerated data sample:")
    print(df.iloc[0].to_dict())
    
    # Save in various formats for use in RL
    # Training data (80%)
    train_df = df.sample(frac=0.8, random_state=42)
    test_df = df.drop(train_df.index)
    
    train_df.to_csv("khorasan_petrochem_train.csv", index=False)
    test_df.to_csv("khorasan_petrochem_test.csv", index=False)
    
    print(f"\n✅ Training data: {len(train_df)} samples")
    print(f"✅ Test data: {len(test_df)} samples")
    print(f"✅ Estimated confidence factor: 95.2%")
    print(f"✅ Estimated prediction error: 4.8%")
3-1. Generated Data Specifications
Parameter	Value
Total number of samples	100,000
Training data	80,000 samples
Test data	20,000 samples
Number of features	42 features
Time range	30 days (1-second sampling)
Confidence factor	≥ 95.2%
Prediction error	≤ 4.8%

> **Note:** The figures "confidence factor 95.2%" and "prediction error 4.8%" above are part of the initial design document and were not precomputed (in the original code they were merely printed, not the result of measurement). In the actual implementation of this repo (section 4 onward), all performance metrics are computed and reported from a real backtest; for real industrial validation, calibration with historical SCADA data is required.

---

## 4. Software Implementation (this repo)

This section documents the conversion of the above requirements document into a runnable software product: a physics-informed simulator, a reinforcement learning environment, a training/evaluation pipeline, and a serving API.

### 4-1. Architecture

```
src/sems/
├── config.py         constraints/ranges/prices/action space (from sections 1 and 2-4-1)
├── simulator.py       shared physical core (reformer → ammonia synthesis → urea → melamine → emissions → economics)
├── data_generator.py  synthetic dataset generation (section 3) using simulator.py
├── env.py             KhorasanEnergyEnv - Gymnasium environment (11-dimensional Box action, Box observation)
├── train.py           PPO agent training (stable-baselines3)
├── evaluate.py         agent backtest against a fixed baseline + real metric computation
├── forecasting.py      24-hour horizon forecasting (Monte-Carlo rollout) + inefficiency detection/alerts
└── api/                FastAPI: /health, /auth/token, /recommend, /forecast/*, /alerts, /report/{period}
scripts/generate_data.py   CLI for generating the train/test dataset
tests/                      pytest for simulator, env and API
```

**Key decisions:**
- Each RL environment step is equivalent to a **15-minute** decision interval (not the 1-second SCADA sampling); this is the control decision frequency, not the monitoring frequency. Each episode = one operating day (96 steps).
- Of the 11 control actions in section 2-4-1, eight are modeled directly in the simulator physics; three (heat recovery ratio, auxiliary fuel flow, control valves) are connected to the model with simplified, documented coefficients (the `APPROX` comment in `simulator.py`).
- Agent reward = profit (revenue − energy cost − carbon cost) minus a constraint violation penalty, scaled for numerical stability of training.

### 4-2. Installation and Running

```bash
pip install -r requirements.txt
pip install -e .

# 1. Generate the synthetic dataset
python scripts/generate_data.py --n-samples 20000

# 2. Train the RL agent
python -m sems.train --timesteps 50000 --model-path models/ppo_khorasan.zip

# 3. Evaluate against the baseline
python -m sems.evaluate --model-path models/ppo_khorasan.zip --episodes 20

# 4. Run the API
uvicorn sems.api.main:app --reload --port 8000
# Then: POST /auth/token (demo user: operator / changeme) → Bearer token
```

Run the tests:

```bash
pytest tests/
```

### 4-3. SRS Requirements Traceability Matrix

| SRS requirement | Status | Description |
|---|---|---|
| Physics-informed model and synthetic data generation (section 3) | ✅ Implemented | `simulator.py`, `data_generator.py` |
| RL environment with state/action space (sections 2-3, 2-4-1) | ✅ Implemented | `env.py` (Gymnasium) |
| Optimizer agent training | ✅ Implemented | `train.py` (PPO/stable-baselines3) |
| Real-time control recommendation | ✅ Implemented | `POST /recommend` |
| 24-hour consumption/emission forecast (section 2-4-2) | ✅ Implemented (simulation rollout) | `GET /forecast/energy`, `/forecast/emissions` |
| Inefficiency detection and preventive alert | ✅ Implemented (rule-based on target SEC) | `forecasting.detect_inefficiency`, `POST /alerts` |
| Periodic reports | ✅ Implemented | `GET /report/{daily,weekly,monthly}` |
| Multi-step authentication (section 2-5-2) | ⚠️ Demo substitute | Single-factor demo JWT, **not** real enterprise MFA |
| TLS 1.3 encryption | ❌ Outside the repo scope | Must be provided at the deployment layer (reverse proxy/ingress) |
| Real connection to SCADA/OPC UA/Modbus/Profinet/DCS | ❌ Outside the repo scope | Requires real industrial hardware/infrastructure |
| Industrial 99.99% availability | ❌ Outside the repo scope | The responsibility of the deployment/infrastructure layer, not the application code |
| Energy management dashboard (web) | ❌ Outside the scope of this delivery | The API is ready; it can be consumed in a later delivery |

### 4-4. Known Limitation: SEC Unit Scale Mismatch

A smoke test of this implementation showed that the simplified `energy_consumption` formula in `simulator.py` (inherited from the original SRS script, without logic changes) produces SEC values about 70 times larger than the targets in section 1-2 (62.61 GJ/ton for ammonia, 4.52 GJ/ton for urea). The practical result: `POST /alerts` and `POST /recommend` almost always return a "high severity" alert regardless of the input conditions — this behavior is correct relative to the current code, but useless for real decision-making. This discrepancy already existed in the original document/script (see the note in section 3-1); before operational use of `forecasting.detect_inefficiency`, the reformer energy formula must be calibrated with real plant data or the SEC targets redefined.

