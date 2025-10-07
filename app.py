"""
DocsAnalyser - Entry Point
Ponto de entrada principal da aplicação com interface gráfica
"""

import sys
import os

# Adiciona o diretório atual ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.gui.main_window import main

if __name__ == "__main__":
    main()
