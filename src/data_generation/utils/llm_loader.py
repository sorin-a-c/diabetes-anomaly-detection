"""
Module for loading and initializing the LLM model.
"""

import os
from llama_cpp import Llama
from tqdm import tqdm
from utils.config import (
    MODEL_PATH,
    MODEL_CONTEXT_SIZE,
    MODEL_THREADS,
    MODEL_BATCH_SIZE,
    MODEL_SEED
)

def load_llm_model(
    model_path: str = MODEL_PATH,
    n_ctx: int = MODEL_CONTEXT_SIZE,
    n_threads: int = MODEL_THREADS,
    n_batch: int = MODEL_BATCH_SIZE,
    n_gpu_layers: int = -1,  # Use all available GPU layers
    seed: int = MODEL_SEED,
) -> Llama:
    """
    Safely loads the LLM model with error handling.
    
    Args:
        model_path: Path to the model file
        n_ctx: Context window size
        n_threads: Number of threads to use
        n_batch: Batch size for prompt processing
        n_gpu_layers: Number of layers to offload to GPU (-1 for all layers)
        seed: Random seed for reproducibility
        
    Returns:
        Llama: Loaded model instance
        
    Raises:
        FileNotFoundError: If model file doesn't exist
        ValueError: If model parameters are invalid
        RuntimeError: If model loading fails
    """
    try:
        # Check if model file exists
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
            
        # Validate parameters
        if n_ctx < 1:
            raise ValueError("Context window size must be positive")
        if n_threads < 1:
            raise ValueError("Number of threads must be positive")
        if n_batch < 1:
            raise ValueError("Batch size must be positive")
            
        # Try to load the model
        tqdm.write(f"Loading model from {model_path}...")
        model = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_threads=n_threads,
            n_batch=n_batch,
            n_gpu_layers=n_gpu_layers,
            seed=seed,
            verbose=False
        )
        tqdm.write("Model loaded successfully!")
        return model
        
    except FileNotFoundError as e:
        tqdm.write(f"Error: {str(e)}")
        tqdm.write("Please ensure the model file exists and the path is correct.")
        raise
    except ValueError as e:
        tqdm.write(f"Error: Invalid parameter - {str(e)}")
        raise
    except Exception as e:
        tqdm.write(f"Error loading model: {str(e)}")
        tqdm.write("Please check if the model file is valid and you have sufficient memory.")
        raise RuntimeError(f"Failed to load model: {str(e)}")