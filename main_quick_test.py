#!/usr/bin/env python3
"""
Teste rápido do sistema integrado - apenas para demonstração
"""

from models import DataGenerator
from experiments import ExperimentRunner
from analysis import ResultAnalyzer

def main():
    print("=" * 80)
    print(" TESTE RÁPIDO - SISTEMA INTEGRADO ".center(80))
    print("=" * 80)
    
    # Configuração para teste rápido
    data_sizes = [500, 1000]  # Datasets menores
    num_rounds = 3           # Menos rodadas
    
    # Usa dados realísticos
    generator = DataGenerator(use_realistic_data=True, data_source="generate")
    
    print(f"Configuração: datasets {data_sizes}, {num_rounds} rodadas cada")
    print("Tipo de dados: Realísticos (estudantes/funcionários)")
    
    # Mostra estatísticas de amostra
    sample = generator.generate_records(100)
    stats = generator.get_data_statistics(sample)
    
    print(f"\nEstatísticas da amostra:")
    print(f"- Setores únicos: {stats['unique_sectors']}")
    print(f"- Salário médio: R$ {stats['salary_stats']['mean']:,.2f}")
    print(f"- Tipo de dados: {stats['data_type']}")
    
    # Executa experimentos
    print(f"\nIniciando experimentos rápidos...")
    runner = ExperimentRunner(
        data_sizes=data_sizes,
        num_rounds=num_rounds,
        data_generator=generator
    )
    
    try:
        results = runner.run_all_experiments()
        
        print(f"\n✅ Experimento concluído com sucesso!")
        print(f"Total de resultados: {len(results)}")
        
        # Mostra alguns resultados interessantes
        print(f"\n📊 Destaques dos resultados:")
        
        # Melhor performance de inserção
        insert_results = [r for r in results if r.operation == 'insert']
        if insert_results:
            best_insert = min(insert_results, key=lambda x: x.get_statistics()['mean_time'])
            stats = best_insert.get_statistics()
            print(f"🚀 Melhor inserção: {best_insert.structure_name} - {stats['mean_time']*1000:.3f}ms")
        
        # Melhor performance de busca
        search_results = [r for r in results if r.operation == 'search']
        if search_results:
            best_search = min(search_results, key=lambda x: x.get_statistics()['mean_time'])
            stats = best_search.get_statistics()
            print(f"🔍 Melhor busca: {best_search.structure_name} - {stats['mean_time']*1000000:.1f}μs")
        
        # Hash table analysis
        hash_results = [r for r in results if r.structure_name == 'HashTable' and r.operation == 'insert']
        if hash_results:
            best_hash = min(hash_results, key=lambda x: x.get_statistics()['mean_time'])
            params = best_hash.parameters
            print(f"🏆 Melhor hash: M={params['M']}, {params['hash_function']}")
        
        # Salva resultados
        runner.save_results("quick_test_results.json")
        print(f"\n💾 Resultados salvos em: quick_test_results.json")
        
        # Análise rápida
        print(f"\n🔬 Análise de complexidade:")
        analyzer = ResultAnalyzer(results)
        
        # Mostra apenas algumas estruturas principais
        for structure in ['LinearArray', 'AVL', 'HashTable']:
            struct_results = [r for r in results if r.structure_name == structure]
            if struct_results:
                print(f"- {structure}: {len(struct_results)} experimentos realizados")
        
        print(f"\n" + "="*80)
        print(" ✅ INTEGRAÇÃO FUNCIONANDO PERFEITAMENTE! ".center(80))
        print("="*80)
        
        print(f"\nPara execução completa:")
        print(f"  python main.py              # Dados realísticos completos")
        print(f"  python main.py --basic      # Dados básicos (mais rápido)")
        
    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()