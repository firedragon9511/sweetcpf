from random import randint
import itertools
import re
import fuzzer
import sys

class CPFUtils:
    def __init__(self, args) -> None:
        self.args = args
        pass

    def random_num(self, n):
        range_start = 10**(n-1)
        range_end = (10**n)-1
        return randint(range_start, range_end)


    def format_cpf(self, raw_cpf):
        if len(raw_cpf) < 10:
            return "Formato Inválido: " + raw_cpf
        raw_cpf = self.clear_cpf(raw_cpf)
        return raw_cpf[:3] + "." + raw_cpf[3:6] + "." + raw_cpf[6:9] + "-" + raw_cpf[9] + raw_cpf[10] + raw_cpf[11:]

    
    def pipe_arr(self, arr):
        arr = arr if type(arr) is not str else [arr]
        for i in arr:
            self.pipe(i)


    def pipe(self, txt):
        if self.args.format_cpf:
            txt = self.format_cpf(txt)

        if self.args.fuzz_cmd is not None:
            fuzzer.Fuzzer.fuzz(self.args.fuzz_cmd, txt)

        if not self.args.no_print:
            print(txt)


    def random_cpf(self, amount = 1, format=False):
        result = []
        raw_cpf: str = ""
        for n in range(0, amount):
            raw_cpf = ""
            for i in range(0,3):
                raw_cpf = raw_cpf + str(self.random_num(3))
            result.append(self.fix_cpf(raw_cpf) if not format else self.format_cpf(self.fix_cpf(raw_cpf)))
        return result if amount > 1 else result[0]


    def clear_cpf(self, cpf: str):
        return cpf.replace(".", "").replace("-","")


    def fix_cpf(self, raw_cpf: str =  "111444777"): 
        raw_cpf = self.clear_cpf(raw_cpf)[:9]
        def d(raw_cpf):
            d1 = 0
            for i in range(0, len(raw_cpf)):
                d1 += ((len(raw_cpf) + 1 - i) * int(raw_cpf[i]))
            return str(0 if d1 % 11 < 2 else 11 - d1 % 11)
        return raw_cpf + d(raw_cpf) + d( raw_cpf + d(raw_cpf) )


    def gen_all(self):
        char=itertools.product('0123456789',repeat=9)
        for pin in char:
            code =''.join(pin)
            self.pipe(self.fix_cpf(code))


    def validate(self, cpf: str) -> bool:
        cpf = self.clear_cpf(cpf)
        return self.fix_cpf(cpf[:9]) == cpf

    
    def validate_list(self, file: str):
        strm = open(file, 'r')
        data: list = strm.read().split('\n')
        for d in data:
            try:
                self.pipe(d + ':' + str(self.validate(d)))
            except ValueError as e:
                self.pipe("Formato invalido: " + d)
        return


    def validate_stdin(self):
        for line in sys.stdin:
            line = line.replace('\n', '')
            try:
                self.pipe(line + ':' + str(self.validate(line)))
            except ValueError as e:
                self.pipe("Formato invalido: " + line)


    def format_stdin(self):
        for line in sys.stdin:
            line = line.replace('\n', '')
            self.pipe(self.format_cpf(line))


    def fix_list(self, file):
        strm = open(file, 'r')
        data: list = strm.read().split('\n')
        for line in data:
            try:
                if not self.validate(line):
                    self.pipe(self.fix_cpf(line))
                else:
                    self.pipe(line)
            except ValueError as e:
                self.pipe("Formato invalido: " + line)
                pass
        return


    def fix_stdin(self):
        for line in sys.stdin:
            line = line.replace('\n', '')
            try:
                if not self.validate(line):
                    self.pipe(self.fix_cpf(line))
                else:
                    self.pipe(line)
            except ValueError as e:
                self.pipe("Formato invalido: " + line)
                pass


    def extract_cpfs_stdin(self):
        arr = []
        for line in sys.stdin:
            arr.append(line)
        result = self.extract_cpf(''.join(arr))
        self.pipe_arr(result)
        return result


    def extract_cpf(self, txt):
        arr = re.findall(r'\d{3}\.\d{3}\.\d{3}-\d{2}', txt)
        arr2 = re.findall(r'\d{11}', txt)
        arr2_final = []
        for cpf in arr2:
            if self.validate(cpf):
                arr2_final.append(cpf)
        return arr + arr2_final