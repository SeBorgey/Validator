import sys

from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import *
import sys
import check
import validate
import core


class Window:
    def __init__(self):
        app = QApplication(sys.argv)
        QCoreApplication.setOrganizationDomain("MIPT")
        QCoreApplication.setApplicationName("validator")
        window = QWidget()
        window.setWindowTitle("VALIDATOR")
        window.setFixedSize(1200, 800)
        tab = QTabWidget()
        core_ = core.Core()
        check_widget = check.Check(core_)
        validate_widget = validate.Validate(core_)
        tab.addTab(check_widget, "Проверить свои тесты")
        tab.addTab(validate_widget, "Сверить с ответом")
        tab.setCurrentIndex(0)
        vbox = QVBoxLayout()
        vbox.addWidget(tab)
        window.setLayout(vbox)
        window.show()
        sys.exit(app.exec_())
