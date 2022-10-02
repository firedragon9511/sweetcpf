import os

class Fuzzer:
    @staticmethod
    def fuzz(cmd: str, cpf):
        os.system(cmd.replace("FUZZ", cpf))