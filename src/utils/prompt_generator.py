"""
Module for generating prompts for the LLM model.
"""

def build_prompt(log_type: str, time_str: str) -> str:
    """
    Builds prompt for the LLM based on given log type and time.
    Provides specific context and guidelines for each log type.
    
    Args:
        log_type: Type of log entry (glucose, diet, mood, etc.)
        time_str: Time of the log entry in HH:MM format
        
    Returns:
        str: Formatted prompt for the LLM
    """
    
    # Define specific guidelines for each log type
    log_type_guidelines = {  # Dict[str, str]
        "glucose": (
            "Report your current blood glucose level. "
            "Include the value in mg/dL or mmol/L. "
            "Mention if it's before/after a meal or medication."
        ),
        "diet": (
            "Describe what you ate or plan to eat. "
            "Include portion sizes and carbohydrate content if known. "
            "Mention if it's a meal or snack."
        ),
        "mood": (
            "Describe your current mood and energy level. "
            "Mention any stress or factors affecting your diabetes management. "
            "Rate your mood on a scale of 1-10 if comfortable."
        ),
        "activity": (
            "Describe your physical activity or exercise. "
            "Include duration and intensity if applicable. "
            "Mention if it's planned or spontaneous."
        ),
        "insulin": (
            "Report your insulin administration. "
            "Include type, dose, and timing relative to meals. "
            "Mention if it's basal or bolus insulin."
        ),
        "medication": (
            "Report any diabetes-related medications taken. "
            "Include dosage and timing. "
            "Mention if you missed any doses."
        ),
        "sleep": (
            "Describe your sleep quality and duration. "
            "Mention any issues affecting your sleep. "
            "Include if you're feeling well-rested."
        ),
        "weight": (
            "Report your current weight if comfortable. "
            "Mention any significant changes. "
            "Include any concerns about weight management."
        ),
        "notes": (
            "Share any general observations or concerns. "
            "Include any symptoms or changes you've noticed. "
            "Mention if you need to adjust your management plan."
        ),
        "other": (
            "Share any other relevant health information. "
            "Include any concerns or questions. "
            "Mention if you need medical advice."
        )
    }
    
    # Get specific guidelines for the log type
    guidelines = log_type_guidelines.get(log_type, "Share any relevant health information.")
    
    return (
        f"You are a diabetic patient using a chatbot to log health data.\n"
        f"It is {time_str}, and you want to log a {log_type} update.\n\n"
        f"Guidelines for {log_type} logging:\n"
        f"{guidelines}\n\n"
        f"Generate a natural, conversational message as if you're talking to your healthcare provider. "
        f"Be specific and include relevant details. "
        f"Keep your message concise but informative.\n\n"
        f"Your message:"
    ) 