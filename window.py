import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import *
import sys
import check
import validate


class Window:
    def __init__(self):
        """
        Инициализация класса Window.
        Создает и настраивает главное окно приложения с вкладками для проверки тестов и сверки с ответом.
        """
        app = QApplication(sys.argv)
        QCoreApplication.setOrganizationDomain("MIPT")
        QCoreApplication.setApplicationName("validator")
        window = QWidget()
        window.setWindowTitle("VALIDATOR")
        window.setFixedSize(1200, 800)
        tab = QTabWidget()
        check_widget = check.Check()
        validate_widget = validate.Validate()
        tab.addTab(check_widget, "Проверить свои тесты")
        tab.addTab(validate_widget, "Сверить с ответом")
        tab.setCurrentIndex(0)
        vbox = QVBoxLayout()
        vbox.addWidget(tab)
        window.setLayout(vbox)
        window.show()
        sys.exit(app.exec_())
