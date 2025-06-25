import json
import os
import numpy as np

# Path setup
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
results_path = os.path.join(base_dir, 'extracted_features', 'anomaly_results.json')

with open(results_path, 'r') as f:
    data = json.load(f)

# Parameters
window_size = 10
transition_day = 15

# Helper: get true anomaly windows for a persona
def get_true_anomaly_windows(persona, n_windows):
    if persona.startswith('Transitional_'):
        # Windows containing the transition day
        transition_entry = transition_day - window_size + 1  # 6
        start = max(0, transition_entry - 1)  # zero-based
        end = min(start + window_size, n_windows)
        true_windows = set(range(start, end))
        return true_windows
    else:
        return set()

# Metrics
from collections import defaultdict
metrics = defaultdict(lambda: defaultdict(dict))

# Abbreviations for the first 8 personas
abbrev_map = {
    "Persona_1_Consistent_Frequent_Varied": "CFV",
    "Persona_2_Consistent_Frequent_Similar": "CFS",
    "Persona_3_Consistent_Infrequent_Varied": "CIV",
    "Persona_4_Consistent_Infrequent_Similar": "CIS",
    "Persona_5_Inconsistent_Frequent_Varied": "IFV",
    "Persona_6_Inconsistent_Frequent_Similar": "IFS",
    "Persona_7_Inconsistent_Infrequent_Varied": "IIV",
    "Persona_8_Inconsistent_Infrequent_Similar": "IIS",
}

# Collect all personas
all_personas = set()
for feature, personas in data.items():
    all_personas.update(personas.keys())
all_personas = sorted(all_personas)

# Collect all features in order
feature_list = list(data.keys())

# Build the combined LaTeX table
latex_table = []
latex_table.append(r"\begin{table*}[ht]")
latex_table.append(r"\centering")
latex_table.append(r"\caption{Anomaly detection metrics (Acc, Prec, Rec, F1) for all personas and features}")
header = ["Persona", "TP (total)", "FP (total)", "FN (total)", "TN (total)", "Acc (total)", "Prec (total)", "Rec (total)", "F1 (total)"]
latex_table.append(r"\begin{tabular}{lccccccccc}")
latex_table.append(r"\hline")
latex_table.append(" & ".join(header) + r" \\")
latex_table.append(r"\hline")

total_TP_sum = total_FP_sum = total_FN_sum = total_TN_sum = 0
for persona_key in all_personas:
    if persona_key in abbrev_map:
        display_name = abbrev_map[persona_key]
    elif persona_key.startswith('Transitional_'):
        name_part = persona_key.replace('Transitional_', '', 1)
        name_split = name_part.split('_', 1)
        display_name = name_split[1].replace('_', ' ') if len(name_split) > 1 else name_part.replace('_', ' ')
    else:
        display_name = persona_key.replace('_', r'\\_')
    total_TP = total_FP = total_FN = total_TN = 0
    for feature in feature_list:
        result = data[feature].get(persona_key)
        if result is not None:
            n_windows = result.get('total_windows', result.get('total_points', 0))
            marked = set(a['index'] for a in result.get('anomalies', []))
            anomalous = get_true_anomaly_windows(persona_key, n_windows)
            all_indices = set(range(n_windows))
            TP = len([i for i in all_indices if i in anomalous and i in marked])
            FP = len([i for i in all_indices if i not in anomalous and i in marked])
            FN = len([i for i in all_indices if i in anomalous and i not in marked])
            TN = len([i for i in all_indices if i not in anomalous and i not in marked])
            total_TP += TP
            total_FP += FP
            total_FN += FN
            total_TN += TN
    total_count = total_TP + total_FP + total_FN + total_TN
    acc = (total_TP + total_TN) / total_count if total_count > 0 else 0.0
    # Special handling for non-anomalous datasets
    if total_TP == 0 and total_FN == 0:
        if total_FP == 0:
            prec = 1.0
            rec = 1.0
        else:
            prec = 0.0
            rec = 0.0
    else:
        prec = total_TP / (total_TP + total_FP) if (total_TP + total_FP) > 0 else None
        rec = total_TP / (total_TP + total_FN) if (total_TP + total_FN) > 0 else None
    f1 = 2*prec*rec/(prec+rec) if (prec is not None and rec is not None and (prec+rec) > 0) else None
    acc_str = f"{acc:.2f}"
    prec_str = f"{prec:.2f}" if prec is not None else ""
    rec_str = f"{rec:.2f}" if rec is not None else ""
    f1_str = f"{f1:.2f}" if f1 is not None else ""
    row = [display_name, str(total_TP), str(total_FP), str(total_FN), str(total_TN), acc_str, prec_str, rec_str, f1_str]
    latex_table.append(" & ".join(row) + r" \\")
    total_TP_sum += total_TP
    total_FP_sum += total_FP
    total_FN_sum += total_FN
    total_TN_sum += total_TN

# Add total row
sum_count = total_TP_sum + total_FP_sum + total_FN_sum + total_TN_sum
acc_total = (total_TP_sum + total_TN_sum) / sum_count if sum_count > 0 else 0.0
if total_TP_sum == 0 and total_FN_sum == 0:
    if total_FP_sum == 0:
        prec_total = 1.0
        rec_total = 1.0
    else:
        prec_total = 0.0
        rec_total = 0.0
else:
    prec_total = total_TP_sum / (total_TP_sum + total_FP_sum) if (total_TP_sum + total_FP_sum) > 0 else None
    rec_total = total_TP_sum / (total_TP_sum + total_FN_sum) if (total_TP_sum + total_FN_sum) > 0 else None
f1_total = 2*prec_total*rec_total/(prec_total+rec_total) if (prec_total is not None and rec_total is not None and (prec_total+rec_total) > 0) else None
acc_total_str = f"{acc_total:.2f}"
prec_total_str = f"{prec_total:.2f}" if prec_total is not None else ""
rec_total_str = f"{rec_total:.2f}" if rec_total is not None else ""
f1_total_str = f"{f1_total:.2f}" if f1_total is not None else ""
total_row = ["Total", str(total_TP_sum), str(total_FP_sum), str(total_FN_sum), str(total_TN_sum), acc_total_str, prec_total_str, rec_total_str, f1_total_str]
latex_table.append(" & ".join(total_row) + r" \\")
latex_table.append(r"\hline")
latex_table.append(r"\end{tabular}")
latex_table.append(r"\end{table*}")
print("\n".join(latex_table)) 