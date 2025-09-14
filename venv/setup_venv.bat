@echo off
REM Script para configurar ambiente virtual no Windows
REM Desenvolvido para o projeto Analisador Léxico - CompiladorPy

echo ================================================================
echo 🔧 CONFIGURANDO AMBIENTE VIRTUAL - ANALISADOR LÉXICO
echo ================================================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado! Instale Python 3.7+ primeiro.
    echo 📥 Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python encontrado!
python --version

echo.
echo 🚀 Criando ambiente virtual...

REM Remove ambiente virtual existente se houver
if exist "venv" (
    echo 🗑️  Removendo ambiente virtual existente...
    rmdir /s /q venv
)

REM Cria novo ambiente virtual
python -m venv venv
if errorlevel 1 (
    echo ❌ Erro ao criar ambiente virtual!
    pause
    exit /b 1
)

echo ✅ Ambiente virtual criado com sucesso!

echo.
echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo 📦 Instalando dependências...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo 🎉 Configuração concluída com sucesso!
echo.
echo 💡 Para usar o ambiente virtual:
echo    1. Execute: venv\Scripts\activate.bat
echo    2. Execute: python -m py_lexer.main -i
echo    3. Para sair: deactivate
echo.

pause
