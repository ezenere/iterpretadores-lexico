import argparse, os, sys
from common import *
from parser import parse_file
from runner import execute

def display_parsed(parsed):
    espacos = ''
    for token in parsed:
        if token.kind == PARENTHESES:
            if token.value == PARENTHESES_L:
                print(f'{espacos}(')
                espacos = espacos + '  '
            else:
                espacos = espacos[:-2]
                print(f'{espacos})')
        elif token.kind == MATH:
            print(f'{espacos}Operador Matemático: ', end='')
            if token.value == MATH_PLUS:
                print('+ (Soma)')
            elif token.value == MATH_MINUS:
                print('- (Subtração)')
            elif token.value == MATH_TIMES:
                print('* (Multiplicação)')
            elif token.value == MATH_FLOAT_DIV:
                print('/ (Divisão)')
            elif token.value == MATH_INT_DIV:
                print('// (Divisão inteira)')
            elif token.value == MATH_MODULLUS:
                print('% (Módulo)')
            elif token.value == MATH_EXPONENTIAL:
                print('^ (Exponenciação)')
        elif token.kind == KEYWORD:
            print(f'{espacos}KEYWORD: ', end='')
            if token.value == KEYWORD_RES:
                print('RES')
        elif token.kind == FLOAT:
            print(f'{espacos}Ponto Flutuante: {token.value}')
        elif token.kind == INT:
            print(f'{espacos}Inteiro: {token.value}')
        elif token.kind == VARIABLE:
            print(f'{espacos}Variável: {token.value}')
        elif token.kind == OPERATION:
            print('OPERAÇÃO')

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument("file", help="O arquivo que você deseja executar")

    args = ap.parse_args()

    if not os.path.exists(args.file):
        print("Erro: o arquivo não existe!")
        sys.exit(1)

    parsed = parse_file(args.file)

    print('Tokens:')
    for expression in parsed:
        display_parsed(expression)

    memory, history = execute(parsed)

    print(memory, history)
