"""
Main script for generating synthetic diabetes management logs.

Code Structure:
---------------
Data Generation/
├── DataGen.py            # Main script that initializes the model and runs generation
├── Persona.py            # Defines different user personas and their behaviors
├── TransitionalDataGen.py # Script for generating transitional persona logs
├── TransitionalPersona.py # Defines transitional personas with behavioral changes
└── utils/                # Utility modules
    ├── llm_loader.py     # Handles loading and initialization of the LLM model
    ├── prompt_generator.py # Generates prompts for different types of log entries
    ├── persona_log_generator.py # Persona-specific log generation and simulation
    ├── transitional_generator.py # Transitional persona log generation
    └── config.py         # Configuration settings (model paths, weights, etc.)

Flow:
-----
1. Model Initialization:
   - Loads the LLM model using settings from config.py
   - Handles any initialization errors

2. Log Generation:
   - generate_multiple_personas() is called with the initialized model
   - For each trait combination (8 possible combinations):
     a. Creates a persona instance with specific traits
     b. Generates logs based on the persona's characteristics
     c. Adds metadata about trait patterns
     d. Saves logs to JSON files

3. Log Structure:
   Each log entry contains:
   - user_id: Unique identifier for the persona
   - timestamp: When the log was created
   - log_type: Type of log (glucose, diet, mood, etc.)
   - message: Generated text describing the log entry
   - metadata: Information about the persona's traits

Usage:
------
Run this script directly to generate logs for all personas:
    python DataGen.py

The script will create a 'synthetic_logs' directory containing JSON files
for each persona's logs.
"""

from utils.config import (
    MODEL_PATH,
    MODEL_CONTEXT_SIZE,
    MODEL_THREADS
)
from utils.llm_loader import load_llm_model
from utils.persona_log_generator import generate_multiple_personas

# Initialize the model
try:
    llm = load_llm_model(
        model_path=MODEL_PATH,
        n_ctx=MODEL_CONTEXT_SIZE,
        n_threads=MODEL_THREADS
    )
except Exception as e:
    print("Failed to initialize model. Please check the error message above.")
    raise

print("Generating logs... This can take a while.")
# Example usage
if __name__ == "__main__":
    generate_multiple_personas(llm=llm, days=30)