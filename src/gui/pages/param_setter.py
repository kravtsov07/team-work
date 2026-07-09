from dataclasses import dataclass

from PySide6.QtWidgets import QFormLayout, QGroupBox, QSpinBox


@dataclass
class Params:
    first: int
    second: int
    third: int
    fourth: int


class ParamSetter(QGroupBox):
    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self):
        form_layout = QFormLayout()
        first_param = QSpinBox()
        first_param.setValue(100)
        first_param.setRange(1, 200)
        form_layout.addRow("Lorem One", first_param)
        self.setLayout(form_layout)

        second_param = QSpinBox()
        second_param.setValue(100)
        second_param.setRange(1, 200)
        form_layout.addRow("Lorem Two", second_param)
        self.setLayout(form_layout)

        third_param = QSpinBox()
        third_param.setValue(100)
        third_param.setRange(1, 200)
        form_layout.addRow("Lorem Three", third_param)
        self.setLayout(form_layout)

        fourth_param = QSpinBox()
        fourth_param.setValue(100)
        fourth_param.setRange(1, 200)
        form_layout.addRow("Lorem Four", fourth_param)
        self.setLayout(form_layout)

    def get_params(self):
        return
