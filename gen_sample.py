# Файл для удобства

from random import randint


def generate_sample_file(
    file_path: str,
    matrix_count: int = 1000,
    min_size: int = 5,
    max_size: int = 50,
) -> None:
    dimensions = [randint(min_size, max_size) for _ in range(matrix_count + 1)]

    with open(file_path, "w") as f:
        for i in range(matrix_count):
            f.write(f"{dimensions[i]} {dimensions[i + 1]}\n")


if __name__ == "__main__":
    generate_sample_file("matrices.txt", matrix_count=1000)
