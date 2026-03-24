import argparse
import os
import sys
from parser import parse_file, parse_expression
from runner import execute, execute_expression, Memory, History
from translator import translate_to_arm_v7
from tester import display_parsed
 
 
def cmd_parse(file):
    parsed = parse_file(file)
    for expression in parsed:
        display_parsed(expression)
        print()
 
 
def cmd_run(file):
    parsed = parse_file(file)
    memory, history = execute(parsed)
    print(f'Memória: {memory}')
    print(f'Histórico: {history}')
 
 
def cmd_translate(file, output):
    parsed = parse_file(file)
    code = translate_to_arm_v7(parsed)
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(code)
        print(f'Assembly salvo em: {output}')
    else:
        print(code)
 
 
def cmd_interactive():
    memory = Memory()
    history = History()
    print('Modo interativo — digite expressões RPN (Ctrl+C ou "sair" ou "q" para sair)')
    print()
    while True:
        try:
            linha = input('>>> ').strip()
        except (KeyboardInterrupt, EOFError):
            print('\nSaindo...')
            break
 
        if not linha or linha.startswith('#'):
            continue
 
        if linha.lower() in ('sair', 'exit', 'quit', 'q'):
            print('Saindo...')
            break
 
        try:
            tokens = parse_expression(linha)
            if not tokens:
                continue
            execute_expression(tokens, memory, history)
            if history.heap:
                print(f'= {history.heap[-1]}')
        except Exception as e:
            print(f'Erro: {e}')
 
 
if __name__ == '__main__':
    ap = argparse.ArgumentParser(
        description='Interpretador de expressões RPN — Fase 1'
    )
 
    modo = ap.add_mutually_exclusive_group(required=True)
    modo.add_argument('-r', '--run',         action='store_true', help='Executa um arquivo de expressões')
    modo.add_argument('-p', '--parse',       action='store_true', help='Exibe os tokens parseados')
    modo.add_argument('-t', '--translate',   action='store_true', help='Traduz para assembly ARMv7')
    modo.add_argument('-i', '--interactive', action='store_true', help='Modo interativo (REPL)')
 
    ap.add_argument('file', nargs='?', help='Arquivo .rpn de entrada')
    ap.add_argument('-o', '--output', help='Arquivo de saída .s (usado com --translate)')
 
    args = ap.parse_args()
 
    if args.interactive:
        cmd_interactive()
        sys.exit(0)
 
    # Os outros modos precisam de arquivo
    if not args.file:
        print('Erro: informe um arquivo de entrada.')
        ap.print_help()
        sys.exit(1)
 
    if not os.path.exists(args.file):
        print(f'Erro: o arquivo "{args.file}" não existe!')
        sys.exit(1)
 
    if args.parse:
        cmd_parse(args.file)
    elif args.run:
        cmd_run(args.file)
    elif args.translate:
        cmd_translate(args.file, args.output)