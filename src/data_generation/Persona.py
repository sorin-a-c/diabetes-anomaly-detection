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

class Trait:
    """Base class for defining behavioral traits."""
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.prompt_modifier = ""

class ConsistencyTrait(Trait):
    """Trait defining time consistency patterns."""
    def __init__(self, is_consistent):
        if is_consistent:
            super().__init__(
                "consistent",
                "Maintains regular logging times with minimal variation"
            )
            # Choose between different consistency levels
            consistency_patterns = [
                (-15, 15),    # Very consistent: ±15 minutes
                (-30, 30),    # Moderately consistent: ±30 minutes
                (-45, 45)     # Somewhat consistent: ±45 minutes
            ]
            self.time_variation = random.choice(consistency_patterns)
            self.prompt_modifier = (
                "- Maintains strict adherence to logging schedule\n"
                "- Uses precise timestamps and regular intervals\n"
                "- Shows high attention to timing details\n"
                "- Rarely deviates from established patterns"
            )
        else:
            super().__init__(
                "inconsistent",
                "Variable logging times with significant variation"
            )
            # Choose between different inconsistency levels
            inconsistency_patterns = [
                (-60, 60),    # Somewhat inconsistent: ±1 hour
                (-120, 120),  # Moderately inconsistent: ±2 hours
                (-180, 180)   # Very inconsistent: ±3 hours
            ]
            self.time_variation = random.choice(inconsistency_patterns)
            self.prompt_modifier = (
                "- Has irregular logging patterns\n"
                "- Often logs at varying times\n"
                "- May miss scheduled logging times\n"
                "- Shows flexibility in timing"
            )

class FrequencyTrait(Trait):
    """Trait defining logging frequency patterns."""
    def __init__(self, is_frequent):
        if is_frequent:
            super().__init__(
                "frequent",
                "Logs multiple times per day with high frequency"
            )
            # Choose between different frequency patterns
            frequency_patterns = [
                (3, 4),  # Moderately frequent: 3-4 logs per day
                (4, 6),  # Very frequent: 4-6 logs per day
                (5, 8)   # Extremely frequent: 5-8 logs per day
            ]
            self.logs_per_day = random.choice(frequency_patterns)
            self.prompt_modifier = (
                "- Logs multiple times throughout the day\n"
                "- Provides frequent updates on status\n"
                "- Maintains detailed daily records\n"
                "- Shows high engagement with logging"
            )
        else:
            super().__init__(
                "infrequent",
                "Logs fewer times per day with lower frequency"
            )
            # Choose between different infrequency patterns
            infrequency_patterns = [
                (1, 1),  # Very infrequent: exactly 1 log per day
                (1, 2),  # Moderately infrequent: 1-2 logs per day
                (2, 3)   # Somewhat infrequent: 2-3 logs per day
            ]
            self.logs_per_day = random.choice(infrequency_patterns)
            self.prompt_modifier = (
                "- Logs once or twice per day\n"
                "- Provides essential updates only\n"
                "- Maintains basic daily records\n"
                "- Shows minimal engagement with logging"
            )

class VarietyTrait(Trait):
    """Trait defining log type and content variety patterns."""
    def __init__(self, is_varied):
        if is_varied:
            super().__init__(
                "varied",
                "Uses diverse log types and detailed content"
            )
            # Choose between different variety patterns
            variety_patterns = [
                {  # Balanced variety
                    LogType.GLUCOSE: 3,
                    LogType.DIET: 3,
                    LogType.MOOD: 3,
                    LogType.ACTIVITY: 3,
                    LogType.INSULIN: 3,
                    LogType.MEDICATION: 3,
                    LogType.SLEEP: 2,
                    LogType.WEIGHT: 2,
                    LogType.NOTES: 2,
                    LogType.OTHER: 2
                },
                {  # Health-focused variety
                    LogType.GLUCOSE: 4,
                    LogType.DIET: 4,
                    LogType.MOOD: 2,
                    LogType.ACTIVITY: 3,
                    LogType.INSULIN: 4,
                    LogType.MEDICATION: 3,
                    LogType.SLEEP: 2,
                    LogType.WEIGHT: 2,
                    LogType.NOTES: 1,
                    LogType.OTHER: 1
                },
                {  # Lifestyle-focused variety
                    LogType.GLUCOSE: 2,
                    LogType.DIET: 4,
                    LogType.MOOD: 4,
                    LogType.ACTIVITY: 4,
                    LogType.INSULIN: 2,
                    LogType.MEDICATION: 2,
                    LogType.SLEEP: 3,
                    LogType.WEIGHT: 2,
                    LogType.NOTES: 3,
                    LogType.OTHER: 2
                }
            ]
            self.log_type_weights = random.choice(variety_patterns)
            self.prompt_modifier = (
                "- Uses diverse log types\n"
                "- Provides varied and detailed content\n"
                "- Shows interest in multiple aspects of health\n"
                "- Maintains comprehensive records"
            )
        else:
            super().__init__(
                "similar",
                "Focuses on specific log types with similar content"
            )
            # Choose between different similarity patterns
            similarity_patterns = [
                {  # Glucose-focused
                    LogType.GLUCOSE: 6,
                    LogType.DIET: 2,
                    LogType.MOOD: 1,
                    LogType.ACTIVITY: 1,
                    LogType.INSULIN: 3,
                    LogType.MEDICATION: 1,
                    LogType.SLEEP: 1,
                    LogType.WEIGHT: 1,
                    LogType.NOTES: 1,
                    LogType.OTHER: 1
                },
                {  # Diet-focused
                    LogType.GLUCOSE: 3,
                    LogType.DIET: 6,
                    LogType.MOOD: 1,
                    LogType.ACTIVITY: 2,
                    LogType.INSULIN: 2,
                    LogType.MEDICATION: 1,
                    LogType.SLEEP: 1,
                    LogType.WEIGHT: 2,
                    LogType.NOTES: 1,
                    LogType.OTHER: 1
                },
                {  # Medication-focused
                    LogType.GLUCOSE: 3,
                    LogType.DIET: 2,
                    LogType.MOOD: 1,
                    LogType.ACTIVITY: 1,
                    LogType.INSULIN: 3,
                    LogType.MEDICATION: 6,
                    LogType.SLEEP: 1,
                    LogType.WEIGHT: 1,
                    LogType.NOTES: 2,
                    LogType.OTHER: 1
                }
            ]
            self.log_type_weights = random.choice(similarity_patterns)
            self.prompt_modifier = (
                "- Focuses on specific log types\n"
                "- Uses similar content patterns\n"
                "- Shows preference for routine updates\n"
                "- Maintains focused records"
            )

class Persona:
    """Base class for user personas with different adherence patterns."""
    
    def __init__(self, user_id, consistency, frequency, variety):
        self.user_id = user_id
        self.consistency_trait = ConsistencyTrait(consistency)
        self.frequency_trait = FrequencyTrait(frequency)
        self.variety_trait = VarietyTrait(variety)
        self._initialize_behavior_patterns()
    
    def _initialize_behavior_patterns(self):
        """Initialize persona-specific behavior patterns."""
        self.log_type_weights = self.variety_trait.log_type_weights
        
        # Base time preferences for logging
        self.time_preferences = {
            "morning": (6, 9),    # 6:00-9:00
            "afternoon": (12, 15), # 12:00-15:00
            "evening": (18, 21)   # 18:00-21:00
        }
    
    def generate_log_times(self, day_start, day, logs_per_day):
        """Generate log times for a given day based on persona pattern."""
        # Use the provided logs_per_day parameter
        # Note: 'day' parameter is not used in base class but maintained for consistency with subclasses
        actual_logs = logs_per_day
        times = []
        
        if self.consistency_trait.name == "consistent":
            # Distribute logs evenly across preferred time periods
            periods = list(self.time_preferences.items())
            for i in range(actual_logs):
                period = periods[i % len(periods)]
                start_hour, _ = period[1]
                base_time = day_start + timedelta(hours=start_hour)
                variation = random.randint(*self.consistency_trait.time_variation)
                times.append(base_time + timedelta(minutes=variation))
        else:
            # Random times during waking hours
            for _ in range(actual_logs):
                hour = random.randint(6, 22)
                minute = random.randint(0, 59)
                times.append(day_start + timedelta(hours=hour, minutes=minute))
        
        return sorted(times)
    
    def get_log_type_weights(self):
        """Get weights for different log types based on persona characteristics."""
        return self.log_type_weights
    
    def get_time_variation(self):
        """Get the amount of time variation in minutes for this persona."""
        return random.randint(*self.consistency_trait.time_variation)
    
    def get_prompt_modifiers(self):
        """Get all prompt modifiers for this persona's traits."""
        return "\n".join([
            self.consistency_trait.prompt_modifier,
            self.frequency_trait.prompt_modifier,
            self.variety_trait.prompt_modifier
        ])

def create_persona(user_id, consistency, frequency, variety):
    """Factory function to create persona instances with specified traits."""
    return Persona(
        user_id=user_id,
        consistency=consistency,
        frequency=frequency,
        variety=variety
    )