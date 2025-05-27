"""
Module for extracting glucose values from text.
"""

import re

def extract_glucose_mgdl(text: str) -> float | None:
    """
    Extracts glucose value from text.
    Handles both mg/dL and mmol/L units, converting mmol/L to mg/dL.
    Also works without a unit, just extracting the number.
    
    Args:
        text: Text containing glucose value
        
    Returns:
        float | None: Extracted glucose value in mg/dL, or None if no valid value found
    """
    # Try to match mg/dL format first (including decimal values)
    match_mgdl = re.search(r"(\d+\.?\d*)\s*mg\s*\/\s*dL", text, re.IGNORECASE)
    if match_mgdl:
        try:
            return float(match_mgdl.group(1))
        except ValueError:
            pass
    
    # Try mmol/L format if mg/dL not found (including decimal values)
    match_mmol = re.search(r"(\d+\.?\d*)\s*mmol\s*\/\s*l", text, re.IGNORECASE)
    if match_mmol:
        try:
            mmol = float(match_mmol.group(1))
            return mmol * 18.0
        except ValueError:
            pass
        
    # Finally try extracting a number if blood sugar/glucose is mentioned
    if re.search(r"blood sugar|glucose", text.lower()):
        # Matches whole numbers (123) or decimals (123.45)
        # \d+ = one or more digits
        # \.? = optional decimal point
        # \d* = zero or more digits after decimal point
        match_num = re.search(r"(\d+\.?\d*)", text)
        if match_num:
            try:
                return float(match_num.group(1))
            except ValueError:
                pass
        
    return None 