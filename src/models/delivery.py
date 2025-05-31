# src/models/delivery.py

class Delivery:
    """
    Represents a delivery task with location, weight, priority, and time window.
    """

    def __init__(self, delivery_id: int, pos: tuple, weight: float, priority: int, time_window: tuple):
        """
        Initialize a Delivery instance.

        :param delivery_id: Unique identifier of the delivery
        :param pos: Coordinates of the delivery point (x, y)
        :param weight: Weight of the package (in kg)
        :param priority: Delivery priority (1: low, 5: high)
        :param time_window: Acceptable delivery time range as a tuple ("HH:MM", "HH:MM")
        """
        self.id = delivery_id
        self.pos = pos
        self.weight = weight
        self.priority = priority
        self.time_window = time_window  # (start_time_str, end_time_str)

        # Delivery status tracking
        self.assigned_drone_id = None
        self.delivered = False

    def __repr__(self):
        return f"<Delivery#{self.id} to={self.pos} weight={self.weight}kg priority={self.priority}>"