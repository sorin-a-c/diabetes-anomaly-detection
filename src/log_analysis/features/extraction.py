import json
import os
import numpy as np
from .helpers import (
    get_time_of_day_category,
    discretize_logging_frequency,
    discretize_text_similarity,
    calculate_logging_frequency,
    calculate_text_similarity
)

def extract_user_features():
    """
    Read all synthetic log files and extract features for each user.
    Returns a dictionary where keys are persona titles and values are feature dictionaries.
    """
    # Get the path to the synthetic_logs directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))), 'synthetic_logs')
    
    # Dictionary to store features for each user
    user_features = {}
    
    # Recursively search for log files in all subdirectories
    def aggregate_by_date(entries):
        agg = {}
        for entry in entries:
            date = entry["date"]
            value = entry["value"]
            if date not in agg:
                agg[date] = []
            agg[date].append(value)
        return agg
    for root, dirs, files in os.walk(logs_dir):
        for filename in files:
            if filename.endswith('_logs.json'):
                # Extract persona title from filename
                persona_title = filename.replace('_logs.json', '')
                
                # Read the log file
                with open(os.path.join(root, filename), 'r') as f:
                    logs = json.load(f)
                
                # Sort logs by timestamp
                logs.sort(key=lambda x: x['timestamp'])
                
                # Calculate features with date association
                time_of_day = [
                    {"date": log["timestamp"].split(" ")[0], "value": get_time_of_day_category(log["timestamp"])}
                    for log in logs
                ]
                log_types = [
                    {"date": log["timestamp"].split(" ")[0], "value": log["log_type"]}
                    for log in logs
                ]
                text_similarities_raw = calculate_text_similarity(logs)
                text_similarities = [
                    {"date": logs[i]["timestamp"].split(" ")[0], "value": text_similarities_raw[i]}
                    for i in range(len(text_similarities_raw))
                ] if text_similarities_raw else []
                
                # Calculate logging frequency
                logging_frequency = calculate_logging_frequency(logs)
                
                # Discretize numerical features
                discretized_frequency = {
                    date: discretize_logging_frequency(count)
                    for date, count in logging_frequency.items()
                }
                discretized_similarities = aggregate_by_date([
                    {"date": entry["date"], "value": discretize_text_similarity(entry["value"])}
                    for entry in text_similarities
                ]) if text_similarities else {}
                
                # Aggregate features by date, storing all values per date in a list
                time_of_day_dict = aggregate_by_date(time_of_day)
                log_types_dict = aggregate_by_date(log_types)
                
                # Store only discretized features with date, all as dicts {date: value}
                features = {
                    'time_of_day': time_of_day_dict,
                    'logging_frequency': discretized_frequency,
                    'log_types': log_types_dict,
                    'text_similarity': discretized_similarities
                }
                
                user_features[persona_title] = features
    
    return user_features 