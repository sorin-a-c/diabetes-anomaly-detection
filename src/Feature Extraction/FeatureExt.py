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
    discretize_glucose_value,
    calculate_logging_frequency,
    calculate_text_similarity,
    calculate_response_latency
)

def extract_user_features():
    """
    Read all synthetic log files and extract features for each user.
    Returns a dictionary where keys are usernames and values are feature dictionaries.
    """
    # Get the path to the synthetic_logs directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'synthetic_logs')
    
    # Dictionary to store features for each user
    user_features = {}
    
    # Read each log file
    for filename in os.listdir(logs_dir):
        if filename.endswith('_logs.json'):
            # Extract username from filename
            username = filename.replace('sim_user_', '').replace('_logs.json', '')
            
            # Read the log file
            with open(os.path.join(logs_dir, filename), 'r') as f:
                logs = json.load(f)
            
            # Sort logs by timestamp
            logs.sort(key=lambda x: x['timestamp'])
            
            # Calculate raw features
            time_of_day = [get_time_of_day_category(log['timestamp']) for log in logs]
            logging_frequency = calculate_logging_frequency(logs)
            log_types = [log['log_type'] for log in logs]
            text_similarities = calculate_text_similarity(logs)
            response_latencies = calculate_response_latency(logs)
            glucose_values = [log.get('glucose_mgdl') for log in logs if log.get('glucose_mgdl') is not None]
            
            # Discretize numerical features
            avg_logs_per_day = np.mean(list(logging_frequency.values()))
            discretized_frequency = discretize_logging_frequency(avg_logs_per_day)
            
            discretized_latencies = [
                discretize_response_latency(latency) 
                for latency in response_latencies
            ] if response_latencies else []
            
            discretized_similarities = [
                discretize_text_similarity(similarity) 
                for similarity in text_similarities
            ] if text_similarities else []
            
            discretized_glucose = [
                discretize_glucose_value(glucose) 
                for glucose in glucose_values
            ] if glucose_values else []
            
            # Store both raw and discretized features
            features = {
                'raw': {
                    'time_of_day': time_of_day,
                    'logging_frequency': logging_frequency,
                    'log_types': log_types,
                    'text_similarity': text_similarities,
                    'response_latency': response_latencies,
                    'glucose_values': glucose_values
                },
                'discretized': {
                    'time_of_day': time_of_day,  # Already categorical
                    'logging_frequency': discretized_frequency,
                    'log_types': log_types,  # Already categorical
                    'text_similarity': discretized_similarities,
                    'response_latency': discretized_latencies,
                    'glucose_values': discretized_glucose
                }
            }
            
            # Add summary statistics
            features['summary'] = {
                'total_logs': len(logs),
                'avg_logs_per_day': avg_logs_per_day,
                'avg_response_latency': np.mean(response_latencies) if response_latencies else 0,
                'avg_text_similarity': np.mean(text_similarities) if text_similarities else 0,
                'time_of_day_distribution': {
                    category: time_of_day.count(category) / len(time_of_day)
                    for category in ['morning', 'afternoon', 'evening', 'night']
                },
                'log_type_distribution': {
                    log_type: log_types.count(log_type) / len(log_types)
                    for log_type in set(log_types)
                },
                'discretized_distributions': {
                    'logging_frequency': discretized_frequency,
                    'response_latency': {
                        category: discretized_latencies.count(category) / len(discretized_latencies)
                        for category in ['very_quick', 'quick', 'moderate', 'slow', 'very_slow']
                    } if discretized_latencies else {},
                    'text_similarity': {
                        category: discretized_similarities.count(category) / len(discretized_similarities)
                        for category in ['very_different', 'different', 'similar', 'very_similar']
                    } if discretized_similarities else {},
                    'glucose_values': {
                        category: discretized_glucose.count(category) / len(discretized_glucose)
                        for category in ['very_low', 'low', 'normal', 'high', 'very_high']
                    } if discretized_glucose else {}
                }
            }
            
            user_features[username] = features
    
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
    for user, features in features_by_user.items():
        print(f"\nUser: {user}")
        print("Summary Statistics:")
        for metric, value in features['summary'].items():
            if isinstance(value, dict):
                print(f"  {metric}:")
                for submetric, subvalue in value.items():
                    print(f"    {submetric}: {subvalue}")
            else:
                print(f"  {metric}: {value}")