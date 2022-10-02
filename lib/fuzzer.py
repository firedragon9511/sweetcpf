import os

#########################################
#                                       #
# by firedragon9511                     #
# https://github.com/firedragon9511/    #
#                                       #
#########################################

class Fuzzer:
    @staticmethod
    def fuzz(cmd: str, cpf):
        os.system(cmd.replace("FUZZ", cpf))