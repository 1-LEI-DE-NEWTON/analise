import numpy as np
import matplotlib.pyplot as plt
import time
from typing import Tuple, List
import seaborn as sns

np.random.seed(100)
sns.set_style("whitegrid")


def count_inversions_naive(arr: np.ndarray) -> int:
    count = 0
    n = len(arr)
    for i in range(n):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                count += 1
    return count


def merge_and_count(arr: np.ndarray, temp: np.ndarray, left: int, mid: int, right: int) -> int:
    i = left
    j = mid + 1
    k = left
    inv_count = 0
    
    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            temp[k] = arr[i]
            i += 1
        else:
            temp[k] = arr[j]
            inv_count += (mid - i + 1)
            j += 1
        k += 1
    
    while i <= mid:
        temp[k] = arr[i]
        i += 1
        k += 1
    
    while j <= right:
        temp[k] = arr[j]
        j += 1
        k += 1
    
    for i in range(left, right + 1):
        arr[i] = temp[i]
    
    return inv_count


def merge_sort_and_count(arr: np.ndarray, temp: np.ndarray, left: int, right: int) -> int:
    inv_count = 0
    if left < right:
        mid = (left + right) // 2
        inv_count += merge_sort_and_count(arr, temp, left, mid)
        inv_count += merge_sort_and_count(arr, temp, mid + 1, right)
        inv_count += merge_and_count(arr, temp, left, mid, right)
    return inv_count


def count_inversions_divide_conquer(arr: np.ndarray) -> int:
    n = len(arr)
    temp = np.zeros(n, dtype=arr.dtype)
    arr_copy = arr.copy()
    return merge_sort_and_count(arr_copy, temp, 0, n - 1)


def generate_random_ranking(n: int, disorder_level: float = 0.5) -> np.ndarray:
    arr = np.arange(n)
    num_swaps = int(n * disorder_level)
    for _ in range(num_swaps):
        i, j = np.random.randint(0, n, 2)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


def generate_test_cases(n: int, num_cases: int = 10, disorder_level: float = 0.5) -> List[np.ndarray]:
    return [generate_random_ranking(n, disorder_level) for _ in range(num_cases)]


def measure_time(algorithm, test_cases: List[np.ndarray]) -> Tuple[float, List[int]]:
    times = []
    results = []
    
    for test_case in test_cases:
        start = time.perf_counter()
        result = algorithm(test_case)
        end = time.perf_counter()
        times.append(end - start)
        results.append(result)
    
    return np.mean(times), results


def validate_algorithms(test_cases: List[np.ndarray]) -> bool:
    for test_case in test_cases:
        result_naive = count_inversions_naive(test_case)
        result_dc = count_inversions_divide_conquer(test_case)
        if result_naive != result_dc:
            return False
    return True


def run_experiment(sizes: np.ndarray, num_cases: int = 10, disorder_level: float = 0.5, max_size_naive: int = 10000) -> dict:
    results = {
        'sizes': [],
        'naive_times': [],
        'dc_times': [],
        'naive_inversions': [],
        'dc_inversions': []
    }
    
    for n in sizes:
        print(f"Processando n={n}...")
        test_cases = generate_test_cases(n, num_cases, disorder_level)
        
        if n <= max_size_naive:
            validation_cases = generate_test_cases(min(n, 1000), min(num_cases, 5), disorder_level)
            is_valid = validate_algorithms(validation_cases)
            if not is_valid:
                print(f"AVISO: Algoritmos retornaram resultados diferentes para n={n}")
        
        if n <= max_size_naive:
            time_naive, inv_naive = measure_time(count_inversions_naive, test_cases)
            results['naive_times'].append(time_naive)
            results['naive_inversions'].append(np.mean(inv_naive))
        else:
            results['naive_times'].append(np.nan)
            results['naive_inversions'].append(np.nan)
        
        time_dc, inv_dc = measure_time(count_inversions_divide_conquer, test_cases)
        results['dc_times'].append(time_dc)
        results['dc_inversions'].append(np.mean(inv_dc))
        results['sizes'].append(n)
    
    return results


def plot_results(results: dict, max_size_naive: int):
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    sizes = np.array(results['sizes'])
    naive_times = np.array(results['naive_times'])
    dc_times = np.array(results['dc_times'])
    
    mask_naive = sizes <= max_size_naive
    
    axes[0, 0].plot(sizes[mask_naive], naive_times[mask_naive], 'o-', label='Algoritmo Ingênuo O(n²)', linewidth=2, markersize=4)
    axes[0, 0].plot(sizes, dc_times, 's-', label='Divisão e Conquista O(n log n)', linewidth=2, markersize=4)
    axes[0, 0].set_xlabel('Número de Produtos (n)', fontsize=12)
    axes[0, 0].set_ylabel('Tempo Médio (segundos)', fontsize=12)
    axes[0, 0].set_title('Comparação de Tempo de Execução', fontsize=14, fontweight='bold')
    axes[0, 0].legend(fontsize=10)
    axes[0, 0].grid(True, alpha=0.3)
    
    axes[0, 1].plot(sizes[mask_naive], naive_times[mask_naive], 'o-', label='Algoritmo Ingênuo O(n²)', linewidth=2, markersize=4)
    axes[0, 1].plot(sizes, dc_times, 's-', label='Divisão e Conquista O(n log n)', linewidth=2, markersize=4)
    axes[0, 1].set_xlabel('Número de Produtos (n)', fontsize=12)
    axes[0, 1].set_ylabel('Tempo Médio (segundos)', fontsize=12)
    axes[0, 1].set_title('Comparação de Tempo (Escala Logarítmica)', fontsize=14, fontweight='bold')
    axes[0, 1].set_xscale('log')
    axes[0, 1].set_yscale('log')
    axes[0, 1].legend(fontsize=10)
    axes[0, 1].grid(True, alpha=0.3, which='both')
    
    axes[1, 0].plot(sizes, dc_times, 's-', color='green', linewidth=2, markersize=4)
    axes[1, 0].set_xlabel('Número de Produtos (n)', fontsize=12)
    axes[1, 0].set_ylabel('Tempo Médio (segundos)', fontsize=12)
    axes[1, 0].set_title('Divisão e Conquista - Escala Completa', fontsize=14, fontweight='bold')
    axes[1, 0].grid(True, alpha=0.3)
    
    axes[1, 1].plot(sizes, results['dc_inversions'], 'o-', color='purple', linewidth=2, markersize=4)
    axes[1, 1].set_xlabel('Número de Produtos (n)', fontsize=12)
    axes[1, 1].set_ylabel('Número Médio de Inversões', fontsize=12)
    axes[1, 1].set_title('Inversões vs Tamanho da Entrada', fontsize=14, fontweight='bold')
    axes[1, 1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('comparison_results.png', dpi=300, bbox_inches='tight')
    plt.show()
    
    print("\n" + "="*60)
    print("RESULTADOS FINAIS")
    print("="*60)
    print(f"Tamanhos testados: {len(sizes)}")
    print(f"Menor tamanho: {sizes[0]}")
    print(f"Maior tamanho: {sizes[-1]}")
    print(f"\nAlgoritmo Ingênuo (testado até n={max_size_naive}):")
    print(f"  Tempo mínimo: {np.nanmin(naive_times):.6f}s")
    print(f"  Tempo máximo: {np.nanmax(naive_times):.6f}s")
    print(f"\nDivisão e Conquista (todos os tamanhos):")
    print(f"  Tempo mínimo: {np.min(dc_times):.6f}s")
    print(f"  Tempo máximo: {np.max(dc_times):.6f}s")
    print(f"\nSpeedup máximo observado: {np.nanmax(naive_times) / dc_times[np.where(mask_naive)[0][-1]]:.2f}x")
    print("="*60)


sizes = np.linspace(100, 1000000, 100, dtype=int)
num_test_cases = 10
disorder_level = 0.5
max_size_naive = 10000

print("="*60)
print("EXPERIMENTO: CONTAGEM DE INVERSÕES EM RANKINGS")
print("="*60)
print(f"Tamanhos de entrada: {len(sizes)} valores de {sizes[0]} a {sizes[-1]}")
print(f"Casos de teste por tamanho: {num_test_cases}")
print(f"Nível de desordem: {disorder_level * 100}%")
print(f"Algoritmo ingênuo executado até n={max_size_naive}")
print("="*60 + "\n")

results = run_experiment(sizes, num_test_cases, disorder_level, max_size_naive)

plot_results(results, max_size_naive)