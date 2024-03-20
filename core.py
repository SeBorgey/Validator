import subprocess
import sys


class Core:
    def __init__(self):
        pass

    test = ""
    my = ""
    true = ""

    @staticmethod
    def validate_test(mypath, samplepath, generator):
        true_output = ""
        my_output = ""
        test_output = ""
        with subprocess.Popen(Core.get_args(generator), stdin=subprocess.PIPE, stdout=subprocess.PIPE) as programming:
            Core.test_output, _ = programming.communicate()
        Core.test = Core.test_output.decode().strip()
        with subprocess.Popen(Core.get_args(mypath), stdin=subprocess.PIPE, stdout=subprocess.PIPE) as programming:
            Core.my_output, _ = programming.communicate(Core.test.encode())
        with subprocess.Popen(Core.get_args(samplepath), stdin=subprocess.PIPE, stdout=subprocess.PIPE) as programming:
            Core.true_output, _ = programming.communicate(Core.test.encode())
        Core.my = Core.my_output.decode().strip()
        Core.true = Core.true_output.decode().strip()
        return Core.my == Core.true

    @staticmethod
    def get_args(path):
        array = list()
        if path[-4:-1] == '.py':
            array.append("python")
        array.append(path)
        return array

    @staticmethod
    def check_test(mypath, test, ans):
        true_output = ""
        with subprocess.Popen(Core.get_args(mypath), stdin=subprocess.PIPE, stdout=subprocess.PIPE) as programming:
            true_output, _ = programming.communicate(test.encode())
        Core.my = true_output.decode().strip()
        return Core.my == ans
