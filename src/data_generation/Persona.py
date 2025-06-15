"""
Base classes for different user personas with distinct behavioral patterns.
"""

from datetime import datetime, timedelta
import random
from dataclasses import dataclass
from enum import Enum

class LogType(Enum):
    GLUCOSE = "glucose"
    DIET = "diet"
    MOOD = "mood"
    ACTIVITY = "activity"
    INSULIN = "insulin"
    MEDICATION = "medication"
    SLEEP = "sleep"
    WEIGHT = "weight"
    NOTES = "notes"
    OTHER = "other"

@dataclass
class LogEntry:
    """Represents a single log entry with all its attributes."""
    timestamp: datetime
    log_type: LogType
    message: str
    metadata: dict = None

class Persona:
    """Base class for user personas with different adherence patterns."""
    
    def __init__(self, user_id: str, description: str):
        self.user_id = user_id
        self.description = description
        self._initialize_behavior_patterns()
    
    def _initialize_behavior_patterns(self):
        """Initialize persona-specific behavior patterns."""
        self.log_type_weights = {
            LogType.GLUCOSE: 3,
            LogType.DIET: 2,
            LogType.MOOD: 1,
            LogType.ACTIVITY: 2,
            LogType.INSULIN: 2,
            LogType.MEDICATION: 1,
            LogType.SLEEP: 1,
            LogType.WEIGHT: 1,
            LogType.NOTES: 1,
            LogType.OTHER: 1
        }
        
        # Base time preferences for logging
        self.time_preferences = {
            "morning": (6, 9),    # 6:00-9:00
            "afternoon": (12, 15), # 12:00-15:00
            "evening": (18, 21)   # 18:00-21:00
        }
    
    def generate_log_times(self, day_start: datetime, day: int, logs_per_day: int) -> list:
        """Generate log times for a given day based on persona pattern."""
        raise NotImplementedError("Subclasses must implement generate_log_times")
    
    def get_log_type_weights(self) -> dict:
        """Get weights for different log types based on persona characteristics."""
        return self.log_type_weights
    
    def get_time_variation(self) -> int:
        """Get the amount of time variation in minutes for this persona."""
        return random.randint(-30, 30)  # Default: ±30 minutes

class ConsistentAdherent(Persona):
    """Persona that logs consistently at regular intervals with high accuracy."""
    
    def _initialize_behavior_patterns(self):
        super()._initialize_behavior_patterns()
        # Higher weights for important measurements
        self.log_type_weights.update({
            LogType.GLUCOSE: 4,
            LogType.INSULIN: 3,
            LogType.MEDICATION: 2,
            LogType.ACTIVITY: 3
        })
    
    def generate_log_times(self, day_start: datetime, day: int, logs_per_day: int) -> list:
        times = []
        for period, (start_hour, end_hour) in self.time_preferences.items():
            base_time = day_start + timedelta(hours=start_hour)
            variation = self.get_time_variation()
            times.append(base_time + timedelta(minutes=variation))
        return sorted(times)
    
    def get_time_variation(self) -> int:
        return random.randint(-15, 15)  # More consistent: ±15 minutes

class InconsistentAdherent(Persona):
    """Persona that logs regularly but with variable timing and detail."""
    
    def _initialize_behavior_patterns(self):
        super()._initialize_behavior_patterns()
        # More emphasis on subjective measures
        self.log_type_weights.update({
            LogType.MOOD: 3,
            LogType.NOTES: 2,
            LogType.GLUCOSE: 2,
            LogType.ACTIVITY: 2
        })
    
    def generate_log_times(self, day_start: datetime, day: int, logs_per_day: int) -> list:
        times = []
        for _ in range(logs_per_day):
            # Random time during waking hours (6:00-22:00)
            hour = random.randint(6, 22)
            minute = random.randint(0, 59)
            times.append(day_start + timedelta(hours=hour, minutes=minute))
        return sorted(times)
    
    def get_time_variation(self) -> int:
        return random.randint(-60, 60)  # More variable: ±60 minutes

class NonAdherentDeceptive(Persona):
    """Persona that appears compliant but fabricates data."""
    
    def _initialize_behavior_patterns(self):
        super()._initialize_behavior_patterns()
        # Focus on easily verifiable metrics
        self.log_type_weights.update({
            LogType.GLUCOSE: 5,
            LogType.MEDICATION: 3,
            LogType.ACTIVITY: 2,
            LogType.DIET: 2
        })
    
    def generate_log_times(self, day_start: datetime, day: int, logs_per_day: int) -> list:
        # Gradually decrease time variation to show suspicious consistency
        variation_minutes = max(5, 60 - (day * 2))  # Starts at 1 hour variation, decreases to 5 min
        times = []
        for period, (start_hour, _) in self.time_preferences.items():
            base_time = day_start + timedelta(hours=start_hour)
            variation = random.randint(-variation_minutes, variation_minutes)
            times.append(base_time + timedelta(minutes=variation))
        return sorted(times)
    
    def get_time_variation(self) -> int:
        return random.randint(-5, 5)  # Very consistent: ±5 minutes

class NonAdherentDeteriorating(Persona):
    """Persona that shows declining compliance over time."""
    
    def _initialize_behavior_patterns(self):
        super()._initialize_behavior_patterns()
        # Gradually reduce logging of important metrics
        self.log_type_weights.update({
            LogType.GLUCOSE: 2,
            LogType.INSULIN: 1,
            LogType.MEDICATION: 1,
            LogType.ACTIVITY: 1
        })
    
    def generate_log_times(self, day_start: datetime, day: int, logs_per_day: int) -> list:
        # Gradually reduce logging frequency
        current_logs = max(1, logs_per_day - int(day / 10))
        times = []
        for _ in range(current_logs):
            # Random time during waking hours
            hour = random.randint(6, 22)
            minute = random.randint(0, 59)
            times.append(day_start + timedelta(hours=hour, minutes=minute))
        return sorted(times)
    
    def get_time_variation(self) -> int:
        return random.randint(-120, 120)  # Very variable: ±2 hours

def create_persona(persona_type: str, user_id: str) -> Persona:
    """Factory function to create persona instances."""
    personas = {
        "consistent_adherent": ConsistentAdherent,
        "inconsistent_adherent": InconsistentAdherent,
        "non_adherent_deceptive": NonAdherentDeceptive,
        "non_adherent_deteriorating": NonAdherentDeteriorating
    }
    
    if persona_type not in personas:
        raise ValueError(f"Unknown persona type: {persona_type}")
        
    return personas[persona_type](
        user_id=user_id,
        description=f"{persona_type.replace('_', ' ').title()} user"
    )