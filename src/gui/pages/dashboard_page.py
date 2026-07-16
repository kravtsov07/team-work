import pyqtgraph as pg
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from src.back.GA import GeneticAlgorithm
from src.back.helpers import PlottingData, pairs_to_dimensions
from src.gui.pages.choice_board import ChoiceBoard
from src.gui.pages.param_setter import GAParamsPanel
from src.gui.pages.results_panel import ResultsPanel


class DashboardPage(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.matrices: list[list[int]] = []
        self.plot_data: PlottingData | None = None
        self.gen_line: pg.InfiniteLine | None = None
        self.cur_gen: int = 0
        self.last_gen: int = 0
        self._setup_ui()
        self.ga: GeneticAlgorithm

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        splitter = QSplitter()

        # Лево
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        self.choice_board = ChoiceBoard()
        left_layout.addWidget(self.choice_board)

        self.param_setter = GAParamsPanel()
        left_layout.addWidget(self.param_setter)

        button_layout = QHBoxLayout()
        self.generate_button = QPushButton("Запустить алгоритм")
        self.generate_button.setStyleSheet("background-color: green")
        self.generate_button.clicked.connect(self._on_generate_clicked)
        self.refresh_button = QPushButton("Значения по умолчанию")
        self.refresh_button.clicked.connect(self._on_refresh_clicked)

        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.generate_button)

        left_layout.addLayout(button_layout)

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

        self.gen_label = QLabel("Поколение: ...")
        self.gen_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(self.gen_label)

        player_layout = QHBoxLayout()  # Кнопки плеера
        self.first_step_button = QPushButton("«")
        self.prev_step_button = QPushButton("<")
        self.next_step_button = QPushButton(">")
        self.last_step_button = QPushButton("»")

        self._player_buttons = (
            self.first_step_button,
            self.prev_step_button,
            self.next_step_button,
            self.last_step_button,
        )

        self.first_step_button.clicked.connect(self._on_first_step_clicked)
        self.prev_step_button.clicked.connect(self._on_prev_step_clicked)
        self.next_step_button.clicked.connect(self._on_next_step_clicked)
        self.last_step_button.clicked.connect(self._on_last_step_clicked)

        player_layout.addWidget(self.first_step_button)
        player_layout.addWidget(self.prev_step_button)
        player_layout.addWidget(self.next_step_button)
        player_layout.addWidget(self.last_step_button)
        right_layout.addLayout(player_layout)

        self._set_player_enabled(False)

        self.result_page = ResultsPanel()
        right_layout.addWidget(self.result_page)

        splitter.addWidget(right_widget)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)

    def _validate_input(self):
        if len(self.matrices) < 3:
            QMessageBox.warning(self, "Invalid input", "Задайте матрицы")
            return False
        return True

    def _on_generate_clicked(self):
        matr = self.choice_board.get_matrices()

        if self.matrices != matr and matr:
            self.matrices = matr
            self.ga = GeneticAlgorithm(pairs_to_dimensions(self.matrices))

        params = self.param_setter.get_params()
        if not self._validate_input():
            return
        self.ga.set_params(params)
        self.ga.evolution(params.steps)

        plot_data = self.ga.get_plot_data()
        self._refresh_plot(plot_data)

    def _set_player_enabled(self, enabled: bool) -> None:
        for button in self._player_buttons:
            button.setEnabled(enabled)

    def _update_player_buttons(self) -> None:
        at_first = self.cur_gen <= 1

        self.first_step_button.setEnabled(not at_first)
        self.prev_step_button.setEnabled(not at_first)
        self.next_step_button.setEnabled(True)
        self.last_step_button.setEnabled(True)

    def _on_refresh_clicked(self):
        self.param_setter.set_default_values()

    def _on_first_step_clicked(self):
        self.ga.go_first_generate()
        self._refresh_plot(self.ga.get_plot_data())

    def _on_prev_step_clicked(self):
        self.ga.go_prev_generate()
        self._refresh_plot(self.ga.get_plot_data())

    def _on_next_step_clicked(self):
        self.ga.go_next_generate()
        self._refresh_plot(self.ga.get_plot_data())

    def _on_last_step_clicked(self):
        params = self.param_setter.get_params()
        self.ga.go_last_generate(params.steps)
        self._refresh_plot(self.ga.get_plot_data())

    def _refresh_plot(self, plot_data: PlottingData):
        self.plot_widget.clear()
        self.gen_line = None
        self.plot_widget.addLegend(offset=(10, 10))

        self.plot_widget.plot(
            plot_data.x,
            [plot_data.target_cost / c for c in plot_data.best_cost],
            pen=pg.mkPen(color="dodgerblue", width=3),
            name="Лучшее значение поколения",
        )
        self.plot_widget.plot(
            plot_data.x,
            [plot_data.target_cost / c for c in plot_data.mean_cost],
            pen=pg.mkPen(color="lightcoral", width=3),
            name="Среднее значение поколения",
        )

        # график точного минимума
        self.plot_widget.plot(
            plot_data.x,
            [1] * len(plot_data.x),
            pen=pg.mkPen(color="magenta", width=3),
            name="Целевое отношение",
        )

        self.plot_widget.plot(
            plot_data.x,
            [plot_data.target_cost / plot_data.greedy_cost] * len(plot_data.x),
            pen=pg.mkPen(color="green", width=3),
            name="Верхняя оценка",
        )

        self.result_page.update_results(plot_data)

        self.cur_gen = self.ga.cur_generation
        self.last_gen = len(self.ga.history)
        self._update_label()
        self._update_player_buttons()

    def _update_label(self) -> None:
        self.gen_label.setText(f"Поколение: {self.cur_gen}")
