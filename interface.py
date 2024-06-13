import customtkinter as ctk  
from tkinter import filedialog  
from logica import AnalisadorDados  

class Interface:  
    def __init__(self):  
        self.root = None  
        self.analisador = AnalisadorDados()  
        self.root_secundario = None  

    def selecionar_arquivo(self):  
        arquivo_path = filedialog.askopenfilename(
            title="Selecione um arquivo", 
            filetypes=[("Arquivos de Texto", ".txt"), ("Arquivos CSV", ".csv")]
        )  

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
        self.root_secundario.geometry("350x200")  

        botoes = [
            ("Texto", self.mostrar_texto),
            ("Gráfico", self.mostrar_grafico),
            ("Voltar", self.voltar_menu_inicial),
            ("Fechar", self.fechar)
        ]

        for texto, comando in botoes:
            Botao(self.root_secundario, texto, comando)

        self.root_secundario.protocol("Fechar", self.fechar_secundario)  
        self.root_secundario.mainloop()  

    def mostrar_texto_terminal(self, texto):  
        janela_texto = ctk.CTkToplevel()  
        janela_texto.title("Resultados")  
        janela_texto.geometry("400x400")  
        
        texto_janela = ctk.CTkTextbox(janela_texto)  
        texto_janela.pack(expand=True, fill='both')  
        
        texto_janela.insert('1.0', texto)  

    def mostrar_texto(self):  
        self.analisador.calcular_Hmax()  
        status_especies = self.analisador.calcular_F()  
        similaridades = self.analisador.IndiceSimilaridade()
        equitabilidades = self.analisador.Equitabilidade()
        indice_diversidade = self.analisador.calcular_indice_diversidade()
        
        
        resultado = f"Hmax:\n" + \
            "\n".join([f"Ponto {i+1}: {hmax}" for i, hmax in enumerate(self.analisador.HMax)]) + \
            "\n\nStatus das espécies:\n" + \
            "\n".join([f"{self.analisador.rotulos[i]}: {status:.2f}%" for i, status in enumerate(status_especies)]) + \
            "\n\nÍndice de Similaridade:\n" + \
            "\n".join([f"Similaridade linha {i} e linha {j}: {similaridade:.2f}%" for i, j, similaridade in similaridades]) + \
            "\n\nÍndice de Diversidade:\n" + \
            "\n".join([f"Indice de diversidade ponto {i+1}: {indice_diversidade:.3f}" for i, indice_diversidade in enumerate(indice_diversidade)]) + \
            "\n\nEquitabilidade:\n" + \
            "\n".join([f"Equitabilidade ponto {i+1}: {equitabilidade:.3f}" for i, equitabilidade in enumerate(equitabilidades)])

        self.mostrar_texto_terminal(resultado)

    def mostrar_grafico(self):  
        self.analisador.calcular_F()
        self.analisador.calcular_Hmax()
        self.analisador.calcular_indice_diversidade()
        self.analisador.plotar_grafico()

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
        
        self.root.protocol("Fechar", self.fechar)  
        self.root.mainloop()  

class Botao:  
    def __init__(self, root, texto, comando):  
        self.botao = ctk.CTkButton(root, text=texto, command=comando)  
        self.botao.pack(pady=10)  

interface = Interface()
interface.criar_menu_inicial()