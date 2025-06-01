from src.utils.generator import (
    generate_drones_from_file,
    generate_deliveries_from_file,
    generate_noflyzones_from_file
)
from src.utils.graph import Graph
from src.algorithms.genetic import GeneticOptimizer
from src.utils.visualizer import plot_delivery_routes


def main():
    # 1. Load data
    drones = generate_drones_from_file()
    deliveries = generate_deliveries_from_file()
    noflyzones = generate_noflyzones_from_file()

    # 2. Prepare position map (ID -> (x, y))
    # Use formatted IDs to prevent collisions
    positions = {f"DR{drone.id}": drone.start_pos for drone in drones}
    positions.update({f"D{delivery.id + 80}": delivery.pos for delivery in deliveries})

    # 3. Build fully connected graph
    graph = Graph()
    for node_id in positions:
        graph.add_node(node_id)

    for i in positions:
        for j in positions:
            if i != j:
                cost = graph.euclidean_distance(positions[i], positions[j])
                graph.add_edge(i, j, cost)

    # 4. Run optimization
    optimizer = GeneticOptimizer(
        drones=drones,
        deliveries=deliveries,
        noflyzones=noflyzones,
        graph=graph,
        positions=positions,
        current_time="00:45"  # HH:MM format
    )

    raw_solution = optimizer.run()

    # 5. Prepare assignment with formatted IDs for visualization
    best_solution = [
        (f"DR{drone_id}", f"D{delivery_id + 80}")
        for drone_id, delivery_id in raw_solution
    ]

    # 6. Output results
    print("\nBest Assignment (drone_id → delivery_id):")
    if not best_solution:
        print("⚠️  No valid assignments found.")
    else:
        for drone_id, delivery_id in best_solution:
            print(f"  {drone_id} → {delivery_id}")

    # 7. Visualize
    plot_delivery_routes(
        drones=drones,
        deliveries=deliveries,
        positions=positions,
        assignments=best_solution,
        noflyzones=noflyzones
    )


if __name__ == "__main__":
    main()