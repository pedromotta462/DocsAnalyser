# 📚 Índice da Documentação - DocsAnalyser v2.0

> 🏠 **[← Voltar para o README principal](../README.md)**

## 🎯 Início Rápido

Novo no DocsAnalyser? Comece por aqui:

1. **[README.md (Raiz)](../README.md)** 🏠
   - Documentação principal do projeto
   - Instalação e uso básico
   - Links para documentação detalhada

2. **[GUIA_RAPIDO.md](GUIA_RAPIDO.md)** ⚡
   - Para clientes (1 página)
   - Para desenvolvedores (1 página)
   - Comandos essenciais
   - Dicas rápidas

3. **[ESTRUTURA_PROJETO.md](ESTRUTURA_PROJETO.md)** 📁
   - Organização completa do projeto
   - Estatísticas de arquivos
   - Navegação rápida

---

## 👥 Para Usuários Finais (Clientes)

### 📘 Manual Completo

**[MANUAL_USUARIO.md](MANUAL_USUARIO.md)** - Guia ilustrado passo a passo
```
• O que é o DocsAnalyser
• Como instalar e executar
• Passo a passo com imagens
• Códigos dos documentos (OFI, TER, IDE, etc)
• Dicas para melhores resultados
• Perguntas frequentes
• Solução de problemas
• Glossário
```

**Ideal para:** Quem vai usar o programa pela primeira vez

---

## 💻 Para Desenvolvedores

### 📖 Documentação Técnica

#### 1. **[README.md (Raiz)](../README.md)** - README Principal
```
• Visão geral técnica
• Instalação com Python
• Funcionalidades detalhadas
• Configuração do Gemini AI
• Exemplos de uso
• Estrutura do projeto
• Tecnologias utilizadas
• Solução de problemas
```

**Ideal para:** Desenvolvedores que vão modificar o código

---

#### 2. **[ARQUITETURA.md](ARQUITETURA.md)** - Arquitetura do Sistema
```
• Diagrama completo da arquitetura
• Estrutura de diretórios detalhada
• Fluxo de dados
• Componentes principais
• Padrões de design utilizados
• Integração com Gemini AI
• Segurança e validações
• Escalabilidade e performance
• Testabilidade
```

**Ideal para:** Entender como o sistema funciona internamente

---

#### 3. **[COMO_GERAR_EXE.md](COMO_GERAR_EXE.md)** - Tutorial de Build
```
• Pré-requisitos
• Passo a passo do build
• Parâmetros do PyInstaller explicados
• Personalizar ícone
• O que será incluído no .exe
• Verificar build
• Solução de problemas de build
• Distribuir o executável
• Atualizar o executável
• Checklist completo
```

**Ideal para:** Gerar o arquivo .exe para distribuição

---

## 📦 Arquivos de Configuração

### Código Principal

```
DocsAnalyser/
├── app.py                        ← Entry point - Interface GUI
├── build_exe.py                  ← Script para gerar .exe
│
├── src/                          ← Código-fonte modular
│   ├── core/
│   │   └── document_analyzer.py  ← Lógica de negócio
│   ├── gui/
│   │   └── main_window.py        ← Interface gráfica Tkinter
│   └── utils/
│       └── helpers.py            ← Funções auxiliares
│
├── docs/                         ← Documentação completa
│   ├── INDICE.md
│   ├── MANUAL_USUARIO.md
│   ├── ARQUITETURA.md
│   └── ...
│
├── config/
│   └── settings.json             ← Configurações do usuário
│
└── assets/
    └── icon.ico                  ← Ícone da aplicação
```

### Configuração

- **`.env`** - Chave API do Gemini (opcional)
- **`renaming_rules.json`** - Regras E-DIPLOMA
- **`config/settings.json`** - Preferências do usuário
- **`requirements.txt`** - Dependências Python

---

## 📊 Fluxogramas e Diagramas

Encontre em **[ARQUITETURA.md](ARQUITETURA.md)**:

1. **Arquitetura Geral** (camadas do sistema)
2. **Estrutura de Diretórios** (organização dos arquivos)
3. **Fluxo de Processamento** (arquivo individual)
4. **Fluxo de Lote** (múltiplos arquivos)
5. **Integração Gemini AI** (PDFs escaneados)

---

## 🎓 Tutoriais Passo a Passo

### Para Usuários

1. **Primeiro Uso**
   - Ver: [MANUAL_USUARIO.md § Como Começar](MANUAL_USUARIO.md#-como-começar)

2. **Usar o Programa**
   - Ver: [MANUAL_USUARIO.md § Usando o Programa](MANUAL_USUARIO.md#-usando-o-programa)

3. **Solucionar Problemas**
   - Ver: [MANUAL_USUARIO.md § Problemas e Soluções](MANUAL_USUARIO.md#-problemas-e-soluções)

### Para Desenvolvedores

1. **Setup do Ambiente**
   - Ver: [GUIA_RAPIDO.md § Setup](GUIA_RAPIDO.md#-setup-do-ambiente)

2. **Desenvolver e Testar**
   - Ver: [README.md § Como Usar](README.md#-como-usar)

3. **Gerar Executável**
   - Ver: [COMO_GERAR_EXE.md](COMO_GERAR_EXE.md)

4. **Entender Arquitetura**
   - Ver: [ARQUITETURA.md](ARQUITETURA.md)

---

## 🔍 Busca Rápida

### Quero Saber Como...

| Tarefa | Documento | Seção |
|--------|-----------|-------|
| **Executar o programa** | MANUAL_USUARIO.md | Como Começar |
| **Instalar Python e dependências** | README.md | Instalação |
| **Gerar o executável (.exe)** | COMO_GERAR_EXE.md | Passo a Passo |
| **Configurar Gemini AI** | README.md | Configuração do Gemini |
| **Entender a arquitetura** | ARQUITETURA.md | Visão Geral |
| **Resolver problemas comuns** | MANUAL_USUARIO.md | Perguntas Frequentes |
| **Modificar o código** | ARQUITETURA.md | Componentes |
| **Distribuir para clientes** | COMO_GERAR_EXE.md | Distribuir |

---

## 📖 Documentos por Público-Alvo

### 👤 Usuário Final (Cliente)

Leia nesta ordem:

1. **[MANUAL_USUARIO.md](MANUAL_USUARIO.md)** - Leia tudo
2. **[GUIA_RAPIDO.md](GUIA_RAPIDO.md)** - Seção "Para Clientes"

**Tempo de leitura:** ~20 minutos

---

### 👨‍💻 Desenvolvedor (Primeira Vez)

Leia nesta ordem:

1. **[RESUMO_COMPLETO.md](RESUMO_COMPLETO.md)** - Visão geral
2. **[README.md](README.md)** - Instalação e uso
3. **[GUIA_RAPIDO.md](GUIA_RAPIDO.md)** - Comandos rápidos
4. **[ARQUITETURA.md](ARQUITETURA.md)** - Entender estrutura

**Tempo de leitura:** ~45 minutos

---

### 🏗️ Desenvolvedor (Build & Deploy)

Leia nesta ordem:

1. **[GUIA_RAPIDO.md](GUIA_RAPIDO.md)** - Setup rápido
2. **[COMO_GERAR_EXE.md](COMO_GERAR_EXE.md)** - Gerar executável
3. **[RESUMO_COMPLETO.md](RESUMO_COMPLETO.md)** - Checklist de entrega

**Tempo de leitura:** ~30 minutos

---

### 🔧 Desenvolvedor (Manutenção)

Consulte conforme necessário:

- **Bug fix:** [ARQUITETURA.md](ARQUITETURA.md)
- **Novo recurso:** [ARQUITETURA.md](ARQUITETURA.md) + [README.md](README.md)
- **Refactoring:** [ARQUITETURA.md](ARQUITETURA.md)

---

## 📑 Glossário Rápido

Encontre definições detalhadas em **[MANUAL_USUARIO.md § Glossário](MANUAL_USUARIO.md#-glossário)**

| Termo | Significado |
|-------|-------------|
| **RA** | Registro Acadêmico (matrícula do aluno) |
| **E-DIPLOMA** | Padrão brasileiro de nomenclatura de documentos |
| **Cross-reference** | Buscar RA de um arquivo usando info de outro |
| **Gemini AI** | IA do Google para processar PDFs escaneados |
| **PyInstaller** | Ferramenta para criar executável |
| **GUI** | Interface gráfica (com janelas e botões) |
| **Tkinter** | Biblioteca Python para criar interfaces gráficas |

---

## 🆘 Suporte

### Precisa de Ajuda?

1. **Primeiro:** Consulte as [Perguntas Frequentes](MANUAL_USUARIO.md#-perguntas-frequentes)
2. **Segundo:** Veja [Problemas e Soluções](MANUAL_USUARIO.md#-problemas-e-soluções)
3. **Terceiro:** Abra uma [issue no GitHub](https://github.com/pedromotta462/DocsAnalyser/issues)

### Reportar Bug

Ao reportar um problema, inclua:

```
• Qual documento estava lendo: _______________
• O que estava tentando fazer: _______________
• O que aconteceu: _______________
• O que esperava: _______________
• Sistema operacional: _______________
• Versão do programa: _______________
```

---

## 📊 Estatísticas da Documentação

```
Total de Documentos: 10 arquivos
  • README.md (raiz)
  • 9 arquivos em docs/
Páginas Totais: ~120
Tempo de Leitura Total: ~2.5 horas
Diagramas: 4
Exemplos de Código: 40+
Tutoriais: 6
```

### Cobertura por Tópico

- ✅ Manual do usuário final
- ✅ Guia de instalação
- ✅ Tutorial de desenvolvimento
- ✅ Documentação de arquitetura
- ✅ Guia de build e deploy
- ✅ FAQ e troubleshooting
- ✅ Glossário
- ✅ Estrutura do projeto
- ✅ Glossário
- ✅ Exemplos práticos

---

## 🎯 Próximos Passos

### Para Começar Agora

**Usuário Final:**
```bash
1. Leia MANUAL_USUARIO.md (20 min)
2. Execute DocsAnalyser.exe
3. Processe seus documentos!
```

**Desenvolvedor:**
```bash
1. Leia ../README.md (raiz) (10 min)
2. Leia GUIA_RAPIDO.md (10 min)
3. Execute: python app.py
4. Explore o código!
4. Explore o código!
```

**Build Master:**
```bash
1. Leia COMO_GERAR_EXE.md (15 min)
2. Execute: python build_exe.py
3. Distribua: dist/DocsAnalyser.exe
```

---

## ✅ Checklist de Leitura

Marque o que você já leu:

### Essencial (Leia Primeiro)
- [ ] RESUMO_COMPLETO.md
- [ ] GUIA_RAPIDO.md

### Para Usuários
- [ ] MANUAL_USUARIO.md

### Para Desenvolvedores
- [ ] README.md
- [ ] ARQUITETURA.md

### Para Build
- [ ] COMO_GERAR_EXE.md

---

## 🔄 Atualizações da Documentação

**Última Atualização:** Outubro 2025  
**Versão:** 2.0  
**Changelog:**

```
v2.0 (Outubro 2025)
  • Criação da documentação completa
  • 9 documentos criados
  • Cobertura 100% de funcionalidades
  • Manuais para usuários e desenvolvedores
  • Tutoriais detalhados
  • Diagramas e fluxogramas
```

---

## 📞 Contato

**Dúvidas sobre a documentação?**

- GitHub: [pedromotta462/DocsAnalyser](https://github.com/pedromotta462/DocsAnalyser)
- Issues: [Abrir Issue](https://github.com/pedromotta462/DocsAnalyser/issues)

---

**DocsAnalyser v2.0** - Documentação Completa  
© 2025 Pedro Motta | Todos os direitos reservados

---

## 🎉 Comece Agora!

Escolha seu caminho:

- 👤 **Usuário?** → [MANUAL_USUARIO.md](MANUAL_USUARIO.md)
- 💻 **Desenvolvedor?** → [RESUMO_COMPLETO.md](RESUMO_COMPLETO.md)
- 📦 **Build?** → [COMO_GERAR_EXE.md](COMO_GERAR_EXE.md)

**Boa leitura!** 📚
