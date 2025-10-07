# 📦 Como Gerar o Executável do DocsAnalyser

> 🏠 **[← Voltar para o README principal](../README.md)** | 📚 **[Ver Índice Completo](INDICE.md)**

## ✅ Pré-requisitos

1. **Python 3.12+** instalado
2. **Ambiente virtual** ativado
3. **Todas as dependências** instaladas

## 🚀 Passo a Passo

### 1. Ativar Ambiente Virtual

```powershell
cd "c:\Users\Pedro Motta\Documents\Pedro Motta\Projetos\DocsAnalyser"
.\venv\Scripts\Activate.ps1
```

### 2. Instalar PyInstaller (se ainda não tiver)

```powershell
pip install pyinstaller
```

### 3. Executar Script de Build

```powershell
python build_exe.py
```

O script irá:
- ✅ Verificar se PyInstaller está instalado
- ✅ Criar ícone padrão (se não existir)
- ✅ Preparar ambiente de build
- ✅ Executar PyInstaller com todos os parâmetros corretos
- ✅ Gerar executável em `dist/DocsAnalyser.exe`

### 4. Testar o Executável

```powershell
.\dist\DocsAnalyser.exe
```

## 📋 Opções Avançadas

### Build Manual (sem script)

Se preferir fazer build manual:

```powershell
pyinstaller --name DocsAnalyser `
  --onefile `
  --windowed `
  --icon assets/icon.ico `
  --add-data "config;config" `
  --add-data "renaming_rules.json;." `
  --add-data ".env;." `
  --hidden-import google.generativeai `
  --hidden-import PIL `
  --hidden-import pdfplumber `
  --hidden-import PyPDF2 `
  --hidden-import docx `
  --hidden-import docx2txt `
  --noconfirm `
  app.py
```

### Parâmetros Explicados

| Parâmetro | Descrição |
|-----------|-----------|
| `--name` | Nome do executável |
| `--onefile` | Gera um único arquivo .exe |
| `--windowed` | Remove janela de console (apenas GUI) |
| `--icon` | Define ícone do executável |
| `--add-data` | Inclui arquivos adicionais |
| `--hidden-import` | Força inclusão de módulos |
| `--noconfirm` | Sobrescreve builds anteriores |

## 🎨 Personalizar Ícone

### Criar Ícone Personalizado

1. Crie uma imagem PNG 256x256
2. Converta para ICO usando: https://convertio.co/png-ico/
3. Salve como `assets/icon.ico`
4. Execute o build novamente

### Ícone Padrão

O script `build_exe.py` cria automaticamente um ícone básico azul com "D" se não existir.

## 📦 O Que Será Incluído no .exe

### Arquivos Empacotados

- ✅ Todo código Python (`src/`)
- ✅ Configurações (`config/settings.json`)
- ✅ Regras de renomeação (`renaming_rules.json`)
- ✅ Variáveis de ambiente (`.env`) - se existir
- ✅ Todas as bibliotecas Python necessárias

### Arquivos NÃO Incluídos

- ❌ Ambiente virtual (`venv/`)
- ❌ Cache Python (`__pycache__/`)
- ❌ Arquivos de teste
- ❌ Arquivos de build anteriores

## 🔍 Verificar Build

### Tamanho Esperado

O executável terá aproximadamente **50-70 MB** devido às bibliotecas incluídas:
- PyPDF2, pdfplumber
- python-docx, docx2txt
- Google Gemini AI
- Pillow, PyMuPDF
- Tkinter

### Testar Funcionalidades

Após gerar o .exe, teste:

1. ✅ Interface abre corretamente
2. ✅ Seleção de diretório funciona
3. ✅ Processamento de PDF funciona
4. ✅ Processamento de DOCX funciona
5. ✅ Gemini AI funciona (se configurado)
6. ✅ Log exibe mensagens corretamente

## 🐛 Solução de Problemas

### Erro: "Failed to execute script"

**Causa:** Módulo Python não encontrado

**Solução:** Adicione ao `--hidden-import`:
```powershell
--hidden-import nome_do_modulo
```

### Erro: "Cannot find data file"

**Causa:** Arquivo não incluído no build

**Solução:** Adicione ao `--add-data`:
```powershell
--add-data "arquivo;destino"
```

### Executável muito grande

**Causa:** Muitas bibliotecas incluídas

**Soluções:**
- Use `--exclude-module` para remover módulos desnecessários
- Considere usar `--onedir` ao invés de `--onefile` (mais rápido)

### Antivírus bloqueia o .exe

**Causa:** Executáveis do PyInstaller às vezes são detectados como suspeitos

**Soluções:**
- Adicione exceção no antivírus
- Assine digitalmente o executável
- Use `--runtime-tmpdir` para mudar local temporário

## 📤 Distribuir o Executável

### O Que Enviar ao Cliente

**Opção 1: Apenas o .exe** (Recomendado)
```
DocsAnalyser.exe  (auto-contido)
```

**Opção 2: Pacote Completo**
```
📦 DocsAnalyser_v2.0/
├── DocsAnalyser.exe
├── GUIA_RAPIDO.pdf  (instruções para o usuário)
├── .env.exemplo     (se usar Gemini AI)
└── README.txt       (informações básicas)
```

### Instruções para o Cliente

Crie um `README.txt` simples:

```
==================================
   DOCSANALYSER v2.0
   Analisador de Documentos
==================================

COMO USAR:

1. Execute DocsAnalyser.exe
2. Selecione a pasta com seus documentos
3. Clique em "Processar Documentos"
4. Aguarde a conclusão

IMPORTANTE:
- Faça backup dos documentos antes
- Feche todos os arquivos PDF/Word
- O programa renomeia permanentemente

SUPORTE:
GitHub: github.com/pedromotta462/DocsAnalyser
Email: seu_email@exemplo.com
```

## 🔄 Atualizar o Executável

Quando fizer mudanças no código:

1. Atualize o código fonte
2. Teste localmente (`python app.py`)
3. Limpe builds anteriores:
   ```powershell
   Remove-Item build -Recurse -Force
   Remove-Item dist -Recurse -Force
   Remove-Item *.spec
   ```
4. Execute novo build: `python build_exe.py`
5. Teste o novo executável
6. Distribua a nova versão

## 📊 Checklist de Build

Antes de distribuir, verifique:

- [ ] Código testado e funcionando
- [ ] Versão atualizada em `src/__init__.py`
- [ ] README e documentação atualizados
- [ ] .env.exemplo criado (se usar Gemini)
- [ ] Ícone personalizado (opcional)
- [ ] Build executado sem erros
- [ ] Executável testado em máquina limpa
- [ ] Tamanho do .exe aceitável (< 100 MB)
- [ ] Antivírus não bloqueia
- [ ] Instruções para usuário criadas

## 💡 Dicas

1. **Build em Ambiente Limpo**: Crie um venv novo para o build para evitar bibliotecas desnecessárias
2. **Teste em Windows Limpo**: Teste o .exe em uma VM ou computador sem Python instalado
3. **Versione os Builds**: Mantenha histórico de versões (`DocsAnalyser_v2.0.exe`, `v2.1.exe`, etc)
4. **Compacte para Distribuição**: Use ZIP para enviar (mais fácil que executáveis grandes por email)

---

**Pronto!** Agora você tem um executável profissional para distribuir! 🎉
