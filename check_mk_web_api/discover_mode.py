import enum


class DiscoverMode(enum.Enum):
    """
    # Members
    NEW: Only discover new services
    REMOVE: Remove exceeding services
    FIXALL: Remove exceeding services and discover new services (Tabula Rasa)
    REFRESH: Start from scratch
    """
    NEW = 'new'
    REMOVE = 'remove'
    FIXALL = 'fixall'
    REFRESH = 'refresh'
