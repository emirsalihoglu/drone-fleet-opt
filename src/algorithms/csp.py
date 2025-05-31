# src/algorithms/csp.py

from datetime import datetime
from shapely.geometry import LineString, Polygon
from src.models.delivery import Delivery
from src.models.noflyzone import NoFlyZone

class CSP:
    """
    Enforces constraints for assigning deliveries to drones.
    """

    def __init__(self, drones: list, deliveries: list, noflyzones: list):
        self.drones = drones
        self.deliveries = deliveries
        self.noflyzones = noflyzones

    def is_delivery_valid(self, drone, delivery: Delivery, current_time: str) -> bool:
        """
        Checks if a drone can perform the delivery without violating constraints:
        - max_weight is not exceeded
        - no-fly zones are avoided
        - time window is respected
        """
        # 1. Weight constraint
        if delivery.weight > drone.max_weight:
            return False

        # 2. No-fly zone constraint
        if self.intersects_no_fly_zone(drone.start_pos, delivery.pos, current_time):
            return False

        # 3. Time window constraint
        if not self.in_time_window(delivery.time_window, current_time):
            return False

        return True

    def in_time_window(self, time_window: tuple, now: str) -> bool:
        """
        Checks if current time is within delivery's acceptable time range.
        """
        fmt = "%H:%M"
        now_time = datetime.strptime(now, fmt)
        start_time = datetime.strptime(time_window[0], fmt)
        end_time = datetime.strptime(time_window[1], fmt)
        return start_time <= now_time <= end_time

    def intersects_no_fly_zone(self, start: tuple, end: tuple, current_time: str) -> bool:
        """
        Checks if the straight path between start and end intersects any active no-fly zone.
        """
        line = LineString([start, end])
        now = datetime.strptime(current_time, "%H:%M")

        for zone in self.noflyzones:
            poly = Polygon(zone.coordinates)
            start_time = datetime.strptime(zone.active_time[0], "%H:%M")
            end_time = datetime.strptime(zone.active_time[1], "%H:%M")

            if start_time <= now <= end_time and line.intersects(poly):
                return True  # Path crosses an active no-fly zone

        return False