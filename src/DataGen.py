"""
Main script for generating synthetic diabetes management logs.

Code Structure:
---------------
src/
├── DataGen.py              # Main script that initializes the model and runs generation
├── Persona.py              # Defines different user personas and their behaviors
└── utils/                  # Utility modules
    ├── config.py           # Configuration settings (model paths, weights, etc.)
    ├── llm_loader.py       # Handles loading and initialization of the LLM model
    ├── prompt_generator.py # Generates prompts for different types of log entries
    ├── glucose_extractor.py# Extracts glucose values from generated text
    └── persona_log_generator.py # Persona-specific log generation and simulation

Flow:
-----
1. Model Initialization:
   - Loads the LLM model using settings from config.py
   - Handles any initialization errors

2. Log Generation:
   - generate_multiple_personas() is called with the initialized model
   - For each persona type (consistent, inconsistent, deceptive, deteriorating):
     a. Creates a persona instance with specific behavior patterns
     b. Generates logs based on the persona's characteristics
     c. Adds metadata about adherence patterns
     d. Saves logs to JSON files

3. Log Structure:
   Each log entry contains:
   - user_id: Unique identifier for the persona
   - timestamp: When the log was created
   - log_type: Type of log (glucose, diet, mood, etc.)
   - message: Generated text describing the log entry
   - glucose_mgdl: Extracted glucose value (if applicable)
   - adherence_pattern: Metadata about the persona's behavior

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
    generate_multiple_personas(llm=llm, days=1, logs_per_day=2)