from PySide6.QtWidgets import QMainWindow

from src.gui.pages.dashboard_page import DashboardPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Перемножение матриц")
        self.setMinimumSize(1000, 600)
        self.dashboard_page = DashboardPage()
        self.setCentralWidget(self.dashboard_page)
