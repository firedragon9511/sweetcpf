import sys, argparse
from argparse import RawTextHelpFormatter
###### include lib/ ######
sys.path.insert(1, 'lib')
##########################
import cpf_utils

#########################################
#                                       #
# by firedragon9511                     #
# https://github.com/firedragon9511/    #
#                                       #
#########################################

args = None
cpfUtils: cpf_utils.CPFUtils = None

def banner():
    return '''

                       _              __ 
 _____      _____  ___| |_ ___ _ __  / _|
/ __\ \ /\ / / _ \/ _ \ __/ __| '_ \| |_ 
\__ \\\ V  V /  __/  __/ || (__| |_) |  _|
|___/ \_/\_/ \___|\___|\__\___| .__/|_|  
                              |_|        
    
-[by firedragon9511]-
'''

def process_args():
    if args.gen_cpfs is not None:
        cpfUtils.pipe_arr(cpfUtils.random_cpf(args.gen_cpfs))

    if args.gen_all:
        cpfUtils.gen_all()
    
    if args.validate is not None:
        cpfUtils.pipe(args.validate + ':' + str(cpfUtils.validate(args.validate)))

    if args.val_list is not None:
        cpfUtils.validate_list(args.val_list)

    if args.format is not None:
        cpfUtils.pipe(cpfUtils.format_cpf(args.format))

    if args.val_stdin:
        cpfUtils.validate_stdin()

    if args.format_stdin:
        cpfUtils.format_stdin()
        pass

    if args.fix is not None:
        cpfUtils.pipe(cpfUtils.fix_cpf(args.fix))
        pass

    if args.fix_list is not None:
        cpfUtils.fix_list(args.fix_list)
        pass

    if args.fix_stdin:
        cpfUtils.fix_stdin()
        pass

    if args.extract_pipe:
        cpfUtils.extract_cpfs_stdin()


def init():
    global args, cpfUtils
    parser = argparse.ArgumentParser(description=banner(), formatter_class=RawTextHelpFormatter, usage="python sweetcpf.py [option]")
    parser.add_argument('-v','--validate', dest='validate', action='store', type=str, help='Validar um CPF.', required=False)
    parser.add_argument('-vL','--val-list', dest='val_list', action='store', type=str, help='Validar uma lista de CPFs.', required=False)
    parser.add_argument('-vP','--val-stdin', dest='val_stdin', help='Validar uma lista de CPFs recebidas por um pipe.', default=False, required=False, action='store_true')
    parser.add_argument('-g','--gen-cpfs', dest='gen_cpfs', action='store', type=int, help='Gerar X CPFs válidos.', required=False)
    parser.add_argument('-aG','--gen-all', dest='gen_all', help='Gerar todas as possibilidades existentes.', default=False, required=False, action='store_true')
    parser.add_argument('-f', '--format', dest='format', help='Formatar um CPF único.', type=str, required=False)
    parser.add_argument('-fA', '--format-all', dest='format_cpf', help='Resultados mostram CPFs formatados.', default=False, action='store_true')
    parser.add_argument('-fP', '--format-stdin', dest='format_stdin', help='Formatar uma lista de CPFs recebidas por um pipe.', default=False, action='store_true')
    parser.add_argument('-c','--fix', dest='fix', action='store', type=str, help='Corrigir um CPF.', required=False)
    parser.add_argument('-cL','--fix-list', dest='fix_list', action='store', type=str, help='Corrigir uma lista de CPFs.', required=False)
    parser.add_argument('-cP','--fix-stdin', dest='fix_stdin', help='Corrigir uma lista de CPFs recebidas por um pipe.', default=False, required=False, action='store_true')
    parser.add_argument('-eP','--extract', dest='extract_pipe', help='Extrair CPFs através de um texto recebido pelo pipe.', required=False, action='store_true')
    parser.add_argument('-nP','--no-print', dest='no_print', help='Não printar resultados.', default=False, required=False,  action='store_true')
    parser.add_argument('-fZ','--fuzz', dest='fuzz_cmd', action='store', type=str, help='Passar CPFs para um comando personalizado, ex.: -f \'sh custom_script.sh FUZZ\'', required=False)

    args=parser.parse_args()

    cpfUtils = cpf_utils.CPFUtils(args)

    process_args()
    pass


init()