import subprocess
import sys


class Core:
    def __init__(self):
        pass

    test = ""
    my = ""
    true = ""

    def validate_test(self, mypath, samplepath, generator):
        true_output = ""
        my_output = ""
        test_output = ""
        with subprocess.Popen(self.get_args(generator), stdin=subprocess.PIPE, stdout=subprocess.PIPE) as programming:
            test_output, _ = programming.communicate()
        self.test = test_output.decode().strip()
        with subprocess.Popen(self.get_args(mypath), stdin=subprocess.PIPE, stdout=subprocess.PIPE) as programming:
            my_output, _ = programming.communicate(self.test.encode())
        with subprocess.Popen(self.get_args(samplepath), stdin=subprocess.PIPE, stdout=subprocess.PIPE) as programming:
            true_output, _ = programming.communicate(self.test.encode())
        self.my = my_output.decode().strip().replace('\r', '')
        self.true = true_output.decode().strip().replace('\r', '')
        return self.my == self.true or self.true=="" or self.my==""

    @staticmethod
    def get_args(path):
        array = list()
        if path[-3:] == '.py':
            array.append("python")
        array.append(path)
        return array

    def check_test(self, mypath, test, ans):
        true_output = ""
        with subprocess.Popen(Core.get_args(mypath), stdin=subprocess.PIPE, stdout=subprocess.PIPE) as programming:
            true_output, _ = programming.communicate(test.encode())
        self.my = true_output.decode().strip().replace('\r', '')
        return self.my == ans
