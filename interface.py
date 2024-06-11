import customtkinter as ctk  # Importa a biblioteca customtkinter para criar interfaces gráficas customizáveis
from tkinter import filedialog  # Importa a biblioteca filedialog do tkinter para manipulação de diálogos de arquivos
from logica import AnalisadorDados  # Importa a classe AnalisadorDados do módulo logica
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class Interface:  # Define a classe Interface
    def __init__(self):  # Método inicializador da classe
        self.root = None  # Atributo para a janela principal
        self.analisador = AnalisadorDados()  # Instancia um objeto AnalisadorDados
        self.root_secundario = None  # Atributo para a janela secundária

    def selecionar_arquivo(self):  # Método para abrir um diálogo de seleção de arquivo
        arquivo_path = filedialog.askopenfilename(
            title="Selecione um arquivo", 
            filetypes=[("Arquivos de Texto", ".txt"), ("Arquivos CSV", ".csv")]
        )  # Abre o diálogo para seleção de arquivo

        if arquivo_path:  # Verifica se um arquivo foi selecionado
            if self.analisador.selecionar_arquivo(arquivo_path):  # Tenta carregar o arquivo no analisador de dados
                self.root.withdraw()  # Esconde a janela principal
                self.criar_menu_secundario()  # Cria a janela secundária
            else:
                self.mostrar_texto_terminal("Formato de arquivo não suportado.")  # Mostra uma mensagem de erro
        else:
            self.mostrar_texto_terminal("Nenhum arquivo selecionado.")  # Mostra uma mensagem de erro

    def criar_menu_secundario(self):  # Método para criar a janela secundária
        if self.root_secundario:  # Verifica se já existe uma janela secundária
            self.root_secundario.destroy()  # Destroi a janela secundária existente
        
        self.root_secundario = ctk.CTk()  # Cria uma nova janela secundária
        self.root_secundario.title("Menu Secundário")  # Define o título da janela
        self.root_secundario.geometry("300x300")  # Define o tamanho da janela

        # Lista de botões e seus comandos correspondentes
        botoes = [
            ("Texto", self.mostrar_texto),
            ("Gráfico", self.mostrar_grafico),
            ("Análise Completa", self.analise_completa),
            ("Voltar", self.voltar_menu_inicial),
            ("Fechar", self.fechar)
        ]

        # Cria e adiciona cada botão à janela secundária
        for texto, comando in botoes:
            Botao(self.root_secundario, texto, comando)

        self.root_secundario.protocol("Fechar", self.fechar_secundario)  # Define a ação ao fechar a janela
        self.root_secundario.mainloop()  # Inicia o loop principal da janela secundária

    def mostrar_texto_terminal(self, texto):  # Método para mostrar texto em uma nova janela
        janela_texto = ctk.CTkToplevel()  # Cria uma nova janela toplevel
        janela_texto.title("Resultados")  # Define o título da janela
        janela_texto.geometry("400x400")  # Define o tamanho da janela
        
        texto_widget = ctk.CTkTextbox(janela_texto)  # Cria um widget de texto
        texto_widget.pack(expand=True, fill='both')  # Adiciona o widget à janela
        
        texto_widget.insert('1.0', texto)  # Insere o texto no widget

    def mostrar_texto(self):  # Método para calcular e mostrar Hmax e o status das espécies
        self.analisador.calcular_Hmax()  # Calcula Hmax
        status_especies = self.analisador.calcular_F()  # Calcula o status das espécies
        similaridades = self.analisador.IndiceSimilaridade()
        # Formata o resultado
        resultado = f"Hmax = {self.analisador.Hi}\n\nStatus das espécies:\n" + \
                    "\n".join([f"Espécie {i+1}: {status}" for i, status in enumerate(status_especies)]) + \
                    "\n\nÍndice de Similaridade:\n" + \
                    "\n".join([f"Similaridade entre linha {i+1} e linha {j+1}: {similaridade:.2f}%" for i, j, similaridade in similaridades])
                    
        #resultado = f"Hmax = {self.analisador.Hi}\n\nStatus das espécies:\n" + "\n".join([f"Espécie {i+1}: {status}" for i, status in enumerate(status_especies)])
        self.mostrar_texto_terminal(resultado)  # Mostra o resultado em uma nova janela

    def mostrar_grafico(self):  # Método para mostrar gráfico (a ser implementado)
        self.analisador.calcular_F()
        self.analisador.calcular_Hmax()
        self.analisador.plotar_grafico()
        
    def analise_completa(self):  # Método para mostrar análise completa (a ser implementado)
        self.mostrar_texto_terminal("Mostrar análise completa")  # Mostra uma mensagem indicando que a análise completa será mostrada

    def voltar_menu_inicial(self):  # Método para voltar ao menu inicial
        self.root.deiconify()  # Mostra a janela principal
        self.root_secundario.withdraw()  # Esconde a janela secundária

    def fechar_secundario(self):  # Método para fechar a janela secundária
        if self.root_secundario:  # Verifica se a janela secundária existe
            self.root_secundario.destroy()  # Destroi a janela secundária
        self.root.deiconify()  # Mostra a janela principal

    def fechar(self):  # Método para fechar todas as janelas
        if self.root_secundario:  # Verifica se a janela secundária existe
            self.root_secundario.destroy()  # Destroi a janela secundária
        if self.root:  # Verifica se a janela principal existe
            self.root.destroy()  # Destroi a janela principal

    def criar_menu_inicial(self):  # Método para criar a janela principal
        self.root = ctk.CTk()  # Cria a janela principal
        self.root.title("Menu Inicial")  # Define o título da janela
        self.root.geometry("300x200")  # Define o tamanho da janela

        Botao(self.root, "Selecionar Arquivo", self.selecionar_arquivo)  # Cria o botão de seleção de arquivo
        
        self.root.protocol("Fechar", self.fechar)  # Define a ação ao fechar a janela
        self.root.mainloop()  # Inicia o loop principal da janela

class Botao:  # Classe para criar botões
    def __init__(self, root, texto, comando):  # Método inicializador da classe
        self.botao = ctk.CTkButton(root, text=texto, command=comando)  # Cria um botão com o texto e comando fornecidos
        self.botao.pack(pady=10)  # Adiciona o botão à janela com espaçamento vertical
