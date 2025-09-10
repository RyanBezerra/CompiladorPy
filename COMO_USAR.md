# 🚀 Como Usar o Analisador Léxico

## ⚡ Formas Mais Fáceis de Executar:

### 🪟 **Windows (Mais Fácil)**
```bash
# Duplo clique no arquivo:
run_lexer.bat

# Ou no terminal:
python -m py_lexer.main
```

### 🐧 **Linux/Mac**
```bash
# Execute o script:
./run_lexer.sh

# Ou no terminal:
python3 -m py_lexer.main
```

## 📝 **Formas Alternativas:**

### 1️⃣ **Automático (Recomendado)**
```bash
python -m py_lexer.main
```
*Automaticamente usa o arquivo `programa.mc`*

### 2️⃣ **Com arquivo específico**
```bash
python -m py_lexer.main meu_arquivo.mc
```

### 3️⃣ **Versão Java (se quiser testar)**
```bash
# Compilar:
cd src
javac -d out util/TokenType.java lexical/Token.java lexical/Scanner.java mini_compiler/Main.java

# Executar:
cd ..
java -cp src/out mini_compiler.Main
```

## 🎯 **O que o programa faz:**
- ✅ Analisa código fonte em arquivos `.mc`
- ✅ Identifica tokens (palavras reservadas, números, operadores, etc.)
- ✅ Mostra posição exata de cada token (linha e coluna)
- ✅ Exibe estatísticas coloridas e organizadas
- ✅ Ignora comentários automaticamente

## 📁 **Arquivos de exemplo:**
- `programa.mc` - Arquivo de exemplo incluído
- Crie seus próprios arquivos `.mc` para testar!

---
*Desenvolvido para a disciplina de Construção de Compiladores I* 🎓

