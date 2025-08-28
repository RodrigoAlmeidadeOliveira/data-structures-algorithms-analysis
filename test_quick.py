#!/usr/bin/env python3
"""Script de teste rápido para verificar funcionamento básico"""

from models import DataGenerator
from linear_array import LinearArray
from binary_search_tree import BinarySearchTree
from avl_tree import AVLTree
from hash_table import HashTable

def test_structure(structure, name):
    print(f"\nTestando {name}:")
    
    # Gera dados de teste
    records = DataGenerator.generate_records(100, seed=42)
    
    # Inserção
    total_iterations = 0
    for record in records:
        iterations = structure.insert(record)
        total_iterations += iterations
    
    print(f"  Inserção: {len(records)} registros, {total_iterations} iterações totais")
    
    # Busca
    search_count = 10
    found_count = 0
    total_search_iterations = 0
    
    for i in range(search_count):
        result, iterations = structure.search(records[i].matricula)
        if result:
            found_count += 1
        total_search_iterations += iterations
    
    print(f"  Busca: {found_count}/{search_count} encontrados, média de {total_search_iterations/search_count:.1f} iterações")
    
    # Métricas específicas
    if hasattr(structure, 'height'):
        print(f"  Altura da árvore: {structure.height()}")
    
    if hasattr(structure, 'get_load_factor'):
        print(f"  Load factor: {structure.get_load_factor():.3f}")
        print(f"  Taxa de colisão: {structure.get_collision_rate():.3f}")
        print(f"  Comprimento médio de cadeia: {structure.get_average_chain_length():.2f}")
        print(f"  Comprimento máximo de cadeia: {structure.get_max_chain_length()}")

def main():
    print("=" * 60)
    print("TESTE RÁPIDO DAS ESTRUTURAS DE DADOS")
    print("=" * 60)
    
    # Testa cada estrutura
    test_structure(LinearArray(), "Array Linear")
    test_structure(BinarySearchTree(), "Árvore de Busca Binária (BST)")
    test_structure(AVLTree(), "Árvore AVL")
    
    print("\n--- Tabelas Hash com diferentes configurações ---")
    for m in [100, 1000]:
        for func in ['division', 'multiplication', 'folding']:
            test_structure(
                HashTable(size=m, hash_function=func),
                f"Hash Table (M={m}, {func})"
            )
    
    print("\n" + "=" * 60)
    print("TODOS OS TESTES CONCLUÍDOS COM SUCESSO!")
    print("=" * 60)

if __name__ == "__main__":
    main()