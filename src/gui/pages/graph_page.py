import pyqtgraph as pg
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget

from src.back.linker import get_plot_data


class GraphPage(QWidget):
    """Страница с графиком"""

    # TODO: интерфейс для пошагового выполнения алгоритма

    next_clicked = Signal()
    back_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Динамика сходимости генетического алгоритма")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        pg.setConfigOption("background", "w")
        pg.setConfigOption("foreground", "k")
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel("left", "Приближенность к целевому")
        self.plot_widget.setLabel("bottom", "Поколение")
        self.plot_widget.showGrid(x=True, y=True)
        layout.addWidget(self.plot_widget)

        regenerate_button = QPushButton("Перезапустить алгоритм для тех же данных")
        regenerate_button.clicked.connect(self._refresh_plot)
        layout.addWidget(regenerate_button)

        layout.addStretch()

        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.back_clicked)

        next_button = QPushButton("Далее")
        next_button.clicked.connect(self.next_clicked)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(back_button)
        button_layout.addWidget(next_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

    def set_data(self, matrices: list[list[int]]):
        self.matrices = matrices
        self._refresh_plot()

    def _refresh_plot(self):
        plot_data = get_plot_data(self.matrices)

        self.plot_widget.clear()
        self.plot_widget.addLegend(offset=(10, 10))
        
        # график лучшего значения
        self.plot_widget.plot(
            plot_data.x,
            [plot_data.target_cost / best_cost for best_cost in plot_data.best_cost],
            pen=pg.mkPen(color='dodgerblue', width=3),
            name="Лучшее значение поколения"
        )
        
        # график среднего значения
        self.plot_widget.plot(
            plot_data.x,
            [plot_data.target_cost / mean_cost for mean_cost in plot_data.mean_cost],
            pen=pg.mkPen(color='lightcoral', width=3),
            name="Среднее значение поколения"
        )
        
        self.plot_widget.plot(
            plot_data.x,
            [1] * len(plot_data.x),
            pen=pg.mkPen(color='magenta', width=3),
            name="Целевое отношение"
        )
