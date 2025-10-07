"""
Interface Gráfica Principal - DocsAnalyser
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
from pathlib import Path
import sys
import os

# Adiciona o diretório raiz ao path para imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.core.document_analyzer import DocumentAnalyzer
from src.utils.helpers import load_config, save_config, count_files_in_directory, format_file_size


class DocsAnalyserGUI:
    """Interface gráfica principal do DocsAnalyser"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("DocsAnalyser - Analisador de Documentos E-DIPLOMA")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Variáveis
        self.directory_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Pronto")
        self.progress_var = tk.DoubleVar()
        self.processing = False
        self.analyzer = None
        
        # Configurações
        self.config = load_config()
        
        # Configurar estilo
        self.setup_style()
        
        # Criar interface
        self.create_widgets()
        
        # Centralizar janela
        self.center_window()
        
    def setup_style(self):
        """Configura o estilo visual da aplicação"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Cores
        bg_color = "#f0f0f0"
        primary_color = "#0078d4"
        success_color = "#28a745"
        danger_color = "#dc3545"
        
        self.root.configure(bg=bg_color)
        
        # Estilo dos botões
        style.configure('Primary.TButton',
                       background=primary_color,
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       padding=10)
        
        style.configure('Success.TButton',
                       background=success_color,
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       padding=10)
        
        style.configure('Danger.TButton',
                       background=danger_color,
                       foreground='white',
                       font=('Segoe UI', 10, 'bold'),
                       padding=8)
        
    def center_window(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def create_widgets(self):
        """Cria todos os widgets da interface"""
        
        # ========== CABEÇALHO ==========
        header_frame = ttk.Frame(self.root, padding="20")
        header_frame.pack(fill=tk.X)
        
        title_label = ttk.Label(
            header_frame,
            text="📄 DocsAnalyser",
            font=('Segoe UI', 24, 'bold'),
            foreground='#0078d4'
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            header_frame,
            text="Sistema de Análise e Renomeação Automática de Documentos",
            font=('Segoe UI', 10),
            foreground='#666'
        )
        subtitle_label.pack()
        
        # ========== SELEÇÃO DE DIRETÓRIO ==========
        dir_frame = ttk.LabelFrame(self.root, text="📁 Diretório de Documentos", padding="15")
        dir_frame.pack(fill=tk.X, padx=20, pady=10)
        
        dir_entry_frame = ttk.Frame(dir_frame)
        dir_entry_frame.pack(fill=tk.X)
        
        self.dir_entry = ttk.Entry(
            dir_entry_frame,
            textvariable=self.directory_var,
            font=('Segoe UI', 10),
            width=60
        )
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = ttk.Button(
            dir_entry_frame,
            text="🔍 Selecionar",
            command=self.browse_directory,
            style='Primary.TButton'
        )
        browse_btn.pack(side=tk.LEFT)
        
        # Informações do diretório
        self.dir_info_label = ttk.Label(
            dir_frame,
            text="Nenhum diretório selecionado",
            font=('Segoe UI', 9),
            foreground='#666'
        )
        self.dir_info_label.pack(anchor=tk.W, pady=(5, 0))
        
        # ========== OPÇÕES ==========
        options_frame = ttk.LabelFrame(self.root, text="⚙️ Opções de Processamento", padding="15")
        options_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.backup_var = tk.BooleanVar(value=self.config.get('auto_backup', True))
        backup_check = ttk.Checkbutton(
            options_frame,
            text="Criar backup antes de renomear arquivos",
            variable=self.backup_var
        )
        backup_check.pack(anchor=tk.W, pady=2)
        
        self.gemini_var = tk.BooleanVar(value=self.config.get('gemini_enabled', True))
        gemini_check = ttk.Checkbutton(
            options_frame,
            text="Usar Gemini AI para PDFs escaneados (requer chave API)",
            variable=self.gemini_var
        )
        gemini_check.pack(anchor=tk.W, pady=2)
        
        # ========== BOTÕES DE AÇÃO ==========
        actions_frame = ttk.Frame(self.root, padding="10")
        actions_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.process_btn = ttk.Button(
            actions_frame,
            text="▶️ Processar Documentos",
            command=self.start_processing,
            style='Success.TButton',
            width=25
        )
        self.process_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(
            actions_frame,
            text="⏹️ Parar",
            command=self.stop_processing,
            style='Danger.TButton',
            width=15,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(
            actions_frame,
            text="🗑️ Limpar Log",
            command=self.clear_log,
            width=15
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # ========== PROGRESSO ==========
        progress_frame = ttk.Frame(self.root, padding="10")
        progress_frame.pack(fill=tk.X, padx=20, pady=5)
        
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='determinate',
            variable=self.progress_var
        )
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        self.status_label = ttk.Label(
            progress_frame,
            textvariable=self.status_var,
            font=('Segoe UI', 9),
            foreground='#666'
        )
        self.status_label.pack(anchor=tk.W)
        
        # ========== LOG DE PROCESSAMENTO ==========
        log_frame = ttk.LabelFrame(self.root, text="📋 Log de Processamento", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            font=('Consolas', 9),
            wrap=tk.WORD,
            height=15
        )
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Configurar tags para colorir o log
        self.log_text.tag_config('success', foreground='#28a745')
        self.log_text.tag_config('error', foreground='#dc3545')
        self.log_text.tag_config('warning', foreground='#ffc107')
        self.log_text.tag_config('info', foreground='#0078d4')
        
        # ========== RODAPÉ ==========
        footer_frame = ttk.Frame(self.root, padding="10")
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        footer_label = ttk.Label(
            footer_frame,
            text="DocsAnalyser v2.0 | E-DIPLOMA DIGITAL | © 2025",
            font=('Segoe UI', 8),
            foreground='#999'
        )
        footer_label.pack()
        
    def browse_directory(self):
        """Abre diálogo para selecionar diretório"""
        initial_dir = self.config.get('last_directory', '')
        directory = filedialog.askdirectory(
            title="Selecione o diretório com os documentos",
            initialdir=initial_dir
        )
        
        if directory:
            self.directory_var.set(directory)
            self.update_directory_info(directory)
            
            # Salvar último diretório
            self.config['last_directory'] = directory
            save_config(self.config)
            
    def update_directory_info(self, directory):
        """Atualiza informações sobre o diretório selecionado"""
        count = count_files_in_directory(directory)
        
        if count > 0:
            self.dir_info_label.config(
                text=f"✅ {count} arquivo(s) encontrado(s) (.pdf, .docx, .doc)",
                foreground='#28a745'
            )
        else:
            self.dir_info_label.config(
                text="⚠️ Nenhum arquivo suportado encontrado neste diretório",
                foreground='#ffc107'
            )
            
    def log_message(self, message, tag='info'):
        """Adiciona mensagem ao log"""
        self.log_text.insert(tk.END, message + '\n', tag)
        self.log_text.see(tk.END)
        self.root.update_idletasks()
        
    def clear_log(self):
        """Limpa o log de processamento"""
        self.log_text.delete('1.0', tk.END)
        self.log_message("Log limpo.", 'info')
        
    def start_processing(self):
        """Inicia o processamento dos documentos"""
        directory = self.directory_var.get()
        
        if not directory:
            messagebox.showwarning(
                "Atenção",
                "Por favor, selecione um diretório antes de processar."
            )
            return
        
        if not Path(directory).exists():
            messagebox.showerror(
                "Erro",
                "O diretório selecionado não existe."
            )
            return
        
        # Confirmar processamento
        count = count_files_in_directory(directory)
        if count == 0:
            messagebox.showwarning(
                "Atenção",
                "Nenhum arquivo suportado encontrado no diretório."
            )
            return
        
        response = messagebox.askyesno(
            "Confirmar Processamento",
            f"Serão processados {count} arquivo(s).\n\n"
            f"Os arquivos serão renomeados permanentemente.\n"
            f"{'Um backup será criado.' if self.backup_var.get() else 'NENHUM backup será criado.'}\n\n"
            f"Deseja continuar?"
        )
        
        if not response:
            return
        
        # Iniciar processamento em thread separada
        self.processing = True
        self.process_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        self.log_message("="*60, 'info')
        self.log_message(f"🚀 Iniciando processamento...", 'info')
        self.log_message(f"📁 Diretório: {directory}", 'info')
        self.log_message("="*60, 'info')
        
        thread = threading.Thread(target=self.process_documents, args=(directory,))
        thread.daemon = True
        thread.start()
        
    def stop_processing(self):
        """Para o processamento"""
        self.processing = False
        self.log_message("⏹️ Processamento interrompido pelo usuário.", 'warning')
        self.status_var.set("Processamento interrompido")
        self.process_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        
    def process_documents(self, directory):
        """Processa os documentos (executado em thread separada)"""
        try:
            # Inicializar analisador
            self.analyzer = DocumentAnalyzer()
            
            # Coletar arquivos
            files = []
            for ext in ['.pdf', '.docx', '.doc']:
                files.extend(Path(directory).glob(f'*{ext}'))
                files.extend(Path(directory).glob(f'*{ext.upper()}'))
            
            total_files = len(files)
            processed = 0
            successful = 0
            
            for i, file_path in enumerate(files):
                if not self.processing:
                    break
                
                # Atualizar status
                self.status_var.set(f"Processando: {file_path.name}")
                self.progress_var.set((i / total_files) * 100)
                
                self.log_message(f"\n📄 Processando: {file_path.name}", 'info')
                
                # Processar arquivo
                success, message = self.analyzer.process_file(str(file_path))
                
                if success:
                    self.log_message(f"   ✅ {message}", 'success')
                    successful += 1
                else:
                    self.log_message(f"   ❌ {message}", 'error')
                
                processed += 1
            
            # Finalizar
            self.progress_var.set(100)
            self.log_message("\n" + "="*60, 'info')
            self.log_message(
                f"✨ Processamento concluído! {successful}/{processed} arquivo(s) processado(s) com sucesso.",
                'success' if successful == processed else 'warning'
            )
            self.log_message("="*60, 'info')
            
            self.status_var.set(f"Concluído: {successful}/{processed} arquivos processados")
            
            messagebox.showinfo(
                "Processamento Concluído",
                f"Processamento concluído!\n\n"
                f"Total: {processed} arquivo(s)\n"
                f"Sucesso: {successful}\n"
                f"Falhas: {processed - successful}"
            )
            
        except Exception as e:
            self.log_message(f"\n❌ ERRO: {str(e)}", 'error')
            messagebox.showerror("Erro", f"Erro durante o processamento:\n{str(e)}")
        
        finally:
            self.process_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.processing = False


def main():
    """Função principal para executar a GUI"""
    root = tk.Tk()
    app = DocsAnalyserGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
