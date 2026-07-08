from dataclasses import dataclass

from src.back.GA import genetic_algorithm
from src.back.helpers import pairs_to_dimensions, get_random_matrices

@dataclass
class PlottingData:
    x: list[int]
    target_cost: int
    best_cost: list[int]
    mean_cost: list[float]

def get_plot_data(matrices: list[list[int]]) -> PlottingData:
    
    dimensions = pairs_to_dimensions(matrices)

    history, min_cost = genetic_algorithm(
        population_size=100,
        steps=200,
        dim_size=len(dimensions),
        dimensions=dimensions,
    )

    return PlottingData(
        x=[snap.generation for snap in history],
        target_cost=min_cost,
        best_cost=[snap.best_cost for snap in history],
        mean_cost=[snap.mean_cost for snap in history],
    )


def get_random_plot_data() -> PlottingData:
    dim_size = 20
    dimensions = pairs_to_dimensions(get_random_matrices(dim_size - 1))
    history, min_cost = genetic_algorithm(
        population_size=100, steps=200, dim_size=dim_size, dimensions=dimensions
    )

    return PlottingData(
        x=[snap.generation for snap in history],
        target_cost=min_cost,
        best_cost=[snap.best_cost for snap in history],
        mean_cost=[snap.mean_cost for snap in history],
    )
