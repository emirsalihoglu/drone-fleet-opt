# src/utils/generator.py

from src.utils.loader import load_drones, load_deliveries, load_noflyzones


def generate_drones_from_file(path="data/drones.json"):
    """
    Loads a list of Drone instances from a JSON file.
    """
    return load_drones(path)


def generate_deliveries_from_file(path="data/deliveries.json"):
    """
    Loads a list of Delivery tasks from a JSON file.
    """
    return load_deliveries(path)


def generate_noflyzones_from_file(path="data/noflyzones.json"):
    """
    Loads a list of No-Fly Zones from a JSON file.
    """
    return load_noflyzones(path)