from dataclasses import dataclass

from src.back.GA import genetic_algorithm
from src.back.helpers import pairs_to_dimensions
from src.gui.pages.param_setter import Params


@dataclass
class PlottingData:
    x: list[int]
    target_cost: int
    best_cost: list[int]
    mean_cost: list[float]
    best_order: str
    populations: list | None = None


def get_plot_data(matrices: list[list[int]], params: Params) -> PlottingData:

    dimensions = pairs_to_dimensions(matrices)

    history, min_cost = genetic_algorithm(
        population_size=params.population_size,
        steps=params.steps,
        dim_size=len(dimensions),
        dimensions=dimensions,
        p_m=params.mutation_rate,
        p_c=params.crossover_rate,
    )

    return PlottingData(
        x=[snap.generation for snap in history],
        target_cost=min_cost,
        best_cost=[snap.best_cost for snap in history],
        mean_cost=[snap.mean_cost for snap in history],
        best_order=str(history[-1].best_individual),
        populations=[snap.population for snap in history],
    )
