import sys
from pathlib import Path
from collections import Counter

from .scanner import Scanner
from .errors import LexicalError


class Colors:
    """Códigos de cores ANSI para terminal"""
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
    """Imprime o cabeçalho bonito"""
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("=" * 80)
    print("🔍 ANALISADOR LÉXICO - COMPILADOR PY")
    print("=" * 80)
    print(f"{Colors.ENDC}")


def print_token(token, index):
    """Imprime um token com formatação colorida"""
    # Cores baseadas no tipo do token
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
    
    color = color_map.get(token.type, Colors.ENDC)
    token_type = f"{color}{Colors.BOLD}{token.type:<12}{Colors.ENDC}"
    lexeme = f"{Colors.WARNING}'{token.lexeme}'{Colors.ENDC}"
    position = f"{Colors.CYAN}L{token.line:2d}:C{token.column:2d}{Colors.ENDC}"
    
    print(f"  {index:2d}. {token_type} → {lexeme:<15} {position}")


def print_statistics(tokens):
    """Imprime estatísticas dos tokens"""
    token_counts = Counter(token.type for token in tokens)
    
    print(f"\n{Colors.HEADER}{Colors.BOLD}📊 ESTATÍSTICAS DOS TOKENS{Colors.ENDC}")
    print(f"{Colors.CYAN}{'─' * 50}{Colors.ENDC}")
    
    for token_type, count in token_counts.most_common():
        percentage = (count / len(tokens)) * 100
        bar = "█" * int(percentage / 2)
        print(f"  {token_type:<12} {count:3d} tokens ({percentage:5.1f}%) {bar}")
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}Total: {len(tokens)} tokens encontrados{Colors.ENDC}")


def print_summary(source_path=None, is_interactive=False):
    """Imprime resumo do arquivo analisado ou entrada interativa"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}📄 ENTRADA ANALISADA{Colors.ENDC}")
    print(f"{Colors.CYAN}{'─' * 50}{Colors.ENDC}")
    
    if is_interactive:
        print(f"  Modo: {Colors.WARNING}Entrada Interativa{Colors.ENDC}")
    else:
        print(f"  Arquivo: {Colors.WARNING}{source_path}{Colors.ENDC}")
        
        # Lê o arquivo para mostrar algumas linhas
        try:
            with open(source_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            print(f"  Linhas: {Colors.GREEN}{len(lines)}{Colors.ENDC}")
            print(f"  Tamanho: {Colors.GREEN}{sum(len(line) for line in lines)} caracteres{Colors.ENDC}")
        except:
            pass


def get_user_input():
    """Obtém entrada do usuário de forma interativa"""
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
                # Se há código digitado, analisa antes de sair
                if lines:
                    return "\n".join(lines)
                return None
            elif line.strip().upper() == "AJUDA":
                print_help()
                print(f"{Colors.GREEN}>>> {Colors.ENDC}", end="", flush=True)
                continue
            elif line.strip() == "":
                # Linha vazia indica fim da entrada
                break
            else:
                lines.append(line)
                print(f"{Colors.GREEN}>>> {Colors.ENDC}", end="", flush=True)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}👋 Saindo...{Colors.ENDC}")
        return None
    
    return "\n".join(lines) if lines else None


def print_help():
    """Imprime ajuda com exemplos de sintaxe"""
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


def analyze_code(source_code, is_interactive=False):
    """Analisa o código fornecido e exibe os tokens"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}🔤 TOKENS ENCONTRADOS{Colors.ENDC}")
    print(f"{Colors.CYAN}{'─' * 80}{Colors.ENDC}")

    try:
        # Cria um scanner temporário com o código fornecido
        scanner = Scanner.from_string(source_code)
        tokens = list(scanner)  # Coleta todos os tokens
        
        if not tokens:
            print(f"{Colors.YELLOW}⚠️  Nenhum token encontrado no código fornecido{Colors.ENDC}")
            return
        
        for i, token in enumerate(tokens, 1):
            print_token(token, i)
            
        print_statistics(tokens)
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Análise léxica concluída com sucesso!{Colors.ENDC}")
        
    except LexicalError as e:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ ERRO LÉXICO:{Colors.ENDC}")
        print(f"{Colors.RED}{str(e)}{Colors.ENDC}")


def interactive_mode():
    """Modo interativo para entrada de código"""
    print_header()
    print(f"{Colors.GREEN}{Colors.BOLD}🎯 MODO INTERATIVO ATIVADO{Colors.ENDC}")
    print(f"{Colors.CYAN}Digite seu código diretamente no terminal!{Colors.ENDC}")
    
    while True:
        source_code = get_user_input()
        if source_code is None:
            break
            
        print_summary(is_interactive=True)
        analyze_code(source_code, is_interactive=True)
        
        # Pergunta se quer continuar
        print(f"\n{Colors.CYAN}Deseja analisar outro código? (s/n): {Colors.ENDC}", end="", flush=True)
        try:
            response = input().strip().lower()
            if response not in ['s', 'sim', 'y', 'yes']:
                break
        except KeyboardInterrupt:
            break
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}👋 Obrigado por usar o Analisador Léxico!{Colors.ENDC}")


def main() -> None:
    # Verifica se foi solicitado modo interativo
    if len(sys.argv) > 1 and sys.argv[1] in ['-i', '--interactive', '--interativo']:
        interactive_mode()
        return
    
    # Se não foi fornecido arquivo, tenta usar programa.mc automaticamente
    if len(sys.argv) < 2:
        source_path = Path("programa.mc")
        if not source_path.exists():
            print(f"{Colors.RED}❌ Arquivo programa.mc não encontrado!{Colors.ENDC}")
            print(f"{Colors.YELLOW}💡 Opções disponíveis:{Colors.ENDC}")
            print(f"  • {Colors.CYAN}python -m py_lexer.main <arquivo.mc>{Colors.ENDC} - Analisar arquivo")
            print(f"  • {Colors.CYAN}python -m py_lexer.main -i{Colors.ENDC} - Modo interativo")
            print(f"  • {Colors.CYAN}python -m py_lexer.main --interativo{Colors.ENDC} - Modo interativo")
            print(f"  • {Colors.CYAN}Coloque um arquivo chamado 'programa.mc' na pasta atual{Colors.ENDC}")
            sys.exit(1)
    else:
        source_path = Path(sys.argv[1])
        if not source_path.exists():
            print(f"{Colors.RED}❌ Arquivo não encontrado: {source_path}{Colors.ENDC}")
            sys.exit(1)

    print_header()
    print_summary(source_path)
    
    # Lê o arquivo e analisa
    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        analyze_code(source_code)
    except Exception as e:
        print(f"{Colors.RED}❌ Erro ao ler arquivo: {e}{Colors.ENDC}")
        sys.exit(1)


if __name__ == "__main__":
    main()


