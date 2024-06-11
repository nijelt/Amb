import customtkinter as ctk
from tkinter import filedialog
from logica import AnalisadorDados

class Interface:
    def __init__(self):
        self.root = None
        self.analisador = AnalisadorDados()
        self.root_secundario = None

    def selecionar_arquivo(self):
        arquivo_path = filedialog.askopenfilename(title="Selecione um arquivo", filetypes=[("Arquivos de Texto", ".txt"), ("Arquivos CSV", ".csv")])

        if arquivo_path:
            if self.analisador.selecionar_arquivo(arquivo_path):
                self.root.withdraw()
                self.criar_menu_secundario()
            else:
                self.mostrar_texto_terminal("Formato de arquivo não suportado.")
        else:
            self.mostrar_texto_terminal("Nenhum arquivo selecionado.")

    def criar_menu_secundario(self):
        if self.root_secundario:
            self.root_secundario.destroy()
        
        self.root_secundario = ctk.CTk()
        self.root_secundario.title("Menu Secundário")
        self.root_secundario.geometry("300x300")

        botoes = [
            ("Texto", self.mostrar_texto),
            ("Gráfico", self.mostrar_grafico),
            ("Análise Completa", self.analise_completa),
            ("Voltar", self.voltar_menu_inicial),
            ("Fechar", self.fechar)
        ]

        for texto, comando in botoes:
            Botao(self.root_secundario, texto, comando)

        self.root_secundario.protocol("WM_DELETE_WINDOW", self.fechar_secundario)
        self.root_secundario.mainloop()

    def mostrar_texto_terminal(self, texto):
        janela_texto = ctk.CTkToplevel()
        janela_texto.title("Resultados")
        janela_texto.geometry("400x400")
        
        texto_widget = ctk.CTkTextbox(janela_texto)
        texto_widget.pack(expand=True, fill='both')
        
        texto_widget.insert('1.0', texto)

    def mostrar_texto(self):
        self.analisador.calcular_Hmax()
        status_especies = self.analisador.calcular_F()
        resultado = f"Hmax = {self.analisador.Hi}\n\nStatus das espécies:\n" + "\n".join([f"Espécie {i+1}: {status}" for i, status in enumerate(status_especies)])
        self.mostrar_texto_terminal(resultado)

    def mostrar_grafico(self):
        self.mostrar_texto_terminal("Mostrar gráfico")

    def analise_completa(self):
        self.mostrar_texto_terminal("Mostrar análise completa")

    def voltar_menu_inicial(self):
        self.root.deiconify()
        self.root_secundario.withdraw()

    def fechar_secundario(self):
        if self.root_secundario:
            self.root_secundario.destroy()
        self.root.deiconify()

    def fechar(self):
        if self.root_secundario:
            self.root_secundario.destroy()
        if self.root:
            self.root.destroy()

    def criar_menu_inicial(self):
        self.root = ctk.CTk()
        self.root.title("Menu Inicial")
        self.root.geometry("300x200")

        Botao(self.root, "Selecionar Arquivo", self.selecionar_arquivo)
        
        self.root.protocol("WM_DELETE_WINDOW", self.fechar)
        self.root.mainloop()

class Botao:
    def __init__(self, root, texto, comando):
        self.botao = ctk.CTkButton(root, text=texto, command=comando)
        self.botao.pack(pady=10)