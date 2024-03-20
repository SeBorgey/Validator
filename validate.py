from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import *
import sys
from pathlib import Path
from core import Core


class Validate(QWidget):
    def __init__(self):
        super().__init__()
        self.settings = QSettings()
        self.button_current = QPushButton()
        self.button_myfile = QPushButton("Мой файл", self)
        self.button_myfile.move(100, 100)

        self.button_sample = QPushButton("Образец", self)
        self.button_sample.move(100, 150)

        self.button_generator = QPushButton("Генератор", self)
        self.button_generator.move(100, 200)

        self.button_run = QPushButton("Запустить", self)
        self.button_run.move(600, 300)
        self.line_edit_myfile = QLineEdit(self)
        self.line_edit_myfile.setGeometry(300, 100, 500, 30)
        self.line_edit_myfile.setText(self.settings.value("validate_myfile"))
        self.line_edit_sample = QLineEdit(self)
        self.line_edit_sample.setGeometry(300, 150, 500, 30)
        self.line_edit_sample.setText(self.settings.value("validate_sample"))
        self.line_edit_generator = QLineEdit(self)
        self.line_edit_generator.setGeometry(300, 200, 500, 30)
        self.line_edit_generator.setText(self.settings.value("validate_generator"))

        self.text_edit_result = QTextEdit(self)
        self.text_edit_result.setGeometry(10, 450, 1000, 250)
        self.text_edit_result.setReadOnly(True)
        self.label_test = QLabel("Количество тестов", self)
        self.label_test.move(200, 300)

        self.line_edit_amount = QLineEdit(self)
        self.line_edit_amount.setGeometry(400, 300, 100, 30)
        self.line_edit_amount.setText('100')

        self.button_myfile.clicked.connect(self.get_path_myfile)
        self.button_sample.clicked.connect(self.get_path_sample)
        self.button_generator.clicked.connect(self.get_path_generator)
        self.button_run.clicked.connect(self.run)

    def run(self):
        self.text_edit_result.setText("")
        for i in range(int(self.line_edit_amount.text())):
            if not Core.validate_test(self.line_edit_myfile.text(),
                                      self.line_edit_sample.text(),
                                      self.line_edit_generator.text()):
                text = "Error\nTest:\n" + Core.test + "\nRight ans:\n" + Core.true + "\nYour ans:\n" + Core.my+'\n'
                self.text_edit_result.setText(text)
                return
        self.text_edit_result.setText("OK")

    def get_path_myfile(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select a File")
        if filename:
            path = str(Path(filename))
            self.line_edit_myfile.setText(path)
            self.settings.setValue("validate_myfile", path)
        pass

    def get_path_sample(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select a File")
        if filename:
            path = str(Path(filename))
            self.line_edit_sample.setText(path)
            self.settings.setValue("validate_sample", path)
        pass

    def get_path_generator(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select a File")
        if filename:
            path = str(Path(filename))
            self.line_edit_generator.setText(path)
            self.settings.setValue("validate_generator", path)
        pass
