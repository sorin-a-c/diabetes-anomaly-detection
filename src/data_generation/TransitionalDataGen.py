"""
Main script for generating synthetic diabetes management logs for transitional personas.

This script generates logs for personas that change their behavior at a specified transition day.
The logs are saved in a separate directory from the stable personas to avoid overwriting existing data.
"""

from utils.config import (
    MODEL_PATH,
    MODEL_CONTEXT_SIZE,
    MODEL_THREADS
)
from utils.llm_loader import load_llm_model
from utils.transitional_generator import generate_all_transitional_personas

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

print("Generating logs for transitional personas... This can take a while.")
# Example usage
if __name__ == "__main__":
    generate_all_transitional_personas(llm=llm, days=30) 