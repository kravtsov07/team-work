from dataclasses import dataclass

from src.back.GA import genetic_algorithm
from src.back.helpers import get_random_matrices, pairs_to_dimensions


@dataclass
class PlottingData:
    x: list[int]
    target_cost: int
    best_cost: list[int]
    mean_cost: list[float]
    best_order: str | None = None  # заполняется, только если GA.py это отдаёт


def get_plot_data(
    matrices: list[list[int]],
    population_size: int = 100,
    steps: int = 200,
    mutation_rate: float = 0.05,
    crossover_rate: float = 0.8,
) -> PlottingData:
    """
    ВАЖНО: mutation_rate и crossover_rate сейчас просто прокидываются дальше.
    genetic_algorithm() в GA.py нужно доработать, чтобы он их принимал и
    реально использовал внутри алгоритма (сейчас там жёстко зашитые
    вероятности, если они вообще есть). Пока этого не сделано, эти два
    параметра в UI будут визуально настраиваться, но не влиять на расчёт.
    """
    dimensions = pairs_to_dimensions(matrices)

    history, min_cost = genetic_algorithm(
        population_size=population_size,
        steps=steps,
        dim_size=len(dimensions),
        dimensions=dimensions,
        # mutation_rate=mutation_rate,
        # crossover_rate=crossover_rate,
        # ^ раскомментировать после того, как GA.py начнёт принимать эти kwargs
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
