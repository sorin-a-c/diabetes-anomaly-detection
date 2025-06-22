import numpy as np
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
import os

def calculate_entropy(values):
    # ... (same as in EntropyCalc.py)
    if not values:
        return 0.0
    counts = Counter(values)
    total = len(values)
    entropy = 0.0
    for count in counts.values():
        probability = count / total
        entropy -= probability * np.log2(probability)
    return entropy

def group_data_by_day(data, timestamps, logs=None):
    """
    Group data by day. If logs are provided, group all log entries by their date.
    Returns a dict: {date: [values or logs]}
    """
    grouped_data = defaultdict(list)
    if logs is not None:
        # Group all log entries by date
        for log in logs:
            date = datetime.fromisoformat(log['timestamp']).date().isoformat()
            grouped_data[date].append(log)
    else:
        # Group feature values by date
        for value, timestamp in zip(data, timestamps):
            date = datetime.fromisoformat(timestamp).date().isoformat()
            grouped_data[date].append(value)
    return dict(grouped_data)

def calculate_window_entropy(data, timestamps, window_size=10):
    # ... (same as in EntropyCalc.py)
    if not data:
        return []
    grouped_data = group_data_by_day(data, timestamps)
    dates = sorted(grouped_data.keys())
    entropies = []
    for i in range(window_size - 1, len(dates)):
        window_dates = dates[i - window_size + 1:i + 1]
        window_values = []
        for date in window_dates:
            window_values.extend(grouped_data[date])
        entropy = calculate_entropy(window_values)
        entropies.append(entropy)
    return entropies

def analyze_user_entropy(user_id, feature_type, all_features=None):
    # ... (same as in EntropyCalc.py)
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    if all_features is None:
        features_dir = base_dir / 'extracted_features'
        features_path = features_dir / 'extracted_features.json'
        if not features_path.exists():
            raise FileNotFoundError(f"Features file not found at {features_path}")
        with open(features_path, 'r') as f:
            all_features = json.load(f)
    if user_id not in all_features:
        raise KeyError(f"User {user_id} not found in features file")
    user_data = all_features[user_id]
    if feature_type not in user_data:
        raise ValueError(f"Unsupported feature type: {feature_type}")
    values = user_data[feature_type]
    # Flatten dict of lists (per date) into a single list of values, preserving date order
    if isinstance(values, dict):
        all_values = []
        for date in sorted(values.keys()):
            v = values[date]
            if isinstance(v, list):
                all_values.extend(v)
            else:
                all_values.append(v)
        values = all_values
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
    logs_dir = base_dir / 'synthetic_logs'
    # Recursively search for the log file in all subdirectories
    log_file = None
    for root, dirs, files in os.walk(logs_dir):
        for filename in files:
            if filename == f'{user_id}_logs.json':
                log_file = Path(root) / filename
                break
        if log_file:
            break
    if not log_file or not log_file.exists():
        raise FileNotFoundError(f"Log file not found for user {user_id} in {logs_dir} or its subdirectories")
    with open(log_file, 'r') as f:
        logs = json.load(f)
    timestamps = [log['timestamp'] for log in logs]
    entropies = calculate_window_entropy(values, timestamps, window_size=10)
    results = {
        'user_id': user_id,
        'feature_type': feature_type,
        'entropies': entropies,
        'total_days': len(entropies),
        'mean_entropy': float(np.mean(entropies)) if entropies else 0.0,
        'max_entropy': float(np.max(entropies)) if entropies else 0.0,
        'min_entropy': float(np.min(entropies)) if entropies else 0.0
    }
    return results

def analyze_all_users_entropy(feature_type):
    # ... (same as in EntropyCalc.py)
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    features_dir = base_dir / 'extracted_features'
    features_path = features_dir / 'extracted_features.json'
    if not features_path.exists():
        raise FileNotFoundError(f"Features file not found at {features_path}")
    with open(features_path, 'r') as f:
        all_features = json.load(f)
    results = {}
    for user_id in all_features.keys():
        try:
            results[user_id] = analyze_user_entropy(user_id, feature_type, all_features=all_features)
        except Exception as e:
            print(f"Error analyzing user {user_id}: {str(e)}")
    return results

def save_entropy_results(all_results):
    # ... (same as in EntropyCalc.py)
    base_dir = Path(__file__).resolve().parent.parent.parent.parent
    features_dir = base_dir / 'extracted_features'
    output_file = features_dir / 'entropy_results.json'
    with open(output_file, 'w') as f:
        json.dump(all_results, f, indent=2) 