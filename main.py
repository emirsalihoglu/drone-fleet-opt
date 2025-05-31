# main.py

from src.utils.generator import generate_drones, generate_deliveries, generate_noflyzones
from src.utils.graph import Graph
from src.algorithms.genetic import GeneticOptimizer
from src.utils.visualizer import plot_delivery_routes

def main():
    # 1. Generate data
    drones = generate_drones(5)
    deliveries = generate_deliveries(10)
    noflyzones = generate_noflyzones(2)

    # 2. Match positions (ID -> (x, y))
    positions = {}
    for d in drones:
        positions[d.id] = d.start_pos
    for delivery in deliveries:
        positions[delivery.id] = delivery.pos

    # 3. Create the graph
    graph = Graph()
    for node_id in positions:
        graph.add_node(node_id)

    # Connect all nodes to each other (suitable for testing)
    for i in positions:
        for j in positions:
            if i != j:
                cost = graph.euclidean_distance(positions[i], positions[j])
                graph.add_edge(i, j, cost)

    # 4. Run the genetic algorithm
    optimizer = GeneticOptimizer(
        drones=drones,
        deliveries=deliveries,
        noflyzones=noflyzones,
        graph=graph,
        positions=positions,
        current_time="10:00"
    )

    best_solution = optimizer.run()
    print("Best Assignment (drone_id, delivery_id):")
    for assignment in best_solution:
        print(f"  Drone {assignment[0]} → Delivery {assignment[1]}")

    # 5. Visualize the route and no-fly zones
    plot_delivery_routes(
        drones=drones,
        deliveries=deliveries,
        positions=positions,
        assignments=best_solution,
        noflyzones=noflyzones
    )

if __name__ == "__main__":
    main()