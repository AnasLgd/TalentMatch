from enum import Enum, auto

class AvailabilityStatus(str, Enum):
    """Enum representing consultant availability status"""
    AVAILABLE = "AVAILABLE"  # Changed from lowercase to uppercase
    PARTIALLY_AVAILABLE = "PARTIALLY_AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    ON_MISSION = "ON_MISSION"  # Changed from on_mission to ON_MISSION