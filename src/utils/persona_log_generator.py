"""
Module for generating synthetic logs for different user personas.
"""

import json
import random
import os
from datetime import datetime, timedelta

from Persona import create_persona
from utils.prompt_generator import build_prompt
from utils.glucose_extractor import extract_glucose_mgdl

def generate_message(llm, prompt: str, max_tokens: int = 100) -> str:
    """
    Runs prompt on LLM and returns response.
    
    Args:
        llm: The language model instance
        prompt: The prompt to run
        max_tokens: Maximum number of tokens to generate
        
    Returns:
        str: The generated response text
    """
    response = llm(prompt, max_tokens=max_tokens)
    return response["choices"][0]["text"].strip()

def simulate_log(llm, user_id: str, timestamp: datetime, log_type: str) -> dict:
    """
    Simulates a log entry for a user at a given timestamp.
    
    Args:
        llm: The language model instance
        user_id: Unique identifier for the user
        timestamp: When the log was created
        log_type: Type of log entry (glucose, diet, mood, etc.)
        
    Returns:
        dict: Dictionary containing the log entry details
    """
    time_str = timestamp.strftime("%H:%M")
    prompt = build_prompt(log_type, time_str)
    message = generate_message(llm, prompt)

    return {
        "user_id": user_id,
        "timestamp": timestamp.isoformat(),
        "log_type": log_type,
        "message": message,
        "glucose_mgdl": extract_glucose_mgdl(message)
    }

def generate_persona_logs(
    llm,
    persona_type: str,
    user_id: str,
    days: int = 30,
    logs_per_day: int = 4,
    output_dir: str = "synthetic_logs"
) -> None:
    """
    Generates synthetic logs for a specific user persona.
    
    Args:
        llm: The language model instance to use for generation
        persona_type: Type of persona to generate logs for
        user_id: Unique identifier for the user
        days: Number of days to generate logs for
        logs_per_day: Target number of logs per day
        output_dir: Directory to save the generated logs
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create persona instance
    persona = create_persona(persona_type, user_id)
    
    # Generate logs
    logs = []  # List of dicts containing log entries
    base_date = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
    
    for day in range(days):
        day_start = base_date + timedelta(days=day)
        
        # Get log times for this day
        log_times = persona.generate_log_times(day_start, day, logs_per_day)
        
        # Generate logs for each time point
        for log_time in sorted(log_times):
            # Get weighted log types for this persona
            weighted_log_types = []
            log_type_weights = persona.get_log_type_weights()  # Dict[str, int]
            for log_type, weight in log_type_weights.items():
                weighted_log_types.extend([log_type] * weight)
                
            log_type = random.choice(weighted_log_types)
            log = simulate_log(llm, persona.user_id, log_time, log_type)
            
            # Add metadata about adherence pattern
            log["adherence_pattern"] = {
                "persona_type": persona_type,
                "description": persona.description,
                "day_in_sequence": day
            }
            
            logs.append(log)
    
    # Save logs
    output_file = os.path.join(output_dir, f"{user_id}_logs.json")
    with open(output_file, "w") as f:
        json.dump(logs, f, indent=2)
        
    print(f"Generated {len(logs)} logs for {user_id} ({persona_type})")
    return logs

def generate_multiple_personas(
    llm,
    days: int = 30,
    logs_per_day: int = 4,
    output_dir: str = "synthetic_logs"
) -> None:
    """
    Generates logs for multiple personas with different adherence patterns.
    
    Args:
        llm: The language model instance to use for generation
        days: Number of days to generate logs for
        logs_per_day: Target number of logs per day
        output_dir: Directory to save the generated logs
    """
    personas = [
        ("consistent_adherent", "sim_user_alice"),
        ("inconsistent_adherent", "sim_user_bob"),
        ("non_adherent_deceptive", "sim_user_charlie"),
        ("non_adherent_deteriorating", "sim_user_dan")
    ]
    
    for persona_type, user_id in personas:
        generate_persona_logs(
            llm=llm,
            persona_type=persona_type,
            user_id=user_id,
            days=days,
            logs_per_day=logs_per_day,
            output_dir=output_dir
        ) 