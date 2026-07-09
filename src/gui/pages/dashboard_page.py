import pyqtgraph as pg
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from src.back.linker import get_plot_data
from src.gui.pages.choice_board import ChoiceBoard
from src.gui.pages.param_setter import ParamSetter
from src.gui.pages.results_panel import ResultsPanel


# TODO: подумать убирать ли вступительную страницу и юзать тока дашбоард
class DashboardPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.matrices: list[list[int]] = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        splitter = QSplitter()

        # Лево
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        self.choice_board = ChoiceBoard()
        left_layout.addWidget(self.choice_board)

        self.param_setter = ParamSetter()
        left_layout.addWidget(self.param_setter)

        left_layout.addStretch()
        left_widget.setMinimumWidth(320)
        left_widget.setMaximumWidth(420)
        splitter.addWidget(left_widget)

        layout.addWidget(splitter)

        # Право
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Динамика сходимости генетического алгоритма")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(title)

        pg.setConfigOption("background", "w")
        pg.setConfigOption("foreground", "k")
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel("left", "Приближенность к целевому")
        self.plot_widget.setLabel("bottom", "Поколение")
        self.plot_widget.showGrid(x=True, y=True)
        right_layout.addWidget(self.plot_widget, 1)

        self.result_page = ResultsPanel()
        right_layout.addWidget(self.result_page)

        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

    def _refresh_plot(self):
        plot_data = get_plot_data(self.matrices)

        self.plot_widget.clear()
        self.plot_widget.addLegend(offset=(10, 10))

        # график лучшего значения
        self.plot_widget.plot(
            plot_data.x,
            [plot_data.target_cost / best_cost for best_cost in plot_data.best_cost],
            pen=pg.mkPen(color="dodgerblue", width=3),
            name="Лучшее значение поколения",
        )

        # график среднего значения
        self.plot_widget.plot(
            plot_data.x,
            [plot_data.target_cost / mean_cost for mean_cost in plot_data.mean_cost],
            pen=pg.mkPen(color="lightcoral", width=3),
            name="Среднее значение поколения",
        )

        self.plot_widget.plot(
            plot_data.x,
            [1] * len(plot_data.x),
            pen=pg.mkPen(color="magenta", width=3),
            name="Целевое отношение",
        )
