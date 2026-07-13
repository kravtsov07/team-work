from dataclasses import dataclass

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPen
from PySide6.QtWidgets import (
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QSpinBox,
)


@dataclass
class Params:
    population_size: int
    steps: int
    mutation_rate: float
    crossover_rate: float


TOOLTIP_MAP = {
    "population": (
        "Количество особей, участвующих в каждом поколении.\n\n"
        " - Большая популяция повышает разнообразие решений и вероятность "
        "найти лучший маршрут.\n"
        " - Слишком большое значение увеличивает время работы алгоритма."
    ),
    "generation": (
        "Максимальное количество поколений, которое создаст алгоритм.\n\n"
        " - Большее число поколений позволяет улучшить решение.\n"
        " - Увеличение значения приводит к более длительным вычислениям."
    ),
    "mutation": (
        "Вероятность случайного изменения потомка (от 0 до 1).\n\n"
        " - Небольшая мутация помогает избежать застревания в локальном оптимуме.\n"
        " - Слишком высокая вероятность может разрушать хорошие решения.\n"
        " - Рекомендуемое значение: 0.01–0.1."
    ),
    "crossover": (
        "Вероятность применения операции скрещивания к паре родителей (от 0 до 1).\n\n"
        " - Скрещивание позволяет объединять удачные части решений.\n"
        " - Обычно используется значение 0.7–0.9."
    ),
}


class GAParamsPanel(QGroupBox):
    """Настройки генетического алгоритма."""

    def __init__(self, parent=None):
        super().__init__("Параметры генетического алгоритма", parent)
        self._setup_ui()

    @staticmethod
    def make_hint_label(text: str, tooltip: str) -> QLabel:
        return HintLabel(text, tooltip)

    def set_default_values(self) -> None:
        self.population_spin.setValue(200)
        self.generations_spin.setValue(100)
        self.mutation_spin.setValue(0.01)
        self.crossover_spin.setValue(0.8)

    def _setup_ui(self) -> None:
        form = QFormLayout(self)

        # Размер популяции
        self.population_spin = QSpinBox()
        self.population_spin.setRange(10, 1000)
        self.population_spin.setValue(200)

        population_text = "Размер популяции:"
        population_label = self.make_hint_label(
            population_text, TOOLTIP_MAP["population"]
        )

        form.addRow(population_label, self.population_spin)

        # Число поколений
        self.generations_spin = QSpinBox()
        self.generations_spin.setRange(10, 1000)
        self.generations_spin.setValue(100)

        generation_text = "Число поколений:"
        generation_label = self.make_hint_label(
            generation_text, TOOLTIP_MAP["generation"]
        )

        form.addRow(generation_label, self.generations_spin)

        # Вероятность мутации
        self.mutation_spin = QDoubleSpinBox()
        self.mutation_spin.setRange(0.0, 1.0)
        self.mutation_spin.setSingleStep(0.01)
        self.mutation_spin.setValue(0.01)

        mutation_text = "Вероятность мутации:"
        mutation_label = self.make_hint_label(mutation_text, TOOLTIP_MAP["mutation"])
        form.addRow(mutation_label, self.mutation_spin)

        # Вероятность скрещивания
        self.crossover_spin = QDoubleSpinBox()
        self.crossover_spin.setRange(0.0, 1.0)
        self.crossover_spin.setSingleStep(0.01)
        self.crossover_spin.setValue(0.8)

        crossover_text = "Вероятность скрещивания:"
        crossover_label = self.make_hint_label(crossover_text, TOOLTIP_MAP["crossover"])
        form.addRow(crossover_label, self.crossover_spin)

    def get_params(self) -> Params:
        return Params(
            population_size=self.population_spin.value(),
            steps=self.generations_spin.value(),
            mutation_rate=self.mutation_spin.value(),
            crossover_rate=self.crossover_spin.value(),
        )


class HintLabel(QLabel):
    def __init__(self, text: str, tooltip: str, parent=None) -> None:
        super().__init__(text, parent)
        self.setToolTip(tooltip)
        self.setCursor(Qt.CursorShape.WhatsThisCursor)
        self.setContentsMargins(0, 0, 0, 3)

    def paintEvent(self, event) -> None:
        super().paintEvent(event)

        text_width = self.fontMetrics().horizontalAdvance(self.text())
        if text_width <= 0:
            return

        painter = QPainter(self)
        pen = QPen()
        pen.setStyle(Qt.PenStyle.DotLine)
        pen.setWidth(1)
        pen.setColor(QColor("#ffF0Ff"))
        painter.setPen(pen)
        y = self.rect().bottom() - 1
        painter.drawLine(0, y, text_width, y)
