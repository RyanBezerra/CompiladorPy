from __future__ import annotations

from typing import Optional, Iterator

from .token import Token
from .token_type import TokenType, RESERVED_KEYWORDS
from .errors import LexicalError


class Scanner:
    def __init__(self, source_path: str) -> None:
        with open(source_path, "r", encoding="utf-8") as f:
            self.source: str = f.read()
        self.length: int = len(self.source)
        self.index: int = 0
        self.line: int = 1
        self.column: int = 1
    
    @classmethod
    def from_string(cls, source_code: str) -> 'Scanner':
        """Cria um Scanner a partir de uma string de código"""
        scanner = cls.__new__(cls)
        scanner.source = source_code
        scanner.length = len(source_code)
        scanner.index = 0
        scanner.line = 1
        scanner.column = 1
        return scanner

    def __iter__(self) -> Iterator[Token]:
        while True:
            token = self.next_token()
            if token is None:
                break
            yield token

    def next_token(self) -> Optional[Token]:
        self._skip_whitespace_and_comments()
        if self._is_eof():
            return None

        start_line, start_col = self.line, self.column
        char = self._advance()

        # Identificadores e palavras reservadas: (a-z|A-Z|_)(a-z|A-Z|_|0-9)*
        if self._is_letter(char) or char == "_":
            lexeme = [char]
            while not self._is_eof():
                c = self._peek()
                if self._is_letter(c) or self._is_digit(c) or c == "_":
                    lexeme.append(self._advance())
                else:
                    break
            text = "".join(lexeme)
            token_type = RESERVED_KEYWORDS.get(text, TokenType.IDENTIFIER)
            return Token(token_type, text, start_line, start_col)

        # Números com ponto decimal: ((0-9)*.)?(0-9)+, exemplos válidos: 123, 123.456, .456
        if char == "." or self._is_digit(char):
            return self._number_token(start_line, start_col, char)

        # Parênteses
        if char == "(":
            return Token(TokenType.LPAREN, "(", start_line, start_col)
        if char == ")":
            return Token(TokenType.RPAREN, ")", start_line, start_col)

        # Operadores matemáticos e relacionais/atribuição
        if char == "+":
            return Token(TokenType.PLUS, "+", start_line, start_col)
        if char == "-":
            return Token(TokenType.MINUS, "-", start_line, start_col)
        if char == "*":
            return Token(TokenType.STAR, "*", start_line, start_col)
        if char == "/":
            # Já tratamos comentários em _skip_whitespace_and_comments
            return Token(TokenType.SLASH, "/", start_line, start_col)

        if char == "=":
            if self._match("="):
                return Token(TokenType.EQUAL_EQUAL, "==", start_line, start_col)
            return Token(TokenType.ASSIGN, "=", start_line, start_col)

        if char == ">":
            if self._match("="):
                return Token(TokenType.GTE, ">=", start_line, start_col)
            return Token(TokenType.GT, ">", start_line, start_col)

        if char == "<":
            if self._match("="):
                return Token(TokenType.LTE, "<=", start_line, start_col)
            return Token(TokenType.LT, "<", start_line, start_col)

        if char == "!":
            if self._match("="):
                return Token(TokenType.NOT_EQUAL, "!=", start_line, start_col)
            self._raise_error("'!' isolado não é permitido; esperava '!='", start_line, start_col)

        # Qualquer outro caractere inválido
        self._raise_error(f"Símbolo inválido: '{char}'", start_line, start_col)

    # -------------------- Helpers léxicos --------------------
    def _number_token(self, start_line: int, start_col: int, first_char: str) -> Optional[Token]:
        # Implementa ((0-9)*.)?(0-9)+
        lexeme = [first_char]
        saw_dot = first_char == "."
        has_digits_after_dot = False
        has_digits_before_dot = first_char.isdigit()

        def is_digit(c: str) -> bool:
            return "0" <= c <= "9"

        # Parte antes do ponto (se começou com dígito)
        if has_digits_before_dot:
            while not self._is_eof() and is_digit(self._peek()):
                lexeme.append(self._advance())

        # Ponto opcional
        if not saw_dot and not self._is_eof() and self._peek() == ".":
            saw_dot = True
            lexeme.append(self._advance())

        # Dígitos após o ponto (obrigatórios se houve ponto ou se começou com '.')
        if saw_dot:
            while not self._is_eof() and is_digit(self._peek()):
                has_digits_after_dot = True
                lexeme.append(self._advance())

            if not has_digits_after_dot:
                self._raise_error("Número inválido: faltam dígitos após o ponto", start_line, start_col)
        else:
            # Sem ponto: já coletamos todos os dígitos acima
            pass

        text = "".join(lexeme)
        # Casos inválidos como '1.' ou '12.' já são pegos pelo has_digits_after_dot
        return Token(TokenType.NUMBER, text, start_line, start_col)

    def _skip_whitespace_and_comments(self) -> None:
        while not self._is_eof():
            c = self._peek()
            # Espaços e quebras de linha
            if c in (" ", "\t", "\r"):
                self._advance()
                continue
            if c == "\n":
                self._advance()
                self.line += 1
                self.column = 1
                continue

            # Comentário de linha '#'
            if c == "#":
                while not self._is_eof() and self._peek() not in ("\n",):
                    self._advance()
                continue

            # Comentário de bloco '/* ... */'
            if c == "/" and self._peek_next() == "*":
                # consome '/*'
                comment_start_line, comment_start_col = self.line, self.column
                self._advance()
                self._advance()
                # percorre até encontrar '*/' ou EOF
                while not self._is_eof():
                    if self._peek() == "\n":
                        self._advance()
                        self.line += 1
                        self.column = 1
                        continue
                    if self._peek() == "*" and self._peek_next() == "/":
                        self._advance()  # '*'
                        self._advance()  # '/'
                        break
                    self._advance()
                else:
                    # EOF alcançado sem fechar comentário
                    self._raise_error("Comentário de múltiplas linhas não finalizado (esperava '*/')", comment_start_line, comment_start_col)
                continue

            break

    # -------------------- Primitivas do scanner --------------------
    def _advance(self) -> str:
        ch = self.source[self.index]
        self.index += 1
        self.column += 1
        return ch

    def _match(self, expected: str) -> bool:
        if self._is_eof() or self.source[self.index] != expected:
            return False
        self.index += 1
        self.column += 1
        return True

    def _peek(self) -> str:
        return "\0" if self._is_eof() else self.source[self.index]

    def _peek_next(self) -> str:
        if self.index + 1 >= self.length:
            return "\0"
        return self.source[self.index + 1]

    def _is_eof(self) -> bool:
        return self.index >= self.length

    def _is_letter(self, c: str) -> bool:
        return ("a" <= c <= "z") or ("A" <= c <= "Z")

    def _is_digit(self, c: str) -> bool:
        return "0" <= c <= "9"

    # -------------------- Erros --------------------
    def _raise_error(self, message: str, start_line: int, start_col: int) -> None:
        raise LexicalError(message, start_line, start_col)


