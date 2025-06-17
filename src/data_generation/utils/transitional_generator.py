"""
Utility functions for generating logs for transitional personas.
"""

import json
import random
import os
import sys
from datetime import datetime, timedelta
from tqdm import tqdm
from contextlib import contextmanager

from TransitionalPersona import TransitionalPersona
from Persona import LogEntry
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

def simulate_log(llm, persona, timestamp, log_type, current_day):
    """
    Simulates a log entry for a persona at a given timestamp.
    
    Args:
        llm: The language model instance
        persona: The transitional persona to generate for
        timestamp: When the log was created
        log_type: Type of log entry
        current_day: The current day (0-based)
        
    Returns:
        LogEntry: The generated log entry
    """
    time_str = timestamp.strftime("%H:%M")
    prompt = build_prompt(log_type, time_str, persona)
    message = generate_message(llm, prompt)
    
    # Get current traits
    consistency, frequency, variety = persona.get_current_traits(current_day)
    
    return LogEntry(
        timestamp=timestamp,
        log_type=log_type,
        message=message,
        metadata={
            "user_id": persona.user_id,
            "phase": "initial" if current_day < persona.transition_day else "final",
            "consistency": consistency.name,
            "frequency": frequency.name,
            "variety": variety.name,
            "transition_day": persona.transition_day
        }
    )

def generate_transitional_persona_logs(
    llm,
    user_id,
    initial_traits,
    final_traits,
    days=30,
    output_dir="synthetic_logs/transitional"
):
    """
    Generates synthetic logs for a transitional persona.
    
    Args:
        llm: The language model instance to use for generation
        user_id: Unique identifier for the user
        initial_traits: Tuple of (consistency, frequency, variety) for initial phase
        final_traits: Tuple of (consistency, frequency, variety) for final phase
        days: Number of days to generate logs for
        output_dir: Directory to save the generated logs
        
    Returns:
        list: List of generated log entries
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create persona instance
    persona = TransitionalPersona(
        user_id=user_id,
        initial_consistency=initial_traits[0],
        initial_frequency=initial_traits[1],
        initial_variety=initial_traits[2],
        final_consistency=final_traits[0],
        final_frequency=final_traits[1],
        final_variety=final_traits[2]
    )
    
    # Generate logs
    logs = []
    base_date = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
    
    # Create progress bar for days
    with tqdm(total=days, desc=f"Generating logs for {user_id}", unit="day") as pbar:
        for day in range(days):
            day_start = base_date + timedelta(days=day)
            
            # Get current traits for this day
            consistency, frequency, variety = persona.get_current_traits(day)
            
            # Get number of logs for this day based on frequency trait
            min_logs, max_logs = frequency.logs_per_day
            logs_per_day = random.randint(min_logs, max_logs)
            
            # Get log times for this day
            log_times = persona.generate_log_times(day_start, day, logs_per_day)
            
            # Generate logs for each time point
            for log_time in sorted(log_times):
                # Get weighted log types for this persona
                weighted_log_types = []
                log_type_weights = persona.get_log_type_weights(day)
                for log_type, weight in log_type_weights.items():
                    weighted_log_types.extend([log_type] * weight)
                    
                log_type = random.choice(weighted_log_types)
                log = simulate_log(llm, persona, log_time, log_type, day)
                logs.append(log)
            
            pbar.update(1)
            pbar.set_postfix({"logs": len(logs)})
    
    # Save logs
    output_file = os.path.join(output_dir, f"{user_id}_logs.json")
    with open(output_file, "w") as f:
        json.dump([log.__dict__ for log in logs], f, indent=2, default=str)
        
    tqdm.write(f"Generated {len(logs)} logs for {user_id}")
    return logs

def generate_all_transitional_personas(
    llm,
    days=30,
    output_dir="synthetic_logs/transitional"
):
    """
    Generates logs for all transitional personas.
    
    Args:
        llm: The language model instance to use for generation
        days: Number of days to generate logs for
        output_dir: Directory to save the generated logs
        
    Returns:
        dict: Dictionary mapping user IDs to their log entries
    """
    # Define all transitional personas
    transitional_personas = [
        # Adherence Breakdown
        {
            "id": "Transitional_1_AdherenceBreakdown",
            "initial": (True, True, True),    # Consistent, Frequent, Varied
            "final": (False, False, False)    # Inconsistent, Infrequent, Similar
        },
        # Gradual Improvement
        {
            "id": "Transitional_2_GradualImprovement",
            "initial": (False, False, False), # Inconsistent, Infrequent, Similar
            "final": (True, True, True)       # Consistent, Frequent, Varied
        },
        # Selective Adherence
        {
            "id": "Transitional_3_SelectiveAdherence",
            "initial": (True, True, True),    # Consistent, Frequent, Varied
            "final": (True, False, False)     # Consistent, Infrequent, Similar
        },
        # Erratic Behavior
        {
            "id": "Transitional_4_ErraticBehavior",
            "initial": (True, False, False),  # Consistent, Infrequent, Similar
            "final": (False, True, True)      # Inconsistent, Frequent, Varied
        },
        # Minimal to Detailed
        {
            "id": "Transitional_5_MinimalToDetailed",
            "initial": (False, False, False), # Inconsistent, Infrequent, Similar
            "final": (True, True, True)       # Consistent, Frequent, Varied
        }
    ]
    
    all_logs = {}
    
    # Create progress bar for personas
    with tqdm(total=len(transitional_personas), desc="Generating logs for transitional personas", unit="persona") as pbar:
        for persona in transitional_personas:
            logs = generate_transitional_persona_logs(
                llm=llm,
                user_id=persona["id"],
                initial_traits=persona["initial"],
                final_traits=persona["final"],
                days=days,
                output_dir=output_dir
            )
            all_logs[persona["id"]] = logs
            pbar.update(1)
            pbar.set_postfix({"current": persona["id"]})
    
    return all_logs 