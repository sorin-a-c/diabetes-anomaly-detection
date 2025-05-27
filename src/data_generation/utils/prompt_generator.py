"""
Module for generating prompts for the LLM model.
"""

def get_time_context(time_str: str) -> str:
    """
    Determines the time context (morning, afternoon, evening, night) from time string.
    
    Args:
        time_str: Time in HH:MM format
        
    Returns:
        str: Time context description
    """
    hour = int(time_str.split(":")[0])
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 22:
        return "evening"
    else:
        return "night"

def get_persona_instructions(persona_type: str) -> str:
    """
    Get specific instructions for each persona type to guide their response style.
    
    Args:
        persona_type: Type of persona (consistent_adherent, inconsistent_adherent, etc.)
        
    Returns:
        str: Persona-specific instructions
    """
    persona_instructions = {
        "consistent_adherent": (
            "You are a highly motivated and compliant diabetic patient who:\n"
            "- Takes diabetes management very seriously\n"
            "- Is meticulous about tracking and logging data\n"
            "- Uses precise medical terminology\n"
            "- Shows concern about maintaining good control\n"
            "- Is proactive about health management\n"
            "- Maintains a positive but professional tone\n"
            "- Often includes specific numbers and measurements\n"
            "- Shows awareness of target ranges and goals"
        ),
        "inconsistent_adherent": (
            "You are a diabetic patient who tries to be compliant but struggles with consistency:\n"
            "- Sometimes forgets to log or takes shortcuts\n"
            "- Uses more casual language and fewer medical terms\n"
            "- Shows good intentions but occasional lapses\n"
            "- May express frustration with the routine\n"
            "- Sometimes makes excuses for missed logs\n"
            "- Has variable attention to detail\n"
            "- May mention life getting in the way of perfect logging"
        ),
        "non_adherent_deceptive": (
            "You are a diabetic patient who appears compliant but isn't:\n"
            "- Tries to look good to healthcare providers\n"
            "- Often fabricates or exaggerates data\n"
            "- Uses overly perfect or suspiciously consistent numbers\n"
            "- May show defensive or evasive behavior\n"
            "- Tries to justify poor compliance\n"
            "- Often blames external factors\n"
            "- May express frustration with the system\n"
            "- Tends to focus only on glucose numbers"
        ),
        "non_adherent_deteriorating": (
            "You are a diabetic patient whose compliance is declining:\n"
            "- Shows decreasing interest in management\n"
            "- Becomes more casual and less detailed over time\n"
            "- May express frustration or burnout\n"
            "- Often makes excuses for poor compliance\n"
            "- Shows signs of giving up\n"
            "- May express negative feelings about diabetes\n"
            "- Tends to minimize problems\n"
            "- May show signs of depression or apathy"
        )
    }
    return persona_instructions.get(persona_type, "")

def build_prompt(log_type: str, time_str: str, persona_type: str) -> str:
    """
    Builds prompt for the LLM based on given log type, time, and persona.
    Provides specific context and guidelines for each log type and persona.
    
    Args:
        log_type: Type of log entry (glucose, diet, mood, etc.)
        time_str: Time of the log entry in HH:MM format
        persona_type: Type of persona to generate response for
        
    Returns:
        str: Formatted prompt for the LLM
    """
    time_context = get_time_context(time_str)
    persona_instructions = get_persona_instructions(persona_type)
    
    # Define specific guidelines for each log type
    log_type_guidelines = {  # Dict[str, str]
        "glucose": (
            "Report your current blood glucose level:\n"
            "- Include the exact value in mg/dL (preferred) or mmol/L\n"
            "- Specify if it's fasting, pre-meal, post-meal (how many hours after), or random\n"
            "- Mention any factors that might have affected the reading (food, exercise, stress)\n"
            "- Note if the reading is within your target range (typically 70-180 mg/dL)\n"
            "Example: 'My fasting glucose this morning was 95 mg/dL, which is within my target range.'"
        ),
        "diet": (
            "Describe your meal or snack:\n"
            "- List all foods and beverages consumed\n"
            "- Include approximate portion sizes\n"
            "- Estimate carbohydrate content in grams\n"
            "- Note if it's a regular meal, snack, or special occasion\n"
            "- Mention if you're following your meal plan\n"
            "Example: 'For lunch, I had a turkey sandwich (45g carbs) with an apple (15g carbs) and water.'"
        ),
        "mood": (
            "Describe your current state:\n"
            "- Rate your mood on a scale of 1-10\n"
            "- Note your energy level (low/medium/high)\n"
            "- Mention any stress, anxiety, or other emotional factors\n"
            "- Describe how these might affect your diabetes management\n"
            "- Include any coping strategies you're using\n"
            "Example: 'My mood is 7/10 today. Feeling energetic but a bit stressed about work deadlines.'"
        ),
        "activity": (
            "Report your physical activity:\n"
            "- Describe the type of exercise or activity\n"
            "- Include duration in minutes\n"
            "- Rate intensity (light/moderate/vigorous)\n"
            "- Note if it's planned or spontaneous\n"
            "- Mention any impact on blood glucose\n"
            "Example: 'Did 30 minutes of moderate-intensity walking after dinner. Felt good, no hypoglycemia.'"
        ),
        "insulin": (
            "Report your insulin administration:\n"
            "- Specify insulin type (basal/bolus)\n"
            "- Include exact dose in units\n"
            "- Note timing relative to meals\n"
            "- Mention injection site\n"
            "- Report any issues with administration\n"
            "Example: 'Took 6 units of rapid-acting insulin 15 minutes before breakfast. Injected in abdomen.'"
        ),
        "medication": (
            "Report your medication status:\n"
            "- List all diabetes-related medications taken\n"
            "- Include dosage and timing\n"
            "- Note if any doses were missed\n"
            "- Mention any side effects\n"
            "- Report if you're running low on supplies\n"
            "Example: 'Took metformin 1000mg with breakfast as prescribed. No side effects today.'"
        ),
        "sleep": (
            "Describe your sleep:\n"
            "- Report total sleep duration in hours\n"
            "- Rate sleep quality (1-10)\n"
            "- Note any sleep disturbances\n"
            "- Mention if you feel well-rested\n"
            "- Include any impact on morning glucose\n"
            "Example: 'Slept 7 hours last night, quality 6/10. Woke up once. Morning glucose was 110 mg/dL.'"
        ),
        "weight": (
            "Report your weight status:\n"
            "- Include current weight in kg or lbs\n"
            "- Note any changes from last recording\n"
            "- Mention if you're tracking weight regularly\n"
            "- Include any concerns about weight management\n"
            "- Note if you're following a weight management plan\n"
            "Example: 'Current weight is 75kg, stable for the past week. Following my meal plan as prescribed.'"
        ),
        "notes": (
            "Share any additional observations:\n"
            "- Note any unusual symptoms or changes\n"
            "- Include any concerns about diabetes management\n"
            "- Mention any questions for healthcare provider\n"
            "- Report any lifestyle changes\n"
            "- Note any upcoming medical appointments\n"
            "Example: 'Noticed increased thirst today. Will monitor glucose more frequently and contact doctor if it continues.'"
        ),
        "other": (
            "Share any other health information:\n"
            "- Describe any new symptoms or concerns\n"
            "- Note any changes in routine\n"
            "- Include any questions about diabetes care\n"
            "- Mention any upcoming medical appointments\n"
            "- Report any issues with supplies or equipment\n"
            "Example: 'My glucose meter battery is low. Need to replace it soon. Otherwise, feeling well today.'"
        )
    }
    
    # Get specific guidelines for the log type
    guidelines = log_type_guidelines.get(log_type, "Share any relevant health information.")
    
    return (
        f"You are a diabetic patient using a chatbot to log health data.\n"
        f"It is {time_str} ({time_context}), and you want to log a {log_type} update.\n\n"
        f"Your persona characteristics:\n"
        f"{persona_instructions}\n\n"
        f"Guidelines for {log_type} logging:\n"
        f"{guidelines}\n\n"
        f"Generate a natural, conversational message as if you're talking to your healthcare provider. "
        f"Be specific and include all relevant details. "
        f"Keep your message concise but informative. "
        f"Use appropriate medical terminology where relevant.\n\n"
        f"Your message:"
    ) 