from main import error


_tokentypes = {'WORD': 1, 'INT': 2, 'STR': 3, 'BOOL': 4, '{': 5, '}': 6, '=': 7, 'do': 8, 'while': 9, 'if': 10,
               'times': 11, '+': 12, '-': 13, '*': 14, '/': 15, '&': 16, '|': 17, '^': 18, '!': 19, '<': 20, '>': 21,
               '@': 22, '#': 23, '$': 24, 'byte': 25, 'word': 26, 'dword': 27}
_spaces = ' \t\v'
_nextline = '\n\r\f'
_quotes = '"' + "'"
_syms = '{}=+-*/&|^!'
_simple = ['do', 'while', 'if']
_comment = ';'


class Token:
    def __init__(self, token_type: str, value=None):
        self.type = _tokentypes[token_type]
        self.value = value


def token(text: str):
    if text in _simple:
        return Token(text)
    if len(text) == 1 and text in _syms:
        return Token(text)

    if text.isdigit():
        return Token('INT', int(text))
    if text == 'true':
        return Token('BOOL', True)
    if text == 'false':
        return Token('BOOL', False)

    if text[0] == '@':
        return Token('@', text[1:])
    if text[0] == '#':
        return Token('#', text[1:])
    if text[0] == '$':
        return Token('$', text[1:])

    if text[0].isalpha():
        return Token('WORD', text)
    error(101, 'Invalid word "'+text+'"')


def lexer(text: str):
    com = [[]]
    buf = ''
    quote = ''
    string = False
    comm = False
    i = 0
    while i < len(text):
        c = text[i]
        if comm:
            if c in _nextline:
                comm = False
            i += 1
            continue

        if c == _comment:
            com[-1].append(token(buf))
            buf = ''
            comm = True
        elif string:
            if c == quote:
                com[-1].append(Token('STR', buf))
                string = False
                buf = ''
            else:
                buf += c
        elif c in _quotes:
            com[-1].append(token(buf))
            buf = ''
            quote = c
            string = True

        elif c == '\\':
            i += 1
            continue
        elif c in _syms:
            com[-1].append(token(buf))
            buf = ''
            com[-1].append(token(c))
        elif c in _spaces:
            com[-1].append(token(buf))
            buf = ''
        elif c in _nextline:
            com[-1].append(token(buf))
            buf = ''
            if text[i-1] != '\\':
                com.append([])

        else:
            buf += c
        i += 1
    return com
