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

    def is_delivery_valid(self, drone, delivery: Delivery, current_time: str, verbose=False) -> bool:
        """
        Checks if a drone can perform the delivery without violating constraints:
        - max_weight is not exceeded
        - no-fly zones are avoided
        - time window is respected
        """
        if delivery.weight > drone.max_weight:
            if verbose:
                print(f"[X] Ağırlık Yetersiz → Drone#{drone.id} taşıma sınırı: {drone.max_weight}kg < Delivery#{delivery.id} ({delivery.weight}kg)")
            return False

        if self.intersects_no_fly_zone(drone.start_pos, delivery.pos, current_time):
            if verbose:
                print(f"[X] No-Fly Zone Engeli → Drone#{drone.id} → Delivery#{delivery.id} yolu yasak bölgeyle kesişiyor.")
            return False

        if not self.in_time_window(delivery.time_window, current_time):
            if verbose:
                print(f"[X] Zaman Uyuşmazlığı → Şu an: {current_time}, Delivery#{delivery.id} için geçerli zaman aralığı: {delivery.time_window[0]} – {delivery.time_window[1]}")
            return False

        if verbose:
            print(f"[✓] Uygun Eşleşme → Drone#{drone.id} → Delivery#{delivery.id}")
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
                return True

        return False