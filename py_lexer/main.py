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


def print_summary(source_path):
    """Imprime resumo do arquivo analisado"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}📄 ARQUIVO ANALISADO{Colors.ENDC}")
    print(f"{Colors.CYAN}{'─' * 50}{Colors.ENDC}")
    print(f"  Arquivo: {Colors.WARNING}{source_path}{Colors.ENDC}")
    
    # Lê o arquivo para mostrar algumas linhas
    try:
        with open(source_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        print(f"  Linhas: {Colors.GREEN}{len(lines)}{Colors.ENDC}")
        print(f"  Tamanho: {Colors.GREEN}{sum(len(line) for line in lines)} caracteres{Colors.ENDC}")
    except:
        pass


def main() -> None:
    # Se não foi fornecido arquivo, tenta usar programa.mc automaticamente
    if len(sys.argv) < 2:
        source_path = Path("programa.mc")
        if not source_path.exists():
            print(f"{Colors.RED}❌ Arquivo programa.mc não encontrado!{Colors.ENDC}")
            print(f"{Colors.YELLOW}💡 Uso: python -m py_lexer.main <arquivo.mc>{Colors.ENDC}")
            print(f"{Colors.CYAN}📁 Ou coloque um arquivo chamado 'programa.mc' na pasta atual{Colors.ENDC}")
            sys.exit(1)
    else:
        source_path = Path(sys.argv[1])
        if not source_path.exists():
            print(f"{Colors.RED}❌ Arquivo não encontrado: {source_path}{Colors.ENDC}")
            sys.exit(1)

    print_header()
    print_summary(source_path)
    
    print(f"\n{Colors.HEADER}{Colors.BOLD}🔤 TOKENS ENCONTRADOS{Colors.ENDC}")
    print(f"{Colors.CYAN}{'─' * 80}{Colors.ENDC}")

    try:
        scanner = Scanner(str(source_path))
        tokens = list(scanner)  # Coleta todos os tokens
        
        for i, token in enumerate(tokens, 1):
            print_token(token, i)
            
        print_statistics(tokens)
        
        print(f"\n{Colors.GREEN}{Colors.BOLD}✅ Análise léxica concluída com sucesso!{Colors.ENDC}")
        
    except LexicalError as e:
        print(f"\n{Colors.RED}{Colors.BOLD}❌ ERRO LÉXICO:{Colors.ENDC}")
        print(f"{Colors.RED}{str(e)}{Colors.ENDC}")
        sys.exit(2)


if __name__ == "__main__":
    main()


