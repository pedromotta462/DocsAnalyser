# 📄 DocsAnalyser v2.0 - Sistema E-DIPLOMA DIGITAL

Sistema profissional de análise e renomeação automática de documentos acadêmicos conforme padrão E-DIPLOMA DIGITAL do governo brasileiro.

## 🌟 Novidades da Versão 2.0

- ✅ **Interface Gráfica Moderna** - Interface intuitiva para facilitar o uso
- ✅ **Executável Standalone** - Não requer instalação de Python
- ✅ **Arquitetura Modular** - Código organizado e manutenível
- ✅ **Integração com Gemini AI** - Processa PDFs escaneados automaticamente
- ✅ **Cross-Reference Inteligente** - Encontra RA por nome entre arquivos
- ✅ **Identificação por Filename** - Usa nome do arquivo para melhor precisão

## � Documentação

- 📖 **[Manual do Usuário](docs/MANUAL_USUARIO.md)** - Guia completo para usuários finais
- ⚡ **[Guia Rápido](docs/GUIA_RAPIDO.md)** - Início rápido (2 páginas)
- 🏗️ **[Arquitetura](docs/ARQUITETURA.md)** - Documentação técnica do sistema
- 🔧 **[Como Gerar EXE](docs/COMO_GERAR_EXE.md)** - Tutorial de build
- 📑 **[Índice Completo](docs/INDICE.md)** - Navegação por toda documentação

## �📋 Funcionalidades

### Tipos de Documentos Suportados (E-DIPLOMA)

| Tipo | Código | Exemplo |
|------|--------|---------|
| Ofício | OFI | OFI_03013.pdf |
| Termo | TER | TER_03013.pdf |
| Identidade/RG | IDE | IDE_03013.pdf |
| CPF | CPF | CPF_03013.pdf |
| Certidão | CER | CER_03013.pdf |
| Ensino Médio | ENS | ENS_03013.pdf |
| Histórico Graduação | HES | HES_03013.pdf |
| Histórico Aproveitamento | HEG | HEG_03013.pdf |
| Diploma | DIP | DIP_03013.pdf |
| Taxa/GRU | GRU | GRU_03013.pdf |

### Recursos Principais

- 🔍 **Extração Automática de RA** (Registro Acadêmico)
  - Do nome do arquivo (ra03013, mat12345)
  - Do conteúdo do documento
  - Por cross-reference de nome entre arquivos
  
- 🤖 **IA para PDFs Escaneados**
  - Usa Google Gemini para documentos sem texto extraível
  - Identifica tipo, RA e nome automaticamente
  
- 📝 **Múltiplos Formatos**
  - PDF (texto e escaneado)
  - DOCX (Word moderno)
  - DOC (Word antigo)

## 🚀 Como Usar

### Opção 1: Executável (.exe) - RECOMENDADO PARA CLIENTES

1. **Baixe o executável**: `DocsAnalyser.exe`
2. **Execute**: Duplo clique no arquivo
3. **Selecione a pasta** com os documentos
4. **Clique em "Processar Documentos"**
5. **Pronto!** Os arquivos serão renomeados automaticamente

> ⚠️ **IMPORTANTE**: Faça backup dos documentos antes de processar!

### Opção 2: Python (Desenvolvimento)

#### Instalação

```bash
# 1. Clone o repositório
git clone https://github.com/pedromotta462/DocsAnalyser.git
cd DocsAnalyser

# 2. Crie ambiente virtual
python -m venv venv

# 3. Ative o ambiente
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# ou
.\venv\Scripts\activate.bat  # Windows CMD

# 4. Instale dependências
pip install -r requirements.txt
```

#### Executar Interface Gráfica

```bash
python app.py
```

> 💡 **Nota**: A versão CLI (linha de comando) foi substituída pela interface gráfica moderna.

## 🔧 Configuração do Gemini AI (Opcional)

Para processar PDFs escaneados, configure a API do Gemini:

1. Obtenha uma chave API em: https://makersuite.google.com/app/apikey
2. Crie um arquivo `.env` na raiz do projeto:

```env
GEMINI_API_KEY=sua_chave_aqui
GEMINI_MODEL=gemini-2.5-flash
```

## 🏗️ Estrutura do Projeto

```
DocsAnalyser/
├── src/                      # Código-fonte modular
│   ├── core/                 # Lógica de negócio
│   │   └── document_analyzer.py
│   ├── gui/                  # Interface gráfica
│   │   └── main_window.py
│   └── utils/                # Utilitários
│       └── helpers.py
├── docs/                     # Documentação completa
│   ├── MANUAL_USUARIO.md
│   ├── GUIA_RAPIDO.md
│   ├── ARQUITETURA.md
│   └── ...
├── config/                   # Configurações
│   └── settings.json
├── assets/                   # Recursos (ícones)
│   └── icon.ico
├── app.py                    # Entry point - Interface GUI
├── build_exe.py              # Script para gerar .exe
├── requirements.txt          # Dependências Python
└── README.md                 # Este arquivo
```

## 📦 Gerar Executável

Para desenvolvedores que desejam gerar o executável standalone:

```bash
# O script build_exe.py cuida de tudo automaticamente
python build_exe.py
```

O executável será criado em `dist/DocsAnalyser.exe` (~60MB)

> 📘 **Documentação detalhada**: Veja [Como Gerar EXE](docs/COMO_GERAR_EXE.md) para instruções completas

### O que o build inclui automaticamente

### O que o build inclui automaticamente

- ✅ Todos os módulos Python necessários
- ✅ Arquivo de configuração (settings.json)
- ✅ Regras de renomeação E-DIPLOMA
- ✅ Ícone personalizado
- ✅ Arquivo .env (se existir)

## 🎯 Exemplos de Uso

### Cenário 1: Documentos com RA no Nome

**Entrada:**
```
ra03013 doc00005 RG pdf-a.pdf
ra03013 doc00006 C.P.F.pdf
ra03013 doc00015 Ensino Médio pdf-a.pdf
```

**Saída:**
```
IDE_03013.pdf
CPF_03013.pdf
ENS_03013.pdf
```

### Cenário 2: Cross-Reference por Nome

**Entrada:**
```
ra03013 doc00005 RG pdf-a.pdf              (RA: 03013, Nome: Kátia Verônica)
TERMO Kátia Verônica Almeida da Silva.pdf (Sem RA explícito)
```

**Saída:**
```
IDE_03013.pdf
TER_03013.pdf  ← RA encontrado por cross-reference!
```

### Cenário 3: PDF Escaneado com Gemini

**Entrada:**
```
Histórico Kátia Verônica.pdf (PDF escaneado, sem texto extraível)
```

**Processamento:**
1. Detecta que não há texto extraível
2. Envia imagem para Gemini AI
3. Gemini identifica: Tipo=historico_graduacao, RA=03013, Nome=Kátia Verônica

**Saída:**
```
HES_03013.pdf
```

## 🛠️ Tecnologias Utilizadas

- **Python 3.12+**
- **Tkinter** - Interface gráfica nativa
- **PyPDF2 & pdfplumber** - Extração de texto de PDFs
- **python-docx & docx2txt** - Processamento de Word
- **Google Gemini AI** - IA para PDFs escaneados
- **PyInstaller** - Geração de executável

## 📊 Fluxo de Processamento

```
1. Seleção de Diretório
   ↓
2. Leitura de Arquivos (.pdf, .docx, .doc)
   ↓
3. Extração de Texto
   ├─→ Texto normal (PyPDF2/pdfplumber)
   └─→ PDF escaneado → Gemini AI
   ↓
4. Identificação do Tipo
   ├─→ Por keywords no texto (peso 2)
   └─→ Por keywords no filename (peso 3)
   ↓
5. Extração de RA
   ├─→ Do filename (ra03013)
   ├─→ Do texto (RA: 03013)
   └─→ Por cross-reference de nome
   ↓
6. Renomeação (padrão E-DIPLOMA)
   └─→ {TIPO}_{RA}.{ext}
```

## ⚠️ Avisos Importantes

1. **Backup**: Sempre faça backup antes de processar documentos
2. **Irreversível**: A renomeação é permanente
3. **Gemini API**: Requer chave API para PDFs escaneados
4. **Ordem**: Processe arquivos com RA antes dos sem RA para melhor cross-reference

## 🐛 Solução de Problemas

### Erro: "Tipo de documento não identificado"
- Verifique se o documento contém keywords reconhecíveis
- Tente adicionar keywords no nome do arquivo
- Para PDFs escaneados, configure o Gemini AI

### Erro: "RA não encontrado (SEMRA)"
- Certifique-se que o RA está no nome do arquivo (ra03013) ou no texto
- Processe arquivos com RA antes dos arquivos sem RA
- Verifique se há arquivos com o mesmo nome de pessoa já processados

### Executável não abre
- Execute como administrador
- Verifique antivírus (pode bloquear executáveis desconhecidos)
- Teste a versão Python para debug

## 📝 Licença

© 2025 Pedro Motta - Todos os direitos reservados

## 🤝 Contribuições

Contribuições são bem-vindas! Abra uma issue ou pull request.

## 📧 Contato

Para suporte ou dúvidas:
- GitHub: [@pedromotta462](https://github.com/pedromotta462)
- Issues: https://github.com/pedromotta462/DocsAnalyser/issues

---

**DocsAnalyser v2.0** - Sistema Profissional para E-DIPLOMA DIGITAL
