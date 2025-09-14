#!/usr/bin/env python3
"""
Script de demonstração do Analisador Léxico Interativo
"""

import sys
from pathlib import Path

# Adiciona o diretório atual ao path para importar o módulo
sys.path.insert(0, str(Path(__file__).parent))

from py_lexer.main import interactive_mode, analyze_code, print_header, Colors

def demo_examples():
    """Demonstra o analisador com exemplos pré-definidos"""
    print_header()
    print(f"{Colors.GREEN}{Colors.BOLD}🎯 DEMONSTRAÇÃO COM EXEMPLOS PRÉ-DEFINIDOS{Colors.ENDC}")
    print("=" * 80)
    
    examples = [
        ("Declaração de variáveis:", "int x = 10\nfloat y = 3.14"),
        ("Estrutura condicional:", "if (x > 5)\n    print(x)"),
        ("Operações matemáticas:", "resultado = x + y * 2"),
        ("Comentários:", "# Este é um comentário\n/* Comentário de bloco */"),
        ("Comparações:", "x >= 5 && y != 0"),
        ("Código complexo:", "int idade = 25\nif (idade >= 18)\n    print(\"Maior de idade\")\nelse\n    print(\"Menor de idade\")")
    ]
    
    for i, (desc, code) in enumerate(examples, 1):
        print(f"\n{Colors.CYAN}{'='*20} EXEMPLO {i} {'='*20}{Colors.ENDC}")
        print(f"{Colors.WARNING}{desc}{Colors.ENDC}")
        print(f"{Colors.GREEN}Código:{Colors.ENDC}")
        for line in code.split('\n'):
            print(f"  {line}")
        print(f"{Colors.CYAN}{'-' * 50}{Colors.ENDC}")
        
        try:
            analyze_code(code)
        except Exception as e:
            print(f"{Colors.RED}Erro: {e}{Colors.ENDC}")
        
        if i < len(examples):
            input(f"\n{Colors.YELLOW}Pressione Enter para continuar...{Colors.ENDC}")

def show_menu():
    """Mostra o menu de opções"""
    print(f"{Colors.HEADER}{Colors.BOLD}🔍 ANALISADOR LÉXICO - COMPILADOR PY{Colors.ENDC}")
    print("=" * 60)
    print(f"{Colors.CYAN}Opções disponíveis:{Colors.ENDC}")
    print(f"  {Colors.GREEN}1.{Colors.ENDC} python test_lexer.py --demo    - Demonstração com exemplos")
    print(f"  {Colors.GREEN}2.{Colors.ENDC} python -m py_lexer.main -i     - Modo interativo")
    print(f"  {Colors.GREEN}3.{Colors.ENDC} python -m py_lexer.main arquivo.mc - Analisar arquivo")
    print(f"  {Colors.GREEN}4.{Colors.ENDC} python test_lexer.py --help   - Mostrar esta ajuda")
    print()

def main():
    """Função principal"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--demo":
            demo_examples()
        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            show_menu()
        else:
            print(f"{Colors.RED}Opção inválida: {sys.argv[1]}{Colors.ENDC}")
            show_menu()
    else:
        show_menu()
        print(f"{Colors.YELLOW}Iniciando modo interativo...{Colors.ENDC}")
        interactive_mode()

if __name__ == "__main__":
    main()
