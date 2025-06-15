"""
This script extracts features from the synthetic log files and saves them to a JSON file.
"""

import json
import os
import numpy as np
from utils.feature_helpers import (
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
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'synthetic_logs')
    
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
            
            # Calculate features
            time_of_day = [get_time_of_day_category(log['timestamp']) for log in logs]
            logging_frequency = calculate_logging_frequency(logs)
            log_types = [log['log_type'] for log in logs]
            text_similarities = calculate_text_similarity(logs)
            response_latencies = calculate_response_latency(logs)
            
            # Discretize numerical features
            discretized_frequency = {
                date: discretize_logging_frequency(count) 
                for date, count in logging_frequency.items()
            }
            
            discretized_latencies = [
                discretize_response_latency(latency) 
                for latency in response_latencies
            ] if response_latencies else []
            
            discretized_similarities = [
                discretize_text_similarity(similarity) 
                for similarity in text_similarities
            ] if text_similarities else []
            
            # Store only discretized features
            features = {
                'time_of_day': time_of_day,  # Already categorical
                'logging_frequency': discretized_frequency,
                'log_types': log_types,  # Already categorical
                'text_similarity': discretized_similarities,
                'response_latency': discretized_latencies
            }
            
            user_features[persona_title] = features
    
    return user_features

if __name__ == '__main__':
    # Get features for all users
    features_by_user = extract_user_features()
    
    # Save features to JSON file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'extracted_features')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'extracted_features.json')
    with open(output_file, 'w') as f:
        json.dump(features_by_user, f, indent=2)
    
    print(f"\nFeatures have been saved to: {output_file}")
    
    # Print results
    for persona, features in features_by_user.items():
        print(f"\nPersona: {persona}")
        for feature_type, values in features.items():
            if isinstance(values, list):
                print(f"  {feature_type}: {len(values)} values")
            else:
                print(f"  {feature_type}: {values}")