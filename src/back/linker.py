from dataclasses import dataclass

from src.back.GA import GeneticAlgorithm
from src.back.helpers import PlottingData
from src.back.helpers import pairs_to_dimensions
from src.gui.pages.param_setter import Params

def get_plot_data(matrices: list[list[int]], params: Params) -> PlottingData:

    dimensions = pairs_to_dimensions(matrices)

    ga = GeneticAlgorithm(dimensions=dimensions)
    
    ga.set_p_c(params.crossover_rate)
    ga.set_p_m(params.mutation_rate)
    ga.evolution(steps=params.steps, population_size=params.population_size)

    return ga.get_plot_data()