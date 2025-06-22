"""
Defines the TransitionalPersona class for generating logs with behavioral changes.
"""

from Persona import Persona, ConsistencyTrait, FrequencyTrait, VarietyTrait, LogType
from datetime import datetime, timedelta
import random

class TransitionalPersona(Persona):
    """
    A persona that changes its behavior at a specified transition day.
    """
    def __init__(
        self,
        user_id: str,
        initial_consistency: bool,
        initial_frequency: bool,
        initial_variety: bool,
        final_consistency: bool,
        final_frequency: bool,
        final_variety: bool,
        transition_day: int = 15
    ):
        """
        Initialize a transitional persona with initial and final traits.
        
        Args:
            user_id: Unique identifier for the persona
            initial_consistency: Whether the persona is initially consistent in timing
            initial_frequency: Whether the persona initially logs frequently
            initial_variety: Whether the persona initially uses varied log types
            final_consistency: Whether the persona is finally consistent in timing
            final_frequency: Whether the persona finally logs frequently
            final_variety: Whether the persona finally uses varied log types
            transition_day: The day when the behavior changes (default: 15)
        """
        super().__init__(user_id, initial_consistency, initial_frequency, initial_variety)
        
        # Store final traits
        self.final_consistency_trait = ConsistencyTrait(final_consistency)
        self.final_frequency_trait = FrequencyTrait(final_frequency)
        self.final_variety_trait = VarietyTrait(final_variety)
        
        self.transition_day = transition_day
        
    def get_current_traits(self, current_day: int) -> tuple[ConsistencyTrait, FrequencyTrait, VarietyTrait]:
        """
        Get the current traits based on the day.
        
        Args:
            current_day: The current day (0-based)
            
        Returns:
            tuple: (consistency_trait, frequency_trait, variety_trait)
        """
        if current_day < self.transition_day:
            return (
                self.consistency_trait,
                self.frequency_trait,
                self.variety_trait
            )
        else:
            return (
                self.final_consistency_trait,
                self.final_frequency_trait,
                self.final_variety_trait
            )
            
    def get_log_type_weights(self, current_day: int) -> dict[LogType, int]:
        """
        Get the weighted log types for the current day.
        
        Args:
            current_day: The current day (0-based)
            
        Returns:
            dict: Mapping of log types to their weights
        """
        consistency, frequency, variety = self.get_current_traits(current_day)
        
        # Use the variety trait's log type weights, which are already configured
        # based on whether the persona is varied or similar
        return variety.log_type_weights
            
    def generate_log_times(self, base_date: datetime, current_day: int, num_logs: int) -> list[datetime]:
        """
        Generate log times for the current day based on current traits.
        
        Args:
            base_date: The base date for the day
            current_day: The current day (0-based) - used to determine which traits to use
            num_logs: Number of logs to generate
            
        Returns:
            list: List of datetime objects for log times
        """
        consistency, frequency, variety = self.get_current_traits(current_day)
        times = []
        
        # Base time preferences for logging (same as parent class)
        time_preferences = {
            "morning": (6, 9),    # 6:00-9:00
            "afternoon": (12, 15), # 12:00-15:00
            "evening": (18, 21)   # 18:00-21:00
        }
        
        if consistency.name == "consistent":
            # Distribute logs evenly across preferred time periods
            periods = list(time_preferences.items())
            for i in range(num_logs):
                period = periods[i % len(periods)]
                start_hour, _ = period[1]
                base_time = base_date.replace(hour=start_hour, minute=0)
                variation = random.randint(*consistency.time_variation)
                times.append(base_time + timedelta(minutes=variation))
        else:
            # Random times during waking hours
            for _ in range(num_logs):
                hour = random.randint(6, 22)
                minute = random.randint(0, 59)
                times.append(base_date.replace(hour=hour, minute=minute))
        
        return sorted(times) 