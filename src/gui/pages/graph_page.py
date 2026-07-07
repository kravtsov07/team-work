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

        title = QLabel("Визуализация")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        note = QLabel(
            "Случайные данные для демонстрации виджета графика.\n"
            "В дальнейшем здесь будет отображаться реальный результат "
            "работы генетического алгоритма."
        )
        note.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(note)

        pg.setConfigOption("background", "w")
        pg.setConfigOption("foreground", "k")
        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setLabel("left", "Значение")
        self.plot_widget.setLabel("bottom", "Поколение")
        self.plot_widget.showGrid(x=True, y=True)
        layout.addWidget(self.plot_widget)

        regenerate_button = QPushButton("Сгенерировать заново")
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

    def set_data(self, matrices: list[dict]):
        self.matrices = matrices
        self._refresh_plot()

    def _refresh_plot(self):
        plot_data = get_plot_data(self.matrices)

        self.plot_widget.clear()
        self.plot_widget.plot(
            plot_data.x,
            plot_data.best_cost,
            pen=pg.mkPen(width=2),
            symbol="o",
        )
