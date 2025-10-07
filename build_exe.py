"""
Script para gerar executável do DocsAnalyser usando PyInstaller
"""

import os
import sys
import subprocess
from pathlib import Path

def build_executable():
    """Gera o executável do DocsAnalyser"""
    
    print("="*60)
    print("🔨 CONSTRUINDO EXECUTÁVEL DO DOCSANALYSER")
    print("="*60)
    
    # Verificar se PyInstaller está instalado
    try:
        import PyInstaller
        print("✅ PyInstaller encontrado")
    except ImportError:
        print("❌ PyInstaller não encontrado")
        print("📦 Instalando PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller instalado com sucesso")
    
    # Parâmetros do PyInstaller
    script_name = "app.py"
    app_name = "DocsAnalyser"
    icon_file = "assets/icon.ico" if os.path.exists("assets/icon.ico") else None
    
    # Comando base do PyInstaller
    command = [
        "pyinstaller",
        "--name", app_name,
        "--onefile",  # Gera um único arquivo executável
        "--windowed",  # Sem console (apenas GUI)
        "--clean",  # Limpa cache antes de construir
        
        # Adicionar dados necessários
        "--add-data", f"config{os.pathsep}config",
        "--add-data", f"renaming_rules.json{os.pathsep}.",
        "--add-data", f".env{os.pathsep}." if os.path.exists(".env") else "",
        
        # Hidden imports para garantir que tudo seja incluído
        "--hidden-import", "google.generativeai",
        "--hidden-import", "PIL",
        "--hidden-import", "pdfplumber",
        "--hidden-import", "PyPDF2",
        "--hidden-import", "docx",
        "--hidden-import", "docx2txt",
        
        # Outras opções
        "--noconfirm",  # Sobrescrever sem perguntar
    ]
    
    # Adicionar ícone se existir
    if icon_file and os.path.exists(icon_file):
        command.extend(["--icon", icon_file])
        print(f"✅ Usando ícone: {icon_file}")
    else:
        print("⚠️  Nenhum ícone definido")
    
    # Adicionar script principal
    command.append(script_name)
    
    # Remover elementos vazios
    command = [c for c in command if c]
    
    print("\n📋 Comando PyInstaller:")
    print(" ".join(command))
    print()
    
    # Executar PyInstaller
    try:
        print("🚀 Iniciando build...")
        result = subprocess.run(command, check=True)
        
        if result.returncode == 0:
            print("\n" + "="*60)
            print("✅ EXECUTÁVEL CRIADO COM SUCESSO!")
            print("="*60)
            print(f"\n📁 Localização: dist/{app_name}.exe")
            print(f"📦 Tamanho: ~{get_file_size(f'dist/{app_name}.exe')}")
            print("\n💡 Você pode distribuir apenas o arquivo .exe para seus clientes!")
            print("   Não é necessário instalar Python ou bibliotecas.")
            print("="*60)
        else:
            print("\n❌ Erro ao criar executável")
            
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro durante o build: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)


def get_file_size(filepath):
    """Retorna tamanho do arquivo em formato legível"""
    if not os.path.exists(filepath):
        return "N/A"
    
    size = os.path.getsize(filepath)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"


def create_icon():
    """Cria um ícone básico se não existir"""
    icon_path = Path("assets/icon.ico")
    
    if icon_path.exists():
        print("✅ Ícone já existe")
        return
    
    print("ℹ️  Nenhum ícone encontrado. Criando ícone padrão...")
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Criar imagem 256x256
        img = Image.new('RGB', (256, 256), color='#0078d4')
        draw = ImageDraw.Draw(img)
        
        # Desenhar um "D" simples
        try:
            font = ImageFont.truetype("arial.ttf", 160)
        except:
            font = ImageFont.load_default()
        
        draw.text((64, 32), "D", fill='white', font=font)
        
        # Salvar como ICO
        img.save(icon_path, format='ICO')
        print(f"✅ Ícone criado: {icon_path}")
        
    except ImportError:
        print("⚠️  Pillow não instalado. Executável será criado sem ícone.")
        print("   Instale com: pip install pillow")
    except Exception as e:
        print(f"⚠️  Erro ao criar ícone: {e}")


def prepare_build():
    """Prepara o ambiente para o build"""
    print("\n📦 Preparando ambiente de build...")
    
    # Criar diretório de assets se não existir
    os.makedirs("assets", exist_ok=True)
    
    # Criar ícone se necessário
    create_icon()
    
    # Verificar arquivos essenciais
    essential_files = ["app.py", "config/settings.json", "renaming_rules.json"]
    for file in essential_files:
        if not os.path.exists(file):
            print(f"⚠️  Arquivo essencial não encontrado: {file}")
    
    print("✅ Ambiente preparado\n")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("   DOCSANALYSER - BUILD EXECUTÁVEL")
    print("="*60 + "\n")
    
    # Preparar ambiente
    prepare_build()
    
    # Perguntar confirmação
    response = input("🔨 Deseja iniciar o build do executável? (S/N): ")
    
    if response.lower() in ['s', 'sim', 'y', 'yes']:
        build_executable()
    else:
        print("\n❌ Build cancelado pelo usuário")
