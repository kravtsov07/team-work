from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ManualInputPage(QWidget):
    """Страница ручного ввода матриц"""

    next_clicked = Signal(list)
    back_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.matrices = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Введите размеры матриц вручную")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        hint = QLabel(
            "Для перемножения цепочки матриц важны только их размеры.\n"
            "Укажите высоту (кол-во строк) и ширину (кол-во столбцов) "
            'очередной матрицы и нажмите "+", чтобы добавить её в цепочку.'
        )
        hint.setWordWrap(True)
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(hint)

        dims_layout = QHBoxLayout()

        dims_layout.addWidget(QLabel("Высота:"))
        self.height_edit = QLineEdit()
        self.height_edit.setPlaceholderText("например, 2")
        self.height_edit.setValidator(QIntValidator(1, 9999, self))
        self.height_edit.textChanged.connect(self._update_add_button_state)
        dims_layout.addWidget(self.height_edit)

        dims_layout.addWidget(QLabel("Ширина:"))
        self.width_edit = QLineEdit()
        self.width_edit.setPlaceholderText("например, 11")
        self.width_edit.setValidator(QIntValidator(1, 9999, self))
        self.width_edit.textChanged.connect(self._update_add_button_state)
        dims_layout.addWidget(self.width_edit)

        self.add_button = QPushButton("+")
        self.add_button.setEnabled(False)
        self.add_button.clicked.connect(self._on_add_clicked)
        dims_layout.addWidget(self.add_button)

        layout.addLayout(dims_layout)

        self.matrices_list_widget = QListWidget()
        layout.addWidget(self.matrices_list_widget)

        remove_last_button = QPushButton("Удалить последнюю")
        remove_last_button.clicked.connect(self._on_remove_last_clicked)
        layout.addWidget(remove_last_button)

        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)

        layout.addStretch()

        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.back_clicked)

        self.next_button = QPushButton("Далее")
        self.next_button.setEnabled(False)
        self.next_button.clicked.connect(self._on_next_clicked)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(back_button)
        button_layout.addWidget(self.next_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

        self._update_status()

    def _current_dimensions_are_valid(self):
        """Проверяет, что оба поля ввода сейчас содержат положительные целые."""
        height_text = self.height_edit.text().strip()
        width_text = self.width_edit.text().strip()
        if not height_text or not width_text:
            return False
        try:
            return int(height_text) > 0 and int(width_text) > 0
        except ValueError:
            return False

    def _update_add_button_state(self):
        self.add_button.setEnabled(self._current_dimensions_are_valid())

    def _on_add_clicked(self):
        if not self._current_dimensions_are_valid():
            return

        rows = int(self.height_edit.text())
        cols = int(self.width_edit.text())

        if self.matrices and rows != self.matrices[-1][1]:
            self.status_label.setText("Данные матрицы невозможно перемножить")
            self.status_label.setStyleSheet("color: red;")
            return

        self.matrices.append((rows, cols))
        self.matrices_list_widget.addItem(
            f"Матрица {len(self.matrices)}: {rows} x {cols}"
        )

        self.height_edit.clear()
        self.width_edit.clear()
        self.add_button.setEnabled(False)
        self.height_edit.setFocus()

        self._update_status()

    def _on_remove_last_clicked(self):
        if not self.matrices:
            return
        self.matrices.pop()
        self.matrices_list_widget.takeItem(self.matrices_list_widget.count() - 1)
        self._update_status()

    def _update_status(self):
        enough_matrices = len(self.matrices) >= 2

        if not self.matrices:
            self.status_label.setText("Добавьте хотя бы 2 матрицы для перемножения.")
            self.status_label.setStyleSheet("color: gray;")
        elif not enough_matrices:
            self.status_label.setText("Нужно хотя бы 2 матрицы.")
            self.status_label.setStyleSheet("color: gray;")
        else:
            self.status_label.setText("Можно считать.")
            self.status_label.setStyleSheet("color: green;")

        self.next_button.setEnabled(enough_matrices)

    def _on_next_clicked(self):
        if not self.next_button.isEnabled():
            return
        payload = [{"rows": rows, "cols": cols} for rows, cols in self.matrices]
        self.next_clicked.emit(payload)
