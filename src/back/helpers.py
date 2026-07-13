from dataclasses import dataclass
from random import randint


@dataclass
class GenerationSnapshot:
    generation: int  # номер поколения
    best_cost: int  # лучшая стоимость
    mean_cost: float  # средняя стоимость
    best_individual: list[int]  # хромосома лучшего решения
    population: list[list[int]]


@dataclass
class PlottingData:
    x: list[int]
    target_cost: float
    greedy_cost: float
    best_cost: list[int]
    mean_cost: list[float]
    best_order: list[int]


def get_data_from_file(file_path: str) -> list[list[int]]:
    matrices = []

    with open(file_path) as f:
        for line in f:
            rows, cols = map(int, line.split())
            if matrices and rows != matrices[-1][1]:
                raise ValueError(
                    f"Неправильная размерность после матрицы {len(matrices)}"
                )

            matrices.append([rows, cols])

    if not matrices:
        raise ValueError("Матрица пуста!")

    return matrices


def get_random_matrices(
    matrix_count: int = 20,
    min_size: int = 5,
    max_size: int = 50,
) -> list[list[int]]:

    dimensions = [randint(min_size, max_size) for _ in range(matrix_count + 1)]

    return [[dimensions[i], dimensions[i + 1]] for i in range(matrix_count)]


def pairs_to_dimensions(matrices: list[list[int]]) -> list[int]:
    dims = [matrices[0][0]]
    for matrix in matrices:
        dims.append(matrix[1])
    return dims


def dimensions_to_pairs(dimensions: list[int]) -> list[list[int]]:
    matrices = []

    for i in range(len(dimensions) - 1):
        matrices.append([dimensions[i], dimensions[i + 1]])

    return matrices


def calculate_min_cost(dimensions: list[int]) -> int:

    # считает точную минимальную стоимость перебором
    n = len(dimensions) - 1
    if n <= 0:
        return 0

    dp = [[0] * n for _ in range(n)]

    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            dp[i][j] = float("inf")

            for k in range(i, j):
                cost = (
                    dp[i][k]
                    + dp[k + 1][j]
                    + dimensions[i] * dimensions[k + 1] * dimensions[j + 1]
                )

                if cost < dp[i][j]:
                    dp[i][j] = cost

    return dp[0][n - 1]


def greedy_cost(dimensions: list[int]) -> int:
    dims = dimensions.copy()
    cost = 0

    while len(dims) > 2:
        best_i = min(
            range(len(dims) - 2),
            key=lambda i: dims[i] * dims[i + 1] * dims[i + 2],
        )

        cost += dims[best_i] * dims[best_i + 1] * dims[best_i + 2]
        dims.pop(best_i + 1)

    return cost
