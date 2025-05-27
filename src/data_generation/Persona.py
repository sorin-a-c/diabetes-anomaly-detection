from utils.config import ADHERENT_LOG_TYPE_WEIGHTS, NON_ADHERENT_LOG_TYPE_WEIGHTS
from datetime import datetime, timedelta
import random

# New modular persona implementation
class Persona:
    """Base class for user personas with different adherence patterns."""
    
    def __init__(self, user_id: str, description: str):
        self.user_id = user_id
        self.description = description
        
    def generate_log_times(self, day_start: datetime, day: int, logs_per_day: int) -> list[datetime]:
        """Generate log times for a given day based on persona pattern."""
        raise NotImplementedError("Subclasses must implement generate_log_times")
        
    def get_log_type_weights(self) -> dict[str, int]:
        """Get weights for different log types based on persona characteristics."""
        return ADHERENT_LOG_TYPE_WEIGHTS  # Default to standard weights


class ConsistentAdherent(Persona):
    """Persona that logs consistently at regular intervals."""
    
    def generate_log_times(self, day_start: datetime, day: int, logs_per_day: int) -> list[datetime]:
        # Regular intervals with small time variation
        return [
            day_start + timedelta(hours=h, minutes=random.randint(-30, 30))
            for h in [2, 8, 14]  # Morning, afternoon, evening
        ]


class InconsistentAdherent(Persona):
    """Persona that logs regularly but at variable times."""
    
    def generate_log_times(self, day_start: datetime, day: int, logs_per_day: int) -> list[datetime]:
        # Random times within wider window
        return [
            day_start + timedelta(minutes=random.randint(0, 840))  # 14 hours spread
            for _ in range(logs_per_day)
        ]


class NonAdherentDeceptive(Persona):
    """Persona that shows suspicious consistency over time."""
    
    def generate_log_times(self, day_start: datetime, day: int, logs_per_day: int) -> list[datetime]:
        # Gradually decrease time variation to show suspicious consistency
        variation_minutes = max(5, 60 - (day * 2))  # Starts at 1 hour variation, decreases to 5 min
        base_times = [2, 8, 14]  # Target times
        return [
            day_start + timedelta(
                hours=h,
                minutes=random.randint(-variation_minutes, variation_minutes)
            )
            for h in base_times
        ]
    
    def get_log_type_weights(self) -> dict[str, int]:
        """Get weights for different log types based on persona characteristics."""
        return NON_ADHERENT_LOG_TYPE_WEIGHTS  # Default to standard weights


class NonAdherentDeteriorating(Persona):
    """Persona that shows deteriorating compliance over time."""
    
    def generate_log_times(self, day_start: datetime, day: int, logs_per_day: int) -> list[datetime]:
        # Gradually reduce logging frequency
        current_logs = max(1, logs_per_day - int(day / 10))
        return [
            day_start + timedelta(minutes=random.randint(0, 840))
            for _ in range(current_logs)
        ]
    
    def get_log_type_weights(self) -> dict[str, int]:
        """Get weights for different log types based on persona characteristics."""
        return NON_ADHERENT_LOG_TYPE_WEIGHTS  # Default to standard weights


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