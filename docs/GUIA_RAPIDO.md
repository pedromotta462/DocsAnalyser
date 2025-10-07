# 🚀 Guia Rápido - DocsAnalyser v2.0

> 🏠 **[← Voltar para o README principal](../README.md)** | 📚 **[Ver Índice Completo](INDICE.md)**

## Para Clientes (Usuários Finais)

### 📦 Instalação Zero!

1. **Baixe** o arquivo `DocsAnalyser.exe`
2. **Execute** (duplo clique)
3. **Pronto!** Não precisa instalar nada

### 📝 Como Usar

```
1. Clique em "🔍 Selecionar" → Escolha a pasta com seus documentos
2. Marque as opções desejadas:
   ☑ Criar backup antes de renomear
   ☑ Usar Gemini AI para PDFs escaneados
3. Clique em "▶️ Processar Documentos"
4. Aguarde... Os arquivos serão renomeados automaticamente!
```

### ⚠️ Antes de Começar

- ✅ Faça **BACKUP** dos documentos
- ✅ Feche todos os arquivos PDF/Word
- ✅ Certifique-se que tem permissão para modificar os arquivos

### 📊 O Que o Sistema Faz

O DocsAnalyser renomeia seus documentos seguindo o padrão **E-DIPLOMA DIGITAL**:

| Documento Original | Arquivo Renomeado |
|-------------------|-------------------|
| `joao_rg.pdf` | `IDE_12345.pdf` |
| `maria_cpf.pdf` | `CPF_67890.pdf` |
| `historico escolar.pdf` | `HES_12345.pdf` |

**Formato:** `{TIPO}_{MATRICULA}.{extensão}`

### 🔤 Códigos dos Documentos

- **OFI** = Ofício de encaminhamento
- **TER** = Termo de responsabilidade
- **IDE** = Identidade/RG
- **CPF** = Cadastro de Pessoa Física
- **CER** = Certidão (nascimento/casamento)
- **ENS** = Certificado de Ensino Médio
- **HES** = Histórico Escolar de Graduação
- **HEG** = Histórico de Aproveitamento
- **DIP** = Diploma
- **GRU** = Taxa/Boleto de pagamento

### ❓ Problemas Comuns

**P: O programa não encontrou o tipo do documento**
- R: Adicione palavras-chave no nome do arquivo (ex: "joao_rg.pdf", "maria_historico.pdf")

**P: Apareceu "SEMRA" no nome do arquivo**
- R: O sistema não encontrou o número de matrícula. Adicione no nome (ex: "ra12345_documento.pdf")

**P: PDF escaneado não foi processado**
- R: Ative a opção "Usar Gemini AI" e configure a chave API (veja manual técnico)

---

## Para Desenvolvedores

### 🔧 Setup do Ambiente

```bash
# Clone o repositório
git clone https://github.com/pedromotta462/DocsAnalyser.git
cd DocsAnalyser

# Crie ambiente virtual
python -m venv venv

# Ative (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Instale dependências
pip install -r requirements.txt
```

### ▶️ Executar

```bash
# Interface Gráfica (Recomendado)
python app.py
```

> 💡 **Nota**: A versão GUI substitui a CLI antiga.

### 🏗️ Gerar Executável

```bash
# Instalar PyInstaller
pip install pyinstaller

# Build
python build_exe.py

# Executável estará em: dist/DocsAnalyser.exe
```

### 🤖 Configurar Gemini AI

1. Obtenha chave em: https://makersuite.google.com/app/apikey
2. Crie `.env`:

```env
GEMINI_API_KEY=sua_chave_aqui
GEMINI_MODEL=gemini-2.5-flash
GEMINI_TEMPERATURE=0.1
```

### 📁 Estrutura

```
src/
├── core/              # Lógica principal
│   └── document_analyzer.py
├── gui/               # Interface gráfica
│   └── main_window.py
└── utils/             # Funções auxiliares
    └── helpers.py
```

### 🧪 Testar

```bash
# Testes unitários
python test_fixes.py

# Teste E-DIPLOMA
python test_ediploma.py
```

### 📦 Customizar Build

Edite `build_exe.py` para:
- Mudar nome do executável
- Adicionar/remover arquivos incluídos
- Alterar ícone
- Modificar parâmetros do PyInstaller

### 🐛 Debug

```bash
# Modo verbose
python app.py --debug

# Ver logs
# Os logs aparecerão na janela "Log de Processamento"
```

---

## 📞 Suporte

**Problemas?** Abra uma issue:
https://github.com/pedromotta462/DocsAnalyser/issues

**Dúvidas?** Consulte o README completo:
[README_v2.md](README_v2.md)

---

**DocsAnalyser v2.0** | © 2025 Pedro Motta
