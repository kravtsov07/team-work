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

        self.first_param = QSpinBox()
        self.first_param.setValue(100)
        self.first_param.setRange(1, 200)
        form_layout.addRow("Lorem One", self.first_param)
        self.setLayout(form_layout)

        self.second_param = QSpinBox()
        self.second_param.setValue(100)
        self.second_param.setRange(1, 200)
        form_layout.addRow("Lorem Two", self.second_param)
        self.setLayout(form_layout)

        self.third_param = QSpinBox()
        self.third_param.setValue(100)
        self.third_param.setRange(1, 200)
        form_layout.addRow("Lorem Three", self.third_param)
        self.setLayout(form_layout)

        self.fourth_param = QSpinBox()
        self.fourth_param.setValue(100)
        self.fourth_param.setRange(1, 200)
        form_layout.addRow("Lorem Four", self.fourth_param)
        self.setLayout(form_layout)

    def get_params(self):
        return Params(
            first=self.first_param.value(),
            second=self.second_param.value(),
            third=self.third_param.value(),
            fourth=self.fourth_param.value(),
        )
