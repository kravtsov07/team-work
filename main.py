import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from src.gui.tentative_main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowIcon(QIcon("icons/icon.png"))
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
