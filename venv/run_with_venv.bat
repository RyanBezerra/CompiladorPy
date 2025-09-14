@echo off
REM Script para executar o analisador léxico com ambiente virtual
REM Desenvolvido para o projeto Analisador Léxico - CompiladorPy

echo ================================================================
echo 🔍 ANALISADOR LÉXICO - COMPILADOR PY
echo ================================================================
echo.

REM Verifica se o ambiente virtual existe
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Ambiente virtual não encontrado!
    echo 💡 Execute primeiro: setup_venv.bat
    pause
    exit /b 1
)

echo 🚀 Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo 🎯 Iniciando analisador léxico...
echo.

REM Executa o analisador
python -m py_lexer.main %*

echo.
echo 🔧 Desativando ambiente virtual...
call venv\Scripts\deactivate.bat

echo.
echo 👋 Obrigado por usar o Analisador Léxico!
pause
