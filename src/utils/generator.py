# src/utils/generator.py

import random
from src.models.drone import Drone
from src.models.delivery import Delivery
from src.models.noflyzone import NoFlyZone

def generate_drones(n=5):
    drones = []
    for i in range(n):
        drone = Drone(
            drone_id=i,
            max_weight=round(random.uniform(2.0, 6.0), 1),
            battery=random.randint(8000, 12000),
            speed=round(random.uniform(8.0, 12.0), 1),
            start_pos=(random.randint(0, 50), random.randint(0, 50))
        )
        drones.append(drone)
    return drones

def generate_deliveries(n=10, node_offset=100):
    deliveries = []
    for i in range(n):
        delivery = Delivery(
            delivery_id=i + node_offset,  # node ID çakışmasın diye drone'lardan farklı
            pos=(random.randint(0, 100), random.randint(0, 100)),
            weight=round(random.uniform(0.5, 3.0), 2),
            priority=random.randint(1, 5),
            time_window=("09:00", "12:00")
        )
        deliveries.append(delivery)
    return deliveries

def generate_noflyzones(n=2):
    zones = []
    for i in range(n):
        x, y = random.randint(20, 80), random.randint(20, 80)
        zone = NoFlyZone(
            zone_id=i,
            coordinates=[
                (x, y), (x+10, y), (x+10, y+10), (x, y+10)
            ],
            active_time=("09:30", "11:00")
        )
        zones.append(zone)
    return zones