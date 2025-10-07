import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import base64
from io import BytesIO

# Bibliotecas necessárias (instale with pip install)
try:
    import PyPDF2
    import pdfplumber
except ImportError:
    print("Para PDFs, instale: pip install PyPDF2 pdfplumber")

try:
    from docx import Document
except ImportError:
    print("Para arquivos Word, instale: pip install python-docx")

try:
    import docx2txt
except ImportError:
    print("Para arquivos .doc, instale: pip install docx2txt")

try:
    import google.generativeai as genai
    from dotenv import load_dotenv
    from PIL import Image
    GEMINI_AVAILABLE = True
except ImportError:
    print("Para usar Gemini AI com PDFs escaneados, instale: pip install google-generativeai python-dotenv pillow")
    GEMINI_AVAILABLE = False

# Carregar variáveis de ambiente
load_dotenv()

class DocumentAnalyzer:
    def __init__(self):
        self.rules = {}
        self.gemini_model = None
        self.processed_files = {}  # Armazena informações dos arquivos já processados
        self.load_rules()
        self.setup_gemini()
    
    def setup_gemini(self):
        """Configura a API do Gemini se disponível"""
        if not GEMINI_AVAILABLE:
            print("⚠️  Gemini AI não disponível. PDFs escaneados não poderão ser processados.")
            return
        
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key or api_key == 'your_gemini_api_key_here':
            print("⚠️  GEMINI_API_KEY não configurada no arquivo .env")
            print("   Configure sua chave da API para processar PDFs escaneados.")
            return
        
        try:
            genai.configure(api_key=api_key)
            
            # Lista de modelos para tentar em ordem de preferência
            model_names = [
                os.getenv('GEMINI_MODEL', 'gemini-2.5-flash'),
                'gemini-2.5-flash',
                'gemini-2.0-flash',
                'gemini-flash-latest',
                'gemini-pro-latest',
                'gemini-2.5-pro',
                'gemini-2.0-flash-001'
            ]
            
            # Tenta cada modelo até encontrar um que funcione
            for model_name in model_names:
                try:
                    self.gemini_model = genai.GenerativeModel(model_name)
                    # Testa se o modelo funciona
                    print(f"✅ Gemini AI configurado com sucesso! Modelo: {model_name}")
                    break
                except Exception as model_error:
                    if model_name == model_names[-1]:  # Último modelo da lista
                        raise model_error
                    continue
                    
        except Exception as e:
            print(f"❌ Erro ao configurar Gemini AI: {e}")
            print("💡 Sugestão: Verifique se sua API key está válida e tem acesso aos modelos Gemini")
    
    def convert_pdf_to_images(self, file_path: str) -> List[Image.Image]:
        """Converte PDF para imagens para análise pelo Gemini"""
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(file_path)
            images = []
            
            for page_num in range(min(3, len(doc))):  # Máximo 3 páginas
                page = doc[page_num]
                pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # 2x zoom
                img_data = pix.tobytes("png")
                img = Image.open(BytesIO(img_data))
                images.append(img)
            
            doc.close()
            return images
        except ImportError:
            print("📦 Para processar PDFs escaneados, instale: pip install PyMuPDF")
            return []
        except Exception as e:
            print(f"❌ Erro ao converter PDF para imagens: {e}")
            return []
    
    def analyze_document_with_gemini(self, file_path: str) -> Tuple[str, str]:
        """Analisa documento usando Gemini AI para PDFs escaneados"""
        if not self.gemini_model:
            return "", ""
        
        try:
            # Para PDFs, converte para imagens
            if file_path.lower().endswith('.pdf'):
                images = self.convert_pdf_to_images(file_path)
                if not images:
                    return "", ""
                
                # Usa apenas a primeira página
                image = images[0]
            else:
                # Para outros formatos de imagem
                image = Image.open(file_path)
            
            # Prompt para extração de informações
            prompt = f"""
Você é um especialista em análise de documentos acadêmicos brasileiros.
Analise CUIDADOSAMENTE este documento e forneça as informações solicitadas.

NOME DO ARQUIVO: {file_path}

INSTRUÇÕES CRÍTICAS - SIGA À RISCA:

1. TIPO DE DOCUMENTO - Responda EXATAMENTE com uma destas palavras (sem aspas):
   oficio - Se for um ofício de encaminhamento
   termo - Se for termo de responsabilidade ou compromisso
   identidade - Se for RG, Carteira de Identidade, Cédula de Identidade
   cpf - Se for Cadastro de Pessoa Física, documento com CPF
   certidao - Se for certidão de nascimento, casamento ou óbito
   ensino_medio - Se for histórico/certificado/boletim de Ensino Médio, 2º Grau, Segundo Grau
   historico_graduacao - Se for histórico escolar de faculdade/universidade/graduação/bacharelado
   historico_aproveitamento - Se for histórico de aproveitamento ou transferência entre instituições
   diploma - Se for diploma de graduação ou pós-graduação
   taxa - Se for GRU, taxa, boleto, comprovante de pagamento

DICAS IMPORTANTES:
- HISTÓRICO com "Ensino Médio" ou "2º Grau" → ensino_medio
- HISTÓRICO com "Graduação" ou "Universidade" → historico_graduacao
- Se tem número de CPF (xxx.xxx.xxx-xx) e título "CPF" → cpf
- Documento de identidade com foto → identidade
- Certidões têm carimbos de cartório → certidao

2. RA - Procure o número de matrícula/RA do aluno (4-6 dígitos)
   Também olhe no nome do arquivo (ex: ra03013)

3. NOME - Nome completo da pessoa (aluno/titular do documento)

FORMATO DE RESPOSTA OBRIGATÓRIO (copie exatamente assim):
TIPO: [palavra_exata_da_lista]
RA: [numero ou NÃO IDENTIFICADO]
NOME: [nome completo ou NÃO IDENTIFICADO]

IMPORTANTE: Use APENAS as palavras exatas da lista de tipos. Não invente tipos novos!
"""
            
            response = self.gemini_model.generate_content([prompt, image])
            
            if response and response.text:
                return self.parse_gemini_response(response.text)
            
        except Exception as e:
            print(f"❌ Erro ao analisar com Gemini AI: {e}")
        
        return "", ""
    
    def parse_gemini_response(self, response_text: str) -> Tuple[str, str]:
        """Faz parse da resposta do Gemini para extrair tipo, RA e nome"""
        extracted_text = ""
        document_type = ""
        
        print(f"🤖 Resposta do Gemini:\n{response_text}\n")
        
        lines = response_text.strip().split('\n')
        
        # Lista exata de tipos válidos do E-DIPLOMA
        valid_types = {
            'oficio', 'termo', 'identidade', 'cpf', 'certidao',
            'ensino_medio', 'historico_graduacao', 'historico_aproveitamento',
            'diploma', 'taxa'
        }
        
        for line in lines:
            line = line.strip()
            
            if line.startswith('TIPO:'):
                tipo_raw = line.replace('TIPO:', '').strip().lower()
                # Remove espaços extras, aspas, etc
                tipo_raw = tipo_raw.replace('"', '').replace("'", "").replace('`', '').strip()
                
                # Verifica se é um tipo válido direto
                if tipo_raw in valid_types:
                    document_type = tipo_raw
                    print(f"✅ Tipo identificado diretamente: {document_type}")
                else:
                    # Tenta mapear variações para tipos válidos
                    if 'oficio' in tipo_raw or 'ofício' in tipo_raw:
                        document_type = 'oficio'
                    elif 'termo' in tipo_raw:
                        document_type = 'termo'
                    elif 'identidade' in tipo_raw or 'rg' in tipo_raw or 'carteira' in tipo_raw:
                        document_type = 'identidade'
                    elif 'cpf' in tipo_raw or 'cadastro de pessoa' in tipo_raw:
                        document_type = 'cpf'
                    elif 'certidao' in tipo_raw or 'certidão' in tipo_raw or 'nascimento' in tipo_raw or 'casamento' in tipo_raw:
                        document_type = 'certidao'
                    elif 'ensino_medio' in tipo_raw or 'ensino médio' in tipo_raw or 'ensino medio' in tipo_raw or 'segundo grau' in tipo_raw:
                        document_type = 'ensino_medio'
                    elif 'historico_graduacao' in tipo_raw or 'histórico escolar' in tipo_raw or 'graduacao' in tipo_raw or 'graduação' in tipo_raw:
                        if 'aproveitamento' in tipo_raw or 'transferencia' in tipo_raw or 'transferência' in tipo_raw:
                            document_type = 'historico_aproveitamento'
                        else:
                            document_type = 'historico_graduacao'
                    elif 'historico_aproveitamento' in tipo_raw:
                        document_type = 'historico_aproveitamento'
                    elif 'diploma' in tipo_raw:
                        document_type = 'diploma'
                    elif 'taxa' in tipo_raw or 'gru' in tipo_raw or 'boleto' in tipo_raw:
                        document_type = 'taxa'
                    
                    if document_type:
                        print(f"✅ Tipo mapeado: '{tipo_raw}' → '{document_type}'")
                    else:
                        print(f"⚠️  Tipo não reconhecido: '{tipo_raw}'")
            
            elif line.startswith('RA:'):
                ra = line.replace('RA:', '').strip()
                if ra and ra != "NÃO IDENTIFICADO" and ra.lower() != "não identificado":
                    # Extrai apenas os dígitos
                    ra_digits = re.sub(r'\D', '', ra)
                    if ra_digits:
                        extracted_text += f"RA: {ra_digits}\n"
                        print(f"📝 RA extraído: {ra_digits}")
            
            elif line.startswith('NOME:'):
                nome = line.replace('NOME:', '').strip()
                if nome and nome != "NÃO IDENTIFICADO" and nome.lower() != "não identificado":
                    extracted_text += f"Nome: {nome}\n"
                    print(f"📝 Nome extraído: {nome}")
        
        if not document_type:
            print("❌ Nenhum tipo de documento foi identificado na resposta!")
        
        return extracted_text.lower(), document_type
    
    def load_rules(self):
        """Carrega as regras de renomeação de um arquivo JSON ou cria regras padrão"""
        try:
            if os.path.exists('renaming_rules.json'):
                with open('renaming_rules.json', 'r', encoding='utf-8') as f:
                    self.rules = json.load(f)
            else:
                # Regras padrão para E-DIPLOMA DIGITAL
                self.rules = {
                    "oficio": {
                        "keywords": ["ofício", "oficio", "encaminhamento", "registro"],
                        "pattern": "OFI_{ra}",
                        "extract_name": False,
                        "extract_matricula": True
                    },
                    "termo": {
                        "keywords": ["termo", "responsabilidade", "registro"],
                        "pattern": "TER_{ra}",
                        "extract_name": False,
                        "extract_matricula": True
                    },
                    "identidade": {
                        "keywords": ["rg", "identidade", "registro geral", "documento de identidade", "carteira de identidade"],
                        "pattern": "IDE_{ra}",
                        "extract_name": False,
                        "extract_matricula": True
                    },
                    "cpf": {
                        "keywords": ["cpf", "cadastro de pessoa física", "cadastro de pessoa fisica", "receita federal"],
                        "pattern": "CPF_{ra}",
                        "extract_name": False,
                        "extract_matricula": True
                    },
                    "certidao": {
                        "keywords": ["certidão", "certidao", "nascimento", "casamento", "união", "matrimônio"],
                        "pattern": "CER_{ra}",
                        "extract_name": False,
                        "extract_matricula": True
                    },
                    "ensino_medio": {
                        "keywords": ["ensino médio", "ensino medio", "conclusão", "conclusao", "segundo grau", "certificado"],
                        "pattern": "ENS_{ra}",
                        "extract_name": False,
                        "extract_matricula": True
                    },
                    "historico_graduacao": {
                        "keywords": ["histórico escolar", "historico escolar", "graduação", "graduacao", "bacharelado", "licenciatura"],
                        "pattern": "HES_{ra}",
                        "extract_name": False,
                        "extract_matricula": True
                    },
                    "historico_aproveitamento": {
                        "keywords": ["aproveitamento", "transferência", "transferencia", "outra instituição", "outra instituicao"],
                        "pattern": "HEG_{ra}",
                        "extract_name": False,
                        "extract_matricula": True
                    },
                    "diploma": {
                        "keywords": ["diploma", "graduação", "graduacao", "título", "titulo"],
                        "pattern": "DIP_{ra}",
                        "extract_name": False,
                        "extract_matricula": True
                    },
                    "taxa": {
                        "keywords": ["gru", "taxa", "pagamento", "guia", "boleto"],
                        "pattern": "GRU_{ra}",
                        "extract_name": False,
                        "extract_matricula": True
                    }
                }
                self.save_rules()
        except Exception as e:
            print(f"Erro ao carregar regras: {e}")
    
    def save_rules(self):
        """Salva as regras no arquivo JSON"""
        try:
            with open('renaming_rules.json', 'w', encoding='utf-8') as f:
                json.dump(self.rules, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Erro ao salvar regras: {e}")
    
    def add_rule(self, document_type: str, keywords: List[str], pattern: str, extract_name: bool = True, extract_matricula: bool = True):
        """Adiciona uma nova regra de renomeação"""
        self.rules[document_type] = {
            "keywords": keywords,
            "pattern": pattern,
            "extract_name": extract_name,
            "extract_matricula": extract_matricula
        }
        self.save_rules()
        print(f"Regra adicionada para '{document_type}': {pattern}")
    
    def extract_text_from_pdf_only(self, file_path: str) -> str:
        """Extrai texto de arquivo PDF (sem usar Gemini)"""
        text = ""
        try:
            # Tentativa 1: pdfplumber (melhor para layouts complexos)
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except:
            try:
                # Tentativa 2: PyPDF2 (fallback)
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            except Exception as e:
                print(f"Erro ao extrair texto do PDF {file_path}: {e}")
        
        return text.lower()
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Extrai texto de arquivo DOCX"""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.lower()
        except Exception as e:
            print(f"Erro ao extrair texto do DOCX {file_path}: {e}")
            return ""
    
    def extract_text_from_doc(self, file_path: str) -> str:
        """Extrai texto de arquivo DOC (formato antigo)"""
        try:
            text = docx2txt.process(file_path)
            return text.lower() if text else ""
        except Exception as e:
            print(f"Erro ao extrair texto do DOC {file_path}: {e}")
            return ""
    
    def extract_matricula_from_filename(self, filename: str) -> Optional[str]:
        """Extrai matrícula (RA) do nome do arquivo usando padrões como 'ra03013'"""
        # Padrões para identificar matrículas no nome do arquivo
        # Ordem importante: do mais específico para o menos específico
        patterns = [
            r'ra(\d{6})',  # ra seguido de 6 dígitos (ex: ra123456)
            r'ra(\d{5})',  # ra seguido de 5 dígitos (ex: ra03013)
            r'ra(\d{4})',  # ra seguido de 4 dígitos (ex: ra1234)
            r'mat(\d+)',   # mat seguido de números (ex: mat12345)
            r'matricula[_\-]?(\d+)',  # matricula seguido de números
        ]
        
        filename_lower = filename.lower()
        for pattern in patterns:
            match = re.search(pattern, filename_lower)
            if match:
                return match.group(1)
        
        return None
    
    def extract_matricula_from_text(self, text: str) -> Optional[str]:
        """Extrai matrícula (RA) do conteúdo do texto do documento"""
        # Padrões para identificar RA no texto do documento
        patterns = [
            r'ra[:\s]+(\d{6})',      # RA: 123456 ou RA 123456
            r'ra[:\s]+(\d{5})',      # RA: 12345
            r'ra[:\s]+(\d{4})',      # RA: 1234
            r'r\.?a\.?[:\s]+(\d+)',  # R.A.: 123456 ou RA.: 123456
            r'registro[:\s]+(\d+)',  # Registro: 123456
            r'matrícula[:\s]+(\d+)', # Matrícula: 123456
            r'matricula[:\s]+(\d+)', # Matricula: 123456
        ]
        
        text_lower = text.lower()
        for pattern in patterns:
            match = re.search(pattern, text_lower)
            if match:
                return match.group(1)
        
        return None
    
    def find_ra_by_name(self, text: str, filename: str = "") -> Optional[str]:
        """Busca RA em arquivos já processados com base no nome da pessoa"""
        # Tenta extrair nome tanto do texto quanto do filename
        nome_procurado = self.extract_name_from_text(text, filename)
        
        if not nome_procurado or nome_procurado == "documento":
            return None
        
        print(f"🔍 Buscando RA para: {nome_procurado}")
        
        # Busca em arquivos já processados
        for original_file, file_info in self.processed_files.items():
            nome_arquivo = file_info.get('nome', '')
            ra_arquivo = file_info.get('ra', '')
            
            if nome_arquivo and ra_arquivo:
                # Compara nomes (normalizado)
                if nome_arquivo == nome_procurado:
                    print(f"🔍 RA encontrado por nome exato: {ra_arquivo} (de {original_file})")
                    return ra_arquivo
                
                # Comparação parcial (pelo menos 2 palavras em comum)
                palavras_procurado = set(nome_procurado.split('_'))
                palavras_arquivo = set(nome_arquivo.split('_'))
                palavras_comuns = palavras_procurado & palavras_arquivo
                
                if len(palavras_comuns) >= 2:  # Pelo menos 2 palavras em comum
                    print(f"🔍 RA encontrado por similaridade: {ra_arquivo} (de {original_file})")
                    print(f"   Palavras em comum: {palavras_comuns}")
                    return ra_arquivo
        
        print(f"⚠️  Nenhum RA encontrado para o nome: {nome_procurado}")
        return None
    
    def extract_name_from_text(self, text: str, filename: str = "") -> str:
        """Extrai nome de pessoa do texto ou do nome do arquivo"""
        
        # Primeiro tenta extrair do nome do arquivo (mais confiável)
        if filename:
            # Remove extensão e RA do nome do arquivo
            filename_clean = filename.lower()
            filename_clean = re.sub(r'\.(pdf|docx?|jpg|png)$', '', filename_clean)
            filename_clean = re.sub(r'ra\d+', '', filename_clean)
            filename_clean = re.sub(r'doc\d+', '', filename_clean)
            
            # Se o arquivo tem um nome de pessoa (TERMO, OFÍCIO, etc + nome)
            for keyword in ['termo', 'oficio', 'ofício', 'historico', 'histórico']:
                if keyword in filename_clean:
                    # Extrai o que vem depois da palavra-chave
                    parts = filename_clean.split(keyword)
                    if len(parts) > 1:
                        potential_name = parts[1].strip()
                        # Remove números e caracteres especiais extras
                        potential_name = re.sub(r'\d+', '', potential_name)
                        potential_name = re.sub(r'[_\-\.]+', ' ', potential_name).strip()
                        
                        if len(potential_name.split()) >= 2:  # Pelo menos 2 palavras
                            cleaned = self.clean_name(potential_name)
                            if cleaned and cleaned != "documento":
                                print(f"📝 Nome extraído do arquivo: {potential_name} → {cleaned}")
                                return cleaned
        
        # Se não encontrou no filename, busca no texto
        patterns = [
            r'nome[:\s]+([^\n\r,;]+(?:\s+[^\n\r,;]+)*)',
            r'portador[:\s]+([^\n\r,;]+(?:\s+[^\n\r,;]+)*)',
            r'titular[:\s]+([^\n\r,;]+(?:\s+[^\n\r,;]+)*)',
            r'eu,\s+([^\n\r,;]+(?:\s+[^\n\r,;]+)*)',  # Para TERMOs
            r'sr\.?\s+([^\n\r,;]+(?:\s+[^\n\r,;]+)*)',
            r'sra\.?\s+([^\n\r,;]+(?:\s+[^\n\r,;]+)*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE | re.UNICODE)
            if match:
                name = match.group(1).strip()
                # Remove quebras de linha e espaços extras
                name = ' '.join(name.split())
                # Limita a 6 palavras (para evitar pegar texto demais)
                words = name.split()[:6]
                name = ' '.join(words)
                # Remove palavras comuns que não são nomes
                exclude_words = ['documento', 'carteira', 'registro', 'geral', 'federal', 'receita', 
                               'declaro', 'termo', 'responsabilidade', 'que']
                if not any(word in name.lower() for word in exclude_words) and len(words) >= 2:
                    cleaned = self.clean_name(name)
                    print(f"📝 Nome extraído do texto: {name} → {cleaned}")
                    return cleaned
        
        return "documento"
    
        # Se não encontrar, usa timestamp como fallback
        import time
        return str(int(time.time()))[-6:]  # Últimos 6 dígitos do timestamp
    
    def clean_name(self, name: str) -> str:
        """Limpa o nome removendo caracteres especiais e espaços"""
        # Remove acentos e caracteres especiais
        import unicodedata
        name = unicodedata.normalize('NFD', name)
        name = ''.join(c for c in name if unicodedata.category(c) != 'Mn')
        
        # Remove espaços e caracteres especiais
        name = re.sub(r'[^a-zA-Z\s]', '', name)
        name = re.sub(r'\s+', '_', name.strip())
        
        return name.lower()
    
    def identify_document_type(self, text: str, filename: str = "") -> Optional[str]:
        """Identifica o tipo de documento baseado no conteúdo e nome do arquivo"""
        text_lower = text.lower()
        filename_lower = filename.lower() if filename else ""
        
        # Pontuação para cada tipo de documento
        scores = {}
        
        for doc_type, rule in self.rules.items():
            score = 0
            
            # Pontuação do texto do documento (peso 2)
            for keyword in rule['keywords']:
                if keyword.lower() in text_lower:
                    score += 2
            
            # Pontuação do nome do arquivo (peso 3 - MAIOR que texto para priorizar filename)
            for keyword in rule['keywords']:
                if keyword.lower() in filename_lower:
                    score += 3
            
            if score > 0:
                scores[doc_type] = score
        
        # Retorna o tipo com maior pontuação
        if scores:
            best_type = max(scores, key=scores.get)
            return best_type
        
        return None
    
    def generate_new_filename(self, document_type: str, original_filename: str, extracted_text: str) -> str:
        """Gera o novo nome do arquivo baseado nas regras do E-DIPLOMA DIGITAL"""
        rule = self.rules.get(document_type)
        if not rule:
            return original_filename
        
        pattern = rule['pattern']
        extension = Path(original_filename).suffix
        
        # Extrai RA (primeiro tenta do nome do arquivo, depois do texto, depois por nome da pessoa)
        ra = None
        if rule.get('extract_matricula', False):
            # Tentativa 1: Do nome do arquivo
            ra = self.extract_matricula_from_filename(original_filename)
            
            # Tentativa 2: Do texto do documento
            if not ra:
                ra = self.extract_matricula_from_text(extracted_text)
            
            # Tentativa 3: Busca por nome em arquivos já processados
            if not ra:
                ra = self.find_ra_by_name(extracted_text, original_filename)
            
            if ra:
                # Garante que o RA tem pelo menos 5 dígitos (completa com zeros à esquerda)
                ra = ra.zfill(5)
                pattern = pattern.replace('{ra}', ra)
                pattern = pattern.replace('{matricula}', ra)  # Compatibilidade com padrão antigo
            else:
                # Se não encontrar RA, deixa como "SEMRA"
                print("⚠️  RA não encontrado. Usando 'SEMRA' no nome do arquivo.")
                pattern = pattern.replace('{ra}', 'SEMRA')
                pattern = pattern.replace('{matricula}', 'SEMRA')
        
        # Extrai nome se necessário (mantido para compatibilidade)
        if rule.get('extract_name', False):
            name = self.extract_name_from_text(extracted_text, original_filename)
            pattern = pattern.replace('{nome}', name)
        
        # Substitui outros placeholders se existirem
        if '{tipo}' in pattern:
            pattern = pattern.replace('{tipo}', document_type)
        
        return pattern + extension
    
    def process_file(self, file_path: str) -> Tuple[bool, str]:
        """Processa um arquivo e retorna se foi processado com sucesso e o novo nome"""
        try:
            file_path = Path(file_path)
            extension = file_path.suffix.lower()
            
            # Extrai texto baseado no tipo de arquivo
            text = ""
            gemini_doc_type = None
            
            if extension == '.pdf':
                # Primeiro tenta extrair texto normal
                text = self.extract_text_from_pdf_only(str(file_path))
                
                # Se não conseguiu, tenta análise completa com Gemini
                if not text.strip() and self.gemini_model:
                    print("🤖 Tentando análise completa com Gemini AI...")
                    gemini_text, gemini_doc_type = self.analyze_document_with_gemini(str(file_path))
                    text = gemini_text
                    
            elif extension == '.docx':
                text = self.extract_text_from_docx(str(file_path))
            elif extension == '.doc':
                text = self.extract_text_from_doc(str(file_path))
            else:
                return False, f"Tipo de arquivo não suportado: {extension}"
            
            if not text.strip():
                return False, "Não foi possível extrair texto do arquivo, mesmo com Gemini AI"
            
            # Identifica o tipo de documento (usa resultado do Gemini se disponível)
            # IMPORTANTE: Passa o nome do arquivo para ajudar na identificação
            doc_type = None
            if gemini_doc_type and gemini_doc_type in self.rules:
                doc_type = gemini_doc_type
                print(f"✅ Usando tipo identificado pelo Gemini: {doc_type}")
            else:
                doc_type = self.identify_document_type(text, file_path.name)
                if doc_type:
                    print(f"✅ Tipo identificado por keywords: {doc_type}")
            
            if not doc_type:
                return False, "Tipo de documento não identificado"
            
            # Gera novo nome
            new_filename = self.generate_new_filename(doc_type, file_path.name, text)
            new_path = file_path.parent / new_filename
            
            # Renomeia o arquivo
            if new_path.exists():
                counter = 1
                stem = Path(new_filename).stem
                extension = Path(new_filename).suffix
                while new_path.exists():
                    new_filename = f"{stem}_{counter}{extension}"
                    new_path = file_path.parent / new_filename
                    counter += 1
            
            file_path.rename(new_path)
            
            # Armazena informações do arquivo processado para cross-referencing
            ra = self.extract_matricula_from_filename(file_path.name) or self.extract_matricula_from_text(text)
            nome = self.extract_name_from_text(text, file_path.name)
            
            if ra or nome != "documento":
                self.processed_files[str(file_path.name)] = {
                    'nome': nome,
                    'ra': ra,
                    'novo_nome': new_filename
                }
                print(f"📝 Arquivo armazenado para cross-referencing: RA={ra}, Nome={nome}")
            
            ai_note = " (via Gemini AI)" if gemini_doc_type else ""
            return True, f"Arquivo renomeado para: {new_filename} (tipo: {doc_type}{ai_note})"
            
        except Exception as e:
            return False, f"Erro ao processar arquivo: {e}"
    
    def process_directory(self, directory_path: str):
        """Processa todos os arquivos em um diretório"""
        directory = Path(directory_path)
        
        if not directory.exists():
            print(f"Diretório não encontrado: {directory_path}")
            return
        
        # Busca arquivos PDF e DOC/DOCX
        files = list(directory.glob('*.pdf')) + list(directory.glob('*.doc')) + list(directory.glob('*.docx'))
        
        if not files:
            print("Nenhum arquivo PDF ou DOC encontrado no diretório")
            return
        
        print(f"Processando {len(files)} arquivo(s)...\n")
        
        success_count = 0
        for file_path in files:
            print(f"Processando: {file_path.name}")
            success, message = self.process_file(str(file_path))
            
            if success:
                success_count += 1
                print(f"✓ {message}")
            else:
                print(f"✗ {message}")
            print()
        
        print(f"Processamento concluído. {success_count}/{len(files)} arquivo(s) processado(s) com sucesso.")

def main():
    analyzer = DocumentAnalyzer()
    
    while True:
        print("\n=== ANALISADOR E RENOMEADOR DE DOCUMENTOS ===")
        print("1. Processar arquivos em um diretório")
        print("2. Processar arquivo específico")
        print("3. Adicionar nova regra de renomeação")
        print("4. Ver regras atuais")
        print("5. Sair")
        
        choice = input("\nEscolha uma opção: ").strip()
        
        if choice == '1':
            directory = input("Digite o caminho do diretório: ").strip()
            analyzer.process_directory(directory)
        
        elif choice == '2':
            file_path = input("Digite o caminho do arquivo: ").strip()
            success, message = analyzer.process_file(file_path)
            print(f"{'✓' if success else '✗'} {message}")
        
        elif choice == '3':
            print("\nAdicionar nova regra:")
            doc_type = input("Tipo de documento (ex: identidade): ").strip()
            keywords_str = input("Palavras-chave separadas por vírgula: ").strip()
            keywords = [k.strip() for k in keywords_str.split(',')]
            pattern = input("Padrão de renomeação (use {nome} para nome, {matricula} para matrícula): ").strip()
            
            extract_name = input("Extrair nome do texto? (s/n): ").strip().lower() == 's'
            extract_matricula = input("Extrair matrícula do nome do arquivo? (s/n): ").strip().lower() == 's'
            
            analyzer.add_rule(doc_type, keywords, pattern, extract_name, extract_matricula)
        
        elif choice == '4':
            print("\nRegras atuais:")
            for doc_type, rule in analyzer.rules.items():
                print(f"- {doc_type}: {rule['pattern']}")
                print(f"  Palavras-chave: {', '.join(rule['keywords'])}")
        
        elif choice == '5':
            print("Encerrando programa...")
            break
        
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()