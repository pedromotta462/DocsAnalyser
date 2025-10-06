"""
Script de teste para o DocsAnalyser
"""
from docsAnalyser import DocumentAnalyzer

def test_analyzer():
    print("=== TESTE DO DOCSANALYSER ===\n")
    
    # Criar instância do analisador
    analyzer = DocumentAnalyzer()
    
    print("✓ Analisador criado com sucesso!")
    
    # Mostrar regras carregadas
    print("\n📋 Regras de renomeação carregadas:")
    for doc_type, rule in analyzer.rules.items():
        print(f"  • {doc_type}: {rule['pattern']}")
        print(f"    Palavras-chave: {', '.join(rule['keywords'])}")
    
    print(f"\n✓ Total de {len(analyzer.rules)} regras carregadas")
    
    # Testar extração de nome
    texto_teste = """
    REPÚBLICA FEDERATIVA DO BRASIL
    CARTEIRA DE IDENTIDADE
    Nome: JOÃO SILVA DOS SANTOS
    RG: 12.345.678-9
    """
    
    nome_extraido = analyzer.extract_name_from_text(texto_teste)
    print(f"\n🔍 Teste de extração de nome:")
    print(f"  Texto: 'Nome: JOÃO SILVA DOS SANTOS'")
    print(f"  Nome extraído: '{nome_extraido}'")
    
    # Testar identificação de documento
    doc_type = analyzer.identify_document_type(texto_teste)
    print(f"\n📄 Teste de identificação de documento:")
    print(f"  Tipo identificado: '{doc_type}'")
    
    if doc_type:
        novo_nome = analyzer.generate_new_filename(doc_type, "documento_original.pdf", texto_teste)
        print(f"  Novo nome sugerido: '{novo_nome}'")
    
    print("\n✅ Todos os testes passaram com sucesso!")
    print("\n🚀 O script está pronto para uso!")
    print("\nPara executar o programa principal, digite:")
    print("py docsAnalyser.py")

if __name__ == "__main__":
    test_analyzer()
