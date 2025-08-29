import time
import random
import json
import numpy as np
from typing import Dict, List, Any
from dataclasses import dataclass
from models import DataGenerator, Record
from linear_array import LinearArray
from binary_search_tree import BinarySearchTree
from avl_tree import AVLTree
from hash_table import HashTable
from metrics import MetricsCollector, PerformanceMetrics


@dataclass
class ExperimentResult:
    structure_name: str
    data_size: int
    operation: str
    metrics: Dict[str, float]
    rounds: List[Dict[str, float]]
    parameters: Dict[str, Any]
    
    def get_statistics(self) -> Dict[str, float]:
        if not self.rounds:
            return {}
        
        time_values = [r['execution_time'] for r in self.rounds]
        memory_values = [r['memory_usage'] for r in self.rounds]
        iteration_values = [r.get('iterations', 0) for r in self.rounds]
        
        return {
            'mean_time': np.mean(time_values),
            'std_time': np.std(time_values),
            'mean_memory': np.mean(memory_values),
            'std_memory': np.std(memory_values),
            'mean_iterations': np.mean(iteration_values),
            'std_iterations': np.std(iteration_values)
        }


class ExperimentRunner:
    def __init__(self, data_sizes: List[int] = None, num_rounds: int = 5, data_generator: DataGenerator = None):
        self.data_sizes = data_sizes or [10000, 50000, 100000]
        self.num_rounds = num_rounds
        self.data_generator = data_generator or DataGenerator(use_realistic_data=False)
        self.collector = MetricsCollector()
        self.results: List[ExperimentResult] = []
    
    def run_all_experiments(self):
        print("=" * 60)
        print("INICIANDO EXPERIMENTOS DE ANÁLISE DE ESTRUTURAS DE DADOS")
        print("=" * 60)
        
        for size in self.data_sizes:
            print(f"\n--- Tamanho do Dataset: {size} registros ---")
            
            # Gera dados para este tamanho usando o gerador configurado
            data = self.data_generator.generate_records(size, seed=42)
            
            # Experimentos com Array Linear
            self._run_linear_array_experiment(data, size)
            
            # Experimentos com BST
            self._run_bst_experiment(data, size)
            
            # Experimentos com AVL
            self._run_avl_experiment(data, size)
            
            # Experimentos com Hash Table (diferentes M e funções)
            for m_size in [100, 1000, 5000]:
                for hash_func in ['division', 'multiplication', 'folding']:
                    self._run_hash_table_experiment(data, size, m_size, hash_func)
        
        return self.results
    
    def _run_linear_array_experiment(self, data: List[Record], size: int):
        print(f"  Array Linear...")
        
        insert_rounds = []
        search_rounds = []
        
        for round_num in range(self.num_rounds):
            # Inserção
            array = LinearArray()
            start_time = time.perf_counter()
            total_iterations = 0
            
            for record in data:
                iterations = array.insert(record)
                total_iterations += iterations
            
            insert_time = time.perf_counter() - start_time
            
            insert_rounds.append({
                'execution_time': insert_time,
                'memory_usage': 0,  # Simplificado
                'iterations': total_iterations
            })
            
            # Busca (amostra aleatória)
            search_sample = random.sample(data, min(1000, len(data)))
            start_time = time.perf_counter()
            total_iterations = 0
            
            for record in search_sample:
                _, iterations = array.search(record.matricula)
                total_iterations += iterations
            
            search_time = time.perf_counter() - start_time
            
            search_rounds.append({
                'execution_time': search_time / len(search_sample),
                'memory_usage': 0,
                'iterations': total_iterations / len(search_sample)
            })
        
        # Registra resultados
        self.results.append(ExperimentResult(
            structure_name="LinearArray",
            data_size=size,
            operation="insert",
            metrics=self._calculate_avg_metrics(insert_rounds),
            rounds=insert_rounds,
            parameters={}
        ))
        
        self.results.append(ExperimentResult(
            structure_name="LinearArray",
            data_size=size,
            operation="search",
            metrics=self._calculate_avg_metrics(search_rounds),
            rounds=search_rounds,
            parameters={}
        ))
    
    def _run_bst_experiment(self, data: List[Record], size: int):
        print(f"  BST...")
        
        insert_rounds = []
        search_rounds = []
        
        for round_num in range(self.num_rounds):
            # Embaralha dados para diferentes ordens de inserção
            shuffled_data = data.copy()
            random.shuffle(shuffled_data)
            
            # Inserção
            bst = BinarySearchTree()
            start_time = time.perf_counter()
            total_iterations = 0
            
            for record in shuffled_data:
                iterations = bst.insert(record)
                total_iterations += iterations
            
            insert_time = time.perf_counter() - start_time
            height = bst.height()
            
            insert_rounds.append({
                'execution_time': insert_time,
                'memory_usage': 0,
                'iterations': total_iterations,
                'height': height
            })
            
            # Busca
            search_sample = random.sample(data, min(1000, len(data)))
            start_time = time.perf_counter()
            total_iterations = 0
            
            for record in search_sample:
                _, iterations = bst.search(record.matricula)
                total_iterations += iterations
            
            search_time = time.perf_counter() - start_time
            
            search_rounds.append({
                'execution_time': search_time / len(search_sample),
                'memory_usage': 0,
                'iterations': total_iterations / len(search_sample)
            })
        
        self.results.append(ExperimentResult(
            structure_name="BST",
            data_size=size,
            operation="insert",
            metrics=self._calculate_avg_metrics(insert_rounds),
            rounds=insert_rounds,
            parameters={'balanced': False}
        ))
        
        self.results.append(ExperimentResult(
            structure_name="BST",
            data_size=size,
            operation="search",
            metrics=self._calculate_avg_metrics(search_rounds),
            rounds=search_rounds,
            parameters={'balanced': False}
        ))
    
    def _run_avl_experiment(self, data: List[Record], size: int):
        print(f"  AVL...")
        
        insert_rounds = []
        search_rounds = []
        
        for round_num in range(self.num_rounds):
            # Embaralha dados
            shuffled_data = data.copy()
            random.shuffle(shuffled_data)
            
            # Inserção
            avl = AVLTree()
            start_time = time.perf_counter()
            total_iterations = 0
            
            for record in shuffled_data:
                iterations = avl.insert(record)
                total_iterations += iterations
            
            insert_time = time.perf_counter() - start_time
            height = avl.height()
            
            insert_rounds.append({
                'execution_time': insert_time,
                'memory_usage': 0,
                'iterations': total_iterations,
                'height': height
            })
            
            # Busca
            search_sample = random.sample(data, min(1000, len(data)))
            start_time = time.perf_counter()
            total_iterations = 0
            
            for record in search_sample:
                _, iterations = avl.search(record.matricula)
                total_iterations += iterations
            
            search_time = time.perf_counter() - start_time
            
            search_rounds.append({
                'execution_time': search_time / len(search_sample),
                'memory_usage': 0,
                'iterations': total_iterations / len(search_sample)
            })
        
        self.results.append(ExperimentResult(
            structure_name="AVL",
            data_size=size,
            operation="insert",
            metrics=self._calculate_avg_metrics(insert_rounds),
            rounds=insert_rounds,
            parameters={'balanced': True}
        ))
        
        self.results.append(ExperimentResult(
            structure_name="AVL",
            data_size=size,
            operation="search",
            metrics=self._calculate_avg_metrics(search_rounds),
            rounds=search_rounds,
            parameters={'balanced': True}
        ))
    
    def _run_hash_table_experiment(self, data: List[Record], size: int, 
                                  m_size: int, hash_func: str):
        print(f"  Hash Table (M={m_size}, func={hash_func})...")
        
        insert_rounds = []
        search_rounds = []
        
        for round_num in range(self.num_rounds):
            # Inserção
            hash_table = HashTable(size=m_size, hash_function=hash_func)
            start_time = time.perf_counter()
            total_iterations = 0
            
            for record in data:
                iterations = hash_table.insert(record)
                total_iterations += iterations
            
            insert_time = time.perf_counter() - start_time
            
            # Métricas específicas da tabela hash
            load_factor = hash_table.get_load_factor()
            collision_rate = hash_table.get_collision_rate()
            avg_chain = hash_table.get_average_chain_length()
            max_chain = hash_table.get_max_chain_length()
            
            insert_rounds.append({
                'execution_time': insert_time,
                'memory_usage': 0,
                'iterations': total_iterations,
                'load_factor': load_factor,
                'collision_rate': collision_rate,
                'avg_chain_length': avg_chain,
                'max_chain_length': max_chain
            })
            
            # Busca
            search_sample = random.sample(data, min(1000, len(data)))
            start_time = time.perf_counter()
            total_iterations = 0
            
            for record in search_sample:
                _, iterations = hash_table.search(record.matricula)
                total_iterations += iterations
            
            search_time = time.perf_counter() - start_time
            
            search_rounds.append({
                'execution_time': search_time / len(search_sample),
                'memory_usage': 0,
                'iterations': total_iterations / len(search_sample)
            })
        
        self.results.append(ExperimentResult(
            structure_name="HashTable",
            data_size=size,
            operation="insert",
            metrics=self._calculate_avg_metrics(insert_rounds),
            rounds=insert_rounds,
            parameters={'M': m_size, 'hash_function': hash_func}
        ))
        
        self.results.append(ExperimentResult(
            structure_name="HashTable",
            data_size=size,
            operation="search",
            metrics=self._calculate_avg_metrics(search_rounds),
            rounds=search_rounds,
            parameters={'M': m_size, 'hash_function': hash_func}
        ))
    
    def _calculate_avg_metrics(self, rounds: List[Dict]) -> Dict[str, float]:
        if not rounds:
            return {}
        
        metrics = {}
        keys = rounds[0].keys()
        
        for key in keys:
            values = [r[key] for r in rounds if key in r]
            if values:
                metrics[f'avg_{key}'] = np.mean(values)
                metrics[f'std_{key}'] = np.std(values)
        
        return metrics
    
    def save_results(self, filename: str = "experiment_results.json"):
        results_dict = []
        for result in self.results:
            results_dict.append({
                'structure': result.structure_name,
                'data_size': result.data_size,
                'operation': result.operation,
                'parameters': result.parameters,
                'statistics': result.get_statistics(),
                'metrics': result.metrics
            })
        
        with open(filename, 'w') as f:
            json.dump(results_dict, f, indent=2)
        
        print(f"\nResultados salvos em: {filename}")