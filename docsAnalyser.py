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
            model_name = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
            self.gemini_model = genai.GenerativeModel(model_name)
            print("✅ Gemini AI configurado com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao configurar Gemini AI: {e}")
    
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
            prompt = """
            Analise este documento e extraia as seguintes informações:
            
            1. TIPO DE DOCUMENTO: Identifique se é:
               - RG/Identidade
               - CPF
               - Comprovante de residência
               - Certidão de casamento
               - Contrato
               - Outro tipo
            
            2. NOME DA PESSOA: Extraia o nome completo da pessoa titular do documento
            
            3. TEXTO RELEVANTE: Extraia palavras-chave importantes do documento
            
            Responda no formato:
            TIPO: [tipo do documento]
            NOME: [nome da pessoa]
            TEXTO: [texto relevante extraído]
            
            Se não conseguir identificar alguma informação, responda "NÃO IDENTIFICADO" para aquele campo.
            """
            
            response = self.gemini_model.generate_content([prompt, image])
            
            if response and response.text:
                return self.parse_gemini_response(response.text)
            
        except Exception as e:
            print(f"❌ Erro ao analisar com Gemini AI: {e}")
        
        return "", ""
    
    def parse_gemini_response(self, response_text: str) -> Tuple[str, str]:
        """Faz parse da resposta do Gemini para extrair tipo e nome"""
        extracted_text = ""
        document_type = ""
        
        lines = response_text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith('TIPO:'):
                tipo_raw = line.replace('TIPO:', '').strip()
                # Mapeia tipos do Gemini para nossos tipos
                if any(palavra in tipo_raw.lower() for palavra in ['rg', 'identidade']):
                    document_type = 'identidade'
                elif 'cpf' in tipo_raw.lower():
                    document_type = 'cpf'
                elif any(palavra in tipo_raw.lower() for palavra in ['comprovante', 'residência', 'residencia']):
                    document_type = 'comprovante_residencia'
                elif 'casamento' in tipo_raw.lower():
                    document_type = 'casamento'
                elif 'contrato' in tipo_raw.lower():
                    document_type = 'contrato'
            
            elif line.startswith('NOME:'):
                nome = line.replace('NOME:', '').strip()
                if nome and nome != "NÃO IDENTIFICADO":
                    extracted_text += f"Nome: {nome}\n"
            
            elif line.startswith('TEXTO:'):
                texto = line.replace('TEXTO:', '').strip()
                if texto and texto != "NÃO IDENTIFICADO":
                    extracted_text += f"{texto}\n"
        
        return extracted_text.lower(), document_type
    
    def load_rules(self):
        """Carrega as regras de renomeação de um arquivo JSON ou cria regras padrão"""
        try:
            if os.path.exists('renaming_rules.json'):
                with open('renaming_rules.json', 'r', encoding='utf-8') as f:
                    self.rules = json.load(f)
            else:
                # Regras padrão
                self.rules = {
                    "identidade": {
                        "keywords": ["rg", "identidade", "registro geral", "documento de identidade", "carteira de identidade"],
                        "pattern": "idt_{nome}_{matricula}",
                        "extract_name": True,
                        "extract_matricula": True
                    },
                    "cpf": {
                        "keywords": ["cpf", "cadastro de pessoa física", "receita federal"],
                        "pattern": "cpf_{nome}_{matricula}",
                        "extract_name": True,
                        "extract_matricula": True
                    },
                    "comprovante_residencia": {
                        "keywords": ["comprovante", "residência", "endereço", "conta de luz", "conta de água", "fatura"],
                        "pattern": "comp_residencia_{nome}_{matricula}",
                        "extract_name": True,
                        "extract_matricula": True
                    },
                    "contrato": {
                        "keywords": ["contrato", "acordo", "termo", "prestação de serviços"],
                        "pattern": "contrato_{tipo}_{nome}_{matricula}",
                        "extract_name": True,
                        "extract_matricula": True
                    },
                    "casamento": {
                        "keywords": ["casamento", "certidão de casamento", "união", "matrimônio"],
                        "pattern": "casamento_{nome}_{matricula}",
                        "extract_name": True,
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
    
    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extrai texto de arquivo PDF"""
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
        
        # Se não conseguiu extrair texto (PDF escaneado), tenta com Gemini
        if not text.strip() and self.gemini_model:
            print("📸 PDF parece ser escaneado. Tentando análise com Gemini AI...")
            gemini_text, _ = self.analyze_document_with_gemini(file_path)
            if gemini_text:
                text = gemini_text
                print("✅ Texto extraído com sucesso usando Gemini AI!")
        
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
        """Extrai matrícula do nome do arquivo usando padrões como 'ra03013'"""
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
    
    def extract_name_from_text(self, text: str) -> str:
        """Extrai nome de pessoa do texto usando padrões comuns"""
        # Padrões comuns para identificar nomes
        patterns = [
            r'nome[:\s]+([A-ZÁÊÇÃÕ][a-záêçãõ]+(?:\s+[A-ZÁÊÇÃÕ][a-záêçãõ]+)*)',
            r'portador[:\s]+([A-ZÁÊÇÃÕ][a-záêçãõ]+(?:\s+[A-ZÁÊÇÃÕ][a-záêçãõ]+)*)',
            r'titular[:\s]+([A-ZÁÊÇÃÕ][a-záêçãõ]+(?:\s+[A-ZÁÊÇÃÕ][a-záêçãõ]+)*)',
            r'sr\.?\s*([A-ZÁÊÇÃÕ][a-záêçãõ]+(?:\s+[A-ZÁÊÇÃÕ][a-záêçãõ]+)*)',
            r'sra\.?\s*([A-ZÁÊÇÃÕ][a-záêçãõ]+(?:\s+[A-ZÁÊÇÃÕ][a-záêçãõ]+)*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                # Remove palavras comuns que não são nomes
                exclude_words = ['documento', 'carteira', 'registro', 'geral', 'federal', 'receita']
                if not any(word in name.lower() for word in exclude_words):
                    return self.clean_name(name)
        
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
    
    def identify_document_type(self, text: str) -> Optional[str]:
        """Identifica o tipo de documento baseado no conteúdo"""
        text_lower = text.lower()
        
        # Pontuação para cada tipo de documento
        scores = {}
        
        for doc_type, rule in self.rules.items():
            score = 0
            for keyword in rule['keywords']:
                if keyword.lower() in text_lower:
                    score += 1
            
            if score > 0:
                scores[doc_type] = score
        
        # Retorna o tipo com maior pontuação
        if scores:
            return max(scores, key=scores.get)
        
        return None
    
    def generate_new_filename(self, document_type: str, original_filename: str, extracted_text: str) -> str:
        """Gera o novo nome do arquivo baseado nas regras"""
        rule = self.rules.get(document_type)
        if not rule:
            return original_filename
        
        pattern = rule['pattern']
        extension = Path(original_filename).suffix
        
        # Extrai informações do texto se necessário
        if rule.get('extract_name', False):
            name = self.extract_name_from_text(extracted_text)
            pattern = pattern.replace('{nome}', name)
        
        # Extrai matrícula do nome do arquivo se necessário
        if rule.get('extract_matricula', False):
            matricula = self.extract_matricula_from_filename(original_filename)
            if matricula:
                pattern = pattern.replace('{matricula}', matricula)
            else:
                # Se não encontrar matrícula, remove o placeholder
                pattern = pattern.replace('_{matricula}', '').replace('{matricula}_', '').replace('{matricula}', '')
        
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
                text = self.extract_text_from_pdf(str(file_path))
                # Se ainda não tem texto, tenta análise completa com Gemini
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
            doc_type = gemini_doc_type if gemini_doc_type else self.identify_document_type(text)
            
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