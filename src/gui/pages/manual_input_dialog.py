from PySide6.QtCore import Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QVBoxLayout,
)


class ManualInputDialog(QDialog):
    """Диалог ручного ввода цепочки матриц.

    Раньше это была отдельная страница мастера (ManualInputPage) с сигналами
    next_clicked/back_clicked. Теперь это модальное окно: пользователь жмёт
    "Редактировать вручную" на DataSourcePanel, здесь набирает цепочку,
    жмёт "Готово", и итоговый список матриц возвращается через get_matrices().
    """

    def __init__(self, parent=None, initial_matrices: list[list[int]] | None = None):
        super().__init__(parent)
        self.setWindowTitle("Ввод матриц вручную")
        self.setMinimumWidth(420)
        self.matrices: list[list[int]] = list(initial_matrices or [])
        self._setup_ui()
        self._reload_list()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        hint = QLabel(
            "Для перемножения цепочки матриц важны только их размеры.\n"
            "Укажите высоту и ширину очередной матрицы и нажмите '+'.\n"
            "Цепочка должна оставаться валидной на каждом шаге.\n"
            "Пример: A: 11 x 2, B: 2 x 3, C: 4 x 11 и так далее"
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

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.button_box.button(QDialogButtonBox.StandardButton.Ok).setText("Готово")
        self.button_box.button(QDialogButtonBox.StandardButton.Cancel).setText("Отмена")
        self.button_box.accepted.connect(self._on_accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        self._update_status()

    # TODO: проверить, возможно слишком дорого обходится
    def _reload_list(self):
        self.matrices_list_widget.clear()
        for i, (rows, cols) in enumerate(self.matrices, start=1):
            self.matrices_list_widget.addItem(f"Матрица {i}: {rows} x {cols}")

    def _current_dimensions_are_valid(self):
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
        self.status_label.clear()
        self._update_status()

    def _on_add_clicked(self):
        if not self._current_dimensions_are_valid():
            return

        rows = int(self.height_edit.text())
        cols = int(self.width_edit.text())

        if self.matrices and rows != self.matrices[-1][1]:
            if self.matrices and cols == self.matrices[0][0]:
                self.matrices = [[rows, cols]] + self.matrices
            else:
                self.status_label.setText("Данные матрицы невозможно перемножить")
                self.status_label.setStyleSheet("color: red;")
                return
        else:
            self.matrices.append([rows, cols])

        self._reload_list()

        self.height_edit.clear()
        self.width_edit.clear()
        self.add_button.setEnabled(False)
        self.height_edit.setFocus()

        self._update_status()

    def _on_remove_last_clicked(self):
        if not self.matrices:
            return
        self.matrices.pop()
        self._reload_list()
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

        self.button_box.button(QDialogButtonBox.StandardButton.Ok).setEnabled(
            enough_matrices
        )

    def _on_accept(self):
        if len(self.matrices) < 2:
            return
        self.accept()

    def get_matrices(self) -> list[list[int]]:
        return self.matrices
