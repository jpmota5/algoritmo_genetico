import random
import time
import tkinter as tk
from tkinter import messagebox

# Função para calcular o fitness de um indivíduo
def calcular_fitness(individuo):
    valores = {chr(65 + i): individuo[i] for i in range(10)}  # Mapear A-J para os dígitos do indivíduo
    send = valores['S'] * 1000 + valores['E'] * 100 + valores['N'] * 10 + valores['D']
    more = valores['M'] * 1000 + valores['O'] * 100 + valores['R'] * 10 + valores['E']
    money = valores['M'] * 10000 + valores['O'] * 1000 + valores['N'] * 100 + valores['E'] * 10 + valores['Y']
    return abs((send + more) - money)

# Função para gerar a população inicial
def gerar_populacao(tamanho):
    return [random.sample(range(10), 10) for _ in range(tamanho)]

# Função de seleção por roleta
def selecao_roleta(populacao, fitness):
    soma_fitness = sum(1 / (f + 1) for f in fitness)
    probabilidades = [(1 / (f + 1)) / soma_fitness for f in fitness]
    selecionados = random.choices(populacao, weights=probabilidades, k=2)
    return selecionados

# Função de seleção por torneio
def selecao_torneio(populacao, fitness, k=3):
    selecionados = []
    for _ in range(2):
        competidores = random.sample(list(zip(populacao, fitness)), k)
        vencedor = min(competidores, key=lambda x: x[1])
        selecionados.append(vencedor[0])
    return selecionados

# Crossover cíclico
def crossover_ciclico(pai1, pai2):
    filho = [-1] * len(pai1)
    index = 0
    while -1 in filho:
        while filho[index] == -1:
            filho[index] = pai1[index]
            index = pai2.index(pai1[index])
    for i in range(len(filho)):
        if filho[i] == -1:
            filho[i] = pai2[i]
    return filho

# Crossover PMX
def crossover_pmx(pai1, pai2):
    size = len(pai1)
    p1, p2 = [0] * size, [0] * size

    # Mapeamento de índices
    for i in range(size):
        p1[pai1[i]] = i
        p2[pai2[i]] = i

    # Selecionar intervalo
    ponto1, ponto2 = sorted(random.sample(range(size), 2))

    filho = [-1] * size
    filho[ponto1:ponto2] = pai1[ponto1:ponto2]

    for i in range(ponto1, ponto2):
        if pai2[i] not in filho:
            valor = pai2[i]
            while filho[p1[valor]] != -1:
                valor = pai2[p1[valor]]
            filho[p1[valor]] = pai2[i]

    for i in range(size):
        if filho[i] == -1:
            filho[i] = pai2[i]

    return filho

# Mutação: troca de duas posições
def mutacao(individuo):
    i, j = random.sample(range(len(individuo)), 2)
    individuo[i], individuo[j] = individuo[j], individuo[i]

# Reinserção ordenada
def reinsercao_ordenada(populacao, filhos, fitness):
    populacao_completa = populacao + filhos
    fitness_completo = [calcular_fitness(ind) for ind in populacao_completa]
    return [x for _, x in sorted(zip(fitness_completo, populacao_completa))[:len(populacao)]]

# Reinserção com elitismo
def reinsercao_elitismo(populacao, filhos, fitness, elite=0.2):
    num_elite = int(len(populacao) * elite)
    elite_individuos = [x for _, x in sorted(zip(fitness, populacao))[:num_elite]]
    restante = filhos[:len(populacao) - num_elite]
    return elite_individuos + restante

# Algoritmo Genético
def algoritmo_genetico(tamanho_populacao, num_geracoes, taxa_crossover, taxa_mutacao, metodo_selecao, metodo_crossover, metodo_reinsercao):
    populacao = gerar_populacao(tamanho_populacao)
    melhor_individuo = None
    melhor_fitness = float('inf')

    for geracao in range(num_geracoes):
        fitness = [calcular_fitness(ind) for ind in populacao]

        # Atualizar melhor indivíduo
        for ind, fit in zip(populacao, fitness):
            if fit < melhor_fitness:
                melhor_individuo, melhor_fitness = ind, fit

        nova_populacao = []
        while len(nova_populacao) < tamanho_populacao:
            # Seleção
            if metodo_selecao == 'roleta':
                pais = selecao_roleta(populacao, fitness)
            elif metodo_selecao == 'torneio':
                pais = selecao_torneio(populacao, fitness)

            # Crossover
            if random.random() < taxa_crossover:
                if metodo_crossover == 'ciclico':
                    filho = crossover_ciclico(pais[0], pais[1])
                elif metodo_crossover == 'pmx':
                    filho = crossover_pmx(pais[0], pais[1])
            else:
                filho = random.choice(pais)

            # Mutação
            if random.random() < taxa_mutacao:
                mutacao(filho)

            nova_populacao.append(filho)

        # Reinserção
        if metodo_reinsercao == 'ordenada':
            populacao = reinsercao_ordenada(populacao, nova_populacao, fitness)
        elif metodo_reinsercao == 'elitismo':
            populacao = reinsercao_elitismo(populacao, nova_populacao, fitness)

    return melhor_individuo, melhor_fitness

# Interface gráfica para interagir com o algoritmo genético
def criar_interface():
    def executar_algoritmo():
        melhor_individuo, melhor_fitness = algoritmo_genetico(
            tamanho_populacao=100,
            num_geracoes=50,
            taxa_crossover=0.8,
            taxa_mutacao=0.05,
            metodo_selecao='roleta',
            metodo_crossover='ciclico',
            metodo_reinsercao='ordenada'
        )

        valores = {chr(65 + i): melhor_individuo[i] for i in range(10)}
        resultado = f"Melhor indivíduo: {valores}\nFitness: {melhor_fitness}"
        messagebox.showinfo("Resultado", resultado)

    janela = tk.Tk()
    janela.title("Algoritmo Genético - Criptoaritmética")

    label = tk.Label(janela, text="Problema: SEND + MORE = MONEY", font=("Arial", 14))
    label.pack(pady=10)

    botao = tk.Button(janela, text="Executar Algoritmo", command=executar_algoritmo, font=("Arial", 12))
    botao.pack(pady=20)

    janela.mainloop()

# Início da aplicação
if __name__ == "__main__":
    criar_interface()
