"""
Configuration settings for the log generation system.
"""

# Model configuration
MODEL_PATH = "models/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
MODEL_CONTEXT_SIZE = 512
MODEL_THREADS = 8
MODEL_BATCH_SIZE = 64

# Parameters to ensure deterministic output
MODEL_SEED = 2025
GENERATION_MAX_TOKENS = 100
GENERATION_TEMPERATURE = 0.0

# Log type weights for different adherence patterns
ADHERENT_LOG_TYPE_WEIGHTS = {
    # High frequency logs
    "glucose": 4,
    
    # Medium frequency logs 
    "diet": 2,
    "mood": 2, 
    "activity": 2,
    "insulin": 2,
    "medication": 2,
    
    # Low frequency logs
    "sleep": 1,
    "weight": 1,
    "notes": 1, 
    "other": 1
}

NON_ADHERENT_LOG_TYPE_WEIGHTS = {
    # High frequency logs
    "glucose": 10,
    
    # Medium frequency logs 
    "diet": 1,
    "mood": 1, 
    "activity": 1,
    "insulin": 1,
    "medication": 1,
    
    # Low frequency logs
    "sleep": 1,
    "weight": 1,
    "notes": 1, 
    "other": 1
} 