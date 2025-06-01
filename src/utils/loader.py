import json
from src.models.drone import Drone
from src.models.delivery import Delivery
from src.models.noflyzone import NoFlyZone


def load_json_file(path):
    """
    Loads raw JSON data from a file.
    """
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def minutes_to_timestr(minute_val):
    """
    Converts an integer minute value to "HH:MM" string format.
    """
    hours = minute_val // 60
    minutes = minute_val % 60
    return f"{hours:02d}:{minutes:02d}"


def convert_time_window_to_str(time_window):
    """
    Converts a tuple/list of 2 integers to ("HH:MM", "HH:MM")
    """
    return (
        minutes_to_timestr(time_window[0]),
        minutes_to_timestr(time_window[1])
    )


def load_drones(path):
    """
    Loads a list of Drone objects from a JSON file.
    """
    data = load_json_file(path)
    return [
        Drone(
            drone_id=d["id"],
            max_weight=d["max_weight"],
            battery=d["battery"],
            speed=d["speed"],
            start_pos=tuple(d["start_pos"])
        )
        for d in data
    ]


def load_deliveries(path):
    """
    Loads a list of Delivery objects from a JSON file.
    Converts time_window from minutes to "HH:MM".
    """
    data = load_json_file(path)
    return [
        Delivery(
            delivery_id=d["id"],
            pos=tuple(d["pos"]),
            weight=d["weight"],
            priority=d["priority"],
            time_window=convert_time_window_to_str(d["time_window"])
        )
        for d in data
    ]


def load_noflyzones(path):
    """
    Loads a list of NoFlyZone objects from a JSON file.
    Converts active_time from minutes to "HH:MM".
    """
    data = load_json_file(path)
    return [
        NoFlyZone(
            zone_id=z["id"],
            coordinates=[tuple(coord) for coord in z["coordinates"]],
            active_time=convert_time_window_to_str(z["active_time"])
        )
        for z in data
    ]