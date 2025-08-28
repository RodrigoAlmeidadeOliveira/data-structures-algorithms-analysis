#!/usr/bin/env python3
"""
Análise Comparativa de Estruturas de Dados
PUCPR - Fundamentos de Algoritmos e Estrutura de Dados
Autor: Sistema de Análise de Estruturas de Dados
"""

import sys
import json
import pandas as pd
from tabulate import tabulate
from experiments import ExperimentRunner
from analysis import ResultAnalyzer


def print_header():
    print("=" * 80)
    print(" ANÁLISE COMPARATIVA DE ESTRUTURAS DE DADOS ".center(80))
    print("=" * 80)
    print("\nEstruturas avaliadas:")
    print("  1. Array Linear")
    print("  2. Árvore de Busca Binária (BST)")
    print("  3. Árvore AVL (BST Balanceada)")
    print("  4. Tabela Hash (3 funções, múltiplos M)")
    print("\nTamanhos de dados: 10.000, 50.000, 100.000 registros")
    print("Rodadas por experimento: 5")
    print("-" * 80)


def print_summary_table(results):
    print("\n" + "=" * 80)
    print(" RESUMO DOS RESULTADOS ".center(80))
    print("=" * 80)
    
    # Organiza dados para tabela
    summary_data = []
    
    for result in results:
        stats = result.get_statistics()
        row = {
            'Estrutura': result.structure_name,
            'N': result.data_size,
            'Operação': result.operation,
            'Tempo Médio (s)': f"{stats.get('mean_time', 0):.6f}",
            'Desvio Tempo': f"{stats.get('std_time', 0):.6f}",
            'Iterações Médias': f"{stats.get('mean_iterations', 0):.1f}"
        }
        
        # Adiciona parâmetros específicos
        if result.structure_name == "HashTable":
            row['Parâmetros'] = f"M={result.parameters['M']}, {result.parameters['hash_function']}"
        elif result.structure_name in ["BST", "AVL"]:
            row['Parâmetros'] = f"balanced={result.parameters.get('balanced', False)}"
        else:
            row['Parâmetros'] = "-"
        
        summary_data.append(row)
    
    # Converte para DataFrame para melhor formatação
    df = pd.DataFrame(summary_data)
    
    # Imprime tabela por operação
    for operation in ['insert', 'search']:
        print(f"\n### Operação: {operation.upper()} ###")
        op_df = df[df['Operação'] == operation]
        
        if not op_df.empty:
            print(tabulate(op_df, headers='keys', tablefmt='grid', showindex=False))


def print_hash_analysis(results):
    print("\n" + "=" * 80)
    print(" ANÁLISE ESPECÍFICA - TABELA HASH ".center(80))
    print("=" * 80)
    
    hash_results = [r for r in results if r.structure_name == "HashTable" and r.operation == "insert"]
    
    if not hash_results:
        return
    
    analysis_data = []
    
    for result in hash_results:
        metrics = result.metrics
        analysis_data.append({
            'N': result.data_size,
            'M': result.parameters['M'],
            'Função Hash': result.parameters['hash_function'],
            'Load Factor': f"{metrics.get('avg_load_factor', 0):.3f}",
            'Taxa Colisão': f"{metrics.get('avg_collision_rate', 0):.3f}",
            'Comp. Médio Cadeia': f"{metrics.get('avg_avg_chain_length', 0):.2f}",
            'Comp. Máx. Cadeia': f"{metrics.get('avg_max_chain_length', 0):.0f}"
        })
    
    df = pd.DataFrame(analysis_data)
    print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))


def print_tree_analysis(results):
    print("\n" + "=" * 80)
    print(" ANÁLISE ESPECÍFICA - ÁRVORES ".center(80))
    print("=" * 80)
    
    tree_results = [r for r in results if r.structure_name in ["BST", "AVL"] and r.operation == "insert"]
    
    if not tree_results:
        return
    
    analysis_data = []
    
    for result in tree_results:
        metrics = result.metrics
        analysis_data.append({
            'Estrutura': result.structure_name,
            'N': result.data_size,
            'Altura Média': f"{metrics.get('avg_height', 0):.1f}",
            'Iterações Inserção': f"{metrics.get('avg_iterations', 0):.1f}",
            'Tempo Inserção (s)': f"{result.get_statistics().get('mean_time', 0):.6f}"
        })
    
    df = pd.DataFrame(analysis_data)
    print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))


def main():
    print_header()
    
    # Configuração dos experimentos
    data_sizes = [10000, 50000, 100000]
    num_rounds = 5
    
    # Executa experimentos
    print("\nIniciando experimentos...")
    runner = ExperimentRunner(data_sizes=data_sizes, num_rounds=num_rounds)
    
    try:
        results = runner.run_all_experiments()
        
        # Salva resultados
        runner.save_results("experiment_results.json")
        
        # Exibe resumo
        print_summary_table(results)
        print_hash_analysis(results)
        print_tree_analysis(results)
        
        # Análise adicional
        print("\n" + "=" * 80)
        print(" ANÁLISE DE COMPLEXIDADE ".center(80))
        print("=" * 80)
        
        analyzer = ResultAnalyzer(results)
        analyzer.print_complexity_analysis()
        
        # Gera gráficos se disponível
        try:
            analyzer.generate_plots()
            print("\nGráficos salvos em: plots/")
        except Exception as e:
            print(f"\nNão foi possível gerar gráficos: {e}")
        
        print("\n" + "=" * 80)
        print(" EXPERIMENTO CONCLUÍDO COM SUCESSO ".center(80))
        print("=" * 80)
        
    except KeyboardInterrupt:
        print("\n\nExperimento interrompido pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nErro durante execução: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()