"""
Teste específico para extração de matrícula do nome do arquivo
"""
from docsAnalyser import DocumentAnalyzer

def test_matricula_extraction():
    print("=== TESTE DE EXTRAÇÃO DE MATRÍCULA ===\n")
    
    analyzer = DocumentAnalyzer()
    
    # Testes de extração de matrícula
    test_filenames = [
        "ra03013 doc00029 Casamento pdf-a.pdf",
        "ra12345 documento identidade.pdf",
        "mat67890 comprovante residencia.docx",
        "RA01234 cpf documento.pdf",
        "matricula_98765 contrato.doc",
        "documento_sem_matricula.pdf",
        "ra1234 teste.pdf",
        "ra123456 outro_teste.pdf"
    ]
    
    print("🔍 Testando extração de matrícula dos nomes de arquivos:")
    for filename in test_filenames:
        matricula = analyzer.extract_matricula_from_filename(filename)
        status = "✅" if matricula else "❌"
        print(f"  {status} '{filename}' → Matrícula: {matricula or 'Não encontrada'}")
    
    print("\n📝 Testando geração de novos nomes com matrícula:")
    
    # Simular texto de documento de casamento
    texto_casamento = """
    CARTÓRIO DE REGISTRO CIVIL
    CERTIDÃO DE CASAMENTO
    Nome: MARIA SILVA SANTOS
    Casamento realizado em...
    """
    
    # Testar com o arquivo de exemplo
    filename_original = "ra03013 doc00029 Casamento pdf-a.pdf"
    doc_type = analyzer.identify_document_type(texto_casamento)
    
    if doc_type:
        novo_nome = analyzer.generate_new_filename(doc_type, filename_original, texto_casamento)
        print(f"  📄 Arquivo original: '{filename_original}'")
        print(f"  🏷️  Tipo identificado: '{doc_type}'")
        print(f"  📝 Novo nome: '{novo_nome}'")
    else:
        print(f"  ❌ Tipo de documento não identificado para: '{filename_original}'")
    
    print("\n📋 Regras atualizadas com suporte a matrícula:")
    for doc_type, rule in analyzer.rules.items():
        extract_mat = "Sim" if rule.get('extract_matricula', False) else "Não"
        print(f"  • {doc_type}: {rule['pattern']}")
        print(f"    Extrai matrícula: {extract_mat}")
    
    print("\n✅ Teste de extração de matrícula concluído!")

if __name__ == "__main__":
    test_matricula_extraction()
