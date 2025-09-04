# mini_compiler  

## Descrição  
O **mini_compiler** é um projeto acadêmico em **Java** voltado para a disciplina de **Construção de Compiladores I**.  
Este módulo corresponde ao **Checkpoint 01: Analisador Léxico** e tem como objetivo implementar e estender um analisador léxico simples para reconhecer identificadores, números, operadores, palavras reservadas, parênteses e comentários, além de tratar erros léxicos.  

O projeto é parte de um compilador em desenvolvimento incremental e **possui peso 2 na primeira nota da disciplina**.  

---

## Estrutura do Projeto  

```mini_compiler/
│
├── src/
│ ├── lexical/
│ │ ├── Scanner.java # Implementação do analisador léxico
│ │ └── Token.java # Estrutura de dados para representar tokens
│ │
│ ├── mini_compiler/
│ │ └── Main.java # Classe principal para execução do compilador
│ │
│ └── util/
│ └── TokenType.java # Enumeração com os tipos de tokens reconhecidos
│
└── README.md # Documentação do projeto
```

---

## Requisitos  

- **Java 11+** (para a versão Java)  
- **Python 3.10+** (para a versão Python do analisador léxico)  
- IDE ou editor de texto de sua preferência (IntelliJ, VS Code, Eclipse, etc.)  

---

## Execução  

### Java  
Dentro da pasta `src`, compile os arquivos:  

```
javac -d out --module-path out $(find src -name "*.java")
```

E execute o programa:

```
java -cp out mini_compiler.Main
```

O arquivo de entrada pode ser configurado dentro da classe `Main.java`.

### Python  
Executar o analisador léxico em Python com o arquivo de entrada (`programa.mc`):

```
python -m py_lexer.main programa.mc
```

Saída: uma linha por token contendo tipo, lexema, linha e coluna de início.


## Exemplos de Uso

Entrada de teste (programa.mc):

```c
int x = 10;
float y = 3.14;
/* comentário de múltiplas linhas */
if (x >= y) {
    print(x);
}
```

## Saída esperada (tokens):

Para a versão Python, exemplos de tokens impressos:

```
Token(type=INT, lexeme='int', line=1, column=1)
Token(type=IDENTIFIER, lexeme='x', line=1, column=5)
Token(type=ASSIGN, lexeme='=', line=1, column=7)
Token(type=NUMBER, lexeme='10', line=1, column=9)
```
## Contribuição

Este projeto é desenvolvido no contexto da disciplina. Sugestões e melhorias podem ser feitas via Merge Requests ou discutidas em sala de aula.

## Licença

Uso acadêmico restrito à disciplina de Construção de Compiladores I.

## Status

Atualmente em desenvolvimento no módulo de Analisador Léxico. Próximos módulos incluirão Analisador Sintático e Analisador Semântico.
