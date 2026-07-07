from enum import Enum

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)


class Choice(Enum):
    CHOICE_RANDOM = 0
    CHOICE_FILE = 1
    CHOICE_MANUAL = 2


class ChoicePage(QWidget):
    """Страница выбора вида входных данных"""

    next_clicked = Signal(object, str)  # (Choice, file_path)
    back_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_file_path = ""
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Выберите вид входных данных:")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        self.choice_group = QButtonGroup(self)

        choices = [
            "Сгенерировать случайные матрицы",
            "Загрузить файл с матрицами",
            "Ввести матрицы вручную",
        ]

        self.radio_buttons = []

        for choice in Choice:
            radio = QRadioButton(choices[choice.value])
            layout.addWidget(radio)

            self.choice_group.addButton(radio, choice.value)
            self.radio_buttons.append(radio)

            if choice == Choice.CHOICE_FILE:
                file_layout = QHBoxLayout()
                file_layout.addSpacing(30)

                self.file_path_edit = QLineEdit()
                self.file_path_edit.setReadOnly(True)
                self.file_path_edit.setPlaceholderText("Файл не выбран")
                file_layout.addWidget(self.file_path_edit, 1)

                browse_button = QPushButton("Выбрать файл")
                browse_button.clicked.connect(self._browse_file)
                file_layout.addWidget(browse_button)

                layout.addLayout(file_layout)

                radio.toggled.connect(
                    lambda checked, edit=self.file_path_edit, browse=browse_button: (
                        self._toggle_file_selector(checked, edit, browse)
                    )
                )

                self.file_path_edit.setVisible(False)
                browse_button.setVisible(False)

        self.radio_buttons[0].setChecked(True)

        layout.addStretch()

        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.back_clicked)

        next_button = QPushButton("Далее")
        next_button.clicked.connect(self._on_next_clicked)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(back_button)
        button_layout.addWidget(next_button)
        button_layout.addStretch()
        layout.addLayout(button_layout)

    def _toggle_file_selector(self, checked, file_edit, browse_button):
        file_edit.setVisible(checked)
        browse_button.setVisible(checked)

        if not checked:
            self.selected_file_path = ""
            file_edit.clear()

    def _browse_file(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Выберите файл с матрицами")
        file_dialog.setNameFilter("Текстовые файлы (*.txt);;Все файлы (*)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.selected_file_path = selected_files[0]
                self.file_path_edit.setText(self.selected_file_path)

    def _on_next_clicked(self):
        selected_choice = Choice(self.choice_group.checkedId())

        if selected_choice == Choice.CHOICE_FILE and not self.selected_file_path:
            return

        self.next_clicked.emit(selected_choice, self.selected_file_path)
