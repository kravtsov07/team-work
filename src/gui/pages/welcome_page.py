from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton


class WelcomePage(QWidget):
    """Страница приветствия"""

    next_clicked = Signal()
    quit_clicked = Signal()

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        hint_text = QLabel(
            "Добро пожаловать в приложение, демонстрирующее\n"
            "генетический алгоритм поиска оптимального перемножения матриц!\n\n"
            "Нажмите 'Далее', чтобы продолжить."
        )
        hint_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(hint_text)
        layout.addStretch()

        quit_button = QPushButton("Выйти")
        quit_button.clicked.connect(self.quit_clicked)

        next_button = QPushButton("Далее")
        next_button.clicked.connect(self.next_clicked)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(quit_button)
        button_layout.addWidget(next_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)
