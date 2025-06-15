"""
This module implements anomaly detection on entropy values and visualizes the results.
It uses a z-score based approach to detect anomalies in the entropy time series.
"""

import numpy as np
import json
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def detect_anomalies(data, z_threshold=2.0):
    """
    Detect anomalies in a time series using z-scores.
    
    Args:
        data: List of numerical values to analyze
        z_threshold: Number of standard deviations to consider as anomaly (default: 2.0)
    
    Returns:
        List of tuples containing (index, value) for detected anomalies
    """
    if len(data) < 2:  # Need at least 2 points for std
        return []
    
    # Calculate z-scores
    mean = np.mean(data)
    std = np.std(data)
    if std == 0:  # If all values are the same
        return []
    
    z_scores = [(x - mean) / std for x in data]
    
    # Find anomalies
    anomalies = []
    for i, z_score in enumerate(z_scores):
        if abs(z_score) > z_threshold:
            anomalies.append((i, data[i]))
    
    return anomalies

def analyze_user_entropy_anomalies(user_id, feature_type):
    """
    Analyze a user's entropy values for anomalies.
    
    Args:
        user_id: The ID of the user to analyze
        feature_type: The type of feature to analyze
    
    Returns:
        Dictionary containing analysis results
    """
    # Get the path to the extracted_features directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    features_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'extracted_features')
    filepath = os.path.join(features_dir, 'entropy_results.json')
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Entropy results file not found at {filepath}")
    
    with open(filepath, 'r') as f:
        all_results = json.load(f)
    
    if feature_type not in all_results:
        raise KeyError(f"Feature type {feature_type} not found in entropy results")
    
    if user_id not in all_results[feature_type]:
        raise KeyError(f"User {user_id} not found in entropy results for {feature_type}")
    
    user_data = all_results[feature_type][user_id]
    values = user_data['entropies']
    
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

def analyze_all_users_entropy_anomalies(feature_type):
    """
    Analyze all users' entropy values for anomalies.
    
    Args:
        feature_type: The type of feature to analyze
    
    Returns:
        Dictionary mapping user IDs to their analysis results
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    features_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'extracted_features')
    filepath = os.path.join(features_dir, 'entropy_results.json')
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Entropy results file not found at {filepath}")
    
    with open(filepath, 'r') as f:
        all_results = json.load(f)
    
    if feature_type not in all_results:
        raise KeyError(f"Feature type {feature_type} not found in entropy results")
    
    results = {}
    
    for user_id in all_results[feature_type].keys():
        try:
            results[user_id] = analyze_user_entropy_anomalies(user_id, feature_type)
        except Exception as e:
            print(f"Error analyzing user {user_id}: {str(e)}")
    
    return results

def plot_entropy_with_anomalies(user_id, feature_type, entropy_data, anomaly_data):
    """
    Create a plot of entropy over time with highlighted anomalies.
    
    Args:
        user_id: The ID of the user
        feature_type: The type of feature being analyzed
        entropy_data: List of entropy values
        anomaly_data: List of anomaly indices and values
    """
    # Create dates for x-axis (assuming data starts from 2025-06-02)
    start_date = datetime(2025, 6, 2)
    dates = [start_date + timedelta(days=i) for i in range(len(entropy_data))]
    
    # Create the plot
    plt.figure(figsize=(12, 6))
    
    # Plot entropy values
    plt.plot(dates, entropy_data, 'b-', label='Entropy')
    
    # Plot anomalies
    anomaly_indices = [a['index'] for a in anomaly_data]
    anomaly_values = [a['value'] for a in anomaly_data]
    plt.scatter([dates[i] for i in anomaly_indices], anomaly_values, 
                color='red', s=100, label='Anomalies', zorder=5)
    
    # Customize the plot
    plt.title(f'Entropy Over Time for {user_id} - {feature_type}')
    plt.xlabel('Date')
    plt.ylabel('Entropy')
    plt.legend()
    plt.grid(True)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the plot
    current_dir = os.path.dirname(os.path.abspath(__file__))
    features_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'extracted_features')
    plots_dir = os.path.join(features_dir, 'entropy_plots')
    os.makedirs(plots_dir, exist_ok=True)
    
    plot_file = os.path.join(plots_dir, f'{user_id}_{feature_type}_entropy.png')
    plt.savefig(plot_file)
    plt.close()

def save_anomaly_results(all_results):
    """
    Save anomaly analysis results to a file.
    
    Args:
        all_results: Dictionary containing all feature type results
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    features_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'extracted_features')
    output_file = os.path.join(features_dir, 'anomaly_results.json')
    
    # Save results, overwriting any existing file
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2)

if __name__ == '__main__':
    # Analyze anomalies for different feature types
    feature_types = ['time_of_day', 'log_types', 'text_similarity', 'response_latency']
    all_results = {}
    
    # Load entropy results for plotting
    current_dir = os.path.dirname(os.path.abspath(__file__))
    features_dir = os.path.join(os.path.dirname(os.path.dirname(current_dir)), 'extracted_features')
    entropy_file = os.path.join(features_dir, 'entropy_results.json')
    
    with open(entropy_file, 'r') as f:
        entropy_results = json.load(f)
    
    for feature_type in feature_types:
        print(f"Analyzing anomalies for {feature_type}...")
        results = analyze_all_users_entropy_anomalies(feature_type)
        all_results[feature_type] = results
        
        # Create plots for each user
        for user_id, analysis in results.items():
            entropy_data = entropy_results[feature_type][user_id]['entropies']
            plot_entropy_with_anomalies(user_id, feature_type, entropy_data, analysis['anomalies'])
        
        print(f"Completed analysis and plotting for {feature_type}")
    
    # Save all results at once
    save_anomaly_results(all_results)
    print("\nAll analyses completed. Results saved to anomaly_results.json")
    print("Plots saved in extracted_features/entropy_plots/") 