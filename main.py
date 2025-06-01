import time
from src.utils.generator import (
    generate_drones_from_file,
    generate_deliveries_from_file,
    generate_noflyzones_from_file
)
from src.utils.graph import Graph
from src.algorithms.genetic import GeneticOptimizer
from src.utils.visualizer import plot_delivery_routes
from src.algorithms.astar import AStar


def main():
    # 1. Load data
    drones = generate_drones_from_file()
    deliveries = generate_deliveries_from_file()
    noflyzones = generate_noflyzones_from_file()

    # 2. Prepare position map (ID -> (x, y))
    positions = {f"DR{drone.id}": drone.start_pos for drone in drones}
    positions.update({f"D{delivery.id + 80}": delivery.pos for delivery in deliveries})

    # 3. Build graph
    graph = Graph()
    for node_id in positions:
        graph.add_node(node_id)
    for i in positions:
        for j in positions:
            if i != j:
                cost = graph.euclidean_distance(positions[i], positions[j])
                graph.add_edge(i, j, cost)

    # 4. Genetic Algorithm
    optimizer = GeneticOptimizer(
        drones=drones,
        deliveries=deliveries,
        noflyzones=noflyzones,
        graph=graph,
        positions=positions,
        current_time="00:45",
        verbose=True
    )

    print("\n⏱ Running Genetic Algorithm...")
    start_ga = time.time()
    raw_solution = optimizer.run()
    end_ga = time.time()
    print(f"✅ Genetic Algorithm runtime: {end_ga - start_ga:.4f} sec")

    # 5. A* single test (optional comparison)
    if drones and deliveries:
        a_star = AStar(graph, positions)
        from_id = f"DR{drones[0].id}"
        to_id = f"D{deliveries[0].id + 80}"
        print(f"\n⏱ Running A* from {from_id} to {to_id}...")
        start_astar = time.time()
        cost, path = a_star.find_path(from_id, to_id)
        end_astar = time.time()
        print(f"✅ A* path cost: {cost:.2f} | runtime: {end_astar - start_astar:.6f} sec")

    # 6. Format best solution
    best_solution = [
        (f"DR{drone_id}", f"D{delivery_id + 80}")
        for drone_id, delivery_id in raw_solution
    ]

    # 7. Output
    print("\nBest Assignment (drone_id → delivery_id):")
    if not best_solution:
        print("⚠️  No valid assignments found.")
    else:
        for drone_id, delivery_id in best_solution:
            print(f"  {drone_id} → {delivery_id}")

    # 8. Visualize
    plot_delivery_routes(
        drones=drones,
        deliveries=deliveries,
        positions=positions,
        assignments=best_solution,
        noflyzones=noflyzones
    )


if __name__ == "__main__":
    main()