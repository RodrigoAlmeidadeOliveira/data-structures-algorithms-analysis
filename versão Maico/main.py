import time
import random
import csv
import matplotlib.pyplot as plt
import os

from funcoes_diversas import (
    Node, StaticLinkedList, BinaryTree, AVLTree, HashTable,
    memoria_usada, tempo_cpu, inicialize_hash_table, gerar_registro,
    capturar_metricas, salvar_metricas, gerar_graficos)


"""Quantidades"""
N = [10000, 50000, 100000]

def executa_array_linear(quantidades):
    for n in quantidades:
        print(f"\n\nArray Linear - N = {n}")
        
        # Medição de inserção
        vetor = StaticLinkedList(n)
        def operacao_insercao():
            for _ in range(n):
                vetor.push(Node(gerar_registro()))
        insertion_metrics = capturar_metricas(operacao_insercao)
        
        insertion_metrics["n_registros"] = n
        salvar_metricas('linear_array_insertion.csv', insertion_metrics)
        
        # Medição de busca
        registros_salvos = [vetor.head.data['matricula']]
        def operacao_busca():
            vetor.search(random.choice(registros_salvos))
        search_metrics = capturar_metricas(operacao_busca)
        
        search_metrics["n_registros"] = n
        salvar_metricas('linear_array_search.csv', search_metrics)


def executa_arvore_binaria(quantidades):
    for n in quantidades:
        print(f"\n\nÁrvore Binária - N = {n}")
        
        # Medição de inserção
        arvore = BinaryTree()
        registros = [gerar_registro() for _ in range(n)]
        def operacao_insercao():
            for registro in registros:
                arvore.push(Node(registro))
        insertion_metrics = capturar_metricas(operacao_insercao)

        insertion_metrics["n_registros"] = n
        salvar_metricas('binary_tree_insertion.csv', insertion_metrics)

        # Medição de busca
        search_key = random.choice(registros)['matricula']
        def operacao_busca():
            arvore.search(search_key)
        search_metrics = capturar_metricas(operacao_busca)

        search_metrics["n_registros"] = n
        salvar_metricas('binary_tree_search.csv', search_metrics)


def executa_arvore_avl(quantidades):
    for n in quantidades:
        print(f"\n\nÁrvore AVL - N = {n}")

        # Medição de inserção
        arvore_avl = AVLTree()
        registros = [gerar_registro() for _ in range(n)]
        def operacao_insercao():
            for registro in registros:
                arvore_avl.push(Node(registro))
        insertion_metrics = capturar_metricas(operacao_insercao)

        insertion_metrics["n_registros"] = n
        salvar_metricas('avl_tree_insertion.csv', insertion_metrics)

        # Medição de busca
        search_key = random.choice(registros)['matricula']
        def operacao_busca():
            arvore_avl.search(search_key)
        search_metrics = capturar_metricas(operacao_busca)

        search_metrics["n_registros"] = n
        salvar_metricas('avl_tree_search.csv', search_metrics)


def executa_tabela_hash(quantidades):
    hash_sizes = [1000, 5000, 10000]
    for n in quantidades:
        for size in hash_sizes:
            for hash_fn_id in range(1, 4):
                print(f"\n\nTabela Hash - N = {n}, Tamanho: {size}, Função Hash: {hash_fn_id}")
                
                hash_table = HashTable(size)
                registros = [gerar_registro() for _ in range(n)]
                
                # Medição de inserção
                def operacao_insercao():
                    for registro in registros:
                        hash_table.insert(Node(registro), hash_fn_id)
                insertion_metrics = capturar_metricas(operacao_insercao)
                
                insertion_metrics["n_registros"] = n
                insertion_metrics["tabela_tamanho"] = size
                insertion_metrics["hash_funcao"] = hash_fn_id
                insertion_metrics["colisoes"] = hash_table.colisoes
                insertion_metrics["load_factor"] = n / size
                salvar_metricas('hash_table_insertion.csv', insertion_metrics)

                # Medição de busca
                search_key = random.choice(registros)['matricula']
                def operacao_busca():
                    hash_table.search(search_key, hash_fn_id)
                search_metrics = capturar_metricas(operacao_busca)

                search_metrics["n_registros"] = n
                search_metrics["tabela_tamanho"] = size
                search_metrics["hash_funcao"] = hash_fn_id
                salvar_metricas('hash_table_search.csv', search_metrics)

def ler_dados_csv(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        return list(reader)

def gerar_graficos_comparativos():
    print("\nGerando gráficos de resultados...")
    
    # Leitura dos dados de inserção
    data_insertion_linear = ler_dados_csv('linear_array_insertion.csv')
    data_insertion_bst = ler_dados_csv('binary_tree_insertion.csv')
    data_insertion_avl = ler_dados_csv('avl_tree_insertion.csv')
    data_insertion_hash = ler_dados_csv('hash_table_insertion.csv')

    # Leitura dos dados de busca
    data_search_linear = ler_dados_csv('linear_array_search.csv')
    data_search_bst = ler_dados_csv('binary_tree_search.csv')
    data_search_avl = ler_dados_csv('avl_tree_search.csv')
    data_search_hash = ler_dados_csv('hash_table_search.csv')

    #
    # Geração dos gráficos de INSERÇÃO
    #

    # Gráfico de tempo de inserção
    series_insertion_time = [
        {'x': [int(d['n_registros']) for d in data_insertion_linear], 'y': [float(d['tempo_execucao']) for d in data_insertion_linear], 'label': 'Array Linear'},
        {'x': [int(d['n_registros']) for d in data_insertion_bst], 'y': [float(d['tempo_execucao']) for d in data_insertion_bst], 'label': 'Árvore Binária'},
        {'x': [int(d['n_registros']) for d in data_insertion_avl], 'y': [float(d['tempo_execucao']) for d in data_insertion_avl], 'label': 'Árvore AVL'}
    ]
    # Filtra dados da Tabela Hash (apenas para a primeira função hash e um tamanho de tabela para não poluir o gráfico)
    hash_data_filtered = [d for d in data_insertion_hash if d['tabela_tamanho'] == '10000' and d['hash_funcao'] == '1']
    series_insertion_time.append({'x': [int(d['n_registros']) for d in hash_data_filtered], 'y': [float(d['tempo_execucao']) for d in hash_data_filtered], 'label': 'Tabela Hash (M=10000, f1)'})

    gerar_graficos(
        "Tempo de Inserção - Comparativo",
        "Número de Registros (N)",
        "Tempo (s)",
        series_insertion_time
    )

    # Gráfico de memória de inserção
    series_insertion_memory = [
        {'x': [int(d['n_registros']) for d in data_insertion_linear], 'y': [float(d['memoria_pico_kb']) for d in data_insertion_linear], 'label': 'Array Linear'},
        {'x': [int(d['n_registros']) for d in data_insertion_bst], 'y': [float(d['memoria_pico_kb']) for d in data_insertion_bst], 'label': 'Árvore Binária'},
        {'x': [int(d['n_registros']) for d in data_insertion_avl], 'y': [float(d['memoria_pico_kb']) for d in data_insertion_avl], 'label': 'Árvore AVL'}
    ]
    # Filtra dados da Tabela Hash
    series_insertion_memory.append({'x': [int(d['n_registros']) for d in hash_data_filtered], 'y': [float(d['memoria_pico_kb']) for d in hash_data_filtered], 'label': 'Tabela Hash (M=10000, f1)'})

    gerar_graficos(
        "Memória de Inserção - Comparativo",
        "Número de Registros (N)",
        "Memória de Pico (KB)",
        series_insertion_memory
    )
    
    #
    # Geração dos gráficos de BUSCA
    #

    # Gráfico de tempo de busca
    series_search_time = [
        {'x': [int(d['n_registros']) for d in data_search_linear], 'y': [float(d['tempo_execucao']) for d in data_search_linear], 'label': 'Array Linear'},
        {'x': [int(d['n_registros']) for d in data_search_bst], 'y': [float(d['tempo_execucao']) for d in data_search_bst], 'label': 'Árvore Binária'},
        {'x': [int(d['n_registros']) for d in data_search_avl], 'y': [float(d['tempo_execucao']) for d in data_search_avl], 'label': 'Árvore AVL'}
    ]
    # Filtra dados da Tabela Hash
    hash_search_data_filtered = [d for d in data_search_hash if d['tabela_tamanho'] == '10000' and d['hash_funcao'] == '1']
    series_search_time.append({'x': [int(d['n_registros']) for d in hash_search_data_filtered], 'y': [float(d['tempo_execucao']) for d in hash_search_data_filtered], 'label': 'Tabela Hash (M=10000, f1)'})
    
    gerar_graficos(
        "Tempo de Busca - Comparativo",
        "Número de Registros (N)",
        "Tempo (s)",
        series_search_time
    )

    # Gráfico de memória de busca
    series_search_memory = [
        {'x': [int(d['n_registros']) for d in data_search_linear], 'y': [float(d['memoria_pico_kb']) for d in data_search_linear], 'label': 'Array Linear'},
        {'x': [int(d['n_registros']) for d in data_search_bst], 'y': [float(d['memoria_pico_kb']) for d in data_search_bst], 'label': 'Árvore Binária'},
        {'x': [int(d['n_registros']) for d in data_search_avl], 'y': [float(d['memoria_pico_kb']) for d in data_search_avl], 'label': 'Árvore AVL'}
    ]
    # Filtra dados da Tabela Hash
    series_search_memory.append({'x': [int(d['n_registros']) for d in hash_search_data_filtered], 'y': [float(d['memoria_pico_kb']) for d in hash_search_data_filtered], 'label': 'Tabela Hash (M=10000, f1)'})
    
    gerar_graficos(
        "Memória de Busca - Comparativo",
        "Número de Registros (N)",
        "Memória de Pico (KB)",
        series_search_memory
    )
    
    #
    # Geração de gráficos de colisões e desempenho da Tabela Hash por função e tamanho
    #
    
    # Gráfico de Colisões por Função de Hash (N=100000)
    hash_collisions_data = [d for d in data_insertion_hash if d['n_registros'] == '100000']
    
    series_collisions = []
    for size in [1000, 5000, 10000]:
        x_labels = []
        y_collisions = []
        
        for fn_id in range(1, 4):
            item = next((d for d in hash_collisions_data if d['tabela_tamanho'] == str(size) and d['hash_funcao'] == str(fn_id)), None)
            if item:
                x_labels.append(f"F{fn_id}")
                y_collisions.append(int(item['colisoes']))
        
        series_collisions.append({'x': x_labels, 'y': y_collisions, 'label': f'Tamanho: {size}'})
        
    gerar_graficos(
        "Número de Colisões por Função Hash (N=100k)",
        "Função Hash",
        "Número de Colisões",
        series_collisions
    )

    # Gráfico de Tempo de Inserção por Função de Hash (N=100000)
    series_hash_insert_time = []
    for size in [1000, 5000, 10000]:
        x_labels = []
        y_times = []
        
        for fn_id in range(1, 4):
            item = next((d for d in hash_collisions_data if d['tabela_tamanho'] == str(size) and d['hash_funcao'] == str(fn_id)), None)
            if item:
                x_labels.append(f"F{fn_id}")
                y_times.append(float(item['tempo_execucao']))
        
        series_hash_insert_time.append({'x': x_labels, 'y': y_times, 'label': f'Tamanho: {size}'})
        
    gerar_graficos(
        "Tempo de Inserção por Função Hash (N=100k)",
        "Função Hash",
        "Tempo (s)",
        series_hash_insert_time
    )

def main():
    """Função principal que executa todos os testes."""
    random.seed(time.time())
    
    # Cria os arquivos CSV para garantir que os cabeçalhos existam
    # para a leitura posterior
    for filename in [
        'linear_array_insertion.csv', 'linear_array_search.csv',
        'binary_tree_insertion.csv', 'binary_tree_search.csv',
        'avl_tree_insertion.csv', 'avl_tree_search.csv',
        'hash_table_insertion.csv', 'hash_table_search.csv'
    ]:
        if os.path.exists(filename):
            os.remove(filename)

    # Execução das análises de desempenho para cada estrutura
    executa_array_linear(N)
    executa_arvore_binaria(N)
    executa_arvore_avl(N)
    executa_tabela_hash(N)
    
    # Geração dos gráficos
    gerar_graficos_comparativos()

    print("\nPrograma Finalizado")


if __name__ == "__main__":
    main()