import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

def plot_entropy_with_anomalies(user_id, feature_type, entropy_data, anomaly_data):
    # X-axis: message/entry count instead of dates
    entry_indices = list(range(1, len(entropy_data) + 1))
    plt.figure(figsize=(12, 6))
    plt.plot(entry_indices, entropy_data, 'b-', label='Entropy')
    anomaly_indices = [a['index'] for a in anomaly_data]
    anomaly_values = [a['value'] for a in anomaly_data]
    plt.scatter([entry_indices[i] for i in anomaly_indices], anomaly_values, 
                color='red', s=100, label='Anomalies', zorder=5)
    plt.title(f'Entropy per Entry for {user_id} - {feature_type}')
    plt.xlabel('Entry Number')
    plt.ylabel('Entropy')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    features_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))), 'extracted_features')
    plots_dir = os.path.join(features_dir, 'entropy_plots')
    os.makedirs(plots_dir, exist_ok=True)
    plot_file = os.path.join(plots_dir, f'{user_id}_{feature_type}_entropy.png')
    plt.savefig(plot_file)
    plt.close() 