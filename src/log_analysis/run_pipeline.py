import os
from features.extraction import extract_user_features
from entropy.calculation import analyze_all_users_entropy, save_entropy_results
from anomalies.detection import analyze_all_users_entropy_anomalies, save_anomaly_results
from anomalies.plotting import plot_entropy_with_anomalies
import json


def main():
    # 1. Feature Extraction
    print("[1/4] Extracting features from synthetic logs...")
    features_by_user = extract_user_features()
    features_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'extracted_features')
    os.makedirs(features_dir, exist_ok=True)
    features_file = os.path.join(features_dir, 'extracted_features.json')
    with open(features_file, 'w') as f:
        json.dump(features_by_user, f, indent=2)
    print(f"Features saved to {features_file}")

    # 2. Entropy Calculation
    print("[2/4] Calculating entropy for all users and features...")
    feature_types = ['time_of_day', 'log_types', 'text_similarity', 'response_latency']
    all_entropy_results = {}
    for feature_type in feature_types:
        print(f"  Calculating entropy for {feature_type}...")
        results = analyze_all_users_entropy(feature_type)
        all_entropy_results[feature_type] = results
    save_entropy_results(all_entropy_results)
    entropy_file = os.path.join(features_dir, 'entropy_results.json')
    print(f"Entropy results saved to {entropy_file}")

    # 3. Anomaly Detection
    print("[3/4] Detecting anomalies in entropy results...")
    all_anomaly_results = {}
    for feature_type in feature_types:
        print(f"  Detecting anomalies for {feature_type}...")
        results = analyze_all_users_entropy_anomalies(feature_type)
        all_anomaly_results[feature_type] = results
    save_anomaly_results(all_anomaly_results)
    anomaly_file = os.path.join(features_dir, 'anomaly_results.json')
    print(f"Anomaly results saved to {anomaly_file}")

    # 4. Plotting
    print("[4/4] Plotting entropy and anomalies...")
    # Load entropy results for plotting
    with open(entropy_file, 'r') as f:
        entropy_results = json.load(f)
    for feature_type in feature_types:
        for user_id, analysis in all_anomaly_results[feature_type].items():
            entropy_data = entropy_results[feature_type][user_id]['entropies']
            plot_entropy_with_anomalies(user_id, feature_type, entropy_data, analysis['anomalies'])
    print("Plots saved in extracted_features/entropy_plots/")
    print("\nPipeline completed successfully.")

if __name__ == "__main__":
    main() 