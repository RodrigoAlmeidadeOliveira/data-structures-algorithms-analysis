#!/usr/bin/env python3
"""
Teste de integração do sistema com dados de cadastro de matrículas
"""

from models import DataGenerator, Record
from student_registration_data import StudentRecord

def test_basic_integration():
    """Testa a integração básica entre os sistemas."""
    print("=== Teste de Integração ===")
    
    # Teste 1: DataGenerator básico
    print("\n1. Testando DataGenerator básico:")
    basic_gen = DataGenerator(use_realistic_data=False)
    basic_records = basic_gen.generate_records(5)
    
    print(f"Gerados {len(basic_records)} registros básicos:")
    for i, record in enumerate(basic_records[:2]):
        print(f"  {i+1}: {record}")
    
    # Teste 2: DataGenerator realístico
    print("\n2. Testando DataGenerator realístico:")
    realistic_gen = DataGenerator(use_realistic_data=True, data_source="generate")
    realistic_records = realistic_gen.generate_records(5)
    
    print(f"Gerados {len(realistic_records)} registros realísticos:")
    for i, record in enumerate(realistic_records[:2]):
        print(f"  {i+1}: {record}")
        print(f"     CPF: {record.cpf}, Email: {record.email}")
        print(f"     Cargo: {record.cargo}, Status: {record.status}")
    
    # Teste 3: Compatibilidade de tipos
    print("\n3. Testando compatibilidade:")
    mixed_records = basic_records + realistic_records
    mixed_records.sort()  # Testa ordenação
    
    print(f"Lista mista ordenada por matrícula: {len(mixed_records)} registros")
    print(f"Primeira matrícula: {mixed_records[0].matricula}")
    print(f"Última matrícula: {mixed_records[-1].matricula}")
    
    # Teste 4: Hash e equality
    print("\n4. Testando hash e equality:")
    record1 = basic_records[0]
    record2 = Record(record1.matricula, "Outro Nome", 5000.0, 999)
    
    print(f"Record1 == Record2: {record1 == record2}")
    print(f"Hash igual: {hash(record1) == hash(record2)}")
    
    # Teste 5: Estatísticas
    print("\n5. Testando estatísticas:")
    stats = realistic_gen.get_data_statistics(realistic_records)
    print(f"Estatísticas: {stats}")
    
    print("\n=== Integração funcionando corretamente! ===")

def test_small_experiment():
    """Testa um experimento pequeno para verificar funcionalidade."""
    print("\n=== Teste de Experimento Pequeno ===")
    
    from experiments import ExperimentRunner
    
    # Experimento muito pequeno
    generator = DataGenerator(use_realistic_data=True, data_source="generate")
    runner = ExperimentRunner(
        data_sizes=[100],  # Muito pequeno para teste rápido
        num_rounds=2,      # Poucas rodadas
        data_generator=generator
    )
    
    try:
        print("Executando experimento de teste...")
        results = runner.run_all_experiments()
        print(f"Experimento concluído! {len(results)} resultados obtidos.")
        
        # Mostra um resultado
        if results:
            result = results[0]
            stats = result.get_statistics()
            print(f"Exemplo - {result.structure_name} ({result.operation}):")
            print(f"  Tempo médio: {stats.get('mean_time', 0):.6f}s")
            print(f"  Iterações médias: {stats.get('mean_iterations', 0):.1f}")
        
    except Exception as e:
        print(f"Erro no experimento: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_basic_integration()
    test_small_experiment()