class ActivateMode(enum.Enum):
    """
    # Members
    DIRTY: Update sites with changes
    ALL: Update all slave sites
    SPECIFIC: Only update specified sites
    """
    DIRTY = 'dirty'
    ALL = 'all'
    SPECIFIC = 'specific'
