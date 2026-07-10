import copy
import random as rd
from dataclasses import dataclass
from src.back.helpers import get_random_matrices, pairs_to_dimensions

""" 
n размерностей
n - 1 матриц
n - 2 операций

"""


@dataclass
class GenerationSnapshot:
    generation: int  # номер поколения
    best_cost: int  # лучшая стоимость
    mean_cost: float  # средняя стоимость
    best_individual: list[int]  # хромосома лучшего решения
    population: list[list[int]]


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


def generate_population(pop_size: int, dim_size: int) -> list[list[int]]:

    # создает популяцию
    return [generate_individual(dim_size - 2) for _ in range(pop_size)]


def generate_individual(ind_size: int) -> list[int]:

    # создает случайную особь (порядок перемножения матриц)
    # [2, 0, 0] т.е. сначала перемножатся 2 и 3, затем 0 и 1 и т.д
    # номер перемножаемой матрицы в текущем списке размерностей(гены)
    # ind_size - 3 - i потому что с каждой итерацией колво размерностей уменьшается на 1
    return [rd.randint(0, ind_size - 1 - i) for i in range(ind_size)]


def is_valid_individual(individual: list[int], n: int) -> bool:

    # проверка по принципу генерации
    if len(individual) != n - 2:
        return False

    return all(0 <= val <= (n - 3 - i) for i, val in enumerate(individual))


def calculate_cost(dimensions: list[int], individual: list[int]) -> int:

    # считает колво операций по особи
    cost = 0
    cur_dim = dimensions.copy()

    for idx in individual:
        # перемножение двух матриц cur_dim[n]xcur_dim[n+1] * cur_dim[n+1]xcur_dim[n+2]
        cost += cur_dim[idx] * cur_dim[idx + 1] * cur_dim[idx + 2]
        # остается матрица размерности cur_dim[n]xcur_dim[n+2]
        cur_dim.pop(idx + 1)
    return cost


def tournament(
    population: list[list[int]], dim: list[int], tournament_size: int = 3
) -> list[int]:

    # выбирается лучший вариант из трех' участников турика
    if tournament_size is None:
        tournament_size = 3
    candidates = rd.choices(population, k=tournament_size)
    return min(candidates, key=lambda ind: calculate_cost(dim, ind))


def mutate(individual: list[int], p_m: float | None = None) -> list[int]:

    # мутация - новый случайный возможный ген (номер перемножаемой матрицы)
    ind_size = len(individual)
    if p_m is None:
        p_m = 1 / ind_size if ind_size != 0 else 0.1

    # по каждому гену проходимся и с шансом меняем
    for i in range(ind_size):
        if rd.random() < p_m:
            individual[i] = rd.randint(0, ind_size - 1 - i)

    return individual


def crossover(
    first_parent: list[int], second_parent: list[int]
) -> tuple[list[int], list[int]]:

    # метод скрещивания - одноточечное
    # выдает корректных детей потому что гены задаются одинаково для обмениваемых позиций =>
    # не будет некорректного гена
    i = rd.randint(1, len(first_parent) - 1)
    return (first_parent[:i] + second_parent[i:], second_parent[:i] + first_parent[i:])


def selection(
    population: list[list[int]],
    dim: list[int],
    tournament_size: int = 3,
    p_m: float | None = 0.1,
    p_c: float | None = 0.8,
) -> list[list[int]]:

    # селекция)
    next_population = []
    len_next_population = 0
    
    # скрещивание с шансом
    if p_c is None:
        p_c = 0.8

    len_old_population = len(population)
    
    count_new_ind = int(len_old_population*0.1) + 1
    ind_size = len(population[0])
    
    # пока хз
    """ for _ in range(count_new_ind - 1):
        next_population.append(generate_individual(ind_size=ind_size))
        len_next_population += 1 """
    
    # пока популяция не фуловая
    while len_next_population < len_old_population:
        # выбор двух родителей независимо
        first_parent = tournament(population, dim, tournament_size)
        second_parent = tournament(population, dim, tournament_size)

        if rd.random() < p_c:
            first_child, second_child = crossover(first_parent, second_parent)
        else:
            first_child = first_parent.copy()
            second_child = second_parent.copy()

        # добавляем с мутацией
        next_population.append(mutate(first_child, p_m))
        len_next_population += 1

        # чтобы не переполнить при нечетном размере популяции
        if len_next_population < len_old_population:
            next_population.append(mutate(second_child, p_m))
            len_next_population += 1
    
    return next_population


def genetic_algorithm(
    population_size: int,
    dim_size: int,
    steps: int,
    tournament_size: int | None = None,
    p_m: float | None = None,
    p_c: float | None = None,
    population: list[list[int]] | None = None,
    dimensions: list[int] | None = None,
    cur_generation_offset: int = 0,
) -> tuple[list[GenerationSnapshot], int]:

    if not dimensions:
        dimensions = pairs_to_dimensions(get_random_matrices(dim_size - 1))

    if len(dimensions) < 32:
        # точное значение лучшего решения
        min_cost = calculate_min_cost(dimensions)
    else:
        # верхняя оценка - цена полученная жадным алгоритмом =>
        # если график лучшего индивида га выше линии target то алгоритм норм отработал
        
        # при больших колвах матриц нужны большие популяции и много поколений
        # для того чтобы алгоритм мог отработать нормально
        min_cost = greedy_cost(dimensions)
    
    history: list[GenerationSnapshot] = []

    # если не задана популяция
    if population is None:
        population = generate_population(population_size, dim_size)

    # делаем заданное колво эволюций
    for step_idx in range(steps):
        gen_number = step_idx + cur_generation_offset + 1
        
        costs = [calculate_cost(dimensions, ind) for ind in population]
        best_cost = min(costs)
        best_ind = population[costs.index(best_cost)].copy()
        
        history.append(
            GenerationSnapshot(
                generation=gen_number,
                best_cost=best_cost,
                mean_cost=sum(costs) / population_size,
                best_individual=best_ind.copy(),
                population=[ind.copy() for ind in population],
            )
        )
        
        """ if best_cost <= min_cost:
            break """
        
        population = selection(population, dimensions, tournament_size, p_m, p_c)
        population[0] = best_ind

    return history, min_cost

# TODO пофиксить, чтобы сходился при dim_size > 50
# для идеала надо менять принцип кодирования индивидов, но чет западло)
