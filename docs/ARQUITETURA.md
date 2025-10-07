# 🏗️ Arquitetura DocsAnalyser v2.0

> 🏠 **[← Voltar para o README principal](../README.md)** | 📚 **[Ver Índice Completo](INDICE.md)**

> ℹ️ **Nota**: O diagrama abaixo mostra a arquitetura completa. A versão atual utiliza apenas a **interface GUI (Tkinter)**, sem CLI.

## 📐 Visão Geral da Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    DOCSANALYSER v2.0                        │
│         Sistema E-DIPLOMA DIGITAL - Arquitetura             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    CAMADA DE APRESENTAÇÃO                   │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐          ┌─────────────────┐          │
│  │   GUI (Tkinter) │          │  CLI (Terminal) │          │
│  │  main_window.py │          │ docsAnalyser.py │          │
│  │                 │          │                 │          │
│  │  - Interface    │          │  - Menu texto   │          │
│  │  - Botões       │          │  - Input/Output │          │
│  │  - Logs         │          │  - Simples      │          │
│  └────────┬────────┘          └────────┬────────┘          │
└───────────┼──────────────────────────

──┼───────────────┘
            │                          │
            └──────────┬───────────────┘
                       │
┌──────────────────────┴──────────────────────────────────────┐
│                   CAMADA DE LÓGICA                          │
├─────────────────────────────────────────────────────────────┤
│  ┌───────────────────────────────────────────────────────┐  │
│  │         DocumentAnalyzer (Core Business Logic)        │  │
│  │                 document_analyzer.py                  │  │
│  ├───────────────────────────────────────────────────────┤  │
│  │                                                       │  │
│  │  Responsabilidades:                                  │  │
│  │  • Extração de texto (PDF, DOCX, DOC)               │  │
│  │  • Identificação de tipo de documento                │  │
│  │  • Extração de RA (matrícula)                        │  │
│  │  • Extração de nomes                                 │  │
│  │  • Cross-referencing entre arquivos                  │  │
│  │  • Geração de novos nomes (E-DIPLOMA)               │  │
│  │  • Renomeação de arquivos                            │  │
│  │                                                       │  │
│  │  Métodos Principais:                                 │  │
│  │  ├─ process_file()          → Processa 1 arquivo    │  │
│  │  ├─ process_directory()     → Processa pasta        │  │
│  │  ├─ identify_document_type() → Identifica tipo      │  │
│  │  ├─ extract_matricula_*()    → Extrai RA           │  │
│  │  ├─ find_ra_by_name()        → Cross-reference     │  │
│  │  └─ generate_new_filename()  → Gera nome E-DIPLOMA │  │
│  │                                                       │  │
│  └───────────────┬───────────────────────────────────────┘  │
└──────────────────┼──────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
┌───────▼────────┐    ┌───────▼────────┐
│  Bibliotecas   │    │  Serviços      │
│  Externas      │    │  Externos      │
├────────────────┤    ├────────────────┤
│ • PyPDF2       │    │ • Gemini AI    │
│ • pdfplumber   │    │   (Google)     │
│ • python-docx  │    │                │
│ • docx2txt     │    │ • .env config  │
│ • PyMuPDF      │    │ • API Keys     │
│ • Pillow       │    │                │
└────────────────┘    └────────────────┘
```

## 🗂️ Estrutura de Diretórios Detalhada

```
DocsAnalyser/
│
├── 📁 src/                          # Código-fonte principal
│   ├── __init__.py                  # Metadata do pacote
│   │
│   ├── 📁 core/                     # Lógica de negócio
│   │   ├── __init__.py
│   │   └── document_analyzer.py    # ⭐ Classe principal (500+ linhas)
│   │       ├── DocumentAnalyzer class
│   │       ├── setup_gemini()
│   │       ├── extract_text_from_pdf_only()
│   │       ├── analyze_document_with_gemini()
│   │       ├── identify_document_type()
│   │       ├── extract_matricula_*()
│   │       ├── find_ra_by_name()
│   │       └── generate_new_filename()
│   │
│   ├── 📁 gui/                      # Interface gráfica
│   │   ├── __init__.py
│   │   └── main_window.py          # ⭐ Interface Tkinter (400+ linhas)
│   │       ├── DocsAnalyserGUI class
│   │       ├── create_widgets()
│   │       ├── browse_directory()
│   │       ├── start_processing()
│   │       └── process_documents()
│   │
│   └── 📁 utils/                    # Utilitários
│       ├── __init__.py
│       └── helpers.py               # Funções auxiliares
│           ├── get_resource_path()
│           ├── load_config()
│           ├── save_config()
│           ├── format_file_size()
│           └── count_files_in_directory()
│
├── 📁 config/                       # Configurações
│   └── settings.json                # Config da aplicação
│       ├── theme
│       ├── auto_backup
│       ├── gemini_enabled
│       └── last_directory
│
├── 📁 assets/                       # Recursos
│   └── icon.ico                     # Ícone do executável
│
├── 📁 dist/                         # Executável gerado (após build)
│   └── DocsAnalyser.exe             # 🎯 Produto final
│
├── � docs/                         # Documentação completa
│   ├── INDICE.md                    # Índice de documentação
│   ├── MANUAL_USUARIO.md            # Manual do usuário
│   ├── GUIA_RAPIDO.md               # Guia rápido
│   ├── ARQUITETURA.md               # Este arquivo
│   └── COMO_GERAR_EXE.md            # Tutorial de build
│
├── 📄 app.py                        # ⭐ Entry point - Interface GUI
├── 📄 build_exe.py                  # Script para gerar .exe
│
├── 📄 .env                          # Variáveis de ambiente (API keys)
├── 📄 renaming_rules.json           # Regras E-DIPLOMA
├── 📄 requirements.txt              # Dependências Python
└── � README.md                     # README principal
```

## 🔄 Fluxo de Dados

### 1. Processamento de Arquivo Individual

```
┌────────────────┐
│  Arquivo PDF   │
│  DOCX, DOC     │
└───────┬────────┘
        │
        ▼
┌──────────────────────────────┐
│ process_file()               │
│ - Valida extensão            │
│ - Determina tipo de arquivo  │
└───────┬──────────────────────┘
        │
        ▼
┌──────────────────────────────────────┐
│ Extração de Texto                    │
├──────────────────────────────────────┤
│ PDF:                                 │
│  ├─► extract_text_from_pdf_only()   │
│  │   ├─ PyPDF2                       │
│  │   └─ pdfplumber                   │
│  │                                   │
│  └─► Se falhar ou vazio:             │
│      └─► analyze_with_gemini()       │
│                                      │
│ DOCX: extract_text_from_docx()       │
│ DOC:  extract_text_from_doc()        │
└───────┬──────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────┐
│ Identificação do Tipo                │
├──────────────────────────────────────┤
│ identify_document_type(text, filename)│
│                                      │
│ Pontuação:                           │
│  • Keywords no texto = +2 pontos     │
│  • Keywords no filename = +3 pontos  │
│                                      │
│ Retorna: oficio, termo, identidade,  │
│          cpf, certidao, ensino_medio,│
│          etc                         │
└───────┬──────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────┐
│ Extração de RA (Matrícula)           │
├──────────────────────────────────────┤
│ Tentativa 1: Filename                │
│  └─► extract_matricula_from_filename()│
│      Padrões: ra03013, mat12345      │
│                                      │
│ Tentativa 2: Texto do Documento      │
│  └─► extract_matricula_from_text()   │
│      Padrões: RA: 03013, R.A.: 03013 │
│                                      │
│ Tentativa 3: Cross-Reference         │
│  └─► find_ra_by_name()               │
│      Busca nome em arquivos já       │
│      processados                     │
│                                      │
│ Se falhar tudo: usa "SEMRA"          │
└───────┬──────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────┐
│ Geração do Novo Nome                 │
├──────────────────────────────────────┤
│ generate_new_filename()              │
│                                      │
│ Formato E-DIPLOMA:                   │
│  {TIPO}_{RA}.{extensão}             │
│                                      │
│ Exemplos:                            │
│  • IDE_03013.pdf                     │
│  • CPF_12345.pdf                     │
│  • ENS_67890.pdf                     │
└───────┬──────────────────────────────┘
        │
        ▼
┌──────────────────────────────────────┐
│ Renomeação do Arquivo                │
├──────────────────────────────────────┤
│ • Verifica se já existe              │
│ • Adiciona contador se necessário    │
│   (IDE_03013_1.pdf)                  │
│ • Executa rename()                   │
│ • Armazena em processed_files{}      │
└───────┬──────────────────────────────┘
        │
        ▼
┌────────────────┐
│ Arquivo        │
│ Renomeado!     │
│ ✅ Sucesso     │
└────────────────┘
```

### 2. Processamento em Lote (Diretório)

```
┌─────────────────┐
│ Diretório com   │
│ N arquivos      │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────┐
│ process_directory()         │
│ - Lista arquivos (.pdf,     │
│   .docx, .doc)              │
│ - Itera sobre cada arquivo  │
└────────┬────────────────────┘
         │
         ├─► Arquivo 1 ──► process_file() ──► Armazena info
         │                                    em processed_files
         ├─► Arquivo 2 ──► process_file() ──► Pode usar info
         │                                    do Arquivo 1
         ├─► Arquivo 3 ──► process_file() ──► Cross-reference
         │                                    com anteriores
         └─► ...
                │
                ▼
         ┌────────────────┐
         │ Relatório      │
         │ Final          │
         │ X/N sucesso    │
         └────────────────┘
```

## 🧩 Componentes Principais

### 1. DocumentAnalyzer (Core)

**Responsabilidade:** Lógica de negócio completa

**Dependências:**
- PyPDF2, pdfplumber (extração PDF)
- python-docx, docx2txt (extração Word)
- google.generativeai (IA para PDFs escaneados)
- PIL, PyMuPDF (conversão PDF→imagem)

**Estado:**
```python
{
    "rules": {dict},              # Regras de renomeação E-DIPLOMA
    "gemini_model": {Model},      # Modelo Gemini AI
    "processed_files": {dict}     # Cache de arquivos processados
}
```

### 2. DocsAnalyserGUI (Interface)

**Responsabilidade:** Apresentação e interação com usuário

**Componentes:**
- Frame de seleção de diretório
- CheckButtons de opções
- Botões de ação (Processar, Parar, Limpar)
- Barra de progresso
- Log de processamento (ScrolledText)

**Comunicação:**
- Cria instância de `DocumentAnalyzer`
- Chama `process_file()` em thread separada
- Atualiza UI com callback messages

### 3. Helpers (Utilitários)

**Funções:**
- `get_resource_path()` - Resolve caminhos (dev vs .exe)
- `load_config()` - Carrega settings.json
- `save_config()` - Salva preferências do usuário
- `count_files_in_directory()` - Conta arquivos suportados
- `format_file_size()` - Formata tamanhos legíveis

## 🔌 Integração com Gemini AI

```
┌─────────────────────────────────────────┐
│ PDF Escaneado (sem texto extraível)     │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ convert_pdf_to_images()                 │
│ - Converte cada página PDF em imagem    │
│ - Usa PyMuPDF (fitz)                    │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ analyze_document_with_gemini()          │
│ - Envia imagem + prompt para Gemini     │
│ - Prompt estruturado com:                │
│   • Nome do arquivo (contexto)          │
│   • Lista de tipos válidos              │
│   • Formato de resposta obrigatório     │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ Gemini Response:                        │
│ TIPO: historico_graduacao               │
│ RA: 03013                               │
│ NOME: Kátia Verônica                    │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ parse_gemini_response()                 │
│ - Extrai tipo, RA, nome                 │
│ - Mapeia variações para tipos válidos   │
│ - Retorna (extracted_text, doc_type)    │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ Continua processamento normal           │
└─────────────────────────────────────────┘
```

## 📊 Padrões de Design Utilizados

### 1. **Singleton-like Pattern**
`DocumentAnalyzer` é instanciado uma vez por sessão de processamento.

### 2. **Strategy Pattern**
Diferentes estratégias de extração de texto:
- PyPDF2
- pdfplumber
- Gemini AI (fallback)

### 3. **Observer Pattern**
GUI observa o processamento via callbacks e atualiza UI.

### 4. **Template Method**
`process_file()` define template de processamento:
1. Validar
2. Extrair texto
3. Identificar tipo
4. Extrair RA
5. Gerar nome
6. Renomear

### 5. **Factory Pattern**
`identify_document_type()` cria o tipo apropriado baseado em regras.

## 🔒 Segurança e Validações

### Validações Implementadas

```python
# 1. Validação de Diretório
validate_directory(path) -> bool

# 2. Validação de Extensão
if extension not in ['.pdf', '.docx', '.doc']:
    return False

# 3. Validação de Tipo nas Regras
if doc_type and doc_type in self.rules:
    # Tipo válido

# 4. Sanitização de Nome
clean_name(name) -> str  # Remove caracteres especiais

# 5. Prevenção de Sobrescrita
if new_path.exists():
    add_counter()  # IDE_03013_1.pdf
```

### Tratamento de Erros

```python
try:
    # Processamento
except FileNotFoundError:
    log("Arquivo não encontrado")
except PermissionError:
    log("Sem permissão para modificar")
except Exception as e:
    log(f"Erro inesperado: {e}")
finally:
    # Cleanup
```

## 📈 Escalabilidade

### Otimizações Implementadas

1. **Threading**: Processamento em thread separada (não bloqueia GUI)
2. **Cache**: `processed_files` evita reprocessamento
3. **Lazy Loading**: Gemini só é inicializado se necessário
4. **Batch Processing**: Processa múltiplos arquivos em uma chamada

### Limitações Conhecidas

- **Memória**: PDFs grandes (>100MB) podem usar muita RAM
- **API Rate Limit**: Gemini tem limite de requisições/minuto
- **Threading**: Apenas 1 thread de processamento (evita race conditions)

## 🧪 Testabilidade

### Testes Implementados

```
tests/
├── test_fixes.py           # Testes das correções
├── test_ediploma.py        # Testes E-DIPLOMA
├── test_gemini.py          # Testes Gemini AI
└── test_analyzer.py        # Testes gerais
```

### Cobertura de Testes

- ✅ Extração de RA do filename
- ✅ Extração de RA do texto
- ✅ Cross-reference por nome
- ✅ Identificação de tipo por filename
- ✅ Nomenclatura E-DIPLOMA
- ✅ Gemini AI integration

## 🚀 Performance

### Métricas Esperadas

| Operação | Tempo Médio |
|----------|-------------|
| PDF texto (5 páginas) | 0.5-1s |
| PDF escaneado (5 páginas) | 3-5s (com Gemini) |
| DOCX | 0.2-0.5s |
| Diretório (100 arquivos) | 2-5 minutos |

### Gargalos

1. **Gemini API**: Rede + processamento remoto
2. **PDFs grandes**: Extração de texto é lenta
3. **Conversão PDF→Imagem**: Requer processamento

## 📦 Empacotamento (PyInstaller)

### Arquivos Incluídos no .exe

```
DocsAnalyser.exe
├── Python Interpreter
├── Bibliotecas:
│   ├── tkinter (GUI)
│   ├── PyPDF2, pdfplumber
│   ├── python-docx, docx2txt
│   ├── google-generativeai
│   ├── PIL, PyMuPDF
│   └── dotenv
├── Código fonte compactado
├── Config files
└── Ícone
```

### Tamanho Final

- **Executável**: ~50-70 MB
- **Memória em execução**: ~100-200 MB
- **Requer**: Windows 7+, nenhuma dependência externa

---

## 📚 Referências Técnicas

- **E-DIPLOMA DIGITAL**: Padrão brasileiro de nomenclatura de documentos acadêmicos
- **Tkinter**: Framework GUI nativo do Python
- **PyInstaller**: Ferramenta para criar executáveis standalone
- **Gemini AI**: Modelo de IA do Google para visão computacional e NLP

---

**DocsAnalyser v2.0** - Arquitetura profissional e escalável
© 2025 Pedro Motta
