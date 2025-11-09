"""
Compilador - Analisador Léxico e Sintático
Checkpoint 01: Analisador Léxico
Checkpoint 02: Analisador Sintático

Disciplina: Projeto de Linguagens de Programação

Integrantes do Grupo:
- Matheus Farias
- Ryan Nascimento
- Luiz Fernando
- Otávio Fernando
"""
# Importa recursos para usar anotações de tipo mais modernas
from __future__ import annotations
# Importa sys para acessar argumentos da linha de comando e sair do programa
import sys
# Importa Path para trabalhar com caminhos de arquivos de forma mais fácil
from pathlib import Path
# Importa dataclass para criar classes de dados automaticamente
from dataclasses import dataclass
# Importa Enum e auto para criar enumerações (tipos de tokens)
from enum import Enum, auto
# Importa Optional para indicar valores que podem ser None
# Importa Iterator para criar iteradores
from typing import Optional, Iterator
# Importa Counter para contar tokens e gerar estatísticas
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
# @dataclass cria automaticamente métodos __init__, __repr__, etc.
@dataclass
class Token:
    type: TokenType      # Tipo do token (INT, IDENTIFIER, NUMBER, etc.)
    lexeme: str          # O texto exato encontrado ("int", "x", "10", etc.)
    line: int            # Linha onde foi encontrado (começa em 1)
    column: int          # Coluna onde foi encontrado (começa em 1)

    def __str__(self) -> str:
        # Retorna uma string formatada com todas as informações do token
        # Exemplo: "Token(type=INT, lexeme='int', line=1, column=1)"
        return f"Token(type={self.type.name}, lexeme='{self.lexeme}', line={self.line}, column={self.column})"


# ============================================================================
# ERRO LÉXICO
# ============================================================================
# Exceção lançada quando encontra um símbolo inválido
# Exemplo: se encontrar "@", que não é permitido, lança este erro
# ============================================================================
class LexicalError(Exception):
    # Construtor da exceção de erro léxico
    def __init__(self, message: str, line: int, column: int) -> None:
        # Chama o construtor da classe pai (Exception)
        super().__init__(message)
        # Armazena a mensagem de erro
        self.message = message
        # Armazena a linha onde o erro ocorreu
        self.line = line
        # Armazena a coluna onde o erro ocorreu
        self.column = column

    def __str__(self) -> str:
        # Retorna uma mensagem formatada com a posição do erro
        # Exemplo: "Erro léxico na linha 3, coluna 5: Símbolo inválido: '@'"
        return f"Erro léxico na linha {self.line}, coluna {self.column}: {self.message}"


# ============================================================================
# SCANNER (ANALISADOR LÉXICO)
# ============================================================================
# Responsável por ler o código e identificar os tokens
# Funciona como um "leitor" que vai caractere por caractere e identifica
# o que é palavra, número, operador, etc.
# ============================================================================
class Scanner:
    # Construtor do Scanner - recebe o caminho do arquivo
    def __init__(self, source_path: str) -> None:
        # Abre o arquivo em modo leitura com codificação UTF-8
        # 'with' garante que o arquivo será fechado automaticamente
        with open(source_path, "r", encoding="utf-8") as f:
            # Lê todo o conteúdo do arquivo e armazena em self.source
            self.source: str = f.read()
        # Calcula o tamanho total do código (número de caracteres)
        self.length: int = len(self.source)
        # Inicializa o índice na posição 0 (primeiro caractere)
        self.index: int = 0
        # Inicializa a linha em 1 (primeira linha)
        self.line: int = 1
        # Inicializa a coluna em 1 (primeira coluna)
        self.column: int = 1
    
    # Método de classe que cria um Scanner a partir de uma string (não de arquivo)
    # Útil para modo interativo ou testes
    @classmethod
    def from_string(cls, source_code: str) -> 'Scanner':
        # Cria uma nova instância sem chamar __init__
        scanner = cls.__new__(cls)
        # Define o código fonte como a string fornecida
        scanner.source = source_code
        # Calcula o tamanho da string
        scanner.length = len(source_code)
        # Inicializa o índice em 0
        scanner.index = 0
        # Inicializa a linha em 1
        scanner.line = 1
        # Inicializa a coluna em 1
        scanner.column = 1
        # Retorna o scanner criado
        return scanner

    # Método especial que permite usar o Scanner em loops 'for'
    # Exemplo: for token in scanner: ...
    def __iter__(self) -> Iterator[Token]:
        # Loop infinito até encontrar o fim do arquivo
        while True:
            # Lê o próximo token
            token = self.next_token()
            # Se retornou None, chegou ao fim do arquivo
            if token is None:
                # Sai do loop
                break
            # Retorna o token (yield permite usar como gerador)
            yield token

    # Lê o próximo token do código fonte
    def next_token(self) -> Optional[Token]:
        """
        Lê o próximo token do código.
        Retorna None quando chega ao fim do arquivo.
        """
        # Primeiro, pula espaços em branco e comentários (não geram tokens)
        self._skip_whitespace_and_comments()
        
        # Se depois de pular espaços chegou ao fim do arquivo, retorna None
        if self._is_eof():
            return None

        # Guarda a posição onde este token começa (linha e coluna)
        # Isso é importante para reportar erros com a posição correta
        start_line, start_col = self.line, self.column
        
        # Lê o próximo caractere e avança o índice
        char = self._advance()

        # ====================================================================
        # IDENTIFICADORES E PALAVRAS RESERVADAS
        # ====================================================================
        # Se o caractere é uma letra ou underscore, é início de identificador
        # Exemplo: "int", "x", "variavel123", "_temp"
        # ====================================================================
        if self._is_letter(char) or char == "_":
            # Lista para construir o nome completo do identificador
            lexeme = [char]
            # Continua lendo enquanto os próximos caracteres forem letra, dígito ou underscore
            while not self._is_eof():
                # Olha o próximo caractere sem avançar
                c = self._peek()
                # Se é letra, dígito ou underscore, faz parte do identificador
                if self._is_letter(c) or self._is_digit(c) or c == "_":
                    # Adiciona o caractere à lista e avança
                    lexeme.append(self._advance())
                else:
                    # Se não é mais parte do identificador, para de ler
                    break
            # Junta todos os caracteres em uma string
            text = "".join(lexeme)
            # Verifica se é palavra reservada (int, float, print, if, else)
            # Se estiver no dicionário RESERVED_KEYWORDS, retorna o tipo correspondente
            # Se não estiver, é um identificador comum (TokenType.IDENTIFIER)
            token_type = RESERVED_KEYWORDS.get(text, TokenType.IDENTIFIER)
            # Retorna o token criado
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
        # Se é parêntese esquerdo, retorna token LPAREN
        if char == "(":
            return Token(TokenType.LPAREN, "(", start_line, start_col)
        # Se é parêntese direito, retorna token RPAREN
        if char == ")":
            return Token(TokenType.RPAREN, ")", start_line, start_col)

        # ====================================================================
        # OPERADORES MATEMÁTICOS
        # ====================================================================
        # Se é '+', retorna token PLUS
        if char == "+":
            return Token(TokenType.PLUS, "+", start_line, start_col)
        # Se é '-', retorna token MINUS
        if char == "-":
            return Token(TokenType.MINUS, "-", start_line, start_col)
        # Se é '*', retorna token STAR
        if char == "*":
            return Token(TokenType.STAR, "*", start_line, start_col)
        # Se é '/', retorna token SLASH
        if char == "/":
            return Token(TokenType.SLASH, "/", start_line, start_col)

        # ====================================================================
        # OPERADOR DE ATRIBUIÇÃO E IGUALDADE
        # ====================================================================
        # "=" sozinho é atribuição, "==" é comparação de igualdade
        # ====================================================================
        if char == "=":
            # Verifica se o próximo caractere também é "="
            if self._match("="):
                # Se sim, é "==" (igualdade)
                return Token(TokenType.EQUAL_EQUAL, "==", start_line, start_col)
            # Se não, é apenas "=" (atribuição)
            return Token(TokenType.ASSIGN, "=", start_line, start_col)

        # ====================================================================
        # OPERADORES RELACIONAIS
        # ====================================================================
        # ">", ">=", "<", "<=", "!="
        # ====================================================================
        # Se é '>', verifica se é ">=" ou apenas ">"
        if char == ">":
            # Verifica se o próximo caractere é "="
            if self._match("="):
                # Se sim, é ">=" (maior ou igual)
                return Token(TokenType.GTE, ">=", start_line, start_col)
            # Se não, é apenas ">" (maior que)
            return Token(TokenType.GT, ">", start_line, start_col)

        # Se é '<', verifica se é "<=" ou apenas "<"
        if char == "<":
            # Verifica se o próximo caractere é "="
            if self._match("="):
                # Se sim, é "<=" (menor ou igual)
                return Token(TokenType.LTE, "<=", start_line, start_col)
            # Se não, é apenas "<" (menor que)
            return Token(TokenType.LT, "<", start_line, start_col)

        # Se é '!', deve ser seguido de "=" para formar "!="
        if char == "!":
            # Verifica se o próximo caractere é "="
            if self._match("="):
                # Se sim, é "!=" (diferente)
                return Token(TokenType.NOT_EQUAL, "!=", start_line, start_col)
            # Se não, é um erro - "!" sozinho não é permitido
            self._raise_error("'!' isolado não é permitido; esperava '!='", start_line, start_col)

        # ====================================================================
        # SÍMBOLO INVÁLIDO
        # ====================================================================
        # Se chegou aqui, é um caractere que não reconhecemos
        # Exemplo: "@", "ç", "`", etc.
        # ====================================================================
        self._raise_error(f"Símbolo inválido: '{char}'", start_line, start_col)

    # Reconhece números com ponto decimal (ex: 123, 123.456, .456)
    def _number_token(self, start_line: int, start_col: int, first_char: str) -> Optional[Token]:
        """
        Reconhece números com ponto decimal.
        Válidos: 123, 123.456, .456
        Inválidos: 1., 12., 156. (não pode terminar em ponto sem dígitos)
        """
        # Lista para construir o número completo
        lexeme = [first_char]
        # Verifica se o primeiro caractere já é um ponto
        saw_dot = first_char == "."
        # Flag para verificar se há dígitos depois do ponto
        has_digits_after_dot = False
        # Verifica se o primeiro caractere é um dígito
        has_digits_before_dot = first_char.isdigit()

        # Função auxiliar para verificar se um caractere é dígito
        def is_digit(c: str) -> bool:
            # Retorna True se o caractere está entre '0' e '9'
            return "0" <= c <= "9"

        # Se começou com dígito, lê todos os dígitos antes do ponto
        if has_digits_before_dot:
            # Enquanto não chegou ao fim e o próximo caractere é dígito
            while not self._is_eof() and is_digit(self._peek()):
                # Adiciona o dígito à lista e avança
                lexeme.append(self._advance())

        # Se ainda não viu o ponto e o próximo caractere é ponto
        if not saw_dot and not self._is_eof() and self._peek() == ".":
            # Marca que viu o ponto
            saw_dot = True
            # Adiciona o ponto à lista e avança
            lexeme.append(self._advance())

        # Se viu o ponto (ou começou com ponto)
        if saw_dot:
            # Lê todos os dígitos depois do ponto
            while not self._is_eof() and is_digit(self._peek()):
                # Marca que há dígitos depois do ponto
                has_digits_after_dot = True
                # Adiciona o dígito à lista e avança
                lexeme.append(self._advance())

            # Se não há dígitos depois do ponto, é um erro (ex: 1., 12.)
            if not has_digits_after_dot:
                # Lança erro: número inválido
                self._raise_error("Número inválido: faltam dígitos após o ponto", start_line, start_col)

        # Junta todos os caracteres em uma string
        text = "".join(lexeme)
        # Retorna um token NUMBER com o número encontrado
        return Token(TokenType.NUMBER, text, start_line, start_col)

    # Pula espaços em branco e comentários (não geram tokens)
    def _skip_whitespace_and_comments(self) -> None:
        """
        Pula espaços em branco e comentários.
        Comentários não geram tokens, são ignorados.
        """
        # Enquanto não chegou ao fim do arquivo
        while not self._is_eof():
            # Olha o caractere atual sem avançar
            c = self._peek()
            
            # Se é espaço, tab ou retorno de carro, pula
            if c in (" ", "\t", "\r"):
                # Avança para o próximo caractere
                self._advance()
                # Continua o loop (pula para a próxima iteração)
                continue
            
            # Se é quebra de linha, pula e atualiza contadores
            if c == "\n":
                # Avança para o próximo caractere
                self._advance()
                # Incrementa a linha
                self.line += 1
                # Reseta a coluna para 1 (início da nova linha)
                self.column = 1
                # Continua o loop
                continue

            # ================================================================
            # COMENTÁRIO DE LINHA (# comentário)
            # ================================================================
            # Se encontrou '#', é início de comentário de linha
            if c == "#":
                # Lê todos os caracteres até encontrar quebra de linha
                while not self._is_eof() and self._peek() not in ("\n", "\r"):
                    # Avança (consome o caractere do comentário)
                    self._advance()
                # Continua o loop (comentário foi ignorado)
                continue

            # ================================================================
            # COMENTÁRIO DE BLOCO (/* comentário */)
            # ================================================================
            # Se encontrou '/' e o próximo é '*', é início de comentário de bloco
            if c == "/" and self._peek_next() == "*":
                # Guarda a posição onde o comentário começou (para reportar erro se não fechar)
                comment_start_line, comment_start_col = self.line, self.column
                # Consome o '/' e o '*'
                self._advance()  # Consome '/'
                self._advance()  # Consome '*'
                # Lê todos os caracteres até encontrar '*/'
                while not self._is_eof():
                    # Se encontrou quebra de linha, atualiza contadores
                    if self._peek() == "\n":
                        # Avança (consome a quebra de linha)
                        self._advance()
                        # Incrementa a linha
                        self.line += 1
                        # Reseta a coluna
                        self.column = 1
                        # Continua o loop interno
                        continue
                    # Se encontrou '*' e o próximo é '/', fim do comentário
                    if self._peek() == "*" and self._peek_next() == "/":
                        # Consome '*' e '/'
                        self._advance()  # Consome '*'
                        self._advance()  # Consome '/'
                        # Sai do loop (comentário foi fechado)
                        break
                    # Avança (consome caractere do comentário)
                    self._advance()
                else:
                    # Se chegou aqui, o loop terminou sem encontrar '*/'
                    # Isso significa que o comentário não foi fechado - é um erro
                    self._raise_error("Comentário de múltiplas linhas não finalizado (esperava '*/')", comment_start_line, comment_start_col)
                # Continua o loop externo (comentário foi ignorado)
                continue

            # Se chegou aqui, não é espaço nem comentário - para o loop
            break

    # Avança para o próximo caractere e retorna o caractere atual
    def _advance(self) -> str:
        # Pega o caractere na posição atual do índice
        ch = self.source[self.index]
        # Incrementa o índice para apontar para o próximo caractere
        self.index += 1
        # Incrementa a coluna (estamos na mesma linha, mas coluna seguinte)
        self.column += 1
        # Retorna o caractere que foi lido
        return ch

    # Verifica se o próximo caractere é o esperado e avança se for
    def _match(self, expected: str) -> bool:
        # Se chegou ao fim OU o caractere atual não é o esperado
        if self._is_eof() or self.source[self.index] != expected:
            # Retorna False (não encontrou o caractere esperado)
            return False
        # Se chegou aqui, encontrou o caractere esperado
        # Avança o índice para o próximo caractere
        self.index += 1
        # Avança a coluna
        self.column += 1
        # Retorna True (encontrou e consumiu o caractere)
        return True

    # Olha o caractere atual sem avançar (não consome o caractere)
    def _peek(self) -> str:
        # Se chegou ao fim, retorna caractere nulo
        # Senão, retorna o caractere na posição atual
        return "\0" if self._is_eof() else self.source[self.index]

    # Olha o próximo caractere sem avançar (olha 1 caractere à frente)
    def _peek_next(self) -> str:
        # Se o próximo índice está além do tamanho do código
        if self.index + 1 >= self.length:
            # Retorna caractere nulo
            return "\0"
        # Senão, retorna o caractere na posição seguinte
        return self.source[self.index + 1]

    # Verifica se chegou ao fim do arquivo (End Of File)
    def _is_eof(self) -> bool:
        # Retorna True se o índice é maior ou igual ao tamanho do código
        return self.index >= self.length

    # Verifica se um caractere é uma letra (a-z ou A-Z)
    def _is_letter(self, c: str) -> bool:
        # Verifica se está entre 'a' e 'z' (minúsculas) OU entre 'A' e 'Z' (maiúsculas)
        return ("a" <= c <= "z") or ("A" <= c <= "Z")

    # Verifica se um caractere é um dígito (0-9)
    def _is_digit(self, c: str) -> bool:
        # Verifica se está entre '0' e '9'
        return "0" <= c <= "9"

    # Lança uma exceção de erro léxico
    def _raise_error(self, message: str, start_line: int, start_col: int) -> None:
        # Cria e lança uma exceção LexicalError com a mensagem e posição
        raise LexicalError(message, start_line, start_col)


# ============================================================================
# ERRO SINTÁTICO
# ============================================================================
# Exceção lançada quando o código não está escrito corretamente
# Exemplo: "int x =" sem valor, ou "print(" sem fechar parêntese
# ============================================================================
class SyntaxError(Exception):
    # Construtor da exceção de erro sintático
    def __init__(self, message: str, line: int, column: int) -> None:
        # Chama o construtor da classe pai (Exception)
        super().__init__(message)
        # Armazena a mensagem de erro
        self.message = message
        # Armazena a linha onde o erro ocorreu
        self.line = line
        # Armazena a coluna onde o erro ocorreu
        self.column = column

    def __str__(self) -> str:
        # Retorna uma mensagem formatada com a posição do erro
        # Exemplo: "Erro sintático na linha 5, coluna 3: Esperado '=', encontrado: 'x'"
        return f"Erro sintático na linha {self.line}, coluna {self.column}: {self.message}"


# ============================================================================
# PARSER (ANALISADOR SINTÁTICO)
# ============================================================================
# Responsável por verificar se o código está escrito corretamente
# Usa os tokens do Scanner para verificar se seguem as regras da gramática
# Exemplo: verifica se "int x = 10" está correto (tipo, nome, =, valor)
# ============================================================================
class Parser:
    # Construtor do Parser - recebe um Scanner
    def __init__(self, scanner: Scanner) -> None:
        # Guarda a referência do scanner
        self.scanner = scanner
        # Converte o scanner em uma lista de tokens (lê todos os tokens de uma vez)
        self.tokens: list[Token] = list(scanner)
        # Inicializa o índice do token atual em 0 (primeiro token)
        self.current = 0
        # Inicializa a lista de erros sintáticos (começa vazia)
        self.errors: list[SyntaxError] = []

    # Método principal que analisa todo o programa sintaticamente
    def parse(self) -> bool:
        """Analisa o programa sintaticamente"""
        # Enquanto não chegou ao fim dos tokens
        while not self._is_at_end():
            try:
                # Tenta analisar uma declaração
                self._declaration()
            except SyntaxError:
                # Se deu erro, tenta recuperar avançando até a próxima declaração
                # Isso permite encontrar múltiplos erros em vez de parar no primeiro
                self._synchronize()
        # Retorna True se não há erros, False se há erros
        return len(self.errors) == 0
    
    # Método de recuperação de erros - avança até encontrar um ponto seguro
    def _synchronize(self) -> None:
        """Recupera de erros sintáticos avançando até a próxima declaração"""
        # Enquanto não chegou ao fim
        while not self._is_at_end():
            # Se o token anterior era um parêntese direito, já está em um ponto seguro
            if self._previous().type == TokenType.RPAREN:
                # Para a recuperação
                return
            # Se encontrou o início de uma nova declaração (int, float, print, if)
            if self._check(TokenType.INT) or self._check(TokenType.FLOAT) or \
               self._check(TokenType.PRINT) or self._check(TokenType.IF):
                # Para a recuperação (encontrou um ponto seguro)
                return
            # Avança para o próximo token (pula tokens até encontrar algo reconhecível)
            self._advance()

    # Analisa uma declaração (pode ser declaração de variável, print, if, ou atribuição)
    def _declaration(self) -> None:
        """DECLARAÇÃO -> TIPO IDENTIFIER ASSIGN EXPRESSAO | print ( EXPRESSAO ) | if ( EXPRESSAO ) DECLARAÇÃO [else DECLARAÇÃO]"""
        # Se o token atual é 'int' ou 'float', é uma declaração de variável com tipo
        if self._check(TokenType.INT) or self._check(TokenType.FLOAT):
            # Analisa declaração de variável com tipo (ex: int x = 10)
            self._type_declaration()
        # Se o token atual é 'print', é um comando de impressão
        elif self._check(TokenType.PRINT):
            # Analisa comando print (ex: print(x))
            self._print_statement()
        # Se o token atual é 'if', é uma estrutura condicional
        elif self._check(TokenType.IF):
            # Analisa estrutura if (ex: if (x > 5) print(x))
            self._if_statement()
        # Se o token atual é um identificador, é uma atribuição simples
        elif self._check(TokenType.IDENTIFIER):
            # Analisa atribuição (ex: x = 10)
            self._assignment()
        else:
            # Se não é nenhum dos casos acima, é um erro
            # Pega o token atual para reportar o erro
            token = self._peek()
            # Registra o erro
            self._error(f"Declaração esperada, encontrado: '{token.lexeme}'", token)
            # Lança exceção para parar a análise desta declaração
            raise SyntaxError("Erro de declaração", token.line, token.column)

    # Analisa declaração de variável com tipo (ex: int x = 10)
    def _type_declaration(self) -> None:
        """TIPO IDENTIFIER ASSIGN EXPRESSAO"""
        # Verifica se o token atual é 'int' ou 'float' e consome se for
        # Se não for nenhum dos dois, é um erro
        if not (self._match(TokenType.INT) or self._match(TokenType.FLOAT)):
            # Pega o token atual para reportar o erro
            token = self._peek()
            # Registra o erro
            self._error("Esperado 'int' ou 'float'", token)
        # Consome um identificador (nome da variável) - obrigatório
        self._consume(TokenType.IDENTIFIER, "Esperado identificador")
        # Consome o operador de atribuição '=' - obrigatório
        self._consume(TokenType.ASSIGN, "Esperado '='")
        # Analisa a expressão (valor que será atribuído)
        self._expression()

    # Analisa atribuição simples (ex: x = 10)
    def _assignment(self) -> None:
        """IDENTIFIER ASSIGN EXPRESSAO"""
        # Consome um identificador (nome da variável) - obrigatório
        self._consume(TokenType.IDENTIFIER, "Esperado identificador")
        # Consome o operador de atribuição '=' - obrigatório
        self._consume(TokenType.ASSIGN, "Esperado '='")
        # Analisa a expressão (valor que será atribuído)
        self._expression()

    # Analisa comando print (ex: print(x))
    def _print_statement(self) -> None:
        """print ( EXPRESSAO )"""
        # Consome a palavra reservada 'print' - obrigatório
        self._consume(TokenType.PRINT, "Esperado 'print'")
        # Consome o parêntese esquerdo '(' - obrigatório
        self._consume(TokenType.LPAREN, "Esperado '('")
        # Analisa a expressão que será impressa
        self._expression()
        # Consome o parêntese direito ')' - obrigatório
        self._consume(TokenType.RPAREN, "Esperado ')'")

    # Analisa estrutura condicional if (ex: if (x > 5) print(x) else print(y))
    def _if_statement(self) -> None:
        """if ( EXPRESSAO ) DECLARAÇÃO [else DECLARAÇÃO]"""
        # Consome a palavra reservada 'if' - obrigatório
        self._consume(TokenType.IF, "Esperado 'if'")
        # Consome o parêntese esquerdo '(' - obrigatório
        self._consume(TokenType.LPAREN, "Esperado '('")
        # Analisa a expressão de condição (ex: x > 5)
        self._expression()
        # Consome o parêntese direito ')' - obrigatório
        self._consume(TokenType.RPAREN, "Esperado ')'")
        # Analisa a declaração que será executada se a condição for verdadeira
        self._declaration()
        # Verifica se há um 'else' (opcional)
        if self._check(TokenType.ELSE):
            # Consome o 'else'
            self._advance()
            # Analisa a declaração que será executada se a condição for falsa
            self._declaration()

    # Analisa expressão (pode ter operadores +, -, >, >=, <, <=, ==, !=)
    def _expression(self) -> None:
        """EXPRESSAO -> TERMO ( (PLUS|MINUS|GT|GTE|LT|LTE|EQUAL_EQUAL|NOT_EQUAL) TERMO )*"""
        # Analisa o primeiro termo
        self._term()
        # Enquanto encontrar operadores de expressão (+, -, >, >=, <, <=, ==, !=)
        while self._match(TokenType.PLUS, TokenType.MINUS, TokenType.GT, TokenType.GTE, 
                          TokenType.LT, TokenType.LTE, TokenType.EQUAL_EQUAL, TokenType.NOT_EQUAL):
            # Analisa o próximo termo (ex: x + y, x >= 5, x == y)
            self._term()

    # Analisa termo (pode ter operadores * e /)
    def _term(self) -> None:
        """TERMO -> FATOR ( (STAR|SLASH) FATOR )*"""
        # Analisa o primeiro fator
        self._factor()
        # Enquanto encontrar operadores de multiplicação ou divisão (*, /)
        while self._match(TokenType.STAR, TokenType.SLASH):
            # Analisa o próximo fator (ex: x * y, x / 2)
            self._factor()

    # Analisa fator (número, identificador ou expressão entre parênteses)
    def _factor(self) -> None:
        """FATOR -> NUMBER | IDENTIFIER | ( EXPRESSAO )"""
        # Se o token atual é um número, consome e retorna
        if self._match(TokenType.NUMBER):
            return
        # Se o token atual é um identificador, consome e retorna
        if self._match(TokenType.IDENTIFIER):
            return
        # Se o token atual é um parêntese esquerdo, é uma expressão entre parênteses
        if self._match(TokenType.LPAREN):
            # Analisa a expressão dentro dos parênteses
            self._expression()
            # Consome o parêntese direito ')' - obrigatório
            self._consume(TokenType.RPAREN, "Esperado ')'")
            return
        # Se chegou aqui, não é nenhum fator válido - é um erro
        token = self._peek()
        # Registra o erro
        self._error(f"Fator esperado, encontrado: '{token.lexeme}'", token)
        # Lança exceção para parar a análise
        raise SyntaxError("Erro de fator", token.line, token.column)

    # Verifica se o token atual corresponde a algum dos tipos fornecidos
    # Se corresponder, consome o token e retorna True
    def _match(self, *types: TokenType) -> bool:
        """Verifica se o token atual corresponde a algum dos tipos"""
        # Para cada tipo fornecido
        for token_type in types:
            # Verifica se o token atual é deste tipo
            if self._check(token_type):
                # Se for, avança para o próximo token (consome o token)
                self._advance()
                # Retorna True (encontrou e consumiu)
                return True
        # Se nenhum tipo correspondeu, retorna False
        return False

    # Verifica se o token atual é do tipo especificado (sem consumir o token)
    def _check(self, token_type: TokenType) -> bool:
        """Verifica se o token atual é do tipo especificado"""
        # Se chegou ao fim dos tokens, retorna False
        if self._is_at_end():
            return False
        # Retorna True se o tipo do token atual é igual ao tipo esperado
        return self._peek().type == token_type

    # Avança para o próximo token e retorna o token anterior
    def _advance(self) -> Token:
        """Avança para o próximo token"""
        # Se não chegou ao fim
        if not self._is_at_end():
            # Incrementa o índice do token atual
            self.current += 1
        # Retorna o token anterior (o que estava antes de avançar)
        return self._previous()

    # Verifica se chegou ao fim da lista de tokens
    def _is_at_end(self) -> bool:
        """Verifica se chegou ao fim"""
        # Retorna True se o índice atual é maior ou igual ao número de tokens
        return self.current >= len(self.tokens)

    # Retorna o token atual sem avançar (não consome o token)
    def _peek(self) -> Token:
        """Retorna o token atual"""
        # Se chegou ao fim, retorna um token EOF (End Of File)
        if self._is_at_end():
            return Token(TokenType.EOF, "", 0, 0)
        # Senão, retorna o token na posição atual
        return self.tokens[self.current]

    # Retorna o token anterior (o que estava antes do token atual)
    def _previous(self) -> Token:
        """Retorna o token anterior"""
        # Retorna o token na posição anterior ao índice atual
        return self.tokens[self.current - 1]

    # Consome um token do tipo esperado (obrigatório)
    # Se não for do tipo esperado, lança erro
    def _consume(self, token_type: TokenType, message: str) -> None:
        """Consome um token do tipo esperado"""
        # Verifica se o token atual é do tipo esperado
        if self._check(token_type):
            # Se for, avança para o próximo token (consome)
            self._advance()
        else:
            # Se não for, é um erro
            # Pega o token atual para reportar o erro
            token = self._peek()
            # Registra o erro com a mensagem fornecida
            self._error(f"{message}, encontrado: '{token.lexeme}'", token)
            # Lança exceção para parar a análise
            raise SyntaxError(message, token.line, token.column)

    # Registra um erro sintático na lista de erros
    def _error(self, message: str, token: Token) -> None:
        """Registra um erro sintático"""
        # Cria uma exceção SyntaxError com a mensagem e posição
        error = SyntaxError(message, token.line, token.column)
        # Adiciona o erro na lista de erros
        self.errors.append(error)
        # Não levanta exceção aqui para permitir recuperação de erros
        # (a exceção é lançada em _consume quando necessário)

    def get_errors(self) -> list[SyntaxError]:
        """Retorna a lista de erros sintáticos"""
        return self.errors


# ============================================================================
# CORES PARA TERMINAL
# ============================================================================
# Define códigos ANSI para colorir a saída do terminal
# ============================================================================
class Colors:
    HEADER = '\033[95m'    # Cor rosa/magenta para cabeçalhos
    BLUE = '\033[94m'      # Cor azul
    CYAN = '\033[96m'      # Cor ciano
    GREEN = '\033[92m'     # Cor verde
    WARNING = '\033[93m'   # Cor amarela (avisos)
    YELLOW = '\033[93m'    # Cor amarela (mesma que WARNING)
    RED = '\033[91m'       # Cor vermelha (erros)
    ENDC = '\033[0m'       # Reset de cor (volta ao padrão)
    BOLD = '\033[1m'       # Texto em negrito
    UNDERLINE = '\033[4m'  # Texto sublinhado


# Imprime o cabeçalho do programa
def print_header():
    # Aplica cor rosa e negrito
    print(f"{Colors.HEADER}{Colors.BOLD}")
    # Imprime linha de separação (80 caracteres de '=')
    print("=" * 80)
    # Imprime o título do programa
    print("🔍 ANALISADOR LÉXICO - COMPILADOR PY")
    # Imprime outra linha de separação
    print("=" * 80)
    # Reseta a cor (volta ao padrão)
    print(f"{Colors.ENDC}")


# Imprime um token formatado com cores
def print_token(token, index):
    # Mapa que associa tipos de tokens a cores
    color_map = {
        'INT': Colors.CYAN,        # int e float em ciano
        'FLOAT': Colors.CYAN,
        'IDENTIFIER': Colors.GREEN, # Identificadores em verde
        'NUMBER': Colors.WARNING,   # Números em amarelo
        'ASSIGN': Colors.RED,       # Operadores em vermelho
        'GTE': Colors.RED,
        'LPAREN': Colors.BLUE,     # Parênteses em azul
        'RPAREN': Colors.BLUE,
        'IF': Colors.HEADER,        # Palavras reservadas em rosa
        'PRINT': Colors.HEADER,
    }
    
    # Pega a cor do token (ou cor padrão se não estiver no mapa)
    color = color_map.get(token.type.name, Colors.ENDC)
    # Formata o tipo do token com cor e negrito, alinhado à esquerda (12 caracteres)
    token_type = f"{color}{Colors.BOLD}{token.type.name:<12}{Colors.ENDC}"
    # Formata o lexema (texto do token) com cor amarela
    lexeme = f"{Colors.WARNING}'{token.lexeme}'{Colors.ENDC}"
    # Formata a posição (linha:coluna) com cor ciano
    position = f"{Colors.CYAN}L{token.line:2d}:C{token.column:2d}{Colors.ENDC}"
    
    # Imprime o token formatado: índice, tipo, seta, lexema, posição
    print(f"  {index:2d}. {token_type} → {lexeme:<15} {position}")


# Imprime estatísticas dos tokens encontrados
def print_statistics(tokens):
    # Conta quantos tokens de cada tipo foram encontrados
    token_counts = Counter(token.type for token in tokens)
    
    # Imprime cabeçalho das estatísticas
    print(f"\n{Colors.HEADER}{Colors.BOLD}📊 ESTATÍSTICAS DOS TOKENS{Colors.ENDC}")
    # Imprime linha de separação
    print(f"{Colors.CYAN}{'─' * 50}{Colors.ENDC}")
    
    # Para cada tipo de token, ordenado por quantidade (mais comum primeiro)
    for token_type, count in token_counts.most_common():
        # Calcula a porcentagem deste tipo em relação ao total
        percentage = (count / len(tokens)) * 100
        # Cria uma barra visual (cada 2% = 1 caractere █)
        bar = "█" * int(percentage / 2)
        # Imprime: nome do tipo, quantidade, porcentagem e barra visual
        print(f"  {token_type.name:<12} {count:3d} tokens ({percentage:5.1f}%) {bar}")
    
    # Imprime o total de tokens encontrados
    print(f"\n{Colors.GREEN}{Colors.BOLD}Total: {len(tokens)} tokens encontrados{Colors.ENDC}")


# Imprime resumo do arquivo ou entrada interativa
def print_summary(source_path=None, is_interactive=False):
    # Imprime cabeçalho do resumo
    print(f"\n{Colors.HEADER}{Colors.BOLD}📄 ENTRADA ANALISADA{Colors.ENDC}")
    # Imprime linha de separação
    print(f"{Colors.CYAN}{'─' * 50}{Colors.ENDC}")
    
    # Se é modo interativo
    if is_interactive:
        # Imprime que é entrada interativa
        print(f"  Modo: {Colors.WARNING}Entrada Interativa{Colors.ENDC}")
    else:
        # Se é arquivo, imprime o nome do arquivo
        print(f"  Arquivo: {Colors.WARNING}{source_path}{Colors.ENDC}")
        try:
            # Tenta abrir o arquivo para ler informações
            with open(source_path, 'r', encoding='utf-8') as f:
                # Lê todas as linhas do arquivo
                lines = f.readlines()
            # Imprime o número de linhas
            print(f"  Linhas: {Colors.GREEN}{len(lines)}{Colors.ENDC}")
            # Imprime o tamanho total (soma do tamanho de todas as linhas)
            print(f"  Tamanho: {Colors.GREEN}{sum(len(line) for line in lines)} caracteres{Colors.ENDC}")
        except:
            # Se der erro ao ler o arquivo, ignora (não quebra o programa)
            pass


# Obtém entrada do usuário no modo interativo
def get_user_input():
    # Imprime instruções para o usuário
    print(f"\n{Colors.CYAN}{Colors.BOLD}💬 Digite seu código (ou cole um trecho):{Colors.ENDC}")
    # Imprime dicas de uso
    print(f"{Colors.WARNING}💡 Dicas:{Colors.ENDC}")
    print(f"  • Digite 'SAIR' para encerrar")
    print(f"  • Digite 'AJUDA' para ver exemplos de sintaxe")
    print(f"  • Use Ctrl+C para sair a qualquer momento")
    # Imprime linha de separação
    print(f"{Colors.CYAN}{'─' * 60}{Colors.ENDC}")
    
    # Lista para armazenar as linhas digitadas
    lines = []
    # Imprime prompt (>>>) e não quebra linha (end="")
    print(f"{Colors.GREEN}>>> {Colors.ENDC}", end="", flush=True)
    
    try:
        # Loop infinito para ler linhas
        while True:
            # Lê uma linha do usuário
            line = input()
            # Se digitou 'SAIR' (ignorando maiúsculas/minúsculas e espaços)
            if line.strip().upper() == "SAIR":
                # Se já digitou código, retorna o código digitado
                if lines:
                    # Junta todas as linhas com quebra de linha
                    return "\n".join(lines)
                # Se não digitou nada, retorna None (sai do programa)
                return None
            # Se digitou 'AJUDA'
            elif line.strip().upper() == "AJUDA":
                # Mostra a ajuda com exemplos
                print_help()
                # Imprime o prompt novamente
                print(f"{Colors.GREEN}>>> {Colors.ENDC}", end="", flush=True)
                # Continua o loop (não adiciona 'AJUDA' ao código)
                continue
            # Se digitou linha vazia, termina a entrada
            elif line.strip() == "":
                # Sai do loop
                break
            else:
                # Se digitou código normal, adiciona à lista
                lines.append(line)
                # Imprime o prompt novamente para a próxima linha
                print(f"{Colors.GREEN}>>> {Colors.ENDC}", end="", flush=True)
    except KeyboardInterrupt:
        # Se o usuário pressionou Ctrl+C, sai graciosamente
        print(f"\n{Colors.YELLOW}👋 Saindo...{Colors.ENDC}")
        return None
    
    # Se chegou aqui, junta todas as linhas e retorna (ou None se não digitou nada)
    return "\n".join(lines) if lines else None


# Imprime ajuda com exemplos de sintaxe
def print_help():
    # Imprime cabeçalho da ajuda
    print(f"\n{Colors.HEADER}{Colors.BOLD}📚 EXEMPLOS DE SINTAXE SUPORTADA{Colors.ENDC}")
    # Imprime linha de separação
    print(f"{Colors.CYAN}{'─' * 60}{Colors.ENDC}")
    
    # Lista de exemplos: (descrição, exemplo)
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
    
    # Para cada exemplo na lista
    for desc, example in examples:
        # Se tem descrição, imprime a descrição
        if desc:
            print(f"\n{Colors.WARNING}{desc}{Colors.ENDC}")
        # Imprime o exemplo em verde
        print(f"  {Colors.GREEN}{example}{Colors.ENDC}")


# Analisa o código fonte (análise léxica e sintática)
def analyze_code(source_code, is_interactive=False, show_tokens=True):
    # Se deve mostrar os tokens, imprime cabeçalho
    if show_tokens:
        print(f"\n{Colors.HEADER}{Colors.BOLD}🔤 TOKENS ENCONTRADOS{Colors.ENDC}")
        print(f"{Colors.CYAN}{'─' * 80}{Colors.ENDC}")

    try:
        # Cria um scanner a partir da string de código
        scanner = Scanner.from_string(source_code)
        # Converte o scanner em lista de tokens (lê todos os tokens)
        tokens = list(scanner)
        
        # Se não encontrou nenhum token
        if not tokens:
            # Imprime aviso
            print(f"{Colors.YELLOW}⚠️  Nenhum token encontrado no código fornecido{Colors.ENDC}")
            return
        
        # Se deve mostrar os tokens
        if show_tokens:
            # Para cada token, imprime formatado
            for i, token in enumerate(tokens, 1):
                # i começa em 1 (primeiro token é 1, não 0)
                print_token(token, i)
            # Imprime estatísticas dos tokens
            print_statistics(tokens)
        
        # ====================================================================
        # ANÁLISE SINTÁTICA
        # ====================================================================
        # Imprime cabeçalho da análise sintática
        print(f"\n{Colors.HEADER}{Colors.BOLD}📐 ANÁLISE SINTÁTICA{Colors.ENDC}")
        print(f"{Colors.CYAN}{'─' * 80}{Colors.ENDC}")
        
        # Cria um novo scanner (precisa criar novamente porque o anterior foi consumido)
        scanner = Scanner.from_string(source_code)
        # Cria um parser com o scanner
        parser = Parser(scanner)
        
        try:
            # Executa a análise sintática
            success = parser.parse()
            # Se a análise foi bem-sucedida (sem erros)
            if success:
                # Imprime mensagem de sucesso
                print(f"{Colors.GREEN}{Colors.BOLD}✅ Análise sintática concluída com sucesso!{Colors.ENDC}")
            else:
                # Se houve erros, pega a lista de erros
                errors = parser.get_errors()
                # Se há erros na lista
                if errors:
                    # Imprime cabeçalho de erros
                    print(f"{Colors.RED}{Colors.BOLD}❌ ERROS SINTÁTICOS ENCONTRADOS:{Colors.ENDC}")
                    # Para cada erro, imprime a mensagem
                    for error in errors:
                        print(f"{Colors.RED}  {str(error)}{Colors.ENDC}")
        except SyntaxError as e:
            # Se lançou exceção de erro sintático, imprime o erro
            print(f"{Colors.RED}{Colors.BOLD}❌ ERRO SINTÁTICO:{Colors.ENDC}")
            print(f"{Colors.RED}{str(e)}{Colors.ENDC}")
        
        # Se deve mostrar tokens, imprime mensagem de sucesso da análise léxica
        if show_tokens:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Análise léxica concluída com sucesso!{Colors.ENDC}")
        
    except LexicalError as e:
        # Se lançou exceção de erro léxico, imprime o erro
        print(f"\n{Colors.RED}{Colors.BOLD}❌ ERRO LÉXICO:{Colors.ENDC}")
        print(f"{Colors.RED}{str(e)}{Colors.ENDC}")


# Modo interativo - permite digitar código diretamente no terminal
def interactive_mode():
    # Imprime o cabeçalho do programa
    print_header()
    # Imprime mensagem de modo interativo ativado
    print(f"{Colors.GREEN}{Colors.BOLD}🎯 MODO INTERATIVO ATIVADO{Colors.ENDC}")
    print(f"{Colors.CYAN}Digite seu código diretamente no terminal!{Colors.ENDC}")
    
    # Loop principal do modo interativo
    while True:
        # Obtém o código digitado pelo usuário
        source_code = get_user_input()
        # Se retornou None, o usuário quer sair
        if source_code is None:
            # Sai do loop
            break
            
        # Imprime resumo (modo interativo)
        print_summary(is_interactive=True)
        # Analisa o código digitado
        analyze_code(source_code, is_interactive=True)
        
        # Pergunta se quer analisar outro código
        print(f"\n{Colors.CYAN}Deseja analisar outro código? (s/n): {Colors.ENDC}", end="", flush=True)
        try:
            # Lê a resposta do usuário
            response = input().strip().lower()
            # Se não respondeu 's', 'sim', 'y' ou 'yes', sai
            if response not in ['s', 'sim', 'y', 'yes']:
                # Sai do loop
                break
        except KeyboardInterrupt:
            # Se pressionou Ctrl+C, sai
            break
    
    # Mensagem de despedida
    print(f"\n{Colors.GREEN}{Colors.BOLD}👋 Obrigado por usar o Analisador Léxico!{Colors.ENDC}")


# Função principal do programa
def main() -> None:
    # Verifica se foi passado argumento '-i', '--interactive' ou '--interativo'
    if len(sys.argv) > 1 and sys.argv[1] in ['-i', '--interactive', '--interativo']:
        # Se sim, inicia o modo interativo
        interactive_mode()
        # Retorna (sai da função)
        return
    
    # Se não foi passado nenhum argumento
    if len(sys.argv) < 2:
        # Tenta usar o arquivo padrão 'programa.mc'
        source_path = Path("programa.mc")
        # Se o arquivo não existe
        if not source_path.exists():
            # Imprime erro
            print(f"{Colors.RED}❌ Arquivo programa.mc não encontrado!{Colors.ENDC}")
            # Imprime opções disponíveis
            print(f"{Colors.YELLOW}💡 Opções disponíveis:{Colors.ENDC}")
            print(f"  • {Colors.CYAN}python3 main.py <arquivo.mc>{Colors.ENDC} - Analisar arquivo")
            print(f"  • {Colors.CYAN}python3 main.py -i{Colors.ENDC} - Modo interativo")
            print(f"  • {Colors.CYAN}Coloque um arquivo chamado 'programa.mc' na pasta atual{Colors.ENDC}")
            # Sai do programa com código de erro
            sys.exit(1)
    else:
        # Se foi passado um argumento, usa como nome do arquivo
        source_path = Path(sys.argv[1])
        # Se o arquivo não existe
        if not source_path.exists():
            # Imprime erro
            print(f"{Colors.RED}❌ Arquivo não encontrado: {source_path}{Colors.ENDC}")
            # Sai do programa com código de erro
            sys.exit(1)

    # Imprime o cabeçalho do programa
    print_header()
    # Imprime resumo do arquivo
    print_summary(source_path)
    
    try:
        # Abre o arquivo em modo leitura com codificação UTF-8
        with open(source_path, 'r', encoding='utf-8') as f:
            # Lê todo o conteúdo do arquivo
            source_code = f.read()
        # Analisa o código (análise léxica e sintática)
        analyze_code(source_code)
    except Exception as e:
        # Se der qualquer erro ao ler o arquivo, imprime o erro
        print(f"{Colors.RED}❌ Erro ao ler arquivo: {e}{Colors.ENDC}")
        # Sai do programa com código de erro
        sys.exit(1)


# Se este arquivo foi executado diretamente (não importado)
if __name__ == "__main__":
    # Executa a função principal
    main()
