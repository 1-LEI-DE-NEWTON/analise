# Contagem de Inversões em Rankings de Marketplace

## 📋 Descrição do Projeto

Este projeto implementa e compara experimentalmente dois algoritmos para contar inversões em vetores, simulando um cenário real de marketplace onde é necessário identificar inconsistências entre diferentes ordenações de produtos.

### Problema
Um marketplace precisa medir diferenças entre rankings de produtos baseados em diferentes critérios (avaliação média, histórico de vendas, etc.). Uma **inversão** ocorre quando um par de produtos (i, j) está fora da ordem esperada, ou seja, quando i < j mas ranking[i] > ranking[j].

### Objetivo
Comparar a eficiência de dois algoritmos de contagem de inversões:
- **Algoritmo Ingênuo**: O(n²) - força bruta
- **Algoritmo Divisão e Conquista**: O(n log n) - baseado em merge sort

---

## 🧮 Algoritmos Implementados

### 1. Algoritmo Ingênuo O(n²)

**Funcionamento:**
- Verifica todos os pares possíveis (i, j) onde i < j
- Conta quantos pares satisfazem a condição arr[i] > arr[j]
- Simples de implementar mas ineficiente para grandes entradas

**Complexidade:**
- Tempo: O(n²)
- Espaço: O(1)

**Implementação:** `count_inversions_naive(arr)`

---

### 2. Algoritmo Divisão e Conquista O(n log n)

**Funcionamento:**
- Baseado no algoritmo merge sort modificado
- Divide o vetor recursivamente em duas metades
- Durante o merge, conta inversões entre elementos das duas metades
- Inversões ocorrem quando um elemento da metade direita é menor que um da esquerda

**Passos:**
1. **Divisão**: Divide o vetor ao meio recursivamente
2. **Conquista**: Conta inversões nas submetades (chamadas recursivas)
3. **Combinação**: Conta inversões entre as metades durante o merge

**Complexidade:**
- Tempo: O(n log n)
- Espaço: O(n) - array temporário para merge

**Implementação:** `count_inversions_divide_conquer(arr)`

**Componentes:**
- `merge_sort_and_count()`: Função recursiva principal
- `merge_and_count()`: Realiza o merge e conta inversões cruzadas

---

## 🔬 Metodologia Experimental

### Geração de Entradas
- **Tamanhos**: 100 valores igualmente espaçados entre 100 e 1.000.000
- **Casos de teste**: 10 vetores distintos para cada tamanho
- **Nível de desordem**: Configurável (padrão: 50% de swaps aleatórios)

### Geração de Rankings
A função `generate_random_ranking()` cria vetores com graus controlados de desordem:
- Inicia com vetor ordenado [0, 1, 2, ..., n-1]
- Realiza número controlado de swaps aleatórios
- Parâmetro `disorder_level` controla o grau de desordem (0.0 = ordenado, 1.0 = muito desordenado)

### Medição de Tempo
- Usa `time.perf_counter()` para alta precisão
- Calcula tempo médio sobre 10 execuções para cada tamanho
- Mesmas entradas para ambos os algoritmos (comparação justa)

### Validação
- Verifica se ambos os algoritmos retornam o mesmo número de inversões
- Executado em subconjunto de casos para garantir corretude
- Alerta emitido se houver discrepância

---

## 📊 Estrutura do Código

### Funções Principais

#### Algoritmos de Contagem
- `count_inversions_naive(arr)`: Implementação O(n²)
- `count_inversions_divide_conquer(arr)`: Implementação O(n log n)
- `merge_sort_and_count(arr, temp, left, right)`: Recursão do merge sort
- `merge_and_count(arr, temp, left, mid, right)`: Merge com contagem

#### Geração de Dados
- `generate_random_ranking(n, disorder_level)`: Cria ranking com desordem controlada
- `generate_test_cases(n, num_cases, disorder_level)`: Gera múltiplos casos de teste

#### Experimentação
- `measure_time(algorithm, test_cases)`: Mede tempo médio de execução
- `validate_algorithms(test_cases)`: Valida consistência dos resultados
- `run_experiment(sizes, num_cases, disorder_level, max_size_naive)`: Executa experimento completo

#### Visualização
- `plot_results(results, max_size_naive)`: Gera gráficos comparativos

---

## 📈 Gráficos Gerados

### 1. Comparação de Tempo (Escala Linear)
- Mostra ambos os algoritmos até o limite do algoritmo ingênuo
- Evidencia crescimento quadrático vs. logarítmico

### 2. Comparação de Tempo (Escala Logarítmica)
- Facilita visualização de diferenças em ordens de grandeza
- Ambos os eixos em escala log

### 3. Divisão e Conquista - Escala Completa
- Mostra desempenho do algoritmo eficiente em toda a faixa
- Demonstra escalabilidade para milhões de elementos

### 4. Inversões vs Tamanho da Entrada
- Mostra relação entre tamanho e número de inversões
- Para desordem fixa, inversões crescem quadraticamente

---

## 🚀 Como Executar

### Requisitos
```bash
pip install numpy matplotlib seaborn
```

### Execução no Google Colab
1. Faça upload do notebook
2. Execute todas as células sequencialmente
3. Gráficos serão exibidos automaticamente e salvos como `comparison_results.png`

### Execução Local
```bash
jupyter notebook inversions_experiment.ipynb
```

### Parâmetros Configuráveis

```python
sizes = np.linspace(100, 1000000, 100, dtype=int)  # Tamanhos a testar
num_test_cases = 10                                 # Casos por tamanho
disorder_level = 0.5                                # Nível de desordem (0-1)
max_size_naive = 10000                             # Limite para algoritmo O(n²)
```

---

## 📊 Resultados Esperados

### Desempenho Teórico
- **n = 1.000**: Ingênuo ~1ms, D&C ~0.1ms (10x mais rápido)
- **n = 10.000**: Ingênuo ~100ms, D&C ~1ms (100x mais rápido)
- **n = 100.000**: Ingênuo ~10s (impraticável), D&C ~10ms (1000x mais rápido)
- **n = 1.000.000**: D&C ~100ms (ingênuo levaria ~15 minutos)

### Observações
- O algoritmo ingênuo torna-se impraticável para n > 50.000
- Divisão e conquista escala linearmente com n log n
- Speedup aumenta com o tamanho da entrada
- Para aplicações reais (milhões de produtos), D&C é essencial

---

## 🔍 Análise de Complexidade

### Algoritmo Ingênuo
- **Melhor caso** O(n²): Vetor ordenado (ainda verifica todos os pares)
- **Pior caso** O(n²): Vetor inversamente ordenado
- **Caso médio** O(n²): Sempre quadrático
- **Espaço** O(1): Apenas contadores

### Divisão e Conquista
- **Melhor caso** O(n log n): Vetor ordenado (menos inversões, mesma estrutura)
- **Pior caso** O(n log n): Vetor inversamente ordenado (máximo de inversões)
- **Caso médio** O(n log n): Sempre logarítmico
- **Espaço** O(n): Array temporário + stack de recursão O(log n)

---

## 💡 Aplicações Práticas

### Marketplace
- Detectar mudanças bruscas entre rankings
- Identificar manipulação de avaliações
- Comparar diferentes critérios de ordenação (preço vs. popularidade)

### Outros Domínios
- **Bioinformática**: Comparar sequências genéticas
- **Sistemas de recomendação**: Medir discordância entre modelos
- **Análise de dados**: Detectar outliers em ordenações
- **Competições**: Comparar rankings de diferentes juízes

---

## 📝 Estrutura de Arquivos

```
projeto/
├── inversions_experiment.ipynb   # Notebook principal
├── README.md                      # Este arquivo
├── comparison_results.png         # Gráficos gerados
└── requirements.txt               # Dependências
```

---

## 🎓 Referências

### Conceitos Teóricos
- **Inversões**: Par (i, j) onde i < j mas A[i] > A[j]
- **Merge Sort**: Algoritmo de ordenação por divisão e conquista
- **Complexidade Assintótica**: Análise de crescimento de algoritmos

### Literatura
- Cormen, T. H. et al. "Introduction to Algorithms" (CLRS)
- Sedgewick, R. "Algorithms" 4th Edition
- Kleinberg, J. & Tardos, E. "Algorithm Design"

---

## 👥 Autores

Projeto desenvolvido para a disciplina de Análise de Algoritmos.

---

## 📄 Licença

Este projeto é desenvolvido para fins educacionais.