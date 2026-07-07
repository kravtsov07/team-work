from dataclasses import dataclass

from src.back.GA import generate_dimensions, genetic_algorithm


@dataclass
class PlottingData:
    x: list[int]
    best_cost: list[int]
    mean_cost: list[float]


def get_dimensions(matrices: list[dict]) -> list[int]:
    dims = [matrices[0]["rows"]]
    for matrix in matrices:
        dims.append(matrix["cols"])
    return dims


def get_plot_data(matrices: list[dict]) -> PlottingData:
    dimensions = get_dimensions(matrices)

    history, min_cost = genetic_algorithm(
        population_size=50,
        steps=200,
        dim_size=len(dimensions),
        dimensions=dimensions,
    )

    return PlottingData(
        x=[snap.generation for snap in history],
        best_cost=[snap.best_cost for snap in history],
        mean_cost=[snap.mean_cost for snap in history],
    )


def get_random_plot_data() -> PlottingData:
    dim_test4 = generate_dimensions(dim_size=10, min_size=10, max_size=50)
    history, min_cost = genetic_algorithm(
        population_size=50, steps=200, dim_size=10, dimensions=dim_test4
    )

    return PlottingData(
        x=[snap.generation for snap in history],
        best_cost=[snap.best_cost for snap in history],
        mean_cost=[snap.mean_cost for snap in history],
    )
