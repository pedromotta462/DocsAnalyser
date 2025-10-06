# Script para ativar ambiente virtual DocsAnalyser
Write-Host "Ativando ambiente virtual para DocsAnalyser..." -ForegroundColor Green

# Navegar para o diretório do projeto
Set-Location "c:\Users\Pedro Motta\Documents\Pedro Motta\Projetos\DocsAnalyser"

# Ativar ambiente virtual
& .\venv\Scripts\Activate.ps1

Write-Host ""
Write-Host "Ambiente virtual ativado!" -ForegroundColor Green
Write-Host "Para testar o script, execute:" -ForegroundColor Yellow
Write-Host "py docsAnalyser.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para desativar o ambiente virtual, digite: deactivate" -ForegroundColor Yellow
