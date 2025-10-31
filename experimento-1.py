import yaml
import time
import random
import numpy as np
import matplotlib.pyplot as plt
import os

#region algoritmos
def count_inversions_naive(arr):
    """
    Calcula o número de inversões em um vetor usando um algoritmo ingênuo (quadrático).
    Complexidade: O(n²).
    """
    n = len(arr)
    inversion_count = 0
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                inversion_count += 1
    return inversion_count

def count_inversions_merge_sort(arr):
    """
    Calcula o número de inversões em um vetor usando um algoritmo de Divisão e Conquista.
    Complexidade: O(n log n).
    """
    _, inversions = _merge_sort_and_count(arr.copy())
    return inversions

def _merge_sort_and_count(arr):
    """Função recursiva que ordena um vetor e conta as inversões."""
    if len(arr) <= 1:
        return arr, 0

    mid = len(arr) // 2
    left_half, left_inversions = _merge_sort_and_count(arr[:mid])
    right_half, right_inversions = _merge_sort_and_count(arr[mid:])
    
    merged_arr, split_inversions = _merge_and_count_split_inv(left_half, right_half)
    
    total_inversions = left_inversions + right_inversions + split_inversions
    return merged_arr, total_inversions

def _merge_and_count_split_inv(left, right):
    """Mescla dois subvetores ordenados e conta as inversões 'split'."""
    merged = []
    inversions = 0
    i, j = 0, 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
            inversions += (len(left) - i)
            
    merged.extend(left[i:])
    merged.extend(right[j:])
    
    return merged, inversions
#endregion

def generate_disordered_ranking(size, disorder_degree):
    """
    Gera um ranking com um grau de desordem específico.
    
    Args:
        size (int): O tamanho do ranking.
        disorder_degree (float): Um valor entre 0.0 (ordenado) e 1.0 (inversamente ordenado).
    
    Returns:
        list: Um vetor de números representando o ranking.
    """
    ranking = list(range(size))
        
    swaps = int((size * (size - 1) / 2) * disorder_degree)
    
    for _ in range(swaps):
        i, j = random.sample(range(size), 2)
        ranking[i], ranking[j] = ranking[j], ranking[i]
        
    return ranking

def plot_results(sizes, times_naive, times_merge, disorder_degree):
    """
    Plota e salva o gráfico de resultados comparando os dois algoritmos.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(sizes, times_naive, 'o-', label=f'Ingênuo (O(n²))')
    plt.plot(sizes, times_merge, 's-', label=f'Divisão e Conquista (O(n log n))')
    
    plt.title(f'Comparação de Desempenho (Grau de Desordem: {disorder_degree})')
    plt.xlabel('Tamanho da Entrada (nº de produtos)')
    plt.ylabel('Tempo Médio de Execução (s)')
    plt.legend()
    plt.grid(True)
    plt.xscale('log')
    plt.yscale('log')
        
    output_dir = "graficos"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    filename = os.path.join(output_dir, f'desempenho_desordem_{str(disorder_degree).replace(".", "_")}.png')
    plt.savefig(filename)
    print(f"Gráfico salvo em: {filename}")
    plt.close()

def run_experiment():
    """
    Executa o experimento completo: gera entradas, mede o tempo e plota os resultados.
    """
    try:
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print("Erro: O arquivo 'config.yaml' não foi encontrado.")
        return
        
    input_sizes_config = config['input_sizes']
    runs_per_size = config['runs_per_size']
    disorder_degrees = config['disorder_degrees']
        
    sizes = np.linspace(
        input_sizes_config['min'], 
        input_sizes_config['max'], 
        input_sizes_config['num_steps'],
        dtype=int
    )

    for degree in disorder_degrees:
        print(f"--- Iniciando experimento para grau de desordem: {degree} ---")
        
        avg_times_naive = []
        avg_times_merge = []

        for n in sizes:
            if n == 0: continue
            
            times_naive = []
            times_merge = []

            print(f"  Testando para n = {n}...")

            for _ in range(runs_per_size):
                ranking = generate_disordered_ranking(n, degree)
                                
                start_time = time.perf_counter()
                inversions_naive = count_inversions_naive(ranking)
                end_time = time.perf_counter()
                times_naive.append(end_time - start_time)
                                
                start_time = time.perf_counter()
                inversions_merge = count_inversions_merge_sort(ranking)
                end_time = time.perf_counter()
                times_merge.append(end_time - start_time)
                                
                if inversions_naive != inversions_merge:
                    print(f"ERRO: Resultados diferentes para n={n}!")
                    print(f"  Ingênuo: {inversions_naive}")
                    print(f"  Merge Sort: {inversions_merge}")
                    print(f"  Ranking: {ranking}")
                    return

            avg_times_naive.append(np.mean(times_naive))
            avg_times_merge.append(np.mean(times_merge))
        
        plot_results(sizes, avg_times_naive, avg_times_merge, degree)

    print("--- Experimento concluído! ---")


if __name__ == '__main__':
    run_experiment()