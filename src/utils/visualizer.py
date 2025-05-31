# src/utils/visualizer.py

import matplotlib.pyplot as plt

def draw_noflyzones(ax, noflyzones):
    """
    Draws no-fly zones as red polygons on the plot.
    """
    for zone in noflyzones:
        xs, ys = zip(*zone.coordinates)
        xs += (xs[0],)  # Close the polygon
        ys += (ys[0],)
        ax.plot(xs, ys, color='red', linestyle='-', linewidth=2, label="No-Fly Zone")

def plot_delivery_routes(drones, deliveries, positions, assignments, noflyzones=None, save_path=None):
    """
    Plots the delivery routes of drones on a 2D map.

    :param drones: List of Drone objects
    :param deliveries: List of Delivery objects
    :param positions: Dict mapping id -> (x, y)
    :param assignments: List of (drone_id, delivery_id)
    :param noflyzones: List of NoFlyZone objects (optional)
    :param save_path: Optional path to save the image
    """
    fig, ax = plt.subplots(figsize=(10, 8))

    # Plot delivery points
    for delivery in deliveries:
        x, y = positions[delivery.id]
        ax.scatter(x, y, color='blue', label='Delivery' if delivery.id == deliveries[0].id else "")
        ax.text(x + 0.5, y + 0.5, f"D{delivery.id - 100}", fontsize=9)

    # Plot drone start positions
    for drone in drones:
        x, y = positions[drone.id]
        ax.scatter(x, y, color='green', marker='^', s=100, label='Drone' if drone.id == drones[0].id else "")
        ax.text(x + 0.5, y + 0.5, f"DR{drone.id}", fontsize=9)

    # Plot delivery routes
    for drone_id, delivery_id in assignments:
        dx, dy = positions[drone_id]
        tx, ty = positions[delivery_id]
        ax.plot([dx, tx], [dy, ty], linestyle='--', color='gray')

    # Plot no-fly zones if available
    if noflyzones:
        draw_noflyzones(ax, noflyzones)

    ax.set_title("Drone Delivery Assignments")
    ax.set_xlabel("X Position (meters)")
    ax.set_ylabel("Y Position (meters)")
    ax.grid(True)
    ax.legend()

    if save_path:
        plt.savefig(save_path)
    plt.show()