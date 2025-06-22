import json
import os
import numpy as np
from .helpers import (
    get_time_of_day_category,
    discretize_logging_frequency,
    discretize_response_latency,
    discretize_text_similarity,
    calculate_logging_frequency,
    calculate_text_similarity,
    calculate_response_latency
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
    
    # Read each log file
    for filename in os.listdir(logs_dir):
        if filename.endswith('_logs.json'):
            # Extract persona title from filename
            persona_title = filename.replace('_logs.json', '')
            
            # Read the log file
            with open(os.path.join(logs_dir, filename), 'r') as f:
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
            response_latencies_raw = calculate_response_latency(logs)
            response_latencies = [
                {"date": logs[i]["timestamp"].split(" ")[0], "value": response_latencies_raw[i]}
                for i in range(len(response_latencies_raw))
            ] if response_latencies_raw else []
            
            # Calculate logging frequency
            logging_frequency = calculate_logging_frequency(logs)
            
            # Discretize numerical features
            discretized_frequency = {
                date: discretize_logging_frequency(count) 
                for date, count in logging_frequency.items()
            }
            discretized_latencies = [
                {"date": entry["date"], "value": discretize_response_latency(entry["value"])}
                for entry in response_latencies
            ] if response_latencies else []
            discretized_similarities = [
                {"date": entry["date"], "value": discretize_text_similarity(entry["value"])}
                for entry in text_similarities
            ] if text_similarities else []
            
            # Store only discretized features with date
            features = {
                'time_of_day': time_of_day,  # Now with date
                'logging_frequency': discretized_frequency,  # Already by date
                'log_types': log_types,  # Now with date
                'text_similarity': discretized_similarities,  # Now with date
                'response_latency': discretized_latencies  # Now with date
            }
            
            user_features[persona_title] = features
    
    return user_features 