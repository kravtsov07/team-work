import random

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
import pyqtgraph as pg

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
        # TODO: реальный алгоритм
        self._plot_random_data()

        regenerate_button = QPushButton("Сгенерировать заново")
        regenerate_button.clicked.connect(self._plot_random_data)
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

    def _plot_random_data(self):
        x = list(range(20))
        y = [random.uniform(0, 100) for _ in x]
        self.plot_widget.clear()
        self.plot_widget.plot(
            x, y, pen=pg.mkPen(width=2), symbol="o"
        )
