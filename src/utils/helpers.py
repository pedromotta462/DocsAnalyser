"""
Funções auxiliares e utilitárias
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any


def get_resource_path(relative_path: str) -> str:
    """
    Obtém o caminho absoluto para um recurso, funciona tanto em dev quanto em executável
    
    Args:
        relative_path: Caminho relativo do recurso
        
    Returns:
        Caminho absoluto do recurso
    """
    try:
        # PyInstaller cria uma pasta temp e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


def load_config(config_file: str = "config/settings.json") -> Dict[str, Any]:
    """
    Carrega configurações de um arquivo JSON
    
    Args:
        config_file: Caminho do arquivo de configuração
        
    Returns:
        Dicionário com as configurações
    """
    config_path = get_resource_path(config_file)
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
    
    # Configurações padrão
    return {
        "theme": "light",
        "auto_backup": True,
        "gemini_enabled": True,
        "last_directory": "",
        "window_size": "800x600"
    }


def save_config(config: Dict[str, Any], config_file: str = "config/settings.json") -> bool:
    """
    Salva configurações em um arquivo JSON
    
    Args:
        config: Dicionário com as configurações
        config_file: Caminho do arquivo de configuração
        
    Returns:
        True se salvou com sucesso, False caso contrário
    """
    config_path = get_resource_path(config_file)
    
    # Cria o diretório se não existir
    os.makedirs(os.path.dirname(config_path), exist_ok=True)
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Erro ao salvar configurações: {e}")
        return False


def format_file_size(size_bytes: int) -> str:
    """
    Formata tamanho de arquivo em formato legível
    
    Args:
        size_bytes: Tamanho em bytes
        
    Returns:
        String formatada (ex: "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def validate_directory(directory: str) -> bool:
    """
    Valida se um diretório existe e é acessível
    
    Args:
        directory: Caminho do diretório
        
    Returns:
        True se válido, False caso contrário
    """
    if not directory:
        return False
    
    path = Path(directory)
    return path.exists() and path.is_dir()


def count_files_in_directory(directory: str, extensions: list = None) -> int:
    """
    Conta arquivos em um diretório
    
    Args:
        directory: Caminho do diretório
        extensions: Lista de extensões para filtrar (ex: ['.pdf', '.docx'])
        
    Returns:
        Número de arquivos
    """
    if not validate_directory(directory):
        return 0
    
    if extensions is None:
        extensions = ['.pdf', '.docx', '.doc']
    
    count = 0
    for ext in extensions:
        count += len(list(Path(directory).glob(f'*{ext}')))
        count += len(list(Path(directory).glob(f'*{ext.upper()}')))
    
    return count
