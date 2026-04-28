import json
import os

WEIGHTS_FILE = "agent_weights.json"

class SmartHomeAgent:
    def __init__(self):
        self.actions = ["Turn ON AC", "Turn ON Fan", "Turn ON Lights", "Turn OFF All Devices"]
        self.weights = self.load_weights()

    def load_weights(self):
        if os.path.exists(WEIGHTS_FILE):
            with open(WEIGHTS_FILE, 'r') as f:
                return json.load(f)
        # Default weights: [Comfort, Energy, Motion, Light]
        return {
            "comfort_w": 0.5,
            "energy_w": 0.3,
            "motion_w": 0.7,
            "light_w": 0.6
        }

    def save_weights(self):
        with open(WEIGHTS_FILE, 'w') as f:
            json.dump(self.weights, f)

    def calculate_utility(self, sensors):
        temp = sensors["temperature"]
        motion = sensors["motion"]
        cost = sensors["energy_cost"]
        light = sensors["light_intensity"]
        
        utilities = {}
        
        # 1. AC Utility (Primarily Temperature and Cost)
        # High utility if hot, low if expensive
        u_ac = (max(0, temp - 24) * self.weights["comfort_w"]) - (cost * 10 * self.weights["energy_w"])
        if not motion: u_ac -= 5 # Drastic reduction if no one is there
        utilities["Turn ON AC"] = u_ac
        
        # 2. Fan Utility (Moderate Temp, cheaper alternative)
        u_fan = (max(0, temp - 21) * self.weights["comfort_w"] * 0.4) - (cost * 2 * self.weights["energy_w"])
        if not motion: u_fan -= 5
        utilities["Turn ON Fan"] = u_fan
        
        # 3. Lights Utility (Light intensity and Motion)
        # High utility if dark and someone is home
        u_lights = (max(0, 500 - light) / 100 * self.weights["light_w"])
        if motion:
            u_lights += 2
        else:
            u_lights -= 10
        utilities["Turn ON Lights"] = u_lights
        
        # 4. Turn OFF Devices Utility (No motion or very high cost)
        u_off = 0
        if not motion:
            u_off += (10 * self.weights["motion_w"])
        u_off += (cost * 20 * self.weights["energy_w"])
        utilities["Turn OFF All Devices"] = u_off
        
        return utilities

    def get_decision(self, sensors):
        utilities = self.calculate_utility(sensors)
        best_action = max(utilities, key=utilities.get)
        explanation = self.generate_explanation(best_action, sensors, utilities)
        
        # Basic Adaptive Behavior: Slightly adjust weights based on successful decisions 
        # (Simulating reinforcement by reinforcing the factors that led to the best action)
        self.adapt_weights(best_action, sensors)
        
        return best_action, utilities, explanation

    def generate_explanation(self, action, sensors, utilities):
        temp = sensors["temperature"]
        motion = sensors["motion"]
        cost = sensors["energy_cost"]
        light = sensors["light_intensity"]
        
        rules = []
        if action == "Turn ON AC":
            rules.append(f"IF Temperature ({temp}°C) > 24 AND Motion is {motion}")
            rules.append(f"THEN AC is prioritized for comfort.")
        elif action == "Turn ON Fan":
            rules.append(f"IF Temperature ({temp}°C) is moderate AND Energy Cost (${cost}) is low")
            rules.append(f"THEN Fan is a cost-effective choice.")
        elif action == "Turn ON Lights":
            rules.append(f"IF Light Intensity ({light} lux) < 500 AND Motion is Detected")
            rules.append(f"THEN Lights are activated for visibility.")
        elif action == "Turn OFF All Devices":
            if not motion:
                rules.append(f"IF No Motion Detected")
                rules.append(f"THEN Power saving mode activated.")
            else:
                rules.append(f"IF Energy Cost (${cost}) is extremely high")
                rules.append(f"THEN Devices turned off to reduce peak load.")
                
        return " | ".join(rules)

    def adapt_weights(self, action, sensors, reward=0):
        """
        Simulates basic reinforcement learning by adjusting weights based on a reward signal.
        Reward > 0: Strengthen the weights that led to this decision.
        Reward < 0: Slightly weaken them.
        """
        lr = 0.005 # Learning rate
        
        if action == "Turn ON AC" or action == "Turn ON Fan":
            # If temp was high, and we turned AC ON, and reward is positive (comfort achieved)
            if sensors["temperature"] > 25:
                self.weights["comfort_w"] = max(0.1, min(1.0, self.weights["comfort_w"] + lr * reward))
            
            # If cost was high, and we still turned AC ON, maybe reduce energy priority if comfort is key
            if sensors["energy_cost"] > 0.3:
                self.weights["energy_w"] = max(0.1, min(1.0, self.weights["energy_w"] - lr * 0.5))

        if action == "Turn OFF All Devices":
            if sensors["energy_cost"] > 0.4:
                self.weights["energy_w"] = max(0.1, min(1.0, self.weights["energy_w"] + lr))
            if not sensors["motion"]:
                self.weights["motion_w"] = max(0.1, min(1.0, self.weights["motion_w"] + lr))
            
        self.save_weights()

    def get_state_summary(self, sensors):
        return f"Temp: {sensors['temperature']}°C, Motion: {sensors['motion']}, Cost: ${sensors['energy_cost']}, Light: {sensors['light_intensity']} lux"
