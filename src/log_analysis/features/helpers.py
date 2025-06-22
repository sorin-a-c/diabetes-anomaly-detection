"""
Helper functions for feature extraction from log data.
"""

from datetime import datetime
from collections import defaultdict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_time_of_day_category(timestamp: str) -> str:
    """
    Categorize timestamp into time-of-day categories.
    
    Args:
        timestamp: ISO format timestamp string
        
    Returns:
        str: Time of day category (morning, afternoon, evening, night)
    """
    hour = datetime.fromisoformat(timestamp).hour
    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 22:
        return "evening"
    else:
        return "night"

def discretize_logging_frequency(logs_per_day: float) -> str:
    """
    Discretize logging frequency into categories.
    
    Args:
        logs_per_day: Average number of logs per day
        
    Returns:
        str: Frequency category (very_low, low, medium, high)
    """
    if logs_per_day < 4:
        return "low"
    elif logs_per_day < 7:
        return "medium"
    elif logs_per_day < 11:
        return "high"
    else:
        return "very_high"

def discretize_text_similarity(similarity: float) -> str:
    """
    Discretize text similarity into categories.
    
    Args:
        similarity: Cosine similarity score between consecutive messages
        
    Returns:
        str: Similarity category (identical, similar, somewhat_different, different)
    """
    if similarity >= 0.7:
        return "identical"
    elif similarity >= 0.4:
        return "similar"
    elif similarity >= 0.2:
        return "moderately_different"
    else:
        return "different"

def calculate_logging_frequency(logs: list) -> dict:
    """
    Calculate number of logs per day.
    
    Args:
        logs: List of log entries
        
    Returns:
        dict: Dictionary with dates as keys and number of logs as values
    """
    logs_per_day = defaultdict(int)
    for log in logs:
        date = datetime.fromisoformat(log['timestamp']).date()
        logs_per_day[date.isoformat()] += 1
    return dict(logs_per_day)

def calculate_text_similarity(logs: list) -> list:
    """
    Calculate semantic similarity between consecutive messages.
    
    Args:
        logs: List of log entries
        
    Returns:
        list: List of similarity scores between consecutive messages
    """
    if len(logs) < 2:
        return []
        
    # Extract messages
    messages = [log['message'] for log in logs]
    
    # Create TF-IDF vectors
    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform(messages)
        
        # Calculate cosine similarity between consecutive messages
        similarities = []
        for i in range(len(messages) - 1):
            similarity = cosine_similarity(
                tfidf_matrix[i:i+1], 
                tfidf_matrix[i+1:i+2]
            )[0][0]
            similarities.append(similarity)
        return similarities
    except:
        # Return zeros if vectorization fails (e.g., empty messages)
        return [0] * (len(messages) - 1) 