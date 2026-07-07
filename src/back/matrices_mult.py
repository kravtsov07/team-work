from src.back.GA import genetic_algorithm


def get_dimensions(matrices):
    dims = [len(matrices[0])]
    for matrix in matrices:
        dims.append(len(matrix[0]))
    return dims


def multiply_matrices(A: list[list[int]], B: list[list[int]]):
    height_A = len(A)
    width_A = len(A[0])
    width_B = len(B[0])

    C = [[0] * width_B for _ in range(height_A)]

    for i in range(height_A):
        for j in range(width_B):
            for k in range(width_A):
                C[i][j] += A[i][k] * B[k][j]

    return C


# TODO: На каком уровне валидацию делать лучше?
def proccess_matrices(matrices: list[list[list[int]]]):
    dimensions = get_dimensions(matrices)

    # TODO: Выработать алгоритм для поиска корректного pop_size и max_gen для оптимизации
    order = genetic_algorithm(
        population_size=500,
        max_generations=400,
        dim_size=len(dimensions),
        dimensions=dimensions,
    )  # Он пока пустой до доработки GA.py

    work = matrices.copy()

    for idx in order:
        left = work[idx]
        right = work[idx + 1]

        product = multiply_matrices(left, right)

        work[idx] = product
        work.pop(idx + 1)

    return work[0]
