from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QMainWindow, QStackedWidget

from src.gui.pages.choice_page import Choice, ChoicePage
from src.gui.pages.graph_page import GraphPage
from src.gui.pages.manual_input_page import ManualInputPage
from src.gui.pages.welcome_page import WelcomePage


class MainWindow(QMainWindow):
    """Страницы в QStackedWidget и переходы между ними"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Перемножение матриц")

        # Текущее состояние выбора режима работы
        self.selected_choice_id = None
        self.selected_file_path = ""
        self.manual_matrices = None

        self._setup_pages()
        self._setup_navigation()

        # Стек истории
        self.history = [self.welcome_page]
        self.stacked_widget.setCurrentWidget(self.welcome_page)

    def _setup_pages(self):
        central_stack = QStackedWidget()
        self.setCentralWidget(central_stack)
        self.stacked_widget = central_stack

        self.welcome_page = WelcomePage()
        self.choice_page = ChoicePage()
        self.manual_input_page = ManualInputPage()
        self.graph_page = GraphPage()

        for page in (
            self.welcome_page,
            self.choice_page,
            self.manual_input_page,
            self.graph_page,
        ):
            self.stacked_widget.addWidget(page)

    def _setup_navigation(self):
        self.welcome_page.quit_clicked.connect(QCoreApplication.instance().quit)  # type: ignore
        self.welcome_page.next_clicked.connect(lambda: self._go_to(self.choice_page))

        self.choice_page.next_clicked.connect(self._on_choice_made)
        self.choice_page.back_clicked.connect(self._go_back)

        self.manual_input_page.next_clicked.connect(self._on_manual_matrices_ready)
        self.manual_input_page.back_clicked.connect(self._go_back)

        self.graph_page.next_clicked.connect(self._on_graph_next)
        self.graph_page.back_clicked.connect(self._go_back)

    def _on_choice_made(self, selected_id, file_path):
        self.selected_choice_id = selected_id
        self.selected_file_path = file_path

        if selected_id is Choice.CHOICE_MANUAL:
            self._go_to(self.manual_input_page)
        else:
            # TODO: запуск обработчика
            self._go_to(self.graph_page)

    def _on_manual_matrices_ready(self, matrices):
        self.manual_matrices = matrices
        # TODO: запуск генетического алгоритма
        self.graph_page.set_data(matrices)

        self._go_to(self.graph_page)

    def _on_graph_next(self):
        # TODO: страница с итоговым результатом
        pass

    def _go_to(self, page):
        self.history.append(page)
        self.stacked_widget.setCurrentWidget(page)

    def _go_back(self):
        if len(self.history) > 1:
            self.history.pop()
            self.stacked_widget.setCurrentWidget(self.history[-1])
