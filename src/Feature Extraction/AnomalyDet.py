"""
This module implements a simple threshold-based anomaly detection method.
It uses a sliding window approach with a threshold of 1.5 times the window size
to detect anomalies in time series data.
"""

import numpy as np
import json
import os

def detect_anomalies(data: list[float], window_size: int = 10, threshold_multiplier: float = 1.5) -> list[tuple[int, float]]:
    """
    Detect anomalies in a time series using a sliding window approach.
    
    Args:
        data: List of numerical values to analyze
        window_size: Size of the sliding window (default: 10)
        threshold_multiplier: Multiplier for the threshold (default: 1.5)
    
    Returns:
        List of tuples containing (index, value) for detected anomalies
    """
    if len(data) < window_size:
        return []
    
    anomalies = []
    threshold = window_size * threshold_multiplier
    
    for i in range(len(data) - window_size + 1):
        window = data[i:i + window_size]
        window_mean = np.mean(window)
        window_std = np.std(window)
        
        # Check if the current value is an anomaly
        current_value = data[i + window_size - 1]
        if abs(current_value - window_mean) > threshold:
            anomalies.append((i + window_size - 1, current_value))
    
    return anomalies

def analyze_user_features(user_id: str, feature_type: str = 'glucose_values') -> dict:
    """
    Analyze a user's features for anomalies.
    
    Args:
        user_id: The ID of the user to analyze
        feature_type: The type of feature to analyze (default: 'glucose_values')
    
    Returns:
        Dictionary containing analysis results
    """
    # Get the path to the extracted_features directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    features_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'extracted_features')
    filepath = os.path.join(features_dir, 'extracted_features.json')
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Features file not found at {filepath}")
    
    with open(filepath, 'r') as f:
        all_features = json.load(f)
    
    if user_id not in all_features:
        raise KeyError(f"User {user_id} not found in features file")
    
    user_data = all_features[user_id]
    
    # Get the raw values for the specified feature type
    if feature_type == 'glucose_values':
        values = user_data['raw']['glucose_values']
    else:
        raise ValueError(f"Unsupported feature type: {feature_type}")
    
    if not values:
        return {
            'user_id': user_id,
            'feature_type': feature_type,
            'anomalies': [],
            'total_points': 0,
            'anomaly_count': 0
        }
    
    # Detect anomalies
    anomalies = detect_anomalies(values)
    
    # Prepare results
    results = {
        'user_id': user_id,
        'feature_type': feature_type,
        'anomalies': [
            {
                'index': idx,
                'value': val
            }
            for idx, val in anomalies
        ],
        'total_points': len(values),
        'anomaly_count': len(anomalies)
    }
    
    return results

def analyze_all_users(feature_type: str = 'glucose_values') -> dict[str, dict]:
    """
    Analyze all users' features for anomalies.
    
    Args:
        feature_type: The type of feature to analyze (default: 'glucose_values')
    
    Returns:
        Dictionary mapping user IDs to their analysis results
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    features_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'extracted_features')
    filepath = os.path.join(features_dir, 'extracted_features.json')
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Features file not found at {filepath}")
    
    with open(filepath, 'r') as f:
        all_features = json.load(f)
    
    results = {}
    
    for user_id in all_features.keys():
        try:
            results[user_id] = analyze_user_features(user_id, feature_type)
        except Exception as e:
            print(f"Error analyzing user {user_id}: {str(e)}")
    
    return results

if __name__ == '__main__':
    # Example usage
    results = analyze_all_users()
    
    # Print results
    for user_id, analysis in results.items():
        print(f"\nUser: {user_id}")
        print(f"Total data points: {analysis['total_points']}")
        print(f"Number of anomalies detected: {analysis['anomaly_count']}")
        if analysis['anomalies']:
            print("Anomalies:")
            for anomaly in analysis['anomalies']:
                print(f"  Index: {anomaly['index']}, Value: {anomaly['value']}") 