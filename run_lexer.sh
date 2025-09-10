#!/bin/bash

echo "================================================================================"
echo "🔍 ANALISADOR LÉXICO - COMPILADOR PY"
echo "================================================================================"
echo

# Verifica se o arquivo programa.mc existe
if [ -f "programa.mc" ]; then
    echo "✅ Arquivo programa.mc encontrado!"
    echo "🚀 Executando analisador léxico..."
    echo
    python3 -m py_lexer.main programa.mc
else
    echo "❌ Arquivo programa.mc não encontrado!"
    echo
    echo "📁 Arquivos .mc disponíveis:"
    ls *.mc 2>/dev/null || echo "   Nenhum arquivo .mc encontrado"
    echo
    echo "💡 Para usar outro arquivo, execute:"
    echo "   python3 -m py_lexer.main nome_do_arquivo.mc"
fi

echo
echo "⏸️  Pressione Enter para sair..."
read

