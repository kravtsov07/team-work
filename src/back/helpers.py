from random import randint


def get_data_from_file(file_path: str) -> list[dict[str, int]]:
    matrices = []

    with open(file_path) as f:
        for line in f:
            rows, cols = map(int, line.split())
            if matrices and rows != matrices[-1]["cols"]:
                raise ValueError(
                    f"Неправильная размерность после матрицы {len(matrices)}"
                )
            matrices.append({"rows": rows, "cols": cols})

    return matrices


def get_random_matrices(
    matrix_count: int = 50,
    min_size: int = 5,
    max_size: int = 50,
) -> list[dict[str, int]]:
    """Generate a random chain of compatible matrices."""

    dimensions = [randint(min_size, max_size) for _ in range(matrix_count + 1)]

    return [
        {
            "rows": dimensions[i],
            "cols": dimensions[i + 1],
        }
        for i in range(matrix_count)
    ]
