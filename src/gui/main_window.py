from PySide6.QtCore import QCoreApplication
from PySide6.QtWidgets import QMainWindow, QStackedWidget

from src.gui.pages.dashboard_page import DashboardPage
from src.gui.pages.welcome_page import WelcomePage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Перемножение матриц")
        self.resize(1100, 650)

        self._setup_pages()
        self._setup_navigation()

        self.stacked_widget.setCurrentWidget(self.welcome_page)

    def _setup_pages(self):
        central_stack = QStackedWidget()
        self.setCentralWidget(central_stack)
        self.stacked_widget = central_stack

        self.welcome_page = WelcomePage()
        self.dashboard_page = DashboardPage()

        for page in (self.welcome_page, self.dashboard_page):
            self.stacked_widget.addWidget(page)

    def _setup_navigation(self):
        self.welcome_page.quit_clicked.connect(QCoreApplication.instance().quit)  # type: ignore
        self.welcome_page.next_clicked.connect(
            lambda: self.stacked_widget.setCurrentWidget(self.dashboard_page)
        )
