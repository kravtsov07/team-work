from src.back.GA import GeneticAlgorithm
from src.back.helpers import PlottingData
from src.back.helpers import pairs_to_dimensions
from src.gui.pages.param_setter import Params

def get_plot_data(matrices: list[list[int]], params: Params) -> PlottingData:

    dimensions = pairs_to_dimensions(matrices)

    ga = GeneticAlgorithm(dimensions=dimensions)
    
    ga.set_params(params=params)
    
    ga.evolution(steps=params.steps)

    return ga.get_plot_data()