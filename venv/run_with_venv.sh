#!/bin/bash
# Script para executar o analisador léxico com ambiente virtual
# Desenvolvido para o projeto Analisador Léxico - CompiladorPy

echo "================================================================"
echo "🔍 ANALISADOR LÉXICO - COMPILADOR PY"
echo "================================================================"
echo

# Verifica se o ambiente virtual existe
if [ ! -f "venv/bin/activate" ]; then
    echo "❌ Ambiente virtual não encontrado!"
    echo "💡 Execute primeiro: ./setup_venv.sh"
    exit 1
fi

echo "🚀 Ativando ambiente virtual..."
source venv/bin/activate

echo
echo "🎯 Iniciando analisador léxico..."
echo

# Executa o analisador
python -m py_lexer.main "$@"

echo
echo "🔧 Desativando ambiente virtual..."
deactivate

echo
echo "👋 Obrigado por usar o Analisador Léxico!"
