import sys
from pathlib import Path

from .scanner import Scanner
from .errors import LexicalError


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: python -m py_lexer.main <arquivo.mc>")
        sys.exit(1)

    source_path = Path(sys.argv[1])
    if not source_path.exists():
        print(f"Arquivo não encontrado: {source_path}")
        sys.exit(1)

    try:
        scanner = Scanner(str(source_path))
        for tk in scanner:
            print(tk)
    except LexicalError as e:
        print(str(e))
        sys.exit(2)


if __name__ == "__main__":
    main()


