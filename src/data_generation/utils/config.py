"""
Configuration settings for the log generation system.
"""

# Model configuration
MODEL_PATH = "models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
MODEL_CONTEXT_SIZE = 512
MODEL_THREADS = 8
MODEL_BATCH_SIZE = 128

# Parameters to ensure deterministic output
MODEL_SEED = 2025
GENERATION_MAX_TOKENS = 100
GENERATION_TEMPERATURE = 0.0 