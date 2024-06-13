import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

pdfFile = PdfPages("output.pdf") 

class AnalisadorDados: 
    def __init__(self):  
        self.dados = None  
        
    def selecionar_arquivo(self, arquivo_path):  
        if arquivo_path.endswith('.txt'):  
            self.dados = np.loadtxt(arquivo_path, skiprows=1, usecols=range(2, 13))  
            self.rotulos = np.loadtxt(arquivo_path, dtype=str, max_rows=1, usecols=range(1,12)) 
        elif arquivo_path.endswith('.csv'):  
            self.dados = pd.read_csv(arquivo_path, index_col=0)
            self.dados = self.dados.apply(pd.to_numeric)
            self.rotulos = pd.read_csv(arquivo_path, header=None, usecols=range(1, 12)).iloc[0].values.astype(str)
        else:  
            return False  
        return True  

    def calcular_Hmax(self):  
        self.HMax = []  
        if isinstance(self.dados, np.ndarray):  
            for linha in self.dados:  
                S = np.count_nonzero(linha)  
                H_max = math.log2(S) if S > 0 else 0 
                H_max = round(H_max,3)
                self.HMax.append(H_max)  
        elif isinstance(self.dados, pd.DataFrame):  
            for _, linha in self.dados.iterrows():  
                S = np.count_nonzero(linha)  
                H_max = math.log2(S) if S > 0 else 0  
                H_max = round(H_max,3)
                self.HMax.append(H_max)  
        return self.HMax
    
    def calcular_F(self):  
        if isinstance(self.dados, np.ndarray):  
            freq = np.count_nonzero(self.dados, axis=0)  
            P = np.shape(self.dados)[0]  
            ocorrencia = (freq / P) * 100  

        elif isinstance(self.dados, pd.DataFrame):  
            freq = self.dados.astype(bool).sum(axis=0)  
            P = self.dados.shape[0]  
            ocorrencia = (freq / P) * 100  
        else:  
            return []  
        return ocorrencia  
                                 
    def IndiceSimilaridade(self):  
        similaridades = []  
        if isinstance(self.dados, pd.DataFrame):  
            matriz_dados = self.dados.to_numpy() 
        else:
            matriz_dados = self.dados
        num_linhas = matriz_dados.shape[0] 

        for i in range(num_linhas): 
            for j in range(i + 1, num_linhas):
                linha1 = matriz_dados[i]
                linha2 = matriz_dados[j]
                
                c = np.count_nonzero(np.logical_and(linha1 > 0, linha2 > 0))  
                a = np.count_nonzero(linha1 > 0)  
                b = np.count_nonzero(linha2 > 0)  

                if a + b == 0:
                    similaridade = 0.0  
                else:
                    similaridade = (2 * c) / (a + b) * 100  

                similaridades.append((i + 1, j + 1, similaridade))

        return similaridades  
    
    def calcular_indice_diversidade(self): 
        indices_diversidade = []
        if isinstance(self.dados, np.ndarray): 
            for linha in self.dados:
                N = np.sum(linha) 
                if N == 0: 
                    indices_diversidade.append(0)
                    continue
                soma = 0
                for ni in linha: 
                    if ni > 0: 
                        soma += ni * math.log10(ni) 
                H = 3.3219 *  (math.log10(N) - (1 / N) * soma)
                indices_diversidade.append(H)
        elif isinstance(self.dados, pd.DataFrame): 
            for _, linha in self.dados.iterrows(): 
                N = np.sum(linha)
                if N == 0:
                    indices_diversidade.append(0)
                    continue
                soma = 0
                for ni in linha:
                    if ni > 0:
                        soma += ni * math.log10(ni)
                H = (3.3219 * math.log10(N)) - ((1 / N) * soma)
                indices_diversidade.append(H)
        return indices_diversidade
    
    def Equitabilidade(self):
        diversidade = self.calcular_indice_diversidade()  
        Hmaximo = self.calcular_Hmax()  
        if diversidade is None or Hmaximo is None:
            return []  
        equitabilidades = []  
        if isinstance(self.dados, np.ndarray):
            for indice_diversidade, hmax in zip(diversidade, Hmaximo):
                if hmax != 0:  
                    E = indice_diversidade / hmax  
                    equitabilidades.append(E)
                else: 
                    E = 0
                    equitabilidades.append(E)  
        elif isinstance(self.dados, pd.DataFrame):  
            for indice_diversidade, hmax in zip(diversidade, Hmaximo):
                if hmax != 0:  
                    E = indice_diversidade / hmax  
                    equitabilidades.append(E)  
                else:
                    E = 0
                    equitabilidades.append(E)
        return equitabilidades  
              
    def plotar_grafico(self):
        HMax = self.HMax  
        equitabilidade = self.Equitabilidade()  
        indices_diversidade = self.calcular_indice_diversidade()  
        status_especies = self.calcular_F()
        rotulo_indices = self.rotulos
        similaridades = self.IndiceSimilaridade()
        
        n_points = len(HMax)
        indices = np.arange(n_points)
        bar_width = 0.25
        fig, axs = plt.subplots(1, 3, figsize=(15, 7))
        bars1 = axs[0].bar(indices, HMax, bar_width, label='HMax', color='skyblue', alpha=0.7)
        bars2 = axs[0].bar(indices + bar_width, equitabilidade, bar_width, label='Equitabilidade', color='red', alpha=0.7)
        bars3 = axs[0].bar(indices + 2 * bar_width, indices_diversidade, bar_width, label='Índice de Diversidade', color='purple', alpha=0.7)
        axs[0].set_title('HMax, Equitabilidade e Índice de Diversidade por Ponto', fontsize=12)
        axs[0].set_xlabel('Pontos', fontsize=10)
        axs[0].set_ylabel('Valores', fontsize=10)
        axs[0].set_xticks(indices + bar_width)
        axs[0].set_xticklabels(range(1, n_points + 1), fontsize=10)
        axs[0].legend(fontsize=10)
        axs[0].grid(True, which='both', linestyle='--', linewidth=0.5, color='grey', alpha=0.7)
        rotulo_indices = np.arange(len(status_especies))
        bars4 = axs[1].bar(rotulo_indices, status_especies, color='lightgreen', alpha=0.7)
        axs[1].set_title('Frequência de ocorrência', fontsize=12)
        axs[1].set_xlabel('Espécies', fontsize=10)
        axs[1].set_ylabel('Frequência de Ocorrência (%)', fontsize=10)
        axs[1].set_xticks(rotulo_indices)
        axs[1].set_xticklabels(self.rotulos, rotation=45, ha='right', fontsize=7)
        axs[1].grid(True, which='both', linestyle='--', linewidth=0.5, color='grey', alpha=0.7)
        indices_sim = np.arange(len(similaridades))
        similaridades_valores = [sim[2] for sim in similaridades]
        bars5 = axs[2].bar(indices_sim, similaridades_valores, color='gold', alpha=0.7)
        axs[2].set_title('Índice de Similaridade', fontsize=12)
        axs[2].set_xlabel('Pares de Linhas', fontsize=10)
        axs[2].set_ylabel('Índice de Similaridade (%)', fontsize=10)
        axs[2].set_xticks(indices_sim)
        axs[2].set_xticklabels(['{}-{}'.format(sim[0], sim[1]) for sim in similaridades], rotation=45, ha='right', fontsize=10)
        axs[2].grid(True, which='both', linestyle='--', linewidth=0.5, color='grey', alpha=0.7)
        
        pdfFile.savefig(fig)
        pdfFile.close()
        plt.tight_layout()
        plt.show()
        