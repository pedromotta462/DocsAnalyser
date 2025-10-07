# 📘 Manual do Usuário - DocsAnalyser v2.0

> 🏠 **[← Voltar para o README principal](../README.md)** | 📚 **[Ver Índice Completo](INDICE.md)**

## 🎯 O QUE É O DOCSANALYSER?

O DocsAnalyser é um **software profissional** que **renomeia automaticamente** seus documentos acadêmicos seguindo o padrão **E-DIPLOMA DIGITAL** do governo brasileiro.

### O Que Ele Faz?

**Transforma isto:**
```
joao_silva_rg.pdf
maria_historico_escolar.pdf
pedro_cpf_frente_verso.pdf
```

**Nisto:**
```
IDE_12345.pdf  (RG do João Silva, matrícula 12345)
HES_67890.pdf  (Histórico da Maria, matrícula 67890)
CPF_54321.pdf  (CPF do Pedro, matrícula 54321)
```

---

## 🚀 COMO COMEÇAR

### Passo 1: Obtenha o Programa

Você receberá um arquivo chamado:
```
📦 DocsAnalyser.exe  (~60 MB)
```

### Passo 2: Execute

1. Localize o arquivo `DocsAnalyser.exe`
2. Clique duas vezes nele
3. Se o Windows perguntar "Deseja executar?", clique em **Executar**

> **Nota:** Alguns antivírus podem bloquear. Se isso acontecer, adicione uma exceção.

---

## 📖 USANDO O PROGRAMA

### Tela Principal

Quando você abre o programa, verá esta tela:

```
┌────────────────────────────────────────────────┐
│       📄 DocsAnalyser                          │
│   Sistema de Análise de Documentos            │
├────────────────────────────────────────────────┤
│                                                │
│ 📁 Diretório de Documentos                    │
│ ┌──────────────────────────┐                  │
│ │ C:\Meus\Documentos       │ [🔍 Selecionar]  │
│ └──────────────────────────┘                  │
│ ✅ 15 arquivo(s) encontrado(s)                │
│                                                │
│ ⚙️ Opções                                     │
│ ☑ Criar backup antes de renomear              │
│ ☑ Usar IA para PDFs escaneados                │
│                                                │
│ [▶️ Processar]  [⏹️ Parar]  [🗑️ Limpar]      │
│                                                │
│ ▰▰▰▰▰▰▱▱▱▱▱▱▱▱▱▱ 40%                        │
│ Processando: documento_5.pdf                  │
│                                                │
│ 📋 Log:                                        │
│ ┌──────────────────────────────────────────┐  │
│ │ ✅ Arquivo 1 renomeado: IDE_12345.pdf    │  │
│ │ ✅ Arquivo 2 renomeado: CPF_12345.pdf    │  │
│ │ ✅ Arquivo 3 renomeado: HES_12345.pdf    │  │
│ └──────────────────────────────────────────┘  │
└────────────────────────────────────────────────┘
```

### Passo a Passo

#### 1️⃣ Selecionar Pasta

1. Clique no botão **"🔍 Selecionar"**
2. Navegue até a pasta com seus documentos
3. Clique em **"Selecionar Pasta"**

**Resultado:** O programa mostrará quantos arquivos encontrou.

```
✅ 15 arquivo(s) encontrado(s) (.pdf, .docx, .doc)
```

#### 2️⃣ Configurar Opções

**Opção 1: Criar backup**
- ☑ **Marcado:** Cria cópia de segurança antes de renomear
- ☐ **Desmarcado:** Renomeia diretamente (sem backup)

**Opção 2: Usar IA**
- ☑ **Marcado:** Usa inteligência artificial para PDFs escaneados
- ☐ **Desmarcado:** Processa apenas PDFs com texto

> **Recomendação:** Deixe ambas marcadas!

#### 3️⃣ Processar Documentos

1. Clique no botão **"▶️ Processar Documentos"**
2. Confirme quando aparecer a mensagem:
   ```
   Serão processados 15 arquivo(s).
   Os arquivos serão renomeados permanentemente.
   Um backup será criado.
   
   Deseja continuar?
   [Sim] [Não]
   ```
3. Aguarde o processamento...

#### 4️⃣ Acompanhar Progresso

Durante o processamento, você verá:

- **Barra de progresso:** Mostra % concluído
- **Status:** Qual arquivo está sendo processado
- **Log:** Resultado de cada arquivo

```
📋 Log de Processamento
══════════════════════════════════════
📄 Processando: joao_rg.pdf
   ✅ Arquivo renomeado para: IDE_12345.pdf

📄 Processando: maria_historico.pdf
   ✅ Arquivo renomeado para: HES_67890.pdf

📄 Processando: termo_responsabilidade.pdf
   🔍 RA encontrado por cross-reference: 12345
   ✅ Arquivo renomeado para: TER_12345.pdf
══════════════════════════════════════
✨ Concluído! 15/15 arquivos processados
```

#### 5️⃣ Verificar Resultado

Quando terminar, aparecerá:

```
┌─────────────────────────────────┐
│  Processamento Concluído!       │
│                                 │
│  Total: 15 arquivo(s)           │
│  Sucesso: 14                    │
│  Falhas: 1                      │
│                                 │
│         [OK]                    │
└─────────────────────────────────┘
```

---

## 📋 CÓDIGOS DOS DOCUMENTOS

O programa usa estes códigos para renomear seus documentos:

| Código | Tipo de Documento | Exemplo |
|--------|-------------------|---------|
| **OFI** | Ofício de encaminhamento | OFI_12345.pdf |
| **TER** | Termo de responsabilidade | TER_12345.pdf |
| **IDE** | RG / Identidade | IDE_12345.pdf |
| **CPF** | CPF | CPF_12345.pdf |
| **CER** | Certidão (nascimento/casamento) | CER_12345.pdf |
| **ENS** | Certificado de Ensino Médio | ENS_12345.pdf |
| **HES** | Histórico Escolar de Graduação | HES_12345.pdf |
| **HEG** | Histórico de Aproveitamento | HEG_12345.pdf |
| **DIP** | Diploma | DIP_12345.pdf |
| **GRU** | GRU / Taxa / Boleto | GRU_12345.pdf |

### Formato do Nome

```
{CÓDIGO}_{MATRÍCULA}.{extensão}

Exemplos:
IDE_12345.pdf     ← RG, matrícula 12345
HES_67890.docx    ← Histórico, matrícula 67890
CPF_03013.pdf     ← CPF, matrícula 03013
```

---

## 💡 DICAS PARA MELHORES RESULTADOS

### 1. Organize os Nomes dos Arquivos

**❌ Ruim:**
```
documento1.pdf
doc_frente.pdf
scan_002.pdf
```

**✅ Bom:**
```
joao_rg.pdf              ← Indica que é RG
maria_historico.pdf      ← Indica que é histórico
pedro_ra12345_cpf.pdf    ← Tem matrícula e tipo
```

### 2. Inclua a Matrícula (RA) no Nome

Se possível, adicione o RA no nome do arquivo:

```
ra12345_documento.pdf      ← Melhor!
mat67890_historico.pdf     ← Melhor!
```

O programa encontrará o RA automaticamente!

### 3. Use Palavras-Chave

Ajude o programa incluindo palavras-chave:

```
joao_silva_rg.pdf          ← "rg" indica identidade
maria_cpf_frente.pdf       ← "cpf" indica CPF
pedro_historico.pdf        ← "historico" indica histórico
termo_responsabilidade.pdf ← "termo" indica termo
```

### 4. Feche os Arquivos

Antes de processar:
```
✅ Feche todos os PDFs abertos
✅ Feche todos os arquivos Word
✅ Não mexa nos arquivos durante o processamento
```

### 5. Faça Backup

Sempre marque a opção:
```
☑ Criar backup antes de renomear arquivos
```

---

## ⚠️ AVISOS IMPORTANTES

### 🔴 LEIA ANTES DE USAR!

1. **BACKUP**: Sempre faça backup dos documentos antes de processar
   
2. **IRREVERSÍVEL**: A renomeação é permanente (a menos que tenha backup)

3. **PERMISSÕES**: Certifique-se de ter permissão para modificar os arquivos

4. **ARQUIVOS ABERTOS**: Feche todos os PDFs/Word antes de processar

5. **ANTIVÍRUS**: Pode bloquear o programa (adicione exceção se necessário)

---

## ❓ PERGUNTAS FREQUENTES

### P: O programa precisa de internet?

**R:** Não para arquivos normais. Apenas se usar a opção "IA para PDFs escaneados".

### P: Posso desfazer a renomeação?

**R:** Sim, se marcou "Criar backup". O backup estará na mesma pasta.

### P: O que significa "SEMRA" no nome do arquivo?

**R:** Significa que o programa não encontrou o número de matrícula (RA).

**Solução:** Adicione o RA no nome do arquivo:
```
joao_rg.pdf  →  ra12345_joao_rg.pdf
```

### P: O programa não reconheceu o tipo do documento

**R:** Adicione palavras-chave no nome:
```
documento.pdf  →  documento_rg.pdf
arquivo.pdf    →  arquivo_historico.pdf
```

### P: Apareceu erro ao processar

**R:** Possíveis causas:
- Arquivo está aberto em outro programa
- Sem permissão para modificar
- Arquivo corrompido
- Sem espaço em disco

### P: Posso processar quantos arquivos?

**R:** Sim! Não há limite. Mas para muitos arquivos (100+), processe em lotes.

### P: Quanto tempo demora?

**R:** 
- Arquivo normal: ~1 segundo cada
- PDF escaneado (com IA): ~5 segundos cada
- 100 arquivos: ~5-10 minutos

### P: O programa é seguro?

**R:** Sim! O código é open-source e pode ser auditado no GitHub.

---

## 🆘 PROBLEMAS E SOLUÇÕES

### Problema: "Python não encontrado"

**Solução:** Você recebeu o arquivo errado. Peça o arquivo `.exe`:
```
✅ Correto: DocsAnalyser.exe
❌ Errado: DocsAnalyser.py
```

### Problema: Antivírus bloqueou

**Solução:**
1. Abra seu antivírus
2. Adicione exceção para `DocsAnalyser.exe`
3. Tente executar novamente

### Problema: Nada acontece ao clicar

**Solução:**
1. Execute como **Administrador**:
   - Clique direito no .exe
   - Selecione "Executar como administrador"

### Problema: Erro "Sem permissão"

**Solução:**
- Certifique-se de ter permissão para modificar os arquivos
- Tente copiar os arquivos para uma pasta sua (ex: Documentos)
- Execute o programa como administrador

### Problema: Arquivos não aparecem

**Solução:**
O programa só processa:
```
✅ .pdf
✅ .docx
✅ .doc
❌ Outros formatos não são suportados
```

---

## 📞 PRECISA DE AJUDA?

### Suporte Técnico

**Email:** seu_email@exemplo.com

**GitHub:** github.com/pedromotta462/DocsAnalyser

### Informações do Sistema

Ao pedir suporte, informe:
```
• Versão do Windows
• Mensagem de erro (se houver)
• O que você estava fazendo
• Captura de tela (se possível)
```

---

## ✅ CHECKLIST DE USO

Antes de usar, verifique:

- [ ] Recebi o arquivo `DocsAnalyser.exe`
- [ ] Fiz backup dos meus documentos
- [ ] Fechei todos os PDFs/Word
- [ ] Tenho permissão para modificar os arquivos
- [ ] Sei onde estão meus documentos

Durante o uso:

- [ ] Selecionei a pasta correta
- [ ] Marquei "Criar backup"
- [ ] Confirmei o processamento
- [ ] Aguardei até completar

Após o uso:

- [ ] Verifiquei os arquivos renomeados
- [ ] Conferi se está tudo correto
- [ ] Guardei o backup em lugar seguro

---

## 📖 GLOSSÁRIO

**RA / Matrícula:** Número de registro acadêmico do aluno (ex: 12345)

**PDF Escaneado:** PDF que é uma foto/imagem (não tem texto copiável)

**Backup:** Cópia de segurança dos arquivos originais

**E-DIPLOMA DIGITAL:** Padrão brasileiro de nomenclatura de documentos acadêmicos

**Cross-reference:** Quando o programa usa informações de um arquivo para processar outro

**IA / Inteligência Artificial:** Tecnologia para ler PDFs escaneados

---

**DocsAnalyser v2.0**  
Sistema Profissional E-DIPLOMA DIGITAL  
© 2025 - Todos os direitos reservados

---

**🎉 Pronto para começar?**

1. Execute `DocsAnalyser.exe`
2. Selecione sua pasta
3. Clique em "Processar"
4. Pronto!

**Boa sorte!** 🚀
