from enum import Enum, auto


class TokenType(Enum):
    # Identificadores e palavras reservadas
    IDENTIFIER = auto()
    INT = auto()
    FLOAT = auto()
    PRINT = auto()
    IF = auto()
    ELSE = auto()

    # Literais
    NUMBER = auto()

    # Operadores matemáticos
    PLUS = auto()       # +
    MINUS = auto()      # -
    STAR = auto()       # *
    SLASH = auto()      # /

    # Atribuição e relacionais
    ASSIGN = auto()         # =
    GT = auto()             # >
    GTE = auto()            # >=
    LT = auto()             # <
    LTE = auto()            # <=
    NOT_EQUAL = auto()      # !=
    EQUAL_EQUAL = auto()    # ==

    # Delimitadores
    LPAREN = auto()     # (
    RPAREN = auto()     # )

    # Sentinela (opcional)
    EOF = auto()


RESERVED_KEYWORDS = {
    "int": TokenType.INT,
    "float": TokenType.FLOAT,
    "print": TokenType.PRINT,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
}


