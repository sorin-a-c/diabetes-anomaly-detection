"""
Module for generating synthetic logs for different user personas.
"""

import json
import random
import os
import sys
from datetime import datetime, timedelta
from tqdm import tqdm
from contextlib import contextmanager

from Persona import Persona, create_persona, LogType, LogEntry
from utils.prompt_generator import build_prompt
from utils.config import (
    GENERATION_MAX_TOKENS,
    GENERATION_TEMPERATURE
)

@contextmanager
def suppress_stdout():
    """Temporarily suppress stdout to prevent interference with progress bars."""
    original_stdout = sys.stdout
    sys.stdout = open(os.devnull, 'w')
    try:
        yield
    finally:
        sys.stdout.close()
        sys.stdout = original_stdout

def generate_message(llm, prompt, max_tokens=GENERATION_MAX_TOKENS, temperature=GENERATION_TEMPERATURE):
    """
    Runs prompt on LLM and returns response.
    
    Args:
        llm: The language model instance
        prompt: The prompt to run
        max_tokens: Maximum number of tokens to generate
        temperature: Temperature for generation (higher = more random)
        
    Returns:
        str: The generated response text
    """
    with suppress_stdout():
        response = llm(
            prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )
    return response["choices"][0]["text"].strip()

def simulate_log(llm, persona, timestamp, log_type):
    """
    Simulates a log entry for a persona at a given timestamp.
    
    Args:
        llm: The language model instance
        persona: The persona to generate for
        timestamp: When the log was created
        log_type: Type of log entry
        
    Returns:
        LogEntry: The generated log entry
    """
    time_str = timestamp.strftime("%H:%M")
    prompt = build_prompt(log_type, time_str, persona)
    message = generate_message(llm, prompt)
    
    return LogEntry(
        timestamp=timestamp,
        log_type=log_type,
        message=message,
        metadata={
            "consistency": persona.consistency_trait.name,
            "frequency": persona.frequency_trait.name,
            "variety": persona.variety_trait.name
        }
    )

def generate_persona_logs(
    llm,
    user_id,
    consistency,
    frequency,
    variety,
    days=30,
    output_dir="synthetic_logs"
):
    """
    Generates synthetic logs for a specific user persona.
    
    Args:
        llm: The language model instance to use for generation
        user_id: Unique identifier for the user
        consistency: Whether the persona is consistent in timing
        frequency: Whether the persona logs frequently
        variety: Whether the persona uses varied log types
        days: Number of days to generate logs for
        output_dir: Directory to save the generated logs
        
    Returns:
        list: List of generated log entries
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create persona instance
    persona = create_persona(user_id, consistency, frequency, variety)
    
    # Generate logs
    logs = []
    base_date = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
    
    # Create progress bar for days
    with tqdm(total=days, desc=f"Generating logs for {user_id}", unit="day") as pbar:
        for day in range(days):
            day_start = base_date + timedelta(days=day)
            
            # Get number of logs for this day based on frequency trait
            min_logs, max_logs = persona.frequency_trait.logs_per_day
            logs_per_day = random.randint(min_logs, max_logs)
            
            # Get log times for this day
            log_times = persona.generate_log_times(day_start, day, logs_per_day)
            
            # Generate logs for each time point
            for log_time in sorted(log_times):
                # Get weighted log types for this persona
                weighted_log_types = []
                log_type_weights = persona.get_log_type_weights()
                for log_type, weight in log_type_weights.items():
                    weighted_log_types.extend([log_type] * weight)
                    
                log_type = random.choice(weighted_log_types)
                log = simulate_log(llm, persona, log_time, log_type)
                logs.append(log)
            
            pbar.update(1)
            pbar.set_postfix({"logs": len(logs)})
    
    # Save logs
    output_file = os.path.join(output_dir, f"{user_id}_logs.json")
    with open(output_file, "w") as f:
        json.dump([log.__dict__ for log in logs], f, indent=2, default=str)
        
    tqdm.write(f"Generated {len(logs)} logs for {user_id}")
    return logs

def generate_multiple_personas(
    llm,
    days=30,
    output_dir="synthetic_logs"
):
    """
    Generates logs for multiple personas with different trait combinations.
    
    Args:
        llm: The language model instance to use for generation
        days: Number of days to generate logs for
        output_dir: Directory to save the generated logs
        
    Returns:
        dict: Dictionary mapping user IDs to their log entries
    """
    # Define all possible trait combinations
    trait_combinations = [
        (True, True, True),    # Consistent, Frequent, Varied
        (True, True, False),   # Consistent, Frequent, Similar
        (True, False, True),   # Consistent, Infrequent, Varied
        (True, False, False),  # Consistent, Infrequent, Similar
        (False, True, True),   # Inconsistent, Frequent, Varied
        (False, True, False),  # Inconsistent, Frequent, Similar
        (False, False, True),  # Inconsistent, Infrequent, Varied
        (False, False, False)  # Inconsistent, Infrequent, Similar
    ]
    
    all_logs = {}
    
    # Create progress bar for personas
    with tqdm(total=len(trait_combinations), desc="Generating logs for personas", unit="persona") as pbar:
        for i, (consistency, frequency, variety) in enumerate(trait_combinations):
            # Create descriptive user ID
            user_id = f"Persona_{i+1}_{'Consistent' if consistency else 'Inconsistent'}_{'Frequent' if frequency else 'Infrequent'}_{'Varied' if variety else 'Similar'}"
            
            logs = generate_persona_logs(
                llm=llm,
                user_id=user_id,
                consistency=consistency,
                frequency=frequency,
                variety=variety,
                days=days,
                output_dir=output_dir
            )
            all_logs[user_id] = logs
            pbar.update(1)
            pbar.set_postfix({"current": user_id})
    
    return all_logs 