import pandas as pd
import os
from datetime import datetime

LOG_FILE = "smart_home_log.csv"

def log_data(sensor_data, utility_scores, selected_action, explanation):
    """
    Logs sensor inputs, utilities, and decisions to a CSV file.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Flatten the data for CSV
    log_entry = {
        "Timestamp": timestamp,
        "Temperature": sensor_data["temperature"],
        "Motion": sensor_data["motion"],
        "Time": sensor_data["time"],
        "EnergyCost": sensor_data["energy_cost"],
        "LightIntensity": sensor_data["light_intensity"],
        "Action": selected_action,
        "RuleExplanation": explanation,
        "AI_Explanation": sensor_data.get("ai_explanation", ""),
        "Reward": sensor_data.get("reward", 0)
    }
    
    # Add each action's utility score
    for action, score in utility_scores.items():
        log_entry[f"U_{action}"] = round(score, 2)
        
    df = pd.DataFrame([log_entry])
    
    if not os.path.isfile(LOG_FILE):
        df.to_csv(LOG_FILE, index=False)
    else:
        df.to_csv(LOG_FILE, mode='a', header=False, index=False)

def get_history_df():
    """
    Returns the history as a pandas DataFrame.
    """
    if not os.path.isfile(LOG_FILE):
        return pd.DataFrame()
    return pd.read_csv(LOG_FILE)

def archive_logs():
    """
    Archives the current log file instead of deleting it.
    """
    if os.path.isfile(LOG_FILE):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"archive_{timestamp}.csv"
        os.rename(LOG_FILE, archive_name)
        return archive_name
    return None
