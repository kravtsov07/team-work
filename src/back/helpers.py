from random import randint

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
) -> list[dict[str, int]]:
    """Generate a random chain of compatible matrices."""

    dimensions = [randint(min_size, max_size) for _ in range(matrix_count + 1)]

    return [
        [dimensions[i], dimensions[i + 1]] for i in range(matrix_count)
    ]

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
