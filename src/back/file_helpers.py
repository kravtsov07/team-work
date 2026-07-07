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
