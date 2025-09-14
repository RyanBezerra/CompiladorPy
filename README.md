# 🔍 Mini Compiler - Analisador Léxico

## 📋 Descrição  
O **mini_compiler** é um projeto acadêmico com implementações em **Java** e **Python** voltado para a disciplina de **Construção de Compiladores I**.  
Este módulo corresponde ao **Checkpoint 01: Analisador Léxico** e tem como objetivo implementar e estender um analisador léxico simples para reconhecer identificadores, números, operadores, palavras reservadas, parênteses e comentários, além de tratar erros léxicos.  

O projeto é parte de um compilador em desenvolvimento incremental e **possui peso 2 na primeira nota da disciplina**.

### ✨ **Novidades da Versão Atualizada:**
- 🎨 **Interface visual colorida** e organizada
- 📊 **Estatísticas detalhadas** dos tokens encontrados
- 🚀 **Execução simplificada** com scripts automáticos
- 🔍 **Detecção automática** do arquivo `programa.mc`
- 📈 **Gráficos de barras** para visualização dos dados
- 💬 **Modo interativo** para digitar código diretamente no terminal
- 🎯 **Teste em tempo real** com entrada do usuário
- 📚 **Sistema de ajuda** com exemplos de sintaxe  

---

## 📁 Estrutura do Projeto  

```
CompiladorPy-main/
│
├── 📄 programa.mc              # Arquivo de exemplo para análise
├── 🚀 run_lexer.bat            # Script para Windows (duplo clique)
├── 🐧 run_lexer.sh             # Script para Linux/Mac
├── 📖 COMO_USAR.md             # Guia de uso simplificado
├── 📋 README.md                # Este arquivo
│
├── 🐍 py_lexer/                # Versão Python (RECOMENDADA)
│   ├── __init__.py
│   ├── main.py                 # Interface visual melhorada
│   ├── scanner.py              # Analisador léxico
│   ├── token.py                # Estrutura de tokens
│   ├── token_type.py           # Tipos de tokens
│   └── errors.py               # Tratamento de erros
│
└── ☕ src/                      # Versão Java
    ├── lexical/
    │   ├── Scanner.java         # Implementação do analisador léxico
    │   └── Token.java           # Estrutura de dados para tokens
    ├── mini_compiler/
    │   └── Main.java            # Classe principal
    ├── util/
    │   └── TokenType.java       # Enumeração dos tipos de tokens
    └── module-info.java
```

---

## ⚙️ Requisitos  

- **Python 3.7+** (para a versão Python - RECOMENDADA)  
- **Java 11+** (para a versão Java - opcional)  
- Terminal ou prompt de comando

---

## 🚀 Execução - Formas Mais Fáceis

### ⚡ **Método 1: Scripts Automáticos (MAIS FÁCIL)**

#### 🪟 **Windows:**
```bash
# Duplo clique no arquivo:
run_lexer.bat

# Ou no terminal:
python -m py_lexer.main
```

#### 🐧 **Linux/Mac:**
```bash
# Execute o script:
./run_lexer.sh

# Ou no terminal:
python3 -m py_lexer.main
```

### 🐍 **Método 2: Python (RECOMENDADO)**

#### **Execução Automática:**
```bash
python -m py_lexer.main
```
*Automaticamente usa o arquivo `programa.mc`*

#### **Com arquivo específico:**
```bash
python -m py_lexer.main meu_arquivo.mc
```

#### **Modo interativo (NOVO!):**
```bash
python -m py_lexer.main -i
# ou
python -m py_lexer.main --interativo
```

### 🎯 **Modo Interativo - Teste em Tempo Real**

O analisador agora suporta **entrada interativa**! Você pode:

- 💬 **Digitar código diretamente** no terminal
- 📋 **Colar trechos de código** para análise
- 🔄 **Testar múltiplos códigos** em sequência
- 📚 **Ver exemplos de sintaxe** com o comando `AJUDA`
- ⚡ **Análise instantânea** sem criar arquivos

#### **Como usar o modo interativo:**

1. **Execute o comando:**
   ```bash
   python -m py_lexer.main -i
   ```

2. **Digite seu código:**
   ```
   >>> int x = 10
   >>> float y = 3.14
   >>> if (x > 5) print(x)
   >>> 
   ```

3. **Veja a análise instantânea** com tokens coloridos e estatísticas

4. **Comandos especiais:**
   - `AJUDA` - Mostra exemplos de sintaxe
   - `SAIR` - Encerra o programa
   - `Ctrl+C` - Sai a qualquer momento

### ☕ **Método 3: Java (Opcional)**

#### **Compilação:**
```bash
cd src
javac -d out util/TokenType.java lexical/Token.java lexical/Scanner.java mini_compiler/Main.java
```

#### **Execução:**
```bash
cd ..
java -cp src/out mini_compiler.Main
```

---

## 🎨 **Saída Visual Melhorada**

A versão Python agora exibe:
- 🎨 **Interface colorida** com códigos de cores por tipo de token
- 📊 **Estatísticas detalhadas** com gráficos de barras
- 📍 **Posição exata** de cada token (linha:coluna)
- 📈 **Contadores** e percentuais de cada tipo de token
- ✅ **Mensagens de sucesso** e tratamento de erros melhorado


## 📝 Exemplos de Uso

### **Entrada de teste (programa.mc):**
```c
int x = 10
float y = 3.14
# comentario de linha ate o fim
if (x >= y)
print(x)
/* comentario
   de bloco */
z1 = .456
z2 = 123.456
z3 = 789
```

### **Saída Visual Melhorada (versão Python):**
```
================================================================================
🔍 ANALISADOR LÉXICO - COMPILADOR PY
================================================================================

📄 ARQUIVO ANALISADO
──────────────────────────────────────────────────
  Arquivo: programa.mc
  Linhas: 10
  Tamanho: 140 caracteres

🔤 TOKENS ENCONTRADOS
────────────────────────────────────────────────────────────────────────────────
   1. INT          → 'int'           L 1:C 1
   2. IDENTIFIER   → 'x'             L 1:C 5
   3. ASSIGN       → '='             L 1:C 7
   4. NUMBER       → '10'            L 1:C 9
   5. FLOAT        → 'float'         L 2:C 1
   ...

📊 ESTATÍSTICAS DOS TOKENS
──────────────────────────────────────────────────
  IDENTIFIER   8 tokens (30.8%) ████████████
  NUMBER       5 tokens (19.2%) ████████
  ASSIGN       4 tokens (15.4%) ██████
  LPAREN       3 tokens (11.5%) ████
  RPAREN       3 tokens (11.5%) ████
  INT          1 tokens ( 3.8%) █
  FLOAT        1 tokens ( 3.8%) █
  IF           1 tokens ( 3.8%) █

Total: 26 tokens encontrados

✅ Análise léxica concluída com sucesso!
```
## 🎯 **Tipos de Tokens Reconhecidos**

| Tipo | Descrição | Exemplos |
|------|-----------|----------|
| `INT` | Palavra reservada | `int` |
| `FLOAT` | Palavra reservada | `float` |
| `IF` | Palavra reservada | `if` |
| `PRINT` | Palavra reservada | `print` |
| `IDENTIFIER` | Identificadores | `x`, `y`, `z1`, `variavel` |
| `NUMBER` | Números | `10`, `3.14`, `.456`, `123.456` |
| `ASSIGN` | Operador de atribuição | `=` |
| `GTE` | Operador de comparação | `>=` |
| `LPAREN` | Parêntese esquerdo | `(` |
| `RPAREN` | Parêntese direito | `)` |

## 🔧 **Recursos Implementados**

- ✅ **Análise léxica completa** com reconhecimento de todos os tipos de tokens
- ✅ **Tratamento de comentários** (linha única `#` e bloco `/* */`)
- ✅ **Detecção de erros léxicos** com mensagens informativas
- ✅ **Interface visual colorida** e organizada
- ✅ **Estatísticas detalhadas** com gráficos
- ✅ **Scripts de execução automática** para Windows e Linux/Mac
- ✅ **Detecção automática** do arquivo de entrada
- ✅ **Modo interativo** para entrada de código em tempo real
- ✅ **Sistema de ajuda** com exemplos de sintaxe
- ✅ **Teste múltiplo** de códigos em sequência

## 📚 **Contribuição**

Este projeto é desenvolvido no contexto da disciplina. Sugestões e melhorias podem ser feitas via Merge Requests ou discutidas em sala de aula.

## 📄 **Licença**

Uso acadêmico restrito à disciplina de Construção de Compiladores I.

## 🚀 **Status**

- ✅ **Analisador Léxico**: Completo e funcional
- 🔄 **Analisador Sintático**: Em desenvolvimento
- ⏳ **Analisador Semântico**: Planejado

---

*Desenvolvido com ❤️ para a disciplina de Construção de Compiladores I* 🎓
