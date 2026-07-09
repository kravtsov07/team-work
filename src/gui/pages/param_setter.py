from dataclasses import dataclass

from PySide6.QtWidgets import QDoubleSpinBox, QFormLayout, QGroupBox, QSpinBox


@dataclass
class Params:
    population_size: int
    steps: int
    mutation_rate: float
    crossover_rate: float


class GAParamsPanel(QGroupBox):
    """Настройки генетического алгоритма."""

    def __init__(self, parent=None):
        super().__init__("Параметры генетического алгоритма", parent)
        self._setup_ui()

    def _setup_ui(self):
        form = QFormLayout(self)

        self.population_spin = QSpinBox()
        self.population_spin.setRange(10, 2000)
        self.population_spin.setValue(100)
        form.addRow("Размер популяции:", self.population_spin)

        self.generations_spin = QSpinBox()
        self.generations_spin.setRange(10, 5000)
        self.generations_spin.setValue(200)
        form.addRow("Число поколений:", self.generations_spin)

        self.mutation_spin = QDoubleSpinBox()
        self.mutation_spin.setRange(0.0, 1.0)
        self.mutation_spin.setSingleStep(0.01)
        self.mutation_spin.setValue(0.05)
        form.addRow("Вероятность мутации:", self.mutation_spin)

        self.crossover_spin = QDoubleSpinBox()
        self.crossover_spin.setRange(0.0, 1.0)
        self.crossover_spin.setSingleStep(0.05)
        self.crossover_spin.setValue(0.8)
        form.addRow("Вероятность скрещивания:", self.crossover_spin)

    def get_params(self) -> Params:
        return Params(
            population_size=self.population_spin.value(),
            steps=self.generations_spin.value(),
            mutation_rate=self.mutation_spin.value(),
            crossover_rate=self.crossover_spin.value(),
        )
