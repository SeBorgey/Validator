from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import *
import sys
from pathlib import Path


class Check(QWidget):
    def __init__(self, core):
        self.settings = QSettings()
        self.set_test = set()
        self.set_test_texts = set()
        super().__init__()
        self.core = core
        self.button_current = QPushButton()
        self.button_file = QPushButton("Файл для проверки", self)
        self.button_file.move(30, 100)
        self.button_add = QPushButton("Добавить", self)
        self.button_add.move(10, 410)
        self.button_delete = QPushButton("Удалить", self)
        self.button_delete.move(120, 410)
        self.button_delete_all = QPushButton("Удалить все", self)
        self.button_delete_all.move(340, 410)
        self.button_save = QPushButton("Сохранить", self)
        self.button_save.move(220, 410)
        self.button_run = QPushButton("Запустить", self)
        self.button_run.setGeometry(550, 200, 200, 200)
        self.line_edit_path = QLineEdit(self)
        self.line_edit_path.setGeometry(230, 100, 500, 30)
        self.line_edit_path.setText(self.settings.value("check_path"))

        self.text_edit_result = QTextEdit(self)
        self.text_edit_result.setGeometry(10, 450, 700, 250)
        self.text_edit_result.setReadOnly(True)
        self.text_edit_test = QTextEdit(self)
        self.text_edit_test.setGeometry(10, 200, 200, 200)
        self.text_edit_ans = QTextEdit(self)
        self.text_edit_ans.setGeometry(280, 200, 200, 200)

        self.label_test = QLabel("Тест", self)
        self.label_test.move(10, 180)
        self.label_ans = QLabel("Ответ", self)
        self.label_ans.move(280, 180)

        self.frame = QFrame(self)
        self.frame.setGeometry(800, 10, 300, 700)
        self.layout_scroll = QVBoxLayout(self.frame)
        self.scroll_area_tests = QScrollArea(self.frame)
        self.scroll_area_tests.setWidgetResizable(True)
        self.layout_scroll.addWidget(self.scroll_area_tests)
        self.container = QWidget()
        self.scroll_area_tests.setWidget(self.container)
        self.layout_scroll = QVBoxLayout(self.container)

        self.button_add.clicked.connect(self.add)
        self.button_delete.clicked.connect(self.delete)
        self.button_save.clicked.connect(self.save)

        self.button_delete_all.clicked.connect(self.delete_all)
        self.button_file.clicked.connect(self.get_path)
        self.button_run.clicked.connect(self.run)
        self.label_warning = QLabel("Поля тест и ответ не должны быть пустыми", self)
        self.label_warning.move(150, 150)
        self.label_warning.setStyleSheet("color:red;")
        self.label_warning.setVisible(False)

        self.button_copy = QPushButton("Скопировать", self)
        self.button_copy.move(90, 170)
        self.button_copy.clicked.connect(self.copy)

        size = self.settings.beginReadArray("tests")
        for i in range(size):
            self.settings.setArrayIndex(i)
            text = str(self.settings.value(str(i)))
            button = QPushButton(text, self.container)
            button.setMinimumHeight(150)
            button.setCheckable(True)
            button.clicked.connect(self.choose)
            button.setStyleSheet("Text-align:left;")
            self.set_test_texts.add(text)
            self.set_test.add(button)
            self.layout_scroll.addWidget(button)
        self.settings.endArray()

    def copy(self):
        text = self.text_edit_test.toPlainText() + '\n'
        c = QApplication.clipboard()
        c.setText(text)

    def run(self):
        self.text_edit_result.setText("")
        for l in self.set_test:
            test, ans = Check.get_test_ans(l)
            if self.core.check_test(self.line_edit_path.text(), test, ans):
                l.setStyleSheet("Text-align:left;background-color:green;")
            else:
                l.setStyleSheet("Text-align:left;background-color:red;")
                text = "Test:\n" + test + "\nRight ans:\n" + ans + "\nYour ans:\n" + self.core.my + '\n\n'
                self.text_edit_result.setText("Error\n" + self.text_edit_result.toPlainText() + text)

    def get_path(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select a File")
        if filename:
            path = Path(filename)
            self.line_edit_path.setText(str(path))
            self.settings.setValue("check_path", str(path))
        pass

    def save_tests(self):
        self.settings.remove("tests")
        self.settings.beginWriteArray("tests")
        i = 0
        for l in self.set_test_texts:
            self.settings.setArrayIndex(i)
            self.settings.setValue(str(i), l)
            i += 1
        self.settings.endArray()

    def delete_all(self):
        self.container = QWidget()
        self.scroll_area_tests.setWidget(self.container)
        self.layout_scroll = QVBoxLayout(self.container)
        self.button_current = QPushButton()
        self.set_test = set()
        self.set_test_texts = set()
        self.settings.remove("tests")

    @staticmethod
    def get_test_ans(button):
        text = button.text()
        index = text.find("\n\n")
        text_test = text[:index]
        text_ans = text[index + 2:]
        return text_test, text_ans

    def choose(self):
        self.button_current.setChecked(False)
        self.button_current = self.sender()
        self.button_current.setChecked(True)
        text = self.button_current.text()
        index = text.find("\n\n")
        text_test = text[:index]
        text_ans = text[index + 2:]
        self.text_edit_test.setText(text_test)
        self.text_edit_ans.setText(text_ans)

    def get_test_text(self):
        test = self.text_edit_test.toPlainText()
        ans = self.text_edit_ans.toPlainText()
        while test[-1] == '\n':
            test = test[:-1]
        while ans[-1] == '\n':
            ans = ans[:-1]
        while test[-1] == ' ':
            test = test[:-1]
        while ans[-1] == ' ':
            ans = ans[:-1]
        test=test.replace(" \n", "\n")
        ans=ans.replace(" \n", "\n")
        text = test + '\n\n' + ans
        return text

    def save(self):
        try:
            text = self.get_test_text()
        except IndexError:
            self.label_warning.setVisible(True)
            return
        self.label_warning.setVisible(False)
        self.set_test_texts.remove(self.button_current.text())
        self.button_current.setText(text)
        self.set_test.add(self.button_current)
        self.text_edit_test.setText("")
        self.text_edit_ans.setText("")
        self.set_test_texts.add(text)
        self.save_tests()

    def delete(self):
        self.set_test_texts.remove(self.button_current.text())
        self.set_test.remove(self.button_current)
        self.button_current.setVisible(False)
        self.layout_scroll.removeWidget(self.button_current)
        self.save_tests()

    def add(self):
        try:
            text = self.get_test_text()
        except IndexError:
            self.label_warning.setVisible(True)
            return
        self.label_warning.setVisible(False)
        button = QPushButton(text, self.container)
        button.setMinimumHeight(150)
        button.setCheckable(True)
        button.clicked.connect(self.choose)
        button.setStyleSheet("Text-align:left;")
        self.set_test.add(button)
        self.layout_scroll.addWidget(button)
        self.text_edit_test.setText("")
        self.text_edit_ans.setText("")
        self.set_test_texts.add(text)
        self.save_tests()
