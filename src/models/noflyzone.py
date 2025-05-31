# src/models/noflyzone.py

class NoFlyZone:
    """
    Represents a no-fly zone area with polygon coordinates and active time.
    """

    def __init__(self, zone_id: int, coordinates: list, active_time: tuple):
        """
        Initialize a NoFlyZone instance.

        :param zone_id: Unique identifier for the no-fly zone
        :param coordinates: List of (x, y) tuples defining polygon corners
        :param active_time: Tuple of active time range strings ("HH:MM", "HH:MM")
        """
        self.id = zone_id
        self.coordinates = coordinates  # [(x1, y1), (x2, y2), ...]
        self.active_time = active_time  # ("09:30", "11:00")

    def __repr__(self):
        return f"<NoFlyZone#{self.id} active={self.active_time}>"