from enum import Enum

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QRadioButton,
    QSpinBox,
    QVBoxLayout,
)

from src.back.helpers import get_data_from_file, get_random_matrices
from src.gui.pages.manual_input_dialog import ManualInputDialog


class Source(Enum):
    RANDOM = 0
    FILE = 1
    MANUAL = 2


class ChoiceBoard(QGroupBox):
    matrices_changed = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.matrices: list[list[int]] = []
        self._setup_ui()
        self._on_source_changed()

    def _setup_ui(self):
        layout = QVBoxLayout()
        self.source_group = QButtonGroup(self)

        # рандом
        random_row = QHBoxLayout()
        self.random_radio = QRadioButton("Случайные матрицы")
        self.random_radio.setChecked(True)
        self.source_group.addButton(self.random_radio, Source.RANDOM.value)
        random_row.addWidget(self.random_radio)

        self.sample_size_spin = QSpinBox()
        # TODO: сделать оповещение об невозможности создания 1-2 матриц вместо этого
        # эт п*здец кринж😊
        self.sample_size_spin.setRange(3, 1000)
        self.sample_size_spin.setValue(20)
        random_row.addWidget(self.sample_size_spin)

        self.generate_button = QPushButton("Сгенерировать")
        self.generate_button.clicked.connect(self._on_generate_clicked)
        random_row.addWidget(self.generate_button)
        random_row.addStretch()
        layout.addLayout(random_row)

        # файл
        file_row = QHBoxLayout()
        self.file_radio = QRadioButton("Загрузить файл")
        self.source_group.addButton(self.file_radio, Source.FILE.value)
        file_row.addWidget(self.file_radio)

        self.file_path_edit = QLineEdit()
        self.file_path_edit.setReadOnly(True)
        self.file_path_edit.setPlaceholderText("Файл не выбран")
        file_row.addWidget(self.file_path_edit, 1)

        self.browse_button = QPushButton("Выбрать файл")
        self.browse_button.clicked.connect(self._on_browse_clicked)
        file_row.addWidget(self.browse_button)
        layout.addLayout(file_row)

        # вручную
        manual_row = QHBoxLayout()
        self.manual_radio = QRadioButton("Ввести вручную")
        self.source_group.addButton(self.manual_radio, Source.MANUAL.value)
        manual_row.addWidget(self.manual_radio)

        self.manual_edit_button = QPushButton("Редактировать вручную")
        self.manual_edit_button.clicked.connect(self._on_manual_edit_clicked)
        manual_row.addWidget(self.manual_edit_button)
        manual_row.addStretch()
        layout.addLayout(manual_row)

        self.source_group.idClicked.connect(self._on_source_changed)

        # общий список + статус
        self.matrices_list_widget = QListWidget()
        self.matrices_list_widget.setMaximumHeight(140)
        layout.addWidget(self.matrices_list_widget)

        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

    def _current_source(self) -> Source:
        return Source(self.source_group.checkedId())

    def _on_source_changed(self, *_):
        source = self._current_source()

        self.sample_size_spin.setEnabled(source is Source.RANDOM)
        self.generate_button.setEnabled(source is Source.RANDOM)

        self.file_path_edit.setEnabled(source is Source.FILE)
        self.browse_button.setEnabled(source is Source.FILE)

        self.manual_edit_button.setEnabled(source is Source.MANUAL)

        self._set_matrices([])
        self.status_label.setText("Настройте источник и получите данные.")
        self.status_label.setStyleSheet("color: gray;")

    def _on_generate_clicked(self):
        amount = self.sample_size_spin.value()
        matrices = get_random_matrices(amount)
        self._set_matrices(matrices)
        self.status_label.setText("Сгенерировано.")
        self.status_label.setStyleSheet("color: green;")

    def _on_browse_clicked(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Выберите файл с матрицами")
        file_dialog.setNameFilter("Текстовые файлы (*.txt);;Все файлы (*)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.selected_file_path = selected_files[0]
                self.file_path_edit.setText(self.selected_file_path)
        else:
            return

        try:
            matrices = get_data_from_file(self.selected_file_path)
        except ValueError as e:
            self._set_matrices([])
            self.status_label.setText(str(e))
            self.status_label.setStyleSheet("color: red;")
            return

        self._set_matrices(matrices)
        self.status_label.setText("Файл загружен.")
        self.status_label.setStyleSheet("color: green;")

    def _on_manual_edit_clicked(self):
        manual_dialog = ManualInputDialog()
        if manual_dialog.exec() == ManualInputDialog.DialogCode.Accepted:
            self._set_matrices(manual_dialog.get_matrices())
            self.status_label.setText("Матрицы успешно заданы.")
            self.status_label.setStyleSheet("color: green;")

    def _set_matrices(self, matrices: list[list[int]]):
        self.matrices = matrices
        self.matrices_list_widget.clear()
        for i, (rows, cols) in enumerate(matrices, start=1):
            self.matrices_list_widget.addItem(f"A{i}: {rows} × {cols}")
        self.matrices_changed.emit(self.matrices)

    def get_matrices(self) -> list[list[int]]:
        return self.matrices
