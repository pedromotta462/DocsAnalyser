# DocsAnalyser - Analisador e Renomeador de Documentos

Este script Python analisa e renomeia automaticamente documentos PDF, DOC e DOCX baseado no conteúdo do arquivo.

## 🚀 Como usar o ambiente virtual

### Opção 1: Script PowerShell (Recomendado)
```powershell
.\ativar_ambiente.ps1
```

### Opção 2: Script Batch
```cmd
.\ativar_ambiente.bat
```

### Opção 3: Manual
```powershell
# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# Executar o script
py docsAnalyser.py

# Desativar ambiente virtual (quando terminar)
deactivate
```

## 📦 Dependências Instaladas

- **PyPDF2**: Leitura de arquivos PDF
- **pdfplumber**: Extração avançada de texto de PDFs
- **python-docx**: Leitura de arquivos DOCX
- **python-docx2txt**: Leitura de arquivos DOC (formato antigo)

## 🔧 Funcionalidades

1. **Processar diretório inteiro**: Analisa todos os PDFs e DOCs em uma pasta
2. **Processar arquivo específico**: Analisa um único arquivo
3. **Adicionar regras personalizadas**: Cria novas regras de renomeação
4. **Visualizar regras**: Mostra todas as regras configuradas

## 📝 Tipos de documento detectados

- **Identidade (RG)**: Detecta carteiras de identidade
- **CPF**: Detecta documentos de CPF
- **Comprovante de residência**: Detecta contas e faturas
- **Contratos**: Detecta contratos e termos

## 🎯 Exemplo de uso

1. Execute o script: `py docsAnalyser.py`
2. Escolha a opção "1" para processar um diretório
3. Digite o caminho da pasta com seus documentos
4. O script irá renomear automaticamente os arquivos baseado no conteúdo

## ⚠️ Importante

- Faça backup dos seus documentos antes de usar o script
- O script renomeia os arquivos permanentemente
- Certifique-se de que tem permissão de escrita na pasta dos documentos
