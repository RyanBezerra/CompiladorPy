#!/bin/bash
# Script para configurar ambiente virtual no Linux/Mac
# Desenvolvido para o projeto Analisador Léxico - CompiladorPy

echo "================================================================"
echo "🔧 CONFIGURANDO AMBIENTE VIRTUAL - ANALISADOR LÉXICO"
echo "================================================================"
echo

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não encontrado! Instale Python 3.7+ primeiro."
    echo "📥 Ubuntu/Debian: sudo apt install python3 python3-pip python3-venv"
    echo "📥 CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "📥 macOS: brew install python3"
    exit 1
fi

echo "✅ Python encontrado!"
python3 --version

echo
echo "🚀 Criando ambiente virtual..."

# Remove ambiente virtual existente se houver
if [ -d "venv" ]; then
    echo "🗑️  Removendo ambiente virtual existente..."
    rm -rf venv
fi

# Cria novo ambiente virtual
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "❌ Erro ao criar ambiente virtual!"
    exit 1
fi

echo "✅ Ambiente virtual criado com sucesso!"

echo
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

echo
echo "📦 Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

echo
echo "🎉 Configuração concluída com sucesso!"
echo
echo "💡 Para usar o ambiente virtual:"
echo "   1. Execute: source venv/bin/activate"
echo "   2. Execute: python -m py_lexer.main -i"
echo "   3. Para sair: deactivate"
echo
