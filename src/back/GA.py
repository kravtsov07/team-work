import random as rd

""" 
n размерностей
n - 1 матриц
n - 2 операций

"""

def generate_dimensions(dim_size: int = 100, min_size: int = 1, max_size: int = 10):
    return [rd.randint(min_size, max_size) for _ in range(dim_size)]

def generate_population(pop_size: int, ind_size: int) -> list[list[int]]:
    return [generate_individual(ind_size) for _ in range(pop_size)]

def generate_individual(ind_size: int):
    return [rd.randint(0, ind_size - 2 - i) for i in range(ind_size - 2)]

def is_valid_individual(individual: list[int], n: int) -> bool:
    if len(individual) != n - 2:
        return False
        
    return all(0 <= val <= (n - 2 - i) for i, val in enumerate(individual))

def calculate_cost(dimensions: list[int], individual: list[int]):
    cost = 0
    cur_dim = dimensions.copy()
    for i in range(len(individual)):
        n = individual[i]
        cost += cur_dim[n] * cur_dim[n + 1] * cur_dim[n + 2]
        cur_dim.pop(n + 1)
    return cost

def tournament(population: list[list[int]], dim: list[int], tournament_size: int = 3) -> list[int]:
    candidates = rd.choices(population, k=tournament_size)
    return min(candidates, key=lambda ind: calculate_cost(dim, ind))

def mutate(individual: list[int], p_m: float = None):
    ind_size = len(individual)
    if p_m == None:
        p_m = 1 / ind_size
        
    for i in range(ind_size):
        if rd.random() < p_m:
            individual[i] = rd.randint(0, ind_size - i)
            
    return individual

def crossover(first_parent: list[int], second_parent: list[int]):
    point = rd.randint(1, len(first_parent) - 1)
    first_child = first_parent[:point] + second_parent[point:] 
    second_child = second_parent[:point] + first_parent[point:]
    return (
        first_child,
        second_child
    )

def selection(population: list[list[int]], dim: list[int], tournament_size: int = 3, p_c: float = 0.8):
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

n = 5

dim = generate_dimensions(n)

ind = generate_individual(n)
print(dim)
print(ind)
print(calculate_cost(dim, ind))