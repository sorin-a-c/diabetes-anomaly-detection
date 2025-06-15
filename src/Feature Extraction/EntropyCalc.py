"""
This module calculates entropy per day based on historical data.
Each day's entropy is calculated using a sliding window of the last 10 days.
"""

import numpy as np
import json
import os
from collections import Counter

def calculate_entropy(values):
    """
    Calculate the entropy of a list of values.
    
    Args:
        values: List of values to calculate entropy for
        
    Returns:
        float: The entropy value
    """
    if not values:
        return 0.0
    
    # Count occurrences of each value
    counts = Counter(values)
    total = len(values)
    
    # Calculate probabilities and entropy
    entropy = 0.0
    for count in counts.values():
        probability = count / total
        entropy -= probability * np.log2(probability)
    
    return entropy

def calculate_window_entropy(data, window_size=10):
    """
    Calculate entropy using a sliding window approach.
    Only includes entropy values when window has at least 5 days of data.
    
    Args:
        data: List of values to analyze
        window_size: Size of the sliding window (default: 10 days)
        
    Returns:
        List of entropy values, starting from the first day with sufficient data (5+ days)
    """
    if not data:
        return []
    
    entropies = []
    # Start from index 4 (5th day) to ensure we have at least 5 days of data
    for i in range(4, len(data)):
        # Get the window of data (up to window_size days before current day)
        start_idx = max(0, i - window_size + 1)
        window_data = data[start_idx:i+1]
        entropy = calculate_entropy(window_data)
        entropies.append(entropy)
    
    return entropies

def calculate_daily_entropy(data):
    """
    Calculate entropy for each day based on a sliding window of historical data.
    
    Args:
        data: List of values to analyze
        
    Returns:
        List of entropy values, one for each day
    """
    return calculate_window_entropy(data, window_size=10)

def analyze_user_entropy(user_id, feature_type):
    """
    Analyze a user's features for entropy patterns.
    
    Args:
        user_id: The ID of the user to analyze
        feature_type: The type of feature to analyze
        
    Returns:
        Dictionary containing entropy analysis results
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
    
    # Get the values for the specified feature type
    if feature_type == 'time_of_day':
        values = user_data['time_of_day']
    elif feature_type == 'log_types':
        values = user_data['log_types']
    elif feature_type == 'text_similarity':
        values = user_data['text_similarity']
    elif feature_type == 'response_latency':
        values = user_data['response_latency']
    else:
        raise ValueError(f"Unsupported feature type: {feature_type}")
    
    if not values:
        return {
            'user_id': user_id,
            'feature_type': feature_type,
            'entropies': [],
            'total_days': 0,
            'mean_entropy': 0.0,
            'max_entropy': 0.0,
            'min_entropy': 0.0
        }
    
    # Calculate entropy for each day
    entropies = calculate_daily_entropy(values)
    
    # Prepare results
    results = {
        'user_id': user_id,
        'feature_type': feature_type,
        'entropies': entropies,
        'total_days': len(entropies),
        'mean_entropy': np.mean(entropies) if entropies else 0.0,
        'max_entropy': np.max(entropies) if entropies else 0.0,
        'min_entropy': np.min(entropies) if entropies else 0.0
    }
    
    return results

def analyze_all_users_entropy(feature_type):
    """
    Analyze all users' features for entropy patterns.
    
    Args:
        feature_type: The type of feature to analyze
        
    Returns:
        Dictionary mapping user IDs to their entropy analysis results
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
            results[user_id] = analyze_user_entropy(user_id, feature_type)
        except Exception as e:
            print(f"Error analyzing user {user_id}: {str(e)}")
    
    return results

def save_entropy_results(all_results):
    """
    Save entropy analysis results to a file.
    
    Args:
        all_results: Dictionary containing all feature type results
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    features_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'extracted_features')
    output_file = os.path.join(features_dir, 'entropy_results.json')
    
    # Save results, overwriting any existing file
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)

if __name__ == '__main__':
    # Analyze entropy for different feature types
    feature_types = ['time_of_day', 'log_types', 'text_similarity', 'response_latency']
    all_results = {}
    
    for feature_type in feature_types:
        print(f"Analyzing entropy for {feature_type}...")
        results = analyze_all_users_entropy(feature_type)
        all_results[feature_type] = results
        print(f"Completed analysis for {feature_type}")
    
    # Save all results at once
    save_entropy_results(all_results)
    print("\nAll entropy analyses completed. Results saved to entropy_results.json") 