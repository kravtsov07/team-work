import random as rd

""" 
n размерностей
n - 1 матриц
n - 2 операций

"""


def calculate_min_cost(dimensions: list[int]) -> int:
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


def generate_dimensions(dim_size: int = 100, min_size: int = 1, max_size: int = 10):
    return [rd.randint(min_size, max_size) for _ in range(dim_size)]


def generate_population(pop_size: int, ind_size: int) -> list[list[int]]:
    return [generate_individual(ind_size) for _ in range(pop_size)]


def generate_individual(ind_size: int):
    return [rd.randint(0, ind_size - 3 - i) for i in range(ind_size - 2)]


def is_valid_individual(individual: list[int], n: int) -> bool:
    if len(individual) != n - 2:
        return False

    return all(0 <= val <= (n - 3 - i) for i, val in enumerate(individual))


def calculate_cost(dimensions: list[int], individual: list[int]):
    cost = 0
    cur_dim = dimensions.copy()
    for i in range(len(individual)):
        n = individual[i]
        cost += cur_dim[n] * cur_dim[n + 1] * cur_dim[n + 2]
        cur_dim.pop(n + 1)
    return cost


def tournament(
    population: list[list[int]], dim: list[int], tournament_size: int = 3
) -> list[int]:
    candidates = rd.choices(population, k=tournament_size)
    return min(candidates, key=lambda ind: calculate_cost(dim, ind))


def mutate(individual: list[int], p_m: float | None = None):
    ind_size = len(individual)
    if p_m is None:
        p_m = 1 / ind_size

    for i in range(ind_size):
        if rd.random() < p_m:
            individual[i] = rd.randint(0, ind_size - 1 - i)

    return individual


def crossover(first_parent: list[int], second_parent: list[int]):
    point = rd.randint(1, len(first_parent) - 1)
    first_child = first_parent[:point] + second_parent[point:]
    second_child = second_parent[:point] + first_parent[point:]
    return (first_child, second_child)


def selection(
    population: list[list[int]],
    dim: list[int],
    tournament_size: int = 3,
    p_c: float = 0.8,
) -> list[list[int]]:
    next_population = []
    len_next_population = 0

    while len_next_population < len(population):
        first_parent = tournament(population, dim, tournament_size)
        second_parent = tournament(population, dim, tournament_size)

        if rd.random() < p_c:
            first_child, second_child = crossover(first_parent, second_parent)
        else:
            first_child = first_parent.copy()
            second_child = second_parent.copy()

        next_population.append(mutate(first_child))
        len_next_population += 1

        if len_next_population < len(population):
            next_population.append(mutate(second_child))
            len_next_population += 1

    return next_population


def genetic_algorithm(
    population_size: int,
    max_generations: int,
    dim_size: int,
    dimensions: list[int] | None = None,
):

    if not dimensions:
        dimensions = generate_dimensions(dim_size)

    best_cost = float("inf")
    min_cost = calculate_min_cost(dimensions)
    print(min_cost)
    generations = 0
    population = generate_population(population_size, dim_size)
    while generations < max_generations:
        population = selection(
            population,
            dimensions,
        )
        best_ind = min(population, key=lambda ind: calculate_cost(dimensions, ind))
        best_cost = calculate_cost(dimensions, best_ind)
        if best_cost == min_cost:
            print(f"Найдено лучшее решение: {best_ind}, стоимость: {best_cost}")
            break
        all_cost = 0
        for ind in population:
            all_cost += calculate_cost(dimensions, ind)

        mean_cost = all_cost / population_size
        print(
            f"Поколение {generations + 1}: Лучший - {best_cost}, Средний - {mean_cost}"
        )
        generations += 1


if __name__ == "__main__":
    dim_test4 = generate_dimensions(dim_size=45, min_size=10, max_size=150)
    genetic_algorithm(
        population_size=500, max_generations=400, dim_size=45, dimensions=dim_test4
    )
