from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.back.helpers import get_random_matrices, get_data_from_file


class PreviewPage(QWidget):
    next_clicked = Signal(list)
    back_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_path = ""
        self.sample_size = 0
        self.matrices = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Предварительный просмотр")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        hint = QLabel("Полученные матрицы")
        hint.setWordWrap(True)
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(hint)

        self.matrices_list_widget = QListWidget()
        layout.addWidget(self.matrices_list_widget)

        self.retry_button = QPushButton("Повтор")
        self.retry_button.clicked.connect(self.retry_clicked)
        self.retry_button.hide()

        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self._on_back_clicked)

        self.next_button = QPushButton("Далее")
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(self._on_next_clicked)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.retry_button)
        button_layout.addWidget(self.next_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

    def add_text(self, matrices: list[list[int]]):
        i = 0
        for i, (rows, cols) in enumerate(matrices, start=1):
            self.matrices_list_widget.addItem(f"A{i}: {rows} × {cols}")

        return i

    def set_file_path(self, file_path: str):
        self.file_path = file_path
        try:
            self.matrices = get_data_from_file(file_path)
            self.add_text(self.matrices)
            self.next_button.setEnabled(True)

        except ValueError as e:
            self.matrices_list_widget.addItem(f"{e}")

    def set_sample_size(self, sample_size: int):
        self.sample_size = sample_size
        self.matrices = get_random_matrices(matrix_count=self.sample_size)

        self.retry_button.show()
        self.add_text(self.matrices)
        self.next_button.setEnabled(True)

    def retry_clicked(self):
        self.matrices = get_random_matrices(matrix_count=self.sample_size)
        self.matrices_list_widget.clear()
        self.add_text(self.matrices)

    def _on_back_clicked(self):
        self.matrices_list_widget.clear()
        self.next_button.setEnabled(False)
        self.back_clicked.emit()
        self.retry_button.hide()

    def _on_next_clicked(self):
        if not self.next_button.isEnabled():
            return

        self.next_clicked.emit(self.matrices)
