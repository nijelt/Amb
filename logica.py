
import pandas as pd
import numpy as np
import math

class AnalisadorDados:
    def __init__(self):
        self.dados = None
        self.Hi = []

    def selecionar_arquivo(self, arquivo_path):
        if arquivo_path.endswith('.txt'):
            self.dados = np.loadtxt(arquivo_path, skiprows=1, usecols=range(2, 13))
        elif arquivo_path.endswith('.csv'):
            self.dados = pd.read_csv(arquivo_path, index_col=0)
        else:
            return False

        return True

    def calcular_Hmax(self):
        self.Hi = []  # Reset Hmax list
        if isinstance(self.dados, np.ndarray):
            for linha in self.dados:
                S = np.count_nonzero(linha)  
                H_max = math.log2(S) if S > 0 else 0  
                self.Hi.append(H_max)
        elif isinstance(self.dados, pd.DataFrame):
            for _, linha in self.dados.iterrows():
                S = np.count_nonzero(linha)  
                H_max = math.log2(S) if S > 0 else 0  
                self.Hi.append(H_max)

    def calcular_F(self):
        status_especies = []

        if isinstance(self.dados, np.ndarray):
            freq = np.count_nonzero(self.dados, axis=0)  # Conta o número de valores diferentes de zero em cada coluna
            P = np.shape(self.dados)[0]  # Número total de amostras (número de linhas)
            ocorre = (freq / P) * 100  # Calcula a frequência relativa de ocorrência

        elif isinstance(self.dados, pd.DataFrame):
            freq = self.dados.astype(bool).sum(axis=0)  # Conta o número de valores diferentes de zero em cada coluna
            P = self.dados.shape[0]  # Número total de amostras (número de linhas)
            ocorre = (freq / P) * 100  # Calcula a frequência relativa de ocorrência

        else:
            return []

        for ocorrencia in ocorre:
            if ocorrencia >= 50:
                status_especies.append("Constante")
            elif 10 <= ocorrencia < 50:
                status_especies.append("Comum")
            else:
                status_especies.append("Rara")

        return status_especies
    
    def Id(self):
        print("Indice diversidade")

    def Equitabilidade(self):
        print("Equitabilidade")
        
    def IndiceSimilaridade(self):
        print("Indice de similaridade")
        
    def obter_dados(self):
        return self.dados
    