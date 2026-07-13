import random as rd

from src.back.helpers import (
    GenerationSnapshot,
    PlottingData,
    calculate_min_cost,
    greedy_cost,
)
from src.gui.pages.param_setter import Params

# по сути generation - x
# best_cost, mean_cost - y


class GeneticAlgorithm:
    def __init__(self, dimensions: list[int]):
        self.dimensions: list[int] = dimensions  # размерности матриц
        self.dims_size: int = len(
            dimensions
        )  # колво размерностей матриц (matr_size = dim_size - 1)
        self.ind_size: int = self.dims_size - 2  # размер индивида
        self.population: list[
            list[int]
        ] = []  # последняя популяция (history[cur_gen].population)
        self.population_size: int = 0  # размер популяции
        self.p_m: float = 1 / (len(dimensions) - 2)  # вероятность мутации
        self.p_c: float = 0.8  # вероятность скрещивания
        self.tournament_size = 3  # размер турика
        self.cur_generation: int = 0  # номер последней генерации
        self.history: dict[int, GenerationSnapshot] = {}  # история поколений

    def set_params(self, params: Params):
        self.set_p_c(params.crossover_rate)
        self.set_p_m(params.mutation_rate)
        self.set_population_size(params.population_size)

    def set_population_size(self, pop_size: int):
        if pop_size >= self.population_size:
            self.population.extend([self._generate_individual() for _ in range(pop_size - self.population_size)])
        else:
            self.population.sort(key=lambda ind: self._calculate_cost(ind))
            self.population = self.population[:pop_size]
        self.population_size = pop_size

    def set_p_c(self, p_c: float):
        self.p_c = p_c

    def set_p_m(self, p_m: float):
        self.p_m = p_m

    def set_tournament_size(self, tournament_size: int):
        self.tournament_size = tournament_size

    def get_min_cost(self):
        # точное значение лучшего решения
        return calculate_min_cost(self.dimensions)

    def get_greedy_cost(self):
        # верхняя оценка - цена полученная жадным алгоритмом =>
        # если график лучшего индивида га выше линии target то алгоритм норм отработал

        # при больших колвах матриц нужны большие популяции и много поколений
        # для того чтобы алгоритм мог отработать нормально
        return greedy_cost(self.dimensions)

    # целевая функция
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
        return (
            first_parent[:i] + second_parent[i:],
            second_parent[:i] + first_parent[i:],
        )

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

    def evolution(self, steps: int):
        if not self.population:
            if self.population_size == 0:
                self.population_size = 100
            self._generate_population(self.population_size)
        # делаем заданное колво эволюций
        for _ in range(steps):
            self.cur_generation += 1
            costs = [self._calculate_cost(ind) for ind in self.population]
            best_cost = min(costs)
            best_ind = self.population[costs.index(best_cost)].copy()

            self.history[self.cur_generation] = GenerationSnapshot(
                generation=self.cur_generation,
                best_cost=best_cost,
                mean_cost=sum(costs) / self.population_size,
                best_individual=best_ind.copy(),
                population=[ind.copy() for ind in self.population],
            )

            self._selection()
            self.population[rd.randint(0, self.population_size - 1)] = best_ind

    def go_first_generate(self):
        if self.cur_generation < 1:
            print("чуваки ни шагу назад")
        self.cur_generation = 1
        self.population = [ind.copy() for ind in self.history[1].population]

    def go_prev_generate(self):
        self.degradation(steps=1)

    def go_next_generate(self):
        if self.population:
            self.evolution(steps=1)
        else:
            print("задайте размер популяции гнилы еб*ные")

    def go_last_generate(self, number_last_gen: int):
        if number_last_gen < self.cur_generation: return
        
        self.evolution(number_last_gen - self.cur_generation)

    def degradation(self, steps: int):
        self.cur_generation = max(0, self.cur_generation - steps)
        if self.cur_generation > 0 and self.cur_generation in self.history:
            self.population = [
                ind.copy() for ind in self.history[self.cur_generation].population
            ]

    def get_history(self):
        # for value in history.values:
        # value: GenerationSnapshot ну и там делаете графики
        return dict(list(self.history.items())[: self.cur_generation])

    def get_plot_data(self) -> PlottingData:
        return PlottingData(
            x=[snap.generation for snap in self.get_history().values()],
            target_cost=self.get_min_cost(),
            greedy_cost=self.get_greedy_cost(),
            best_cost=[snap.best_cost for snap in self.get_history().values()],
            mean_cost=[snap.mean_cost for snap in self.get_history().values()],
            best_order=self.get_history()[self.cur_generation].best_individual,
        )