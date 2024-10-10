from PyQt5.QtCore import QSettings, QThread, pyqtSignal
from PyQt5.QtWidgets import *
import sys
from pathlib import Path


class TestRunner(QThread):
    update_progress = pyqtSignal(int)
    finished = pyqtSignal()
    error_occurred = pyqtSignal(str)
    stop_signal = False

    def __init__(self, core, myfile, sample, generator, amount):
        super().__init__()
        self.core = core
        self.myfile = myfile
        self.sample = sample
        self.generator = generator
        self.amount = amount

    def run(self):
        for i in range(int(self.amount)):
            if self.stop_signal:
                break
            if not self.core.validate_test(self.myfile, self.sample, self.generator):
                error_text = (f"Error\nTest:\n{self.core.test}\nRight ans:\n{self.core.true}\nYour ans:\n{self.core.my}\n")
                self.error_occurred.emit(error_text)
                return
            self.update_progress.emit(i + 1)
        self.finished.emit()

    def stop(self):
        self.stop_signal = True


class Validate(QWidget):
    def __init__(self, core):
        super().__init__()
        self.core = core
        self.settings = QSettings()
        self.thread = None

        self.button_current = QPushButton()
        self.button_myfile = QPushButton("Мой файл", self)
        self.button_myfile.move(100, 100)

        self.button_sample = QPushButton("Образец", self)
        self.button_sample.move(100, 150)

        self.button_generator = QPushButton("Генератор", self)
        self.button_generator.move(100, 200)

        self.button_run = QPushButton("Запустить", self)
        self.button_run.move(600, 300)

        self.button_stop = QPushButton("Остановить", self)
        self.button_stop.move(720, 300)
        self.button_stop.setEnabled(False)

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

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(10, 400, 1000, 30)
        self.progress_bar.setMaximum(int(self.line_edit_amount.text()))

        self.button_myfile.clicked.connect(self.get_path_myfile)
        self.button_sample.clicked.connect(self.get_path_sample)
        self.button_generator.clicked.connect(self.get_path_generator)
        self.button_run.clicked.connect(self.run)
        self.button_stop.clicked.connect(self.stop)

    def run(self):
        self.text_edit_result.clear()

        self.settings.setValue("validate_myfile", self.line_edit_myfile.text())
        self.settings.setValue("validate_sample", self.line_edit_sample.text())
        self.settings.setValue("validate_generator", self.line_edit_generator.text())

        self.progress_bar.setMaximum(int(self.line_edit_amount.text()))

        self.button_run.setEnabled(False)
        self.button_stop.setEnabled(True)

        self.thread = TestRunner(self.core,
                                 self.line_edit_myfile.text(),
                                 self.line_edit_sample.text(),
                                 self.line_edit_generator.text(),
                                 self.line_edit_amount.text())
        self.thread.update_progress.connect(self.update_progress_bar)
        self.thread.finished.connect(self.tests_finished)
        self.thread.error_occurred.connect(self.display_error)
        self.thread.start()

    def stop(self):
        if self.thread:
            self.thread.stop()

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def tests_finished(self):
        self.text_edit_result.append("OK")
        self.button_run.setEnabled(True)
        self.button_stop.setEnabled(False)

    def display_error(self, error_text):
        self.text_edit_result.setText(error_text)
        self.button_run.setEnabled(True)
        self.button_stop.setEnabled(False)

    def get_path_myfile(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select a File")
        if filename:
            path = str(Path(filename))
            self.line_edit_myfile.setText(path)
            self.settings.setValue("validate_myfile", path)

    def get_path_sample(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select a File")
        if filename:
            path = str(Path(filename))
            self.line_edit_sample.setText(path)
            self.settings.setValue("validate_sample", path)

    def get_path_generator(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select a File")
        if filename:
            path = str(Path(filename))
            self.line_edit_generator.setText(path)
            self.settings.setValue("validate_generator", path)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    core = None
    window = Validate(core)
    window.show()
    sys.exit(app.exec_())
