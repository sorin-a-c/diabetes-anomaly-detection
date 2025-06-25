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
    # Draw vertical line for transitional personas at transition point, accounting for window size offset
    if user_id.startswith('Transitional_'):
        transition_day = 15
        window_size = 10
        transition_entry = transition_day - window_size + 1  # 6
        if 1 <= transition_entry <= len(entry_indices):
            plt.axvline(x=transition_entry, color='green', linestyle='--', linewidth=2, label='Transition')
        # Highlight the anomaly window (all windows containing the transition day)
        anomaly_start = transition_entry
        anomaly_end = transition_entry + window_size - 1
        anomaly_start = max(anomaly_start, 1)
        anomaly_end = min(anomaly_end, len(entry_indices))
        plt.axvspan(anomaly_start, anomaly_end, color='orange', alpha=0.2, label='Anomaly Window')
        persona_name = user_id.replace('Transitional_', '').replace('_', ' ')
        feature_name = feature_type.replace('_', ' ')
        plot_title = f'Entropy per {feature_name} for {persona_name}'
    else:
        persona_name = user_id.replace('_', ' ')
        feature_name = feature_type.replace('_', ' ')
        plot_title = f'Entropy per {feature_name} for {persona_name}'
    plt.title(plot_title)
    plt.xlabel('Window Number')
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