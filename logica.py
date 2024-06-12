import pandas as pd  # Importa a biblioteca pandas, utilizada para a leitura de arquivos CSV
import numpy as np  # Importa a biblioteca numpy, utilizada para operações matemáticas e manipulação de arrays
import math  # Importa a biblioteca math, utilizada para operações matemáticas, como logaritmos
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

pdfFile = PdfPages("output.pdf") #inicia o pdf

class AnalisadorDados:  # Define a classe AnalisadorDados (como se fosse uma biblioteca)
    def __init__(self):  # Método inicializador da classe
        self.dados = None  # Atributo para armazenar os dados
        
    def selecionar_arquivo(self, arquivo_path):  # Método para selecionar e carregar um arquivo de dados/arquivo_path esta na interface
        if arquivo_path.endswith('.txt'):  # Verifica se o arquivo é um .txt
            self.dados = np.loadtxt(arquivo_path, skiprows=1, usecols=range(2, 13))  # Carrega o arquivo .txt ignorando a primeira linha e selecionando as colunas de 2 a 12
            self.rotulos = np.loadtxt(arquivo_path, dtype=str, max_rows=1, usecols=range(1,12)) #carrega a primeira linha do arquivo como rotulos        
        elif arquivo_path.endswith('.csv'):  # Verifica se o arquivo é um .csv
            self.dados = pd.read_csv(arquivo_path, index_col=0)
            self.dados = self.dados.apply(pd.to_numeric)# Carrega o arquivo .csv utilizando a primeira coluna como índice
            self.rotulos = pd.read_csv(arquivo_path, header=None, usecols=range(1, 12)).iloc[0].values.astype(str)
            #le a primeira linha, ignorando a primeira coluna. iloc[0] significa que ele acha a primeira linha do dataframe
        else:  # Se o arquivo não for .txt ou .csv
            return False  # Retorna False
        return True  # Retorna True se o arquivo foi carregado com sucesso

    def calcular_Hmax(self):  # Método para calcular o Hmax
        self.HMax = []  # Reseta a lista de Hmax
        if isinstance(self.dados, np.ndarray):  # Verifica se os dados são um array numpy
            for linha in self.dados:  # Itera sobre cada linha dos dados
                S = np.count_nonzero(linha)  # Conta o número de elementos diferentes de zero na linha
                H_max = math.log2(S) if S > 0 else 0 # Calcula Hmax usando logaritmo base 2 de S, se S for maior que 0
                H_max = round(H_max,3)
                self.HMax.append(H_max)  # Adiciona o Hmax calculado à lista Hi
        elif isinstance(self.dados, pd.DataFrame):  # Verifica se os dados são um DataFrame do pandas
            for _, linha in self.dados.iterrows():  # Itera sobre cada linha dos dados
                S = np.count_nonzero(linha)  # Conta o número de elementos diferentes de zero na linha
                H_max = math.log2(S) if S > 0 else 0  # Calcula Hmax usando logaritmo base 2 de S, se S for maior que 0
                H_max = round(H_max,3)
                self.HMax.append(H_max)  # Adiciona o Hmax calculado à lista Hi
        return self.HMax
    
    

    def calcular_F(self):  # Método para calcular a frequência relativa de ocorrência
        if isinstance(self.dados, np.ndarray):  # Verifica se os dados são um array numpy
            freq = np.count_nonzero(self.dados, axis=0)  # Conta o número de valores diferentes de zero em cada coluna
            P = np.shape(self.dados)[0]  # Obtém o número total de amostras (número de linhas)
            ocorrencia = (freq / P) * 100  # Calcula a frequência relativa de ocorrência

        elif isinstance(self.dados, pd.DataFrame):  # Verifica se os dados são um DataFrame do pandas
            freq = self.dados.astype(bool).sum(axis=0)  # Conta o número de valores diferentes de zero em cada coluna
            P = self.dados.shape[0]  # Obtém o número total de amostras (número de linhas)
            ocorrencia = (freq / P) * 100  # Calcula a frequência relativa de ocorrência
        else:  # Se os dados não forem nem numpy array nem DataFrame
            return []  # Retorna uma lista vazia

        return ocorrencia  # Retorna a lista de status das espécies
                                 
    def IndiceSimilaridade(self):  # Método para calcular o índice de similaridade de Sørensen
        similaridades = []  # Lista para armazenar os resultados das similaridades
        
        if isinstance(self.dados, pd.DataFrame):  # Converte DataFrame para numpy array se necessário
            matriz_dados = self.dados.to_numpy() 
        else:
            matriz_dados = self.dados

        num_linhas = matriz_dados.shape[0] #calcula o numero de linhas da matriz

        for i in range(num_linhas): #itera até chegar ao fim das linhas
            for j in range(i + 1, num_linhas):
                linha1 = matriz_dados[i]
                linha2 = matriz_dados[j]
                
                c = np.count_nonzero(np.logical_and(linha1 > 0, linha2 > 0))  # Número de espécies comuns
                a = np.count_nonzero(linha1 > 0)  # Número de espécies na comunidade A
                b = np.count_nonzero(linha2 > 0)  # Número de espécies na comunidade B

                if a + b == 0:
                    similaridade = 0.0  # Evita divisão por zero se ambas as linhas forem vazias
                else:
                    similaridade = (2 * c) / (a + b) * 100  # Calcula o índice de Sørensen e multiplica por 100

                similaridades.append((i + 1, j + 1, similaridade))

        return similaridades  
    
    def calcular_indice_diversidade(self): #começo do calculo de diversidade
        indices_diversidade = []
        if isinstance(self.dados, np.ndarray): #teste para verificar se um array numpy
            for linha in self.dados:
                N = np.sum(linha) #soma todos os valores da linha
                if N == 0: #caso haja uma linha composta por zeros o programa ignora ela e não calcula o ni 
                    indices_diversidade.append(0)
                    continue
                soma = 0
                for ni in linha: 
                    if ni > 0: #itera sobre os valores, ignorando os zeros
                        soma += ni * math.log10(ni) 
                H = 3.3219 *  (math.log10(N) - (1 / N) * soma)
                indices_diversidade.append(H)
        elif isinstance(self.dados, pd.DataFrame): #teste para verificar se é um dataframe (csv)
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
        diversidade = self.calcular_indice_diversidade()  # Calcula os índices de diversidade
        Hmaximo = self.calcular_Hmax()  # Calcula o Hmax

        if diversidade is None or Hmaximo is None:
            return []  # Retorna uma lista vazia se um dos valores for None

        equitabilidades = []  # Lista para armazenar os valores de equitabilidade

        if isinstance(self.dados, np.ndarray):
            for indice_diversidade, hmax in zip(diversidade, Hmaximo):
                if hmax != 0:  # Evita a divisão por zero
                    E = indice_diversidade / hmax  # Calcula a equitabilidade
                    equitabilidades.append(E)  # Adiciona o valor de equitabilidade à lista
        elif isinstance(self.dados, pd.DataFrame):  # Se os dados forem um DataFrame do pandas
            for indice_diversidade, hmax in zip(diversidade, Hmaximo):
                if hmax != 0:  # Evita a divisão por zero
                    E = indice_diversidade / hmax  # Calcula a equitabilidade
                    equitabilidades.append(E)  # Adiciona o valor de equitabilidade à lista
        return equitabilidades  # Retorna a lista de equitabilidades
              
   
    def plotar_grafico(self):
        # Calcula os valores
        HMax = self.HMax  # Exemplo de valores de HMax
        equitabilidade = self.Equitabilidade()  # Exemplo de valores de equitabilidade
        indices_diversidade = self.calcular_indice_diversidade()  # Exemplo de valores de índice de diversidade
        status_especies = self.calcular_F()
        rotulo_indices = self.rotulos
        similaridades = self.IndiceSimilaridade()
        
        # Número de pontos
        n_points = len(HMax)

        # Configura os índices das barras
        indices = np.arange(n_points)

        # Largura das barras
        bar_width = 0.25

        # Cria a figura e os eixos
        fig, axs = plt.subplots(1, 3, figsize=(15, 7))

        # Gráfico de Hmax, Equitabilidade e Índice de Diversidade por Ponto
        bars1 = axs[0].bar(indices, HMax, bar_width, label='HMax', color='skyblue', alpha=0.7)
        bars2 = axs[0].bar(indices + bar_width, equitabilidade, bar_width, label='Equitabilidade', color='red', alpha=0.7)
        bars3 = axs[0].bar(indices + 2 * bar_width, indices_diversidade, bar_width, label='Índice de Diversidade', color='purple', alpha=0.7)

        # Títulos e Rótulos do primeiro gráfico
        axs[0].set_title('HMax, Equitabilidade e Índice de Diversidade por Ponto', fontsize=12)
        axs[0].set_xlabel('Pontos', fontsize=10)
        axs[0].set_ylabel('Valores', fontsize=10)
        axs[0].set_xticks(indices + bar_width)
        axs[0].set_xticklabels(range(1, n_points + 1), fontsize=10)
        axs[0].legend(fontsize=10)
        axs[0].grid(True, which='both', linestyle='--', linewidth=0.5, color='grey', alpha=0.7)

        # Gráfico de Frequência de Ocorrência (usando a porcentagem de ocorrência)
        rotulo_indices = np.arange(len(status_especies))
        bars4 = axs[1].bar(rotulo_indices, status_especies, color='lightgreen', alpha=0.7)

        # Títulos e Rótulos do segundo gráfico
        axs[1].set_title('Frequência de ocorrência', fontsize=12)
        axs[1].set_xlabel('Espécies', fontsize=10)
        axs[1].set_ylabel('Frequência de Ocorrência (%)', fontsize=10)
        axs[1].set_xticks(rotulo_indices)
        axs[1].set_xticklabels(self.rotulos, rotation=45, ha='right', fontsize=10)
        axs[1].grid(True, which='both', linestyle='--', linewidth=0.5, color='grey', alpha=0.7)
        
         # Gráfico de Índice de Similaridade
        indices_sim = np.arange(len(similaridades))
        similaridades_valores = [sim[2] for sim in similaridades]
        bars5 = axs[2].bar(indices_sim, similaridades_valores, color='gold', alpha=0.7)

        # Títulos e Rótulos do terceiro gráfico
        axs[2].set_title('Índice de Similaridade', fontsize=12)
        axs[2].set_xlabel('Pares de Linhas', fontsize=10)
        axs[2].set_ylabel('Índice de Similaridade (%)', fontsize=10)
        axs[2].set_xticks(indices_sim)
        axs[2].set_xticklabels(['{}-{}'.format(sim[0], sim[1]) for sim in similaridades], rotation=45, ha='right', fontsize=10)
        axs[2].grid(True, which='both', linestyle='--', linewidth=0.5, color='grey', alpha=0.7)
                
        pdfFile.savefig(fig)
        pdfFile.close()
        # Ajusta layout e exibe o gráfico
        plt.tight_layout()
        plt.show()
        
    def obter_dados(self):  # Método para obter os dados carregados
        return self.dados  # Retorna os dados