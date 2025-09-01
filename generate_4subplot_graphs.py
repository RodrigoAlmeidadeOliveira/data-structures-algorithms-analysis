import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Carregar dados
df_raw = pd.read_csv('/Users/rodrigoalmeidadeoliveira/Documents/Doutorado/Disciplinas/FundamentosAlgoritmos/DataStructuresAndAlgorithms/Tarefas/resultados_bst.csv')
df_summary = pd.read_csv('/Users/rodrigoalmeidadeoliveira/Documents/Doutorado/Disciplinas/FundamentosAlgoritmos/DataStructuresAndAlgorithms/Tarefas/resumo_metricas_bst.csv')

# Converter memoria para MB e calcular porcentagem
df_raw['memoria_mb'] = df_raw['memoria_pico'] / (1024 * 1024)

# Preparar dados para os gráficos
volumes = [10000, 50000, 100000]
data_sizes = [v/1000 for v in volumes]  # Converter para milhares

# Dados para BST sem balanceamento e com balanceamento
def get_means_by_type(metric, tipo):
    means = []
    for volume in volumes:
        subset = df_raw[(df_raw['tipo_bst'] == tipo) & (df_raw['volume'] == volume)]
        means.append(subset[metric].mean())
    return means

# Função para criar gráfico no padrão especificado
def create_benchmark_graph(test_type=0, structure_name="BST"):
    """
    test_type: 0 para inserção, 1 para busca
    """
    
    # Configurar figura com 4 subplots
    plt.figure(figsize=(10, 6))
    
    # Subplot 1: Tempo (ms)
    plt.subplot(4, 1, 1)
    if test_type == 0:
        # Tempo de inserção
        mean_times_sem = [t * 1000 for t in get_means_by_type('tempo_insercao', 'sem_balanceamento')]  # Converter para ms
        mean_times_com = [t * 1000 for t in get_means_by_type('tempo_insercao', 'com_balanceamento')]
        plt.title(f"Benchmark {structure_name} - Inserção")
    else:
        # Tempo de busca
        mean_times_sem = [t * 1000 for t in get_means_by_type('tempo_busca', 'sem_balanceamento')]  # Converter para ms
        mean_times_com = [t * 1000 for t in get_means_by_type('tempo_busca', 'com_balanceamento')]
        plt.title(f"Benchmark {structure_name} - Busca")
    
    plt.plot(data_sizes, mean_times_sem, marker="o", color="red", label="Sem Balanceamento")
    plt.plot(data_sizes, mean_times_com, marker="o", color="blue", label="Com Balanceamento")
    plt.ylabel("Tempo (ms)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Subplot 2: Memória (%)
    plt.subplot(4, 1, 2)
    mean_mems_sem = get_means_by_type('memoria_mb', 'sem_balanceamento')
    mean_mems_com = get_means_by_type('memoria_mb', 'com_balanceamento')
    
    # Calcular porcentagem relativa ao máximo
    max_mem = max(max(mean_mems_sem), max(mean_mems_com))
    mean_mems_sem_pct = [(m/max_mem) * 100 for m in mean_mems_sem]
    mean_mems_com_pct = [(m/max_mem) * 100 for m in mean_mems_com]
    
    plt.plot(data_sizes, mean_mems_sem_pct, marker="o", color="blue")
    plt.plot(data_sizes, mean_mems_com_pct, marker="o", color="green")
    plt.ylabel("Memória (%)")
    plt.grid(True, alpha=0.3)
    
    # Subplot 3: CPU (%)
    plt.subplot(4, 1, 3)
    mean_cpus_sem = get_means_by_type('cpu_percent', 'sem_balanceamento')
    mean_cpus_com = get_means_by_type('cpu_percent', 'com_balanceamento')
    
    plt.plot(data_sizes, mean_cpus_sem, marker="o", color="green")
    plt.plot(data_sizes, mean_cpus_com, marker="o", color="orange")
    plt.xlabel("Tamanho do Array")
    plt.ylabel("CPU (%)")
    plt.grid(True, alpha=0.3)
    
    # Subplot 4: Iterações
    plt.subplot(4, 1, 4)
    if test_type == 0:
        mean_iters_sem = get_means_by_type('iteracoes_insercao', 'sem_balanceamento')
        mean_iters_com = get_means_by_type('iteracoes_insercao', 'com_balanceamento')
    else:
        mean_iters_sem = get_means_by_type('iteracoes_busca', 'sem_balanceamento')
        mean_iters_com = get_means_by_type('iteracoes_busca', 'com_balanceamento')
    
    plt.plot(data_sizes, mean_iters_sem, marker="o", color="purple")
    plt.plot(data_sizes, mean_iters_com, marker="o", color="brown")
    plt.xlabel("Tamanho do Array")
    plt.ylabel("Iterações")
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if test_type == 0:
        plt.savefig('/Users/rodrigoalmeidadeoliveira/Documents/Doutorado/Disciplinas/FundamentosAlgoritmos/DataStructuresAndAlgorithms/Tarefas/benchmark_bst_insercao.png', 
                    dpi=300, bbox_inches='tight')
    else:
        plt.savefig('/Users/rodrigoalmeidadeoliveira/Documents/Doutorado/Disciplinas/FundamentosAlgoritmos/DataStructuresAndAlgorithms/Tarefas/benchmark_bst_busca.png', 
                    dpi=300, bbox_inches='tight')
    plt.close()

# Gerar gráficos para inserção e busca
print("Gerando gráfico de benchmark - Inserção...")
create_benchmark_graph(test_type=0, structure_name="BST")

print("Gerando gráfico de benchmark - Busca...")
create_benchmark_graph(test_type=1, structure_name="BST")

# Gráfico comparativo adicional - BST vs Array Linear (simulado)
def create_comparison_graph():
    plt.figure(figsize=(12, 8))
    
    # Simular dados de Array Linear para comparação
    # Array Linear: O(1) inserção, O(n) busca
    array_insert_times = [0.01, 0.05, 0.1]  # Tempo constante
    array_search_times = [5, 25, 50]  # Tempo linear
    
    bst_insert_times_sem = get_means_by_type('tempo_insercao', 'sem_balanceamento')
    bst_insert_times_com = get_means_by_type('tempo_insercao', 'com_balanceamento')
    bst_search_times_sem = get_means_by_type('tempo_busca', 'sem_balanceamento')
    bst_search_times_com = get_means_by_type('tempo_busca', 'com_balanceamento')
    
    # Subplot 1: Comparação de Inserção
    plt.subplot(2, 2, 1)
    plt.plot(data_sizes, array_insert_times, marker="s", color="orange", linewidth=2, label="Array Linear")
    plt.plot(data_sizes, bst_insert_times_sem, marker="o", color="red", linewidth=2, label="BST Sem Balanc.")
    plt.plot(data_sizes, bst_insert_times_com, marker="^", color="blue", linewidth=2, label="BST Com Balanc.")
    plt.title("Tempo de Inserção")
    plt.ylabel("Tempo (s)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    
    # Subplot 2: Comparação de Busca
    plt.subplot(2, 2, 2)
    plt.plot(data_sizes, array_search_times, marker="s", color="orange", linewidth=2, label="Array Linear")
    plt.plot(data_sizes, bst_search_times_sem, marker="o", color="red", linewidth=2, label="BST Sem Balanc.")
    plt.plot(data_sizes, bst_search_times_com, marker="^", color="blue", linewidth=2, label="BST Com Balanc.")
    plt.title("Tempo de Busca")
    plt.ylabel("Tempo (s)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    
    # Subplot 3: Altura das Estruturas
    plt.subplot(2, 2, 3)
    array_height = [1, 1, 1]  # Array sempre altura 1
    bst_height_sem = get_means_by_type('altura_arvore', 'sem_balanceamento')
    bst_height_com = get_means_by_type('altura_arvore', 'com_balanceamento')
    
    plt.plot(data_sizes, array_height, marker="s", color="orange", linewidth=2, label="Array Linear")
    plt.plot(data_sizes, bst_height_sem, marker="o", color="red", linewidth=2, label="BST Sem Balanc.")
    plt.plot(data_sizes, bst_height_com, marker="^", color="blue", linewidth=2, label="BST Com Balanc.")
    plt.title("Altura da Estrutura")
    plt.xlabel("Tamanho (milhares)")
    plt.ylabel("Altura")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Subplot 4: Complexidade Teórica
    plt.subplot(2, 2, 4)
    theoretical_log = [np.log2(v) for v in volumes]
    theoretical_linear = data_sizes
    theoretical_constant = [1, 1, 1]
    
    plt.plot(data_sizes, theoretical_constant, '--', color="orange", linewidth=2, label="O(1)")
    plt.plot(data_sizes, theoretical_log, '--', color="green", linewidth=2, label="O(log n)")
    plt.plot(data_sizes, theoretical_linear, '--', color="red", linewidth=2, label="O(n)")
    plt.title("Complexidade Teórica")
    plt.xlabel("Tamanho (milhares)")
    plt.ylabel("Operações")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.yscale('log')
    
    plt.tight_layout()
    plt.savefig('/Users/rodrigoalmeidadeoliveira/Documents/Doutorado/Disciplinas/FundamentosAlgoritmos/DataStructuresAndAlgorithms/Tarefas/comparacao_estruturas.png', 
                dpi=300, bbox_inches='tight')
    plt.close()

print("Gerando gráfico de comparação entre estruturas...")
create_comparison_graph()

print("\nGráficos gerados com sucesso!")
print("Arquivos criados:")
print("1. benchmark_bst_insercao.png - Benchmark BST inserção (4 subplots)")
print("2. benchmark_bst_busca.png - Benchmark BST busca (4 subplots)")
print("3. comparacao_estruturas.png - Comparação Array vs BST")