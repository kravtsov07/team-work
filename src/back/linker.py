from src.back.GA import genetic_algorithm


def get_dimensions(matrices: list[list[int]]) -> list[int]:
    dims = [matrices[0][0]]
    for matrix in matrices:
        dims.append(matrix[1])

    return dims


def get_plot_data(matrices: list[list[int]]):
    dimensions = get_dimensions(matrices)
    history, min_cost = genetic_algorithm(
        population_size=50,
        steps=200,
        dim_size=len(dimensions),
        dimensions=dimensions,  # TODO: подумать об оптимизации поколений.
    )

    plot_data = {
        "x": [snap.generation for snap in history],
        "best_cost": [snap.best_cost for snap in history],
        "mean_cost": [snap.mean_cost for snap in history],
    }

    return plot_data
