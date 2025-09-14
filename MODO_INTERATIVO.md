# 💬 Modo Interativo - Analisador Léxico

## 🎯 Visão Geral

O **Modo Interativo** permite que você teste o analisador léxico diretamente no terminal, digitando ou colando código em tempo real, sem precisar criar arquivos.

## 🚀 Como Usar

### 1. **Iniciar o Modo Interativo**

```bash
# Opção 1: Comando curto
python -m py_lexer.main -i

# Opção 2: Comando longo
python -m py_lexer.main --interativo

# Opção 3: Comando em português
python -m py_lexer.main --interativo
```

### 2. **Interface do Modo Interativo**

```
================================================================================
🔍 ANALISADOR LÉXICO - COMPILADOR PY
================================================================================

🎯 MODO INTERATIVO ATIVADO
Digite seu código diretamente no terminal!

💬 Digite seu código (ou cole um trecho):
💡 Dicas:
  • Digite 'SAIR' para encerrar
  • Digite 'AJUDA' para ver exemplos de sintaxe
  • Use Ctrl+C para sair a qualquer momento
────────────────────────────────────────────────────────────────
>>> 
```

### 3. **Comandos Especiais**

| Comando | Descrição |
|---------|-----------|
| `AJUDA` | Mostra exemplos de sintaxe suportada |
| `SAIR` | Encerra o programa |
| `Ctrl+C` | Sai a qualquer momento |
| **Linha vazia** | Finaliza a entrada e inicia a análise |

## 📝 Exemplos de Uso

### **Exemplo 1: Declaração de Variáveis**
```
>>> int x = 10
>>> float y = 3.14
>>> 
```

### **Exemplo 2: Estruturas Condicionais**
```
>>> if (x > 5)
>>>     print(x)
>>> 
```

### **Exemplo 3: Operações Matemáticas**
```
>>> resultado = x + y * 2
>>> 
```

### **Exemplo 4: Comentários**
```
>>> # Este é um comentário
>>> /* Comentário de bloco */
>>> 
```

## 🎨 Saída Visual

O modo interativo exibe:

- 🎨 **Tokens coloridos** por tipo
- 📍 **Posição exata** (linha:coluna)
- 📊 **Estatísticas detalhadas** com gráficos
- ✅ **Mensagens de sucesso** ou ❌ **erros léxicos**

### **Exemplo de Saída:**
```
🔤 TOKENS ENCONTRADOS
────────────────────────────────────────────────────────────────────────────────
   1. INT          → 'int'           L 1:C 1
   2. IDENTIFIER   → 'x'             L 1:C 5
   3. ASSIGN       → '='             L 1:C 7
   4. NUMBER       → '10'            L 1:C 9

📊 ESTATÍSTICAS DOS TOKENS
──────────────────────────────────────────────────
  IDENTIFIER   1 tokens (25.0%) ████████
  NUMBER       1 tokens (25.0%) ████████
  ASSIGN       1 tokens (25.0%) ████████
  INT          1 tokens (25.0%) ████████

Total: 4 tokens encontrados

✅ Análise léxica concluída com sucesso!
```

## 🔄 Fluxo de Trabalho

1. **Execute** o comando para iniciar o modo interativo
2. **Digite** seu código linha por linha
3. **Pressione Enter** em uma linha vazia para analisar
4. **Veja** os resultados com tokens coloridos e estatísticas
5. **Escolha** se quer analisar outro código ou sair

## 💡 Dicas de Uso

- ✅ **Cole código** diretamente do editor
- ✅ **Teste rapidamente** diferentes sintaxes
- ✅ **Use AJUDA** para ver exemplos válidos
- ✅ **Experimente** com erros para ver mensagens de erro
- ✅ **Teste múltiplos códigos** em sequência

## 🚫 Limitações

- ❌ **Não salva** o código digitado
- ❌ **Não suporta** arquivos muito grandes
- ❌ **Reinicia** o scanner a cada análise

## 🎓 Casos de Uso

- **Aprendizado**: Teste diferentes construções da linguagem
- **Debugging**: Verifique tokens de trechos específicos
- **Demonstração**: Mostre o funcionamento do analisador
- **Desenvolvimento**: Teste rapidamente durante implementação

---

*Desenvolvido com ❤️ para facilitar o aprendizado de compiladores* 🎓
