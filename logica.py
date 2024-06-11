import pandas as pd  # Importa a biblioteca pandas, utilizada para a leitura de arquivos CSV
import numpy as np  # Importa a biblioteca numpy, utilizada para operações matemáticas e manipulação de arrays
import math  # Importa a biblioteca math, utilizada para operações matemáticas, como logaritmos

class AnalisadorDados:  # Define a classe AnalisadorDados
    def __init__(self):  # Método inicializador da classe
        self.dados = None  # Atributo para armazenar os dados
        self.Hi = []  # Atributo para armazenar os valores de Hmax

    def selecionar_arquivo(self, arquivo_path):  # Método para selecionar e carregar um arquivo de dados
        if arquivo_path.endswith('.txt'):  # Verifica se o arquivo é um .txt
            self.dados = np.loadtxt(arquivo_path, skiprows=1, usecols=range(2, 13))  # Carrega o arquivo .txt ignorando a primeira linha e selecionando as colunas de 2 a 12
        elif arquivo_path.endswith('.csv'):  # Verifica se o arquivo é um .csv
            self.dados = pd.read_csv(arquivo_path, index_col=0)  # Carrega o arquivo .csv utilizando a primeira coluna como índice
        else:  # Se o arquivo não for .txt ou .csv
            return False  # Retorna False
        return True  # Retorna True se o arquivo foi carregado com sucesso

    def calcular_Hmax(self):  # Método para calcular o Hmax
        self.Hi = []  # Reseta a lista de Hmax
        if isinstance(self.dados, np.ndarray):  # Verifica se os dados são um array numpy
            for linha in self.dados:  # Itera sobre cada linha dos dados
                S = np.count_nonzero(linha)  # Conta o número de elementos diferentes de zero na linha
                H_max = math.log2(S) if S > 0 else 0  # Calcula Hmax usando logaritmo base 2 de S, se S for maior que 0
                self.Hi.append(H_max)  # Adiciona o Hmax calculado à lista Hi
        elif isinstance(self.dados, pd.DataFrame):  # Verifica se os dados são um DataFrame do pandas
            for _, linha in self.dados.iterrows():  # Itera sobre cada linha dos dados
                S = np.count_nonzero(linha)  # Conta o número de elementos diferentes de zero na linha
                H_max = math.log2(S) if S > 0 else 0  # Calcula Hmax usando logaritmo base 2 de S, se S for maior que 0
                self.Hi.append(H_max)  # Adiciona o Hmax calculado à lista Hi

    def calcular_F(self):  # Método para calcular a frequência relativa de ocorrência
        status_especies = []  # Lista para armazenar o status das espécies

        if isinstance(self.dados, np.ndarray):  # Verifica se os dados são um array numpy
            freq = np.count_nonzero(self.dados, axis=0)  # Conta o número de valores diferentes de zero em cada coluna
            P = np.shape(self.dados)[0]  # Obtém o número total de amostras (número de linhas)
            ocorre = (freq / P) * 100  # Calcula a frequência relativa de ocorrência

        elif isinstance(self.dados, pd.DataFrame):  # Verifica se os dados são um DataFrame do pandas
            freq = self.dados.astype(bool).sum(axis=0)  # Conta o número de valores diferentes de zero em cada coluna
            P = self.dados.shape[0]  # Obtém o número total de amostras (número de linhas)
            ocorre = (freq / P) * 100  # Calcula a frequência relativa de ocorrência

        else:  # Se os dados não forem nem numpy array nem DataFrame
            return []  # Retorna uma lista vazia

        for ocorrencia in ocorre:  # Itera sobre as frequências de ocorrência
            if ocorrencia >= 50:  # Se a frequência for maior ou igual a 50%
                status_especies.append("Constante")  # Adiciona "Constante" à lista de status
            elif 10 <= ocorrencia < 50:  # Se a frequência estiver entre 10% e 50%
                status_especies.append("Comum")  # Adiciona "Comum" à lista de status
            else:  # Se a frequência for menor que 10%
                status_especies.append("Rara")  # Adiciona "Rara" à lista de status

        return status_especies  # Retorna a lista de status das espécies
    
    def Id(self):  # Método para calcular o índice de diversidade (a ser implementado)
        print("Indice diversidade")  # Imprime "Indice diversidade"

    def Equitabilidade(self):  # Método para calcular a equitabilidade (a ser implementado)
        print("Equitabilidade")  # Imprime "Equitabilidade"
        
    def IndiceSimilaridade(self):  # Método para calcular o índice de similaridade (a ser implementado)
        print("Indice de similaridade")  # Imprime "Indice de similaridade"
        
    def obter_dados(self):  # Método para obter os dados carregados
        return self.dados  # Retorna os dados
