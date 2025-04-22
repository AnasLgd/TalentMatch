from enum import Enum, auto

class AvailabilityStatus(str, Enum):
    """Enum representing consultant availability status"""
    PROCESS = "PROCESS"  # Candidats en cours de process
    QUALIFIED = "QUALIFIED"  # Candidats qualifiés (vivier)
    MISSION = "MISSION"  # Consultants en mission
    INTERCO = "INTERCO"  # Consultants en intercontrat
    AVAILABLE = "AVAILABLE"  # Statut legacy - Disponible
    PARTIALLY_AVAILABLE = "PARTIALLY_AVAILABLE"  # Statut legacy - Partiellement disponible
    UNAVAILABLE = "UNAVAILABLE"  # Statut legacy - Indisponible
    ON_MISSION = "ON_MISSION"  # Statut legacy - En mission