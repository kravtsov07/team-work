from dataclasses import dataclass

from src.back.GA import genetic_algorithm
from src.back.helpers import get_random_matrices, pairs_to_dimensions


@dataclass
class PlottingData:
    x: list[int]
    target_cost: int
    best_cost: list[int]
    mean_cost: list[float]
    best_order: str


def get_plot_data(
    matrices: list[list[int]],
    population_size: int = 100,
    steps: int = 200,
    mutation_rate: float = 0.05,
    crossover_rate: float = 0.8,
) -> PlottingData:

    dimensions = pairs_to_dimensions(matrices)

    history, min_cost = genetic_algorithm(
        population_size=population_size,
        steps=steps,
        dim_size=len(dimensions),
        dimensions=dimensions,
        # mutation_rate=mutation_rate,
        # crossover_rate=crossover_rate,
    )

    return PlottingData(
        x=[snap.generation for snap in history],
        target_cost=min_cost,
        best_cost=[snap.best_cost for snap in history],
        mean_cost=[snap.mean_cost for snap in history],
        best_order=str(history[-1].best_individual),
    )
