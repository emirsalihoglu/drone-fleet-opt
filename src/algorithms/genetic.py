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
        self.debug_print_limit = 10
        self.debug_print_count = 0

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
        """
        Fitness = (total_priority_score) - (energy_cost * penalty_factor)
        """
        total_energy = 0
        total_priority_score = 0
        seen_drones = set()
        mAh_per_meter = 5
        penalty_factor = 0.1
        priority_weight = 10  # ⬅️ Her priority puanı 10 ile çarpılıyor

        for drone_id, delivery_id in solution:
            if drone_id in seen_drones:
                return 0
            seen_drones.add(drone_id)

            drone = next(d for d in self.drones if d.id == drone_id)
            delivery = next(d for d in self.deliveries if d.id == delivery_id)

            if not self.csp.is_delivery_valid(drone, delivery, self.current_time, verbose=False):
                return 0

            from_id = f"DR{drone.id}"
            to_id = f"D{delivery.id + 80}"
            cost, _ = self.astar.find_path(from_id, to_id)

            energy_used = cost * mAh_per_meter
            total_energy += energy_used
            total_priority_score += delivery.priority * priority_weight

            if drone.speed > 0:
                travel_time = cost / drone.speed
            else:
                travel_time = float("inf")

            if self.verbose and self.debug_print_count < self.debug_print_limit:
                print(f"Drone#{drone.id} → Delivery#{delivery.id} | Distance: {cost:.2f} m | Speed: {drone.speed} m/s | Time: {travel_time:.2f} sec")
                self.debug_print_count += 1

        penalty = total_energy * penalty_factor
        return total_priority_score - penalty

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

        if self.verbose:
            print("\n[!] En iyi çözüme ait eşleşme detayları:")
            for drone_id, delivery_id in best:
                drone = next(d for d in self.drones if d.id == drone_id)
                delivery = next(d for d in self.deliveries if d.id == delivery_id)
                self.csp.is_delivery_valid(drone, delivery, self.current_time, verbose=True)

        return best