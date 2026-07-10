import copy
import random as rd
from dataclasses import dataclass
# from src.back.helpers import get_random_matrices, pairs_to_dimensions

def get_random_matrices(
    matrix_count: int = 20,
    min_size: int = 5,
    max_size: int = 50,
) -> list[list[int]]:

    dimensions = [rd.randint(min_size, max_size) for _ in range(matrix_count + 1)]

    return [[dimensions[i], dimensions[i + 1]] for i in range(matrix_count)]


def pairs_to_dimensions(matrices: list[list[int]]) -> list[int]:
    dims = [matrices[0][0]]
    for matrix in matrices:
        dims.append(matrix[1])
    return dims


@dataclass
class GenerationSnapshot:
    generation: int  # номер поколения
    best_cost: int  # лучшая стоимость
    mean_cost: float  # средняя стоимость
    best_individual: list[int]  # хромосома лучшего решения
    population: list[list[int]]

class GeneticAlgorithm:
    def __init__(self, dimensions: list[int]):
        self.dimensions: list[int] = dimensions # размерности матриц
        self.dims_size: int = len(dimensions) # колво размерностей матриц (matr_size = dim_size - 1)
        self.ind_size: int = self.dims_size - 2 # размер индивида
        self.population: list[list[int]] = [] # последняя популяция (history[cur_gen].population)
        self.p_m: float = 1/len(dimensions) # вероятность мутации
        self.p_c: float = 0.8 # вероятность скрещивания
        self.tournament_size = 3 # размер турика
        self.cur_generation: int = -1 # индекс последней генерации
        self.history: list[GenerationSnapshot] = {} # история поколений
    
    def set_p_c(self, p_c):
        self.p_c = p_c
    
    def get_min_cost(self):
        if self.dims_size < 32:
            # точное значение лучшего решения
            min_cost = calculate_min_cost(self.dimensions)
        else:
            # верхняя оценка - цена полученная жадным алгоритмом =>
            # если график лучшего индивида га выше линии target то алгоритм норм отработал
            
            # при больших колвах матриц нужны большие популяции и много поколений
            # для того чтобы алгоритм мог отработать нормально
            min_cost = greedy_cost(self.dimensions)

        return min_cost
    
    def _calculate_cost(self, individual: list[int]) -> int:

        # считает колво операций по особи
        cost = 0
        cur_dim = self.dimensions.copy()

        for idx in individual:
            # перемножение двух матриц cur_dim[n]xcur_dim[n+1] * cur_dim[n+1]xcur_dim[n+2]
            cost += cur_dim[idx] * cur_dim[idx + 1] * cur_dim[idx + 2]
            # остается матрица размерности cur_dim[n]xcur_dim[n+2]
            cur_dim.pop(idx + 1)
        return cost
    
    def _tournament(self) -> list[int]:
        candidates = rd.choices(self.population, k=self.tournament_size)
        return min(candidates, key=lambda ind: self._calculate_cost(ind))
    
    def _mutate(self, individual: list[int]) -> list[int]:

        # мутация - новый случайный возможный ген (номер перемножаемой матрицы)
        ind_size = len(individual)

        # по каждому гену проходимся и с шансом меняем
        for i in range(ind_size):
            if rd.random() < self.p_m:
                individual[i] = rd.randint(0, ind_size - 1 - i)

        return individual
    
    def _crossover(
        self, first_parent: list[int], second_parent: list[int]
    ) -> tuple[list[int], list[int]]:

        # метод скрещивания - одноточечное
        # выдает корректных детей потому что гены задаются одинаково для обмениваемых позиций =>
        # не будет некорректного гена
        i = rd.randint(1, len(first_parent) - 1)
        return (first_parent[:i] + second_parent[i:], second_parent[:i] + first_parent[i:])
    
    def _generate_individual(self) -> list[int]:
        # создает случайную особь (порядок перемножения матриц)
        # [2, 0, 0] т.е. сначала перемножатся 2 и 3, затем 0 и 1 и т.д
        # номер перемножаемой матрицы в текущем списке размерностей(гены)
        # ind_size - 1 - i потому что с каждой итерацией колво размерностей уменьшается на 1
        return [rd.randint(0, self.ind_size - 1 - i) for i in range(self.ind_size)]
    
    def _generate_population(self, pop_size: int) -> list[list[int]]:
        # создает популяцию
        self.population = [self._generate_individual() for _ in range(pop_size)]
    
    def _selection(self) -> list[list[int]]:

        # селекция)
        next_population = []
        len_next_population = 0

        len_old_population = len(self.population)
        
        """ 
        count_new_ind = int(len_old_population*0.1) + 1
        ind_size = len(self.population[0])
        
        # пока хз
        for _ in range(count_new_ind - 1):
            next_population.append(generate_individual(ind_size=ind_size))
            len_next_population += 1 """
        
        # пока популяция не фуловая
        while len_next_population < len_old_population:
            # выбор двух родителей независимо
            first_parent = self._tournament()
            second_parent = self._tournament()

            if rd.random() < self.p_c:
                first_child, second_child = self._crossover(first_parent, second_parent)
            else:
                first_child = first_parent.copy()
                second_child = second_parent.copy()

            # добавляем с мутацией
            next_population.append(self._mutate(first_child))
            len_next_population += 1

            # чтобы не переполнить при нечетном размере популяции
            if len_next_population < len_old_population:
                next_population.append(self._mutate(second_child))
                len_next_population += 1
        
        self.population = next_population
            
    def evolution(self, steps: int, population_size: int = 100):
        if not self.population:
            self._generate_population(pop_size=population_size)
        # делаем заданное колво эволюций
        for step_idx in range(steps):
            gen_number = self.cur_generation + step_idx + 1
            self.cur_generation += 1
            costs = [self._calculate_cost(ind) for ind in self.population]
            best_cost = min(costs)
            best_ind = self.population[costs.index(best_cost)].copy()
            
            self.history[gen_number] = GenerationSnapshot(
                        generation=gen_number,
                        best_cost=best_cost,
                        mean_cost=sum(costs) / population_size,
                        best_individual=best_ind.copy(),
                        population=[ind.copy() for ind in self.population]
                    )
            
            """ if best_cost <= min_cost:
                break """
            
            self._selection()
            self.population[rd.randint(0, population_size - 1)] = best_ind


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

if __name__ == "__main__":
    ga = GeneticAlgorithm([9, 21, 19, 11, 23, 10, 36, 34, 24, 9, 27, 44, 46, 14, 42, 10, 5, 43, 42, 7])
    ga.evolution(200, 100)
    last_snap = ga.history[ga.cur_generation-1]
    min_cost = ga.get_min_cost()
    print(f"Финальное поколение: {last_snap.generation}")
    print(f"Ожидаемый результат: {min_cost}")
    print(f"Лучший кост: {last_snap.best_cost}")
    print(f"Средний кост: {last_snap.mean_cost}")
    print(f"Лучшее решение: {last_snap.best_individual}")
# def culc_lower_cost(dimensions: list[int]):
    
#     dimensions.sort()
    
#     return len(dimensions)*dimensions[0]*dimensions[1]*dimensions[2]

# def generate_population(pop_size: int, ind_size: int) -> list[list[int]]:

#     # создает популяцию
#     return [generate_individual(ind_size) for _ in range(pop_size)]


# def generate_individual(ind_size: int) -> list[int]:

#     # создает случайную особь (порядок перемножения матриц)
#     # [2, 0, 0] т.е. сначала перемножатся 2 и 3, затем 0 и 1 и т.д
#     # номер перемножаемой матрицы в текущем списке размерностей(гены)
#     # ind_size - 3 - i потому что с каждой итерацией колво размерностей уменьшается на 1
#     return [rd.randint(0, ind_size - 1 - i) for i in range(ind_size)]


# def is_valid_individual(individual: list[int], n: int) -> bool:

#     # проверка по принципу генерации
#     if len(individual) != n - 2:
#         return False

#     return all(0 <= val <= (n - 3 - i) for i, val in enumerate(individual))


# def calculate_cost(dimensions: list[int], individual: list[int]) -> int:

#     # считает колво операций по особи
#     cost = 0
#     cur_dim = dimensions.copy()

#     for idx in individual:
#         # перемножение двух матриц cur_dim[n]xcur_dim[n+1] * cur_dim[n+1]xcur_dim[n+2]
#         cost += cur_dim[idx] * cur_dim[idx + 1] * cur_dim[idx + 2]
#         # остается матрица размерности cur_dim[n]xcur_dim[n+2]
#         cur_dim.pop(idx + 1)
#     return cost


# def tournament(
#     population: list[list[int]], dim: list[int], tournament_size: int = 3
# ) -> list[int]:

#     # выбирается лучший вариант из трех' участников турика
#     if tournament_size is None:
#         tournament_size = 3
#     candidates = rd.choices(population, k=tournament_size)
#     return min(candidates, key=lambda ind: calculate_cost(dim, ind))


# def mutate(individual: list[int], p_m: float | None = None) -> list[int]:

#     # мутация - новый случайный возможный ген (номер перемножаемой матрицы)
#     ind_size = len(individual)
#     if p_m is None:
#         p_m = 1 / ind_size if ind_size != 0 else 0.1

#     # по каждому гену проходимся и с шансом меняем
#     for i in range(ind_size):
#         if rd.random() < p_m:
#             individual[i] = rd.randint(0, ind_size - 1 - i)

#     return individual


# def crossover(
#     first_parent: list[int], second_parent: list[int]
# ) -> tuple[list[int], list[int]]:

#     # метод скрещивания - одноточечное
#     # выдает корректных детей потому что гены задаются одинаково для обмениваемых позиций =>
#     # не будет некорректного гена
#     i = rd.randint(1, len(first_parent) - 1)
#     return (first_parent[:i] + second_parent[i:], second_parent[:i] + first_parent[i:])


# def selection(
#     population: list[list[int]],
#     dim: list[int],
#     tournament_size: int = 3,
#     p_m: float | None = 0.1,
#     p_c: float | None = 0.8,
# ) -> list[list[int]]:

#     # селекция)
#     next_population = []
#     len_next_population = 0
    
#     # скрещивание с шансом
#     if p_c is None:
#         p_c = 0.8

#     len_old_population = len(population)
    
#     count_new_ind = int(len_old_population*0.1) + 1
#     ind_size = len(population[0])
    
#     # пока хз
#     """ for _ in range(count_new_ind - 1):
#         next_population.append(generate_individual(ind_size=ind_size))
#         len_next_population += 1 """
    
#     # пока популяция не фуловая
#     while len_next_population < len_old_population:
#         # выбор двух родителей независимо
#         first_parent = tournament(population, dim, tournament_size)
#         second_parent = tournament(population, dim, tournament_size)

#         if rd.random() < p_c:
#             first_child, second_child = crossover(first_parent, second_parent)
#         else:
#             first_child = first_parent.copy()
#             second_child = second_parent.copy()

#         # добавляем с мутацией
#         next_population.append(mutate(first_child, p_m))
#         len_next_population += 1

#         # чтобы не переполнить при нечетном размере популяции
#         if len_next_population < len_old_population:
#             next_population.append(mutate(second_child, p_m))
#             len_next_population += 1
    
#     return next_population


# def genetic_algorithm(
#     population_size: int,
#     dim_size: int,
#     steps: int,
#     tournament_size: int | None = None,
#     p_m: float | None = None,
#     p_c: float | None = None,
#     population: list[list[int]] | None = None,
#     dimensions: list[int] | None = None,
#     cur_generation_offset: int = 0,
# ) -> tuple[list[GenerationSnapshot], int]:

#     if not dimensions:
#         dimensions = pairs_to_dimensions(get_random_matrices(dim_size - 1))

#     if len(dimensions) < 32:
#         # точное значение лучшего решения
#         min_cost = calculate_min_cost(dimensions)
#     else:
#         # верхняя оценка - цена полученная жадным алгоритмом =>
#         # если график лучшего индивида га выше линии target то алгоритм норм отработал
        
#         # при больших колвах матриц нужны большие популяции и много поколений
#         # для того чтобы алгоритм мог отработать нормально
#         min_cost = greedy_cost(dimensions)
    
#     history: list[GenerationSnapshot] = []

#     # если не задана популяция
#     if population is None:
#         population = generate_population(population_size, dim_size-2)

#     # делаем заданное колво эволюций
#     for step_idx in range(steps):
#         gen_number = step_idx + cur_generation_offset + 1
        
#         costs = [calculate_cost(dimensions, ind) for ind in population]
#         best_cost = min(costs)
#         best_ind = population[costs.index(best_cost)].copy()
        
#         history.append(
#             GenerationSnapshot(
#                 generation=gen_number,
#                 best_cost=best_cost,
#                 mean_cost=sum(costs) / population_size,
#                 best_individual=best_ind.copy(),
#                 population=[ind.copy() for ind in population],
#             )
#         )
        
#         """ if best_cost <= min_cost:
#             break """
        
#         population = selection(population, dimensions, tournament_size, p_m, p_c)
#         population[0] = best_ind

#     return history, min_cost

# TODO пофиксить, чтобы сходился при dim_size > 50
# для идеала надо менять принцип кодирования индивидов, но чет западло)
