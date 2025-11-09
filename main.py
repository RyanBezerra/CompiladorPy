"""
Compilador - Analisador Léxico e Sintático
Checkpoint 01: Analisador Léxico
Checkpoint 02: Analisador Sintático

Disciplina: Construção de Compiladores I

Integrantes do Grupo:
- [Adicione os nomes dos integrantes aqui]
"""
from __future__ import annotations
import sys
from pathlib import Path
from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional, Iterator
from collections import Counter


# ============================================================================
# TIPOS DE TOKENS
# ============================================================================
# Define todos os tipos de "palavras" que o compilador pode reconhecer
# Exemplo: quando vê "int", sabe que é um tipo de variável
#          quando vê "123", sabe que é um número
# ============================================================================
class TokenType(Enum):
    IDENTIFIER = auto()      # Nome de variável (ex: x, variavel, nome_var)
    INT = auto()             # Palavra reservada "int"
    FLOAT = auto()           # Palavra reservada "float"
    PRINT = auto()           # Palavra reservada "print"
    IF = auto()              # Palavra reservada "if"
    ELSE = auto()            # Palavra reservada "else"
    NUMBER = auto()          # Número (ex: 10, 3.14, .456)
    PLUS = auto()            # Operador +
    MINUS = auto()           # Operador -
    STAR = auto()            # Operador *
    SLASH = auto()           # Operador /
    ASSIGN = auto()          # Operador =
    GT = auto()              # Operador >
    GTE = auto()             # Operador >=
    LT = auto()              # Operador <
    LTE = auto()            # Operador <=
    NOT_EQUAL = auto()       # Operador !=
    EQUAL_EQUAL = auto()     # Operador ==
    LPAREN = auto()          # Parêntese esquerdo (
    RPAREN = auto()          # Parêntese direito )
    EOF = auto()             # Fim do arquivo


# ============================================================================
# PALAVRAS RESERVADAS
# ============================================================================
# Tabela que mapeia palavras especiais para seus tipos
# Quando o scanner encontra "int", verifica aqui e retorna TokenType.INT
# ============================================================================
RESERVED_KEYWORDS = {
    "int": TokenType.INT,
    "float": TokenType.FLOAT,
    "print": TokenType.PRINT,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
}


# ============================================================================
# TOKEN
# ============================================================================
# Representa uma "palavra" encontrada no código
# Exemplo: quando encontra "int x = 10", cria 4 tokens:
#   - Token(INT, "int", linha=1, coluna=1)
#   - Token(IDENTIFIER, "x", linha=1, coluna=5)
#   - Token(ASSIGN, "=", linha=1, coluna=7)
#   - Token(NUMBER, "10", linha=1, coluna=9)
# ============================================================================
@dataclass
class Token:
    type: TokenType      # Tipo do token (INT, IDENTIFIER, NUMBER, etc.)
    lexeme: str          # O texto exato encontrado ("int", "x", "10", etc.)
    line: int            # Linha onde foi encontrado
    column: int          # Coluna onde foi encontrado

    def __str__(self) -> str:
        return f"Token(type={self.type.name}, lexeme='{self.lexeme}', line={self.line}, column={self.column})"


# ============================================================================
# ERRO LÉXICO
# ============================================================================
# Exceção lançada quando encontra um símbolo inválido
# Exemplo: se encontrar "@", que não é permitido, lança este erro
# ============================================================================
class LexicalError(Exception):
    def __init__(self, message: str, line: int, column: int) -> None:
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column

    def __str__(self) -> str:
        return f"Erro léxico na linha {self.line}, coluna {self.column}: {self.message}"


# ============================================================================
# SCANNER (ANALISADOR LÉXICO)
# ============================================================================
# Responsável por ler o código e identificar os tokens
# Funciona como um "leitor" que vai caractere por caractere e identifica
# o que é palavra, número, operador, etc.
# ============================================================================
class Scanner:
    def __init__(self, source_path: str) -> None:
        # Lê o arquivo de código
        with open(source_path, "r", encoding="utf-8") as f:
            self.source: str = f.read()
        self.length: int = len(self.source)  # Tamanho total do código
        self.index: int = 0                  # Posição atual (qual caractere está lendo)
        self.line: int = 1                   # Linha atual
        self.column: int = 1                # Coluna atual
    
    @classmethod
    def from_string(cls, source_code: str) -> 'Scanner':
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
        """
        Lê o próximo token do código.
        Retorna None quando chega ao fim do arquivo.
        """
        # Pula espaços em branco e comentários
        self._skip_whitespace_and_comments()
        
        # Se chegou ao fim do arquivo, retorna None
        if self._is_eof():
            return None

        # Guarda a posição onde este token começa (para reportar erros)
        start_line, start_col = self.line, self.column
        
        # Lê o próximo caractere
        char = self._advance()

        # ====================================================================
        # IDENTIFICADORES E PALAVRAS RESERVADAS
        # ====================================================================
        # Se começa com letra ou underscore, é um identificador
        # Exemplo: "int", "x", "variavel123"
        # ====================================================================
        if self._is_letter(char) or char == "_":
            lexeme = [char]  # Lista para construir o nome completo
            # Continua lendo enquanto for letra, dígito ou underscore
            while not self._is_eof():
                c = self._peek()
                if self._is_letter(c) or self._is_digit(c) or c == "_":
                    lexeme.append(self._advance())
                else:
                    break
            text = "".join(lexeme)
            # Verifica se é palavra reservada (int, float, etc.) ou identificador comum
            token_type = RESERVED_KEYWORDS.get(text, TokenType.IDENTIFIER)
            return Token(token_type, text, start_line, start_col)

        # ====================================================================
        # NÚMEROS
        # ====================================================================
        # Se começa com dígito ou ponto, é um número
        # Exemplo: "123", "3.14", ".456"
        # ====================================================================
        if char == "." or self._is_digit(char):
            return self._number_token(start_line, start_col, char)

        # ====================================================================
        # PARÊNTESES
        # ====================================================================
        if char == "(":
            return Token(TokenType.LPAREN, "(", start_line, start_col)
        if char == ")":
            return Token(TokenType.RPAREN, ")", start_line, start_col)

        # ====================================================================
        # OPERADORES MATEMÁTICOS
        # ====================================================================
        if char == "+":
            return Token(TokenType.PLUS, "+", start_line, start_col)
        if char == "-":
            return Token(TokenType.MINUS, "-", start_line, start_col)
        if char == "*":
            return Token(TokenType.STAR, "*", start_line, start_col)
        if char == "/":
            return Token(TokenType.SLASH, "/", start_line, start_col)

        # ====================================================================
        # OPERADOR DE ATRIBUIÇÃO E IGUALDADE
        # ====================================================================
        # "=" é atribuição, "==" é comparação de igualdade
        # ====================================================================
        if char == "=":
            if self._match("="):  # Verifica se o próximo é também "="
                return Token(TokenType.EQUAL_EQUAL, "==", start_line, start_col)
            return Token(TokenType.ASSIGN, "=", start_line, start_col)

        # ====================================================================
        # OPERADORES RELACIONAIS
        # ====================================================================
        # ">", ">=", "<", "<=", "!=", "=="
        # ====================================================================
        if char == ">":
            if self._match("="):  # Verifica se é ">="
                return Token(TokenType.GTE, ">=", start_line, start_col)
            return Token(TokenType.GT, ">", start_line, start_col)

        if char == "<":
            if self._match("="):  # Verifica se é "<="
                return Token(TokenType.LTE, "<=", start_line, start_col)
            return Token(TokenType.LT, "<", start_line, start_col)

        if char == "!":
            if self._match("="):  # Verifica se é "!="
                return Token(TokenType.NOT_EQUAL, "!=", start_line, start_col)
            # "!" sozinho não é permitido
            self._raise_error("'!' isolado não é permitido; esperava '!='", start_line, start_col)

        # ====================================================================
        # SÍMBOLO INVÁLIDO
        # ====================================================================
        # Se chegou aqui, é um caractere que não reconhecemos
        # Exemplo: "@", "ç", "`", etc.
        # ====================================================================
        self._raise_error(f"Símbolo inválido: '{char}'", start_line, start_col)

    def _number_token(self, start_line: int, start_col: int, first_char: str) -> Optional[Token]:
        """
        Reconhece números com ponto decimal.
        Válidos: 123, 123.456, .456
        Inválidos: 1., 12., 156. (não pode terminar em ponto sem dígitos)
        """
        lexeme = [first_char]
        saw_dot = first_char == "."  # Já viu o ponto?
        has_digits_after_dot = False  # Tem dígitos depois do ponto?
        has_digits_before_dot = first_char.isdigit()  # Tem dígitos antes do ponto?

        def is_digit(c: str) -> bool:
            return "0" <= c <= "9"

        if has_digits_before_dot:
            while not self._is_eof() and is_digit(self._peek()):
                lexeme.append(self._advance())

        if not saw_dot and not self._is_eof() and self._peek() == ".":
            saw_dot = True
            lexeme.append(self._advance())

        if saw_dot:
            while not self._is_eof() and is_digit(self._peek()):
                has_digits_after_dot = True
                lexeme.append(self._advance())

            if not has_digits_after_dot:
                self._raise_error("Número inválido: faltam dígitos após o ponto", start_line, start_col)

        text = "".join(lexeme)
        return Token(TokenType.NUMBER, text, start_line, start_col)

    def _skip_whitespace_and_comments(self) -> None:
        """
        Pula espaços em branco e comentários.
        Comentários não geram tokens, são ignorados.
        """
        while not self._is_eof():
            c = self._peek()
            
            # Pula espaços, tabs e retornos de carro
            if c in (" ", "\t", "\r"):
                self._advance()
                continue
            
            # Pula quebras de linha (atualiza contador de linha)
            if c == "\n":
                self._advance()
                self.line += 1
                self.column = 1
                continue

            # ================================================================
            # COMENTÁRIO DE LINHA (# comentário)
            # ================================================================
            # Lê tudo até encontrar quebra de linha
            if c == "#":
                while not self._is_eof() and self._peek() not in ("\n", "\r"):
                    self._advance()
                continue

            # ================================================================
            # COMENTÁRIO DE BLOCO (/* comentário */)
            # ================================================================
            # Lê tudo entre /* e */
            if c == "/" and self._peek_next() == "*":
                comment_start_line, comment_start_col = self.line, self.column
                self._advance()
                self._advance()
                while not self._is_eof():
                    if self._peek() == "\n":
                        self._advance()
                        self.line += 1
                        self.column = 1
                        continue
                    if self._peek() == "*" and self._peek_next() == "/":
                        self._advance()
                        self._advance()
                        break
                    self._advance()
                else:
                    self._raise_error("Comentário de múltiplas linhas não finalizado (esperava '*/')", comment_start_line, comment_start_col)
                continue

            break

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

    def _raise_error(self, message: str, start_line: int, start_col: int) -> None:
        raise LexicalError(message, start_line, start_col)


# ============================================================================
# ERRO SINTÁTICO
# ============================================================================
# Exceção lançada quando o código não está escrito corretamente
# Exemplo: "int x =" sem valor, ou "print(" sem fechar parêntese
# ============================================================================
class SyntaxError(Exception):
    def __init__(self, message: str, line: int, column: int) -> None:
        super().__init__(message)
        self.message = message
        self.line = line
        self.column = column

    def __str__(self) -> str:
        return f"Erro sintático na linha {self.line}, coluna {self.column}: {self.message}"


# ============================================================================
# PARSER (ANALISADOR SINTÁTICO)
# ============================================================================
# Responsável por verificar se o código está escrito corretamente
# Usa os tokens do Scanner para verificar se seguem as regras da gramática
# Exemplo: verifica se "int x = 10" está correto (tipo, nome, =, valor)
# ============================================================================
class Parser:
    def __init__(self, scanner: Scanner) -> None:
        self.scanner = scanner
        self.tokens: list[Token] = list(scanner)
        self.current = 0
        self.errors: list[SyntaxError] = []

    def parse(self) -> bool:
        """Analisa o programa sintaticamente"""
        while not self._is_at_end():
            try:
                self._declaration()
            except SyntaxError:
                # Tenta recuperar do erro avançando até a próxima declaração
                self._synchronize()
        return len(self.errors) == 0
    
    def _synchronize(self) -> None:
        """Recupera de erros sintáticos avançando até a próxima declaração"""
        while not self._is_at_end():
            if self._previous().type == TokenType.RPAREN:
                return
            if self._check(TokenType.INT) or self._check(TokenType.FLOAT) or \
               self._check(TokenType.PRINT) or self._check(TokenType.IF):
                return
            self._advance()

    def _declaration(self) -> None:
        """DECLARAÇÃO -> TIPO IDENTIFIER ASSIGN EXPRESSAO | print ( EXPRESSAO ) | if ( EXPRESSAO ) DECLARAÇÃO [else DECLARAÇÃO]"""
        if self._check(TokenType.INT) or self._check(TokenType.FLOAT):
            self._type_declaration()
        elif self._check(TokenType.PRINT):
            self._print_statement()
        elif self._check(TokenType.IF):
            self._if_statement()
        elif self._check(TokenType.IDENTIFIER):
            self._assignment()
        else:
            token = self._peek()
            self._error(f"Declaração esperada, encontrado: '{token.lexeme}'", token)
            raise SyntaxError("Erro de declaração", token.line, token.column)

    def _type_declaration(self) -> None:
        """TIPO IDENTIFIER ASSIGN EXPRESSAO"""
        if not (self._match(TokenType.INT) or self._match(TokenType.FLOAT)):
            token = self._peek()
            self._error("Esperado 'int' ou 'float'", token)
        self._consume(TokenType.IDENTIFIER, "Esperado identificador")
        self._consume(TokenType.ASSIGN, "Esperado '='")
        self._expression()

    def _assignment(self) -> None:
        """IDENTIFIER ASSIGN EXPRESSAO"""
        self._consume(TokenType.IDENTIFIER, "Esperado identificador")
        self._consume(TokenType.ASSIGN, "Esperado '='")
        self._expression()

    def _print_statement(self) -> None:
        """print ( EXPRESSAO )"""
        self._consume(TokenType.PRINT, "Esperado 'print'")
        self._consume(TokenType.LPAREN, "Esperado '('")
        self._expression()
        self._consume(TokenType.RPAREN, "Esperado ')'")

    def _if_statement(self) -> None:
        """if ( EXPRESSAO ) DECLARAÇÃO [else DECLARAÇÃO]"""
        self._consume(TokenType.IF, "Esperado 'if'")
        self._consume(TokenType.LPAREN, "Esperado '('")
        self._expression()
        self._consume(TokenType.RPAREN, "Esperado ')'")
        self._declaration()
        if self._check(TokenType.ELSE):
            self._advance()
            self._declaration()

    def _expression(self) -> None:
        """EXPRESSAO -> TERMO ( (PLUS|MINUS|GT|GTE|LT|LTE|EQUAL_EQUAL|NOT_EQUAL) TERMO )*"""
        self._term()
        while self._match(TokenType.PLUS, TokenType.MINUS, TokenType.GT, TokenType.GTE, 
                          TokenType.LT, TokenType.LTE, TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL):
            self._term()

    def _term(self) -> None:
        """TERMO -> FATOR ( (STAR|SLASH) FATOR )*"""
        self._factor()
        while self._match(TokenType.STAR, TokenType.SLASH):
            self._factor()

    def _factor(self) -> None:
        """FATOR -> NUMBER | IDENTIFIER | ( EXPRESSAO )"""
        if self._match(TokenType.NUMBER):
            return
        if self._match(TokenType.IDENTIFIER):
            return
        if self._match(TokenType.LPAREN):
            self._expression()
            self._consume(TokenType.RPAREN, "Esperado ')'")
            return
        token = self._peek()
        self._error(f"Fator esperado, encontrado: '{token.lexeme}'", token)
        raise SyntaxError("Erro de fator", token.line, token.column)

    def _match(self, *types: TokenType) -> bool:
        """Verifica se o token atual corresponde a algum dos tipos"""
        for token_type in types:
            if self._check(token_type):
                self._advance()
                return True
        return False

    def _check(self, token_type: TokenType) -> bool:
        """Verifica se o token atual é do tipo especificado"""
        if self._is_at_end():
            return False
        return self._peek().type == token_type

    def _advance(self) -> Token:
        """Avança para o próximo token"""
        if not self._is_at_end():
            self.current += 1
        return self._previous()

    def _is_at_end(self) -> bool:
        """Verifica se chegou ao fim"""
        return self.current >= len(self.tokens)

    def _peek(self) -> Token:
        """Retorna o token atual"""
        if self._is_at_end():
            return Token(TokenType.EOF, "", 0, 0)
        return self.tokens[self.current]

    def _previous(self) -> Token:
        """Retorna o token anterior"""
        return self.tokens[self.current - 1]

    def _consume(self, token_type: TokenType, message: str) -> None:
        """Consome um token do tipo esperado"""
        if self._check(token_type):
            self._advance()
        else:
            token = self._peek()
            self._error(f"{message}, encontrado: '{token.lexeme}'", token)
            raise SyntaxError(message, token.line, token.column)

    def _error(self, message: str, token: Token) -> None:
        """Registra um erro sintático"""
        error = SyntaxError(message, token.line, token.column)
        self.errors.append(error)
        # Não levanta exceção para permitir recuperação de erros

    def get_errors(self) -> list[SyntaxError]:
        """Retorna a lista de erros sintáticos"""
        return self.errors


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header():
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("=" * 80)
    print("🔍 ANALISADOR LÉXICO - COMPILADOR PY")
    print("=" * 80)
    print(f"{Colors.ENDC}")


def print_token(token, index):
    color_map = {
        'INT': Colors.CYAN,
        'FLOAT': Colors.CYAN,
        'IDENTIFIER': Colors.GREEN,
        'NUMBER': Colors.WARNING,
        'ASSIGN': Colors.RED,
        'GTE': Colors.RED,
        'LPAREN': Colors.BLUE,
        'RPAREN': Colors.BLUE,
        'IF': Colors.HEADER,
        'PRINT': Colors.HEADER,
    }
    
    color = color_map.get(token.type.name, Colors.ENDC)
    token_type = f"{color}{Colors.BOLD}{token.type.name:<12}{Colors.ENDC}"
    lexeme = f"{Colors.WARNING}'{token.lexeme}'{Colors.ENDC}"
    position = f"{Colors.CYAN}L{token.line:2d}:C{token.column:2d}{Colors.ENDC}"
    
    print(f"  {index:2d}. {token_type} → {lexeme:<15} {position}")


def print_statistics(tokens):
    token_counts = Counter(token.type for token in tokens)
    
    print(f"\n{Colors.HEADER}{Colors.BOLD}📊 ESTATÍSTICAS DOS TOKENS{Colors.ENDC}")
    print(f"{Colors.CYAN}{'─' * 50}{Colors.ENDC}")
    
    for token_type, count in token_counts.most_common():
        percentage = (count / len(tokens)) * 100
        bar = "█" * int(percentage / 2)
        print(f"  {token_type.name:<12} {count:3d} tokens ({percentage:5.1f}%) {bar}")
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}Total: {len(tokens)} tokens encontrados{Colors.ENDC}")


def print_summary(source_path=None, is_interactive=False):
    print(f"\n{Colors.HEADER}{Colors.BOLD}📄 ENTRADA ANALISADA{Colors.ENDC}")
    print(f"{Colors.CYAN}{'─' * 50}{Colors.ENDC}")
    
    if is_interactive:
        print(f"  Modo: {Colors.WARNING}Entrada Interativa{Colors.ENDC}")
    else:
        print(f"  Arquivo: {Colors.WARNING}{source_path}{Colors.ENDC}")
        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            print(f"  Linhas: {Colors.GREEN}{len(lines)}{Colors.ENDC}")
            print(f"  Tamanho: {Colors.GREEN}{sum(len(line) for line in lines)} caracteres{Colors.ENDC}")
        except:
            pass


def get_user_input():
    print(f"\n{Colors.CYAN}{Colors.BOLD}💬 Digite seu código (ou cole um trecho):{Colors.ENDC}")
    print(f"{Colors.WARNING}💡 Dicas:{Colors.ENDC}")
    print(f"  • Digite 'SAIR' para encerrar")
    print(f"  • Digite 'AJUDA' para ver exemplos de sintaxe")
    print(f"  • Use Ctrl+C para sair a qualquer momento")
    print(f"{Colors.CYAN}{'─' * 60}{Colors.ENDC}")
    
    lines = []
    print(f"{Colors.GREEN}>>> {Colors.ENDC}", end="", flush=True)
    
    try:
        while True:
            line = input()
            if line.strip().upper() == "SAIR":
                if lines:
                    return "\n".join(lines)
                return None
            elif line.strip().upper() == "AJUDA":
                print_help()
                print(f"{Colors.GREEN}>>> {Colors.ENDC}", end="", flush=True)
                continue
            elif line.strip() == "":
                break
            else:
                lines.append(line)
                print(f"{Colors.GREEN}>>> {Colors.ENDC}", end="", flush=True)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 Saindo...{Colors.ENDC}")
        return None
    
    return "\n".join(lines) if lines else None


def print_help():
    print(f"\n{Colors.HEADER}{Colors.BOLD}📚 EXEMPLOS DE SINTAXE SUPORTADA{Colors.ENDC}")
    print(f"{Colors.CYAN}{'─' * 60}{Colors.ENDC}")
    
    examples = [
        ("Variáveis:", "int x = 10"),
        ("Números:", "float y = 3.14"),
        ("Operações:", "x + y * 2"),
        ("Comparações:", "x >= 5"),
        ("Condicionais:", "if (x > 0)"),
        ("Impressão:", "print(x)"),
        ("Comentários:", "# Este é um comentário"),
        ("", "/* Comentário de bloco */"),
    ]
    
    for desc, example in examples:
        if desc:
            print(f"\n{Colors.WARNING}{desc}{Colors.ENDC}")
        print(f"  {Colors.GREEN}{example}{Colors.ENDC}")


def analyze_code(source_code, is_interactive=False, show_tokens=True):
    if show_tokens:
        print(f"\n{Colors.HEADER}{Colors.BOLD}🔤 TOKENS ENCONTRADOS{Colors.ENDC}")
        print(f"{Colors.CYAN}{'─' * 80}{Colors.ENDC}")

    try:
        scanner = Scanner.from_string(source_code)
        tokens = list(scanner)
        
        if not tokens:
            print(f"{Colors.YELLOW}⚠️  Nenhum token encontrado no código fornecido{Colors.ENDC}")
            return
        
        if show_tokens:
            for i, token in enumerate(tokens, 1):
                print_token(token, i)
            print_statistics(tokens)
        
        # Análise sintática
        print(f"\n{Colors.HEADER}{Colors.BOLD}📐 ANÁLISE SINTÁTICA{Colors.ENDC}")
        print(f"{Colors.CYAN}{'─' * 80}{Colors.ENDC}")
        
        scanner = Scanner.from_string(source_code)
        parser = Parser(scanner)
        
        try:
            success = parser.parse()
            if success:
                print(f"{Colors.GREEN}{Colors.BOLD}✅ Análise sintática concluída com sucesso!{Colors.ENDC}")
            else:
                errors = parser.get_errors()
                if errors:
                    print(f"{Colors.RED}{Colors.BOLD}❌ ERROS SINTÁTICOS ENCONTRADOS:{Colors.ENDC}")
                    for error in errors:
                        print(f"{Colors.RED}  {str(error)}{Colors.ENDC}")
        except SyntaxError as e:
            print(f"{Colors.RED}{Colors.BOLD}❌ ERRO SINTÁTICO:{Colors.ENDC}")
            print(f"{Colors.RED}{str(e)}{Colors.ENDC}")
        
        if show_tokens:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Análise léxica concluída com sucesso!{Colors.ENDC}")
        
    except LexicalError as e:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ ERRO LÉXICO:{Colors.ENDC}")
        print(f"{Colors.RED}{str(e)}{Colors.ENDC}")


def interactive_mode():
    print_header()
    print(f"{Colors.GREEN}{Colors.BOLD}🎯 MODO INTERATIVO ATIVADO{Colors.ENDC}")
    print(f"{Colors.CYAN}Digite seu código diretamente no terminal!{Colors.ENDC}")
    
    while True:
        source_code = get_user_input()
        if source_code is None:
            break
            
        print_summary(is_interactive=True)
        analyze_code(source_code, is_interactive=True)
        
        print(f"\n{Colors.CYAN}Deseja analisar outro código? (s/n): {Colors.ENDC}", end="", flush=True)
        try:
            response = input().strip().lower()
            if response not in ['s', 'sim', 'y', 'yes']:
                break
        except KeyboardInterrupt:
            break
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}👋 Obrigado por usar o Analisador Léxico!{Colors.ENDC}")


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] in ['-i', '--interactive', '--interativo']:
        interactive_mode()
        return
    
    if len(sys.argv) < 2:
        source_path = Path("programa.mc")
        if not source_path.exists():
            print(f"{Colors.RED}❌ Arquivo programa.mc não encontrado!{Colors.ENDC}")
            print(f"{Colors.YELLOW}💡 Opções disponíveis:{Colors.ENDC}")
            print(f"  • {Colors.CYAN}python3 main.py <arquivo.mc>{Colors.ENDC} - Analisar arquivo")
            print(f"  • {Colors.CYAN}python3 main.py -i{Colors.ENDC} - Modo interativo")
            print(f"  • {Colors.CYAN}Coloque um arquivo chamado 'programa.mc' na pasta atual{Colors.ENDC}")
            sys.exit(1)
    else:
        source_path = Path(sys.argv[1])
        if not source_path.exists():
            print(f"{Colors.RED}❌ Arquivo não encontrado: {source_path}{Colors.ENDC}")
            sys.exit(1)

    print_header()
    print_summary(source_path)
    
    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        analyze_code(source_code)
    except Exception as e:
        print(f"{Colors.RED}❌ Erro ao ler arquivo: {e}{Colors.ENDC}")
        sys.exit(1)


if __name__ == "__main__":
    main()
