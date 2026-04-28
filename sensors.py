import random
import numpy as np
from datetime import datetime

def generate_sensor_data():
    """
    Generates realistic smart home sensor data with random fluctuations.
    """
    # Base values
    temp = random.uniform(18.0, 32.0)
    motion = random.choice([True, False, False]) # More likely to be false
    current_hour = datetime.now().hour
    energy_cost = random.uniform(0.1, 0.5) # $/kWh
    light_intensity = random.uniform(50, 1000) # lux (50 is very dark, 1000 is bright daylight)

    # Add Gaussian Noise to simulate real-world uncertainty
    noise_temp = np.random.normal(0, 0.5)
    noise_light = np.random.normal(0, 50)
    noise_energy = np.random.normal(0, 0.02)

    data = {
        "temperature": round(temp + noise_temp, 2),
        "motion": motion,
        "time": current_hour,
        "energy_cost": round(abs(energy_cost + noise_energy), 3),
        "light_intensity": round(abs(light_intensity + noise_light), 1)
    }
    
    return data

def get_manual_data(temp, motion, time, cost, light):
    """
    Applies noise even to manual input to represent sensor calibration errors.
    """
    noise_temp = np.random.normal(0, 0.2)
    noise_light = np.random.normal(0, 20)
    
    return {
        "temperature": round(temp + noise_temp, 2),
        "motion": motion,
        "time": time,
        "energy_cost": cost,
        "light_intensity": round(abs(light + noise_light), 1)
    }
