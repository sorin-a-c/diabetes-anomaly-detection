import json
import numpy as np
import os

# Path to entropy results (go up 4 levels from this file to project root)
base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
results_path = os.path.join(base_dir, 'extracted_features', 'entropy_results.json')

with open(results_path, 'r') as f:
    data = json.load(f)

features = [
    ("time_of_day", "Time of Day"),
    ("logging_frequency", "Log Frequency"),
    ("log_types", "Log Type"),
    ("text_similarity", "Semantic Similarity"),
]

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

# Collect all persona names
personas = set()
for feature in data:
    personas.update(data[feature].keys())
personas = sorted(personas)

print(r"\begin{table*}[ht]")
print(r"\centering")
print(r"\caption{Baseline entropy values (mean $\pm$ standard deviation) by persona and feature}")
print(r"\begin{tabular}{lcccc}")
print(r"\hline")
print(r"Persona & Time of Day & Log Frequency & Log Type & Semantic Similarity \\")
print(r"\hline")

for persona in personas:
    display_name = abbrev_map.get(persona, persona.replace("_", r"\_"))
    row = [display_name]
    for feature_key, _ in features:
        if persona in data.get(feature_key, {}):
            entropies = data[feature_key][persona]["entropies"][:5]
            if entropies:
                mean = np.mean(entropies)
                std = np.std(entropies)
                row.append(f"{mean:.2f} $\\pm$ {std:.2f}")
            else:
                row.append("--")
        else:
            row.append("--")
    print(" & ".join(row) + r" \\")
print(r"\hline")
print(r"\end{tabular}")
print(r"\end{table*}")