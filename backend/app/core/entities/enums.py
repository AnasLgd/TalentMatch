from enum import Enum, auto

class AvailabilityStatus(str, Enum):
    """Enum representing consultant availability status"""
    SOURCED = "SOURCED"      # Talent en cours de création ou qualification initiale
    QUALIFIED = "QUALIFIED"  # Consultant qualifié, disponible dans le vivier
    MISSION = "MISSION"      # Consultant actuellement en mission
    INTERCO = "INTERCO"      # Consultant en période d'intercontrat
    ARCHIVED = "ARCHIVED"    # Consultant archivé (ex-LEAVING)