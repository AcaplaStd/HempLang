# HempLang Programming Language
# (C) 2019 Acapla Studios


from sys import argv
from lexer import lexer


def error(code: int, text: str):
    print('ERROR ', code, ': ', text, sep='')
    print('\n[Exiting program]\n')
    exit(code)


if __name__ == '__main__':
    if len(argv) > 1:
        adr = argv[1]
    else:
        adr = input()
    with open(adr) as file:
        text = file.read()

    commands = lexer(text)
    for c in commands:  # This is 'testilka'
        print(*c)
