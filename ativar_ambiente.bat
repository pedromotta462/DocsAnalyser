@echo off
echo Ativando ambiente virtual para DocsAnalyser...
cd /d "c:\Users\Pedro Motta\Documents\Pedro Motta\Projetos\DocsAnalyser"
call .\venv\Scripts\activate.bat
echo.
echo Ambiente virtual ativado! Para testar o script, execute:
echo python docsAnalyser.py
echo.
echo Para desativar o ambiente virtual, digite: deactivate
cmd /k
