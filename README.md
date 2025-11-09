# Compilador - Analisador Léxico e Sintático

Compilador simples em Python para análise léxica e sintática de código.

## 📋 Requisitos

- **Python 3.7 ou superior**

### Verificação do Python

Para verificar se o Python está instalado, abra o terminal e digite:

```bash
python3 --version
```

Se aparecer algo como `Python 3.7.x` ou superior, está pronto!

### Instalação do Python (se necessário)

- **Linux (Ubuntu/Debian)**: `sudo apt install python3`
- **Windows**: Baixe em https://www.python.org/downloads/
- **macOS**: `brew install python3` ou baixe em https://www.python.org/downloads/

## 📦 Dependências

**Nenhuma dependência externa é necessária!**

O projeto usa apenas bibliotecas padrão do Python:
- `sys` - Sistema
- `pathlib` - Caminhos de arquivos
- `dataclasses` - Estruturas de dados
- `enum` - Enumerações
- `typing` - Tipos
- `collections` - Coleções

Todas essas bibliotecas já vêm instaladas com o Python.

## 🚀 Instruções de Execução

### 1. Abrir o terminal

- **Linux/Mac**: Abra o Terminal
- **Windows**: Abra o Prompt de Comando ou PowerShell

### 2. Navegar até a pasta do projeto

```bash
cd caminho/para/CompiladorPy
```

### 3. Executar o compilador

#### Opção A: Analisar arquivo padrão (programa.mc)

```bash
python3 main.py
```

#### Opção B: Analisar arquivo específico

```bash
python3 main.py programa_ckp2_quarta.mc
```

#### Opção C: Modo interativo

```bash
python3 main.py -i
```

## 📁 Arquivos do Projeto

- `main.py` - Código completo do compilador
- `programa.mc` - Exemplo básico de código
- `programa_ckp2_quarta.mc` - Exemplo mais completo (Checkpoint 2)

## 📝 O que o compilador faz?

1. **Análise Léxica**: Identifica palavras, números, operadores, etc.
2. **Análise Sintática**: Verifica se o código está escrito corretamente

## ✅ O que o código pode ter?

- **Palavras reservadas**: `int`, `float`, `print`, `if`, `else`
- **Variáveis**: letras e números (ex: `x`, `variavel123`)
- **Números**: `10`, `3.14`, `.456`
- **Operadores**: `+`, `-`, `*`, `/`, `=`, `>`, `>=`, `<`, `<=`, `==`, `!=`
- **Parênteses**: `(`, `)`
- **Comentários**: `# comentário` ou `/* comentário */`

## 📖 Exemplo de Código

Crie um arquivo `.mc` com:
```
int x = 10
float y = 3.14
print(x)
if (x > 5)
    print(y)
```

Depois execute:
```bash
python3 main.py seu_arquivo.mc
```

## ❓ Problemas Comuns

### Erro: "python3: comando não encontrado"

**Solução**: Use `python` em vez de `python3`:
```bash
python main.py
```

### Erro: "Arquivo não encontrado"

**Solução**: Verifique se o arquivo está na mesma pasta do `main.py`

### Erro: "Permission denied"

**Solução Linux/Mac**: Dê permissão de execução:
```bash
chmod +x main.py
```

## 🧪 Teste Rápido

Para testar se está tudo funcionando:

```bash
python3 main.py programa.mc
```

Se aparecer "✅ Análise sintática concluída com sucesso!", está tudo certo!

## 📚 Entendendo o Código

O arquivo `main.py` está organizado assim:

1. **TokenType** - Define os tipos de tokens (palavras, números, etc.)
2. **Scanner** - Lê o código e identifica os tokens
3. **Parser** - Verifica se o código está correto
4. **main()** - Função principal que executa tudo

Cada parte tem comentários explicando o que faz.
