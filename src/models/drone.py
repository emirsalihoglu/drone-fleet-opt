# src/models/drone.py

class Drone:
    """
    Represents a delivery drone with specific capabilities.
    """

    def __init__(self, drone_id: int, max_weight: float, battery: int, speed: float, start_pos: tuple):
        """
        Initialize a Drone instance.

        :param drone_id: Unique identifier of the drone
        :param max_weight: Maximum weight the drone can carry (in kg)
        :param battery: Battery capacity (in mAh)
        :param speed: Flight speed (in meters per second)
        :param start_pos: Starting position as a tuple (x, y)
        """
        self.id = drone_id
        self.max_weight = max_weight
        self.battery = battery
        self.speed = speed
        self.start_pos = start_pos

        # Operational state
        self.current_pos = start_pos
        self.remaining_battery = battery
        self.carrying_weight = 0.0
        self.active = True  # Can be used for availability status

    def reset(self):
        """
        Resets the drone to its initial state.
        """
        self.current_pos = self.start_pos
        self.remaining_battery = self.battery
        self.carrying_weight = 0.0
        self.active = True

    def __repr__(self):
        return f"<Drone#{self.id} pos={self.current_pos} battery={self.remaining_battery}mAh>"