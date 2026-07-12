from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFormLayout, QGroupBox, QLabel, QPushButton

from src.back.linker import PlottingData
from src.gui.pages.mult_order import MultOrder


class ResultsPanel(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Результаты", parent)
        self._setup_ui()
        self.clear()

    def _setup_ui(self):
        form = QFormLayout(self)

        self.best_cost_label = QLabel()
        form.addRow("Лучшая стоимость:", self.best_cost_label)

        self.ratio_label = QLabel()
        form.addRow("Отношение к целевому:", self.ratio_label)

        self.converged_label = QLabel()
        form.addRow("Сошлось на поколении:", self.converged_label)

        self.order_label = QLabel()
        self.order_label.setWordWrap(True)
        form.addRow("Порядок умножения:", self.order_label)

        self.show_tree_button = QPushButton("Показать дерево умножения")
        self.show_tree_button.setEnabled(False)
        self.show_tree_button.clicked.connect(self._show_mult_tree)
        form.addRow(self.show_tree_button)

    def clear(self):
        self.best_cost_label.setText("—")
        self.ratio_label.setText("—")
        self.converged_label.setText("—")
        self.order_label.setText("—")

    def update_results(self, plot_data: PlottingData):
        if not plot_data.best_cost:
            self.clear()
            return

        best_cost = plot_data.best_cost[-1]
        self.best_cost_label.setText(f"{best_cost:,}".replace(",", " "))

        ratio = plot_data.target_cost / best_cost if best_cost else 0
        self.ratio_label.setText(f"{ratio:.3f}")

        best_so_far = min(plot_data.best_cost)
        converged_gen = next(
            gen
            for gen, cost in zip(plot_data.x, plot_data.best_cost)
            if cost == best_so_far
        )
        self.converged_label.setText(str(converged_gen))

        self.order_label.setText(str(plot_data.best_order))
        self._order = plot_data.best_order
        self.show_tree_button.setEnabled(True)
        self._make_selectable()

    def _make_selectable(self):
        flags = (
            Qt.TextInteractionFlag.TextSelectableByMouse
            | Qt.TextInteractionFlag.TextSelectableByKeyboard
        )

        for label in (
            self.best_cost_label,
            self.ratio_label,
            self.converged_label,
            self.order_label,
        ):
            label.setTextInteractionFlags(flags)

    def _show_mult_tree(self):
        if not self._order:
            return

        dialog = MultOrder(self)
        dialog.set_snapshot(self._order)
        dialog.exec()
