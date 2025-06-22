import numpy as np
import json
import os

def detect_anomalies(data, z_threshold=2.0):
    # ... (same as in AnomalyDet.py)
    if len(data) < 2:
        return []
    mean = np.mean(data)
    std = np.std(data)
    if std == 0:
        return []
    z_scores = [(x - mean) / std for x in data]
    anomalies = []
    for i, z_score in enumerate(z_scores):
        if abs(z_score) > z_threshold:
            anomalies.append((i, data[i]))
    return anomalies

def analyze_user_entropy_anomalies(user_id, feature_type):
    # ... (same as in AnomalyDet.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    features_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))), 'extracted_features')
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
    anomalies = detect_anomalies(values)
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
    # ... (same as in AnomalyDet.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    features_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))), 'extracted_features')
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

def save_anomaly_results(all_results):
    # ... (same as in AnomalyDet.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    features_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))), 'extracted_features')
    output_file = os.path.join(features_dir, 'anomaly_results.json')
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2) 