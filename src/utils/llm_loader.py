"""
Module for loading and initializing the LLM model.
"""

import os
from llama_cpp import Llama

def load_llm_model(model_path: str, n_ctx: int = 1024, n_threads: int = 6) -> Llama:
    """
    Safely loads the LLM model with error handling.
    
    Args:
        model_path: Path to the model file
        n_ctx: Context window size
        n_threads: Number of threads to use
        
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
            
        # Try to load the model
        print(f"Loading model from {model_path}...")
        model = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_threads=n_threads
        )
        print("Model loaded successfully!")
        return model
        
    except FileNotFoundError as e:
        print(f"Error: {str(e)}")
        print("Please ensure the model file exists and the path is correct.")
        raise
    except ValueError as e:
        print(f"Error: Invalid parameter - {str(e)}")
        raise
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        print("Please check if the model file is valid and you have sufficient memory.")
        raise RuntimeError(f"Failed to load model: {str(e)}")