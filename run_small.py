#!/usr/bin/env python3
"""
Script para executar experimentos com datasets menores para teste rápido
"""

import sys
import json
from experiments import ExperimentRunner
from analysis import ResultAnalyzer

def main():
    print("=" * 80)
    print(" ANÁLISE RÁPIDA - DATASETS REDUZIDOS ".center(80))
    print("=" * 80)
    
    # Configuração para teste rápido
    data_sizes = [1000, 5000, 10000]  # Datasets menores
    num_rounds = 3  # Menos rodadas
    
    print(f"\nConfiguração:")
    print(f"  Tamanhos: {data_sizes}")
    print(f"  Rodadas: {num_rounds}")
    print("-" * 80)
    
    # Executa experimentos
    print("\nIniciando experimentos...")
    runner = ExperimentRunner(data_sizes=data_sizes, num_rounds=num_rounds)
    
    try:
        results = runner.run_all_experiments()
        
        # Salva resultados
        runner.save_results("experiment_results_small.json")
        
        # Análise básica
        print("\n" + "=" * 80)
        print(" RESUMO DOS RESULTADOS ".center(80))
        print("=" * 80)
        
        analyzer = ResultAnalyzer(results)
        
        # Imprime estatísticas básicas
        for size in data_sizes:
            print(f"\n--- N = {size} ---")
            
            for struct in ['LinearArray', 'BST', 'AVL']:
                insert_results = [r for r in results if r.structure_name == struct 
                                 and r.data_size == size and r.operation == 'insert']
                search_results = [r for r in results if r.structure_name == struct 
                                 and r.data_size == size and r.operation == 'search']
                
                if insert_results:
                    stats = insert_results[0].get_statistics()
                    print(f"  {struct}:")
                    print(f"    Inserção: {stats['mean_time']:.6f}s (±{stats['std_time']:.6f}s)")
                    
                if search_results:
                    stats = search_results[0].get_statistics()
                    print(f"    Busca:    {stats['mean_time']:.6f}s (±{stats['std_time']:.6f}s)")
        
        # Análise de complexidade
        print("\n" + "=" * 80)
        analyzer.print_complexity_analysis()
        
        # Tenta gerar gráficos
        try:
            analyzer.generate_plots()
            print("\nGráficos salvos em: plots/")
        except Exception as e:
            print(f"\nAviso: Não foi possível gerar gráficos: {e}")
        
        print("\n" + "=" * 80)
        print(" EXPERIMENTO RÁPIDO CONCLUÍDO ".center(80))
        print("=" * 80)
        
    except KeyboardInterrupt:
        print("\n\nExperimento interrompido pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nErro durante execução: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()