import random
from copy import deepcopy
from src.algorithms.astar import AStar
from src.algorithms.csp import CSP


class GeneticOptimizer:
    """
    Genetic Algorithm to optimize drone delivery assignments.
    """

    def __init__(self, drones, deliveries, noflyzones, graph, positions, current_time, verbose=False):
        self.drones = drones
        self.deliveries = deliveries
        self.noflyzones = noflyzones
        self.graph = graph
        self.positions = positions
        self.current_time = current_time
        self.verbose = verbose
        self.csp = CSP(drones, deliveries, noflyzones)
        self.astar = AStar(graph, positions)

    def generate_initial_population(self, size=10):
        population = []
        for _ in range(size):
            solution = []
            available_deliveries = deepcopy(self.deliveries)
            random.shuffle(available_deliveries)

        for drone in self.drones:
            for delivery in available_deliveries:
                if self.csp.is_delivery_valid(drone, delivery, self.current_time, verbose=False):
                    solution.append((drone.id, delivery.id))
                    available_deliveries.remove(delivery)
                    break
            population.append(solution)
        return population

    def fitness(self, solution):
        total_cost = 0
        seen_drones = set()  # ✅ tanımlandı

        for drone_id, delivery_id in solution:
            if drone_id in seen_drones:
                return 0
            seen_drones.add(drone_id)

            drone = next(d for d in self.drones if d.id == drone_id)
            delivery = next(d for d in self.deliveries if d.id == delivery_id)

            if not self.csp.is_delivery_valid(drone, delivery, self.current_time, verbose=False):
                return 0

            cost, _ = self.astar.find_path(f"DR{drone_id}", f"D{delivery_id + 80}")
            total_cost += cost

        return len(solution) * 100 - total_cost

    def crossover(self, parent1, parent2):
        mid = len(parent1) // 2
        child = parent1[:mid] + [p for p in parent2 if p not in parent1[:mid]]
        return child

    def mutate(self, solution, mutation_rate=0.2):
        if random.random() < mutation_rate and solution:
            i = random.randint(0, len(solution) - 1)
            drone_id, _ = solution[i]
            drone = next(d for d in self.drones if d.id == drone_id)
            assigned_ids = [dlv_id for _, dlv_id in solution]
            unassigned = [d for d in self.deliveries if d.id not in assigned_ids]
            random.shuffle(unassigned)

            for new_delivery in unassigned:
                if self.csp.is_delivery_valid(drone, new_delivery, self.current_time, verbose=False):
                    solution[i] = (drone_id, new_delivery.id)
                    break
        return solution

    def run(self, generations=30, population_size=10):
        population = self.generate_initial_population(population_size)

        for _ in range(generations):
            population.sort(key=self.fitness, reverse=True)
            new_population = [population[0]]  # Elitism
            while len(new_population) < population_size:
                p1, p2 = random.sample(population[:5], 2)
                child = self.crossover(p1, p2)
                child = self.mutate(child)
                new_population.append(child)
            population = new_population

        best = max(population, key=self.fitness)

        # Final çözüm için detaylı log
        if self.verbose:
            print("\n[!] En iyi çözüme ait eşleşme detayları:")
            for drone_id, delivery_id in best:
                drone = next(d for d in self.drones if d.id == drone_id)
                delivery = next(d for d in self.deliveries if d.id == delivery_id)
                self.csp.is_delivery_valid(drone, delivery, self.current_time, verbose=True)

        return best