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


def dimensions_to_pairs(dimensions: list[int]) -> list[list[int]]:
    matrices = []

    for i in range(len(dimensions) - 1):
        matrices.append([dimensions[i], dimensions[i + 1]])

    return matrices
