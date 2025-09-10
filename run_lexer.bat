@echo off
echo ================================================================================
echo 🔍 ANALISADOR LÉXICO - COMPILADOR PY
echo ================================================================================
echo.

REM Verifica se o arquivo programa.mc existe
if exist "programa.mc" (
    echo ✅ Arquivo programa.mc encontrado!
    echo 🚀 Executando analisador léxico...
    echo.
    python -m py_lexer.main programa.mc
) else (
    echo ❌ Arquivo programa.mc não encontrado!
    echo.
    echo 📁 Arquivos .mc disponíveis:
    dir *.mc 2>nul
    echo.
    echo 💡 Para usar outro arquivo, execute:
    echo    python -m py_lexer.main nome_do_arquivo.mc
)

echo.
echo ⏸️  Pressione qualquer tecla para sair...
pause >nul

