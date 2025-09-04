from dataclasses import dataclass
from .token_type import TokenType


@dataclass
class Token:
    type: TokenType
    lexeme: str
    line: int
    column: int

    def __str__(self) -> str:
        return f"Token(type={self.type.name}, lexeme='{self.lexeme}', line={self.line}, column={self.column})"


