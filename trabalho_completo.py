#!/usr/bin/env python3
"""
================================================================================
ANÁLISE COMPARATIVA DE ESTRUTURAS DE DADOS
PONTIFÍCIA UNIVERSIDADE CATÓLICA DO PARANÁ
PROGRAMA DE PÓS-GRADUAÇÃO EM INFORMÁTICA APLICADA
FUNDAMENTOS DE ALGORITMOS E ESTRUTURA DE DADOS
PROF. ANDRÉ GUSTAVO HOCHULI

Trabalho 01: Análise Comparativa de Estruturas de Dados
================================================================================

Este código implementa e compara diferentes estruturas de dados:
- Arrays lineares
- Árvores de busca binária (BST)
- Árvores AVL (balanceadas)
- Tabelas hash com três funções diferentes

O objetivo é avaliar o desempenho em operações de inserção e busca,
considerando métricas como tempo de execução, uso de memória e iterações.

================================================================================
"""

import time
import random
import string
import json
import os
import sys
import tracemalloc
import psutil
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
from tabulate import tabulate
import math

# ================================================================================
# SEÇÃO 1: MODELOS DE DADOS
# ================================================================================

class Record:
    """Classe que representa um registro de funcionário/estudante."""
    
    def __init__(self, matricula: int, nome: str, salario: float, codigo_setor: int):
        self.matricula = int(matricula)  # Matrícula de 9 dígitos
        self.nome = nome
        self.salario = salario
        self.codigo_setor = codigo_setor
    
    def __repr__(self):
        return f"Record(matricula={self.matricula}, nome='{self.nome}', salario={self.salario:.2f}, setor={self.codigo_setor})"
    
    def __eq__(self, other):
        if isinstance(other, Record):
            return self.matricula == other.matricula
        return False
    
    def __lt__(self, other):
        if isinstance(other, Record):
            return self.matricula < other.matricula
        return NotImplemented
    
    def __hash__(self):
        return hash(self.matricula)


class DataGenerator:
    """Gerador de dados fictícios para os experimentos."""
    
    @staticmethod
    def generate_records(n: int, seed: Optional[int] = None) -> List[Record]:
        """
        Gera n registros fictícios com dados aleatórios.
        
        Args:
            n: Número de registros a gerar
            seed: Semente para reprodutibilidade
        
        Returns:
            Lista de registros Record
        """
        if seed is not None:
            random.seed(seed)
        
        print(f"Gerando {n:,} registros fictícios...")
        
        records = []
        used_matriculas = set()
        
        for i in range(n):
            # Gera matrícula única de 9 dígitos
            matricula = random.randint(100000000, 999999999)
            while matricula in used_matriculas:
                matricula = random.randint(100000000, 999999999)
            used_matriculas.add(matricula)
            
            # Gera nome aleatório
            nome = ''.join(random.choices(string.ascii_uppercase, k=5)) + ' ' + \
                   ''.join(random.choices(string.ascii_uppercase, k=8))
            
            # Gera salário entre 2000 e 20000
            salario = random.uniform(2000.0, 20000.0)
            
            # Gera código do setor entre 1 e 100
            codigo_setor = random.randint(1, 100)
            
            records.append(Record(matricula, nome, salario, codigo_setor))
            
            # Mostra progresso
            if (i + 1) % 10000 == 0:
                print(f"  Progresso: {i+1:,}/{n:,} registros gerados...")
        
        print(f"✓ {n:,} registros gerados com sucesso")
        return records


# ================================================================================
# SEÇÃO 2: ESTRUTURAS DE DADOS
# ================================================================================

# --------------------------------------------------------------------------------
# 2.1 Array Linear
# --------------------------------------------------------------------------------

class LinearArray:
    """
    Implementação de array linear (lista).
    - Inserção: O(1) - adiciona no final
    - Busca: O(n) - busca sequencial
    """
    
    def __init__(self):
        self.data: List[Record] = []
        self.iterations = 0
    
    def insert(self, record: Record) -> int:
        """Insere um registro no array. Retorna número de iterações."""
        self.iterations = 1  # Uma operação de inserção
        self.data.append(record)
        return self.iterations
    
    def search(self, matricula: int) -> Tuple[Optional[Record], int]:
        """Busca um registro pela matrícula. Retorna (registro, iterações)."""
        self.iterations = 0
        for record in self.data:
            self.iterations += 1
            if record.matricula == matricula:
                return record, self.iterations
        return None, self.iterations
    
    def size(self) -> int:
        """Retorna o tamanho do array."""
        return len(self.data)
    
    def clear(self):
        """Limpa o array."""
        self.data.clear()
        self.iterations = 0


# --------------------------------------------------------------------------------
# 2.2 Árvore de Busca Binária (BST)
# --------------------------------------------------------------------------------

class BSTNode:
    """Nó da árvore de busca binária."""
    
    def __init__(self, record: Record):
        self.record = record
        self.left: Optional[BSTNode] = None
        self.right: Optional[BSTNode] = None


class BinarySearchTree:
    """
    Implementação de árvore de busca binária sem balanceamento.
    - Inserção: O(log n) médio, O(n) pior caso
    - Busca: O(log n) médio, O(n) pior caso
    """
    
    def __init__(self):
        self.root: Optional[BSTNode] = None
        self.iterations = 0
        self.size_count = 0
    
    def insert(self, record: Record) -> int:
        """Insere um registro na árvore. Retorna número de iterações."""
        self.iterations = 0
        if self.root is None:
            self.root = BSTNode(record)
            self.iterations = 1
        else:
            self._insert_recursive(self.root, record)
        self.size_count += 1
        return self.iterations
    
    def _insert_recursive(self, node: BSTNode, record: Record) -> BSTNode:
        """Inserção recursiva na árvore."""
        self.iterations += 1
        
        if record.matricula < node.record.matricula:
            if node.left is None:
                node.left = BSTNode(record)
            else:
                self._insert_recursive(node.left, record)
        elif record.matricula > node.record.matricula:
            if node.right is None:
                node.right = BSTNode(record)
            else:
                self._insert_recursive(node.right, record)
        
        return node
    
    def search(self, matricula: int) -> Tuple[Optional[Record], int]:
        """Busca um registro pela matrícula. Retorna (registro, iterações)."""
        self.iterations = 0
        return self._search_recursive(self.root, matricula), self.iterations
    
    def _search_recursive(self, node: Optional[BSTNode], matricula: int) -> Optional[Record]:
        """Busca recursiva na árvore."""
        if node is None:
            return None
        
        self.iterations += 1
        
        if matricula == node.record.matricula:
            return node.record
        elif matricula < node.record.matricula:
            return self._search_recursive(node.left, matricula)
        else:
            return self._search_recursive(node.right, matricula)
    
    def height(self) -> int:
        """Calcula a altura da árvore."""
        return self._height_recursive(self.root)
    
    def _height_recursive(self, node: Optional[BSTNode]) -> int:
        """Cálculo recursivo da altura."""
        if node is None:
            return 0
        return 1 + max(self._height_recursive(node.left), 
                      self._height_recursive(node.right))
    
    def size(self) -> int:
        """Retorna o número de elementos na árvore."""
        return self.size_count
    
    def clear(self):
        """Limpa a árvore."""
        self.root = None
        self.iterations = 0
        self.size_count = 0


# --------------------------------------------------------------------------------
# 2.3 Árvore AVL (Balanceada)
# --------------------------------------------------------------------------------

class AVLNode:
    """Nó da árvore AVL."""
    
    def __init__(self, record: Record):
        self.record = record
        self.left: Optional[AVLNode] = None
        self.right: Optional[AVLNode] = None
        self.height = 1


class AVLTree:
    """
    Implementação de árvore AVL (balanceada).
    - Inserção: O(log n) garantido
    - Busca: O(log n) garantido
    """
    
    def __init__(self):
        self.root: Optional[AVLNode] = None
        self.iterations = 0
        self.size_count = 0
    
    def insert(self, record: Record) -> int:
        """Insere um registro na árvore. Retorna número de iterações."""
        self.iterations = 0
        self.root = self._insert_recursive(self.root, record)
        self.size_count += 1
        return self.iterations
    
    def _insert_recursive(self, node: Optional[AVLNode], record: Record) -> AVLNode:
        """Inserção recursiva com balanceamento."""
        self.iterations += 1
        
        # Inserção normal BST
        if node is None:
            return AVLNode(record)
        
        if record.matricula < node.record.matricula:
            node.left = self._insert_recursive(node.left, record)
        elif record.matricula > node.record.matricula:
            node.right = self._insert_recursive(node.right, record)
        else:
            return node  # Duplicata não permitida
        
        # Atualiza altura
        node.height = 1 + max(self._get_height(node.left), 
                             self._get_height(node.right))
        
        # Obtém o fator de balanceamento
        balance = self._get_balance(node)
        
        # Casos de desbalanceamento e rotações
        # Caso 1 - Left Left
        if balance > 1 and record.matricula < node.left.record.matricula:
            return self._rotate_right(node)
        
        # Caso 2 - Right Right
        if balance < -1 and record.matricula > node.right.record.matricula:
            return self._rotate_left(node)
        
        # Caso 3 - Left Right
        if balance > 1 and record.matricula > node.left.record.matricula:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        
        # Caso 4 - Right Left
        if balance < -1 and record.matricula < node.right.record.matricula:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        
        return node
    
    def _rotate_left(self, z: AVLNode) -> AVLNode:
        """Rotação à esquerda."""
        self.iterations += 1
        y = z.right
        T2 = y.left
        
        # Realiza rotação
        y.left = z
        z.right = T2
        
        # Atualiza alturas
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        
        return y
    
    def _rotate_right(self, z: AVLNode) -> AVLNode:
        """Rotação à direita."""
        self.iterations += 1
        y = z.left
        T3 = y.right
        
        # Realiza rotação
        y.right = z
        z.left = T3
        
        # Atualiza alturas
        z.height = 1 + max(self._get_height(z.left), self._get_height(z.right))
        y.height = 1 + max(self._get_height(y.left), self._get_height(y.right))
        
        return y
    
    def _get_height(self, node: Optional[AVLNode]) -> int:
        """Obtém a altura de um nó."""
        if node is None:
            return 0
        return node.height
    
    def _get_balance(self, node: Optional[AVLNode]) -> int:
        """Calcula o fator de balanceamento de um nó."""
        if node is None:
            return 0
        return self._get_height(node.left) - self._get_height(node.right)
    
    def search(self, matricula: int) -> Tuple[Optional[Record], int]:
        """Busca um registro pela matrícula. Retorna (registro, iterações)."""
        self.iterations = 0
        return self._search_recursive(self.root, matricula), self.iterations
    
    def _search_recursive(self, node: Optional[AVLNode], matricula: int) -> Optional[Record]:
        """Busca recursiva na árvore."""
        if node is None:
            return None
        
        self.iterations += 1
        
        if matricula == node.record.matricula:
            return node.record
        elif matricula < node.record.matricula:
            return self._search_recursive(node.left, matricula)
        else:
            return self._search_recursive(node.right, matricula)
    
    def height(self) -> int:
        """Retorna a altura da árvore."""
        return self._get_height(self.root)
    
    def size(self) -> int:
        """Retorna o número de elementos na árvore."""
        return self.size_count
    
    def clear(self):
        """Limpa a árvore."""
        self.root = None
        self.iterations = 0
        self.size_count = 0


# --------------------------------------------------------------------------------
# 2.4 Tabela Hash
# --------------------------------------------------------------------------------

class HashTable:
    """
    Implementação de tabela hash com tratamento de colisões por encadeamento.
    Suporta três funções hash diferentes:
    - Divisão
    - Multiplicação
    - Folding
    """
    
    def __init__(self, size: int = 100, hash_function: str = 'division'):
        """
        Inicializa a tabela hash.
        
        Args:
            size: Tamanho da tabela (M)
            hash_function: Função hash a usar ('division', 'multiplication', 'folding')
        """
        self.size = size
        self.table: List[List[Record]] = [[] for _ in range(size)]
        self.hash_function_name = hash_function
        self.iterations = 0
        self.collisions = 0
        self.total_elements = 0
        
        # Seleciona a função hash
        if hash_function == 'division':
            self.hash_func = self._hash_division
        elif hash_function == 'multiplication':
            self.hash_func = self._hash_multiplication
        elif hash_function == 'folding':
            self.hash_func = self._hash_folding
        else:
            self.hash_func = self._hash_division
    
    def _hash_division(self, key: int) -> int:
        """Função hash por divisão: h(k) = k mod M"""
        return key % self.size
    
    def _hash_multiplication(self, key: int) -> int:
        """Função hash por multiplicação: h(k) = ⌊M × (k × A mod 1)⌋"""
        A = 0.6180339887  # (√5 - 1) / 2 - Constante de Knuth
        return int(self.size * ((key * A) % 1))
    
    def _hash_folding(self, key: int) -> int:
        """Função hash por folding: divide a chave em partes e soma"""
        key_str = str(key)
        chunk_size = 3
        chunks = [key_str[i:i+chunk_size] for i in range(0, len(key_str), chunk_size)]
        total = sum(int(chunk) for chunk in chunks)
        return total % self.size
    
    def insert(self, record: Record) -> int:
        """Insere um registro na tabela. Retorna número de iterações."""
        self.iterations = 1
        index = self.hash_func(record.matricula)
        
        # Verifica se há colisão
        if len(self.table[index]) > 0:
            self.collisions += 1
        
        # Verifica se já existe
        for existing_record in self.table[index]:
            self.iterations += 1
            if existing_record.matricula == record.matricula:
                return self.iterations  # Já existe, não insere
        
        self.table[index].append(record)
        self.total_elements += 1
        return self.iterations
    
    def search(self, matricula: int) -> Tuple[Optional[Record], int]:
        """Busca um registro pela matrícula. Retorna (registro, iterações)."""
        self.iterations = 1
        index = self.hash_func(matricula)
        
        for record in self.table[index]:
            self.iterations += 1
            if record.matricula == matricula:
                return record, self.iterations
        
        return None, self.iterations
    
    def get_load_factor(self) -> float:
        """Calcula o load factor (N/M)."""
        return self.total_elements / self.size
    
    def get_collision_rate(self) -> float:
        """Calcula a taxa de colisões."""
        if self.total_elements == 0:
            return 0.0
        return self.collisions / self.total_elements
    
    def get_average_chain_length(self) -> float:
        """Calcula o comprimento médio das cadeias."""
        non_empty_buckets = sum(1 for bucket in self.table if bucket)
        if non_empty_buckets == 0:
            return 0.0
        return self.total_elements / non_empty_buckets
    
    def get_max_chain_length(self) -> int:
        """Retorna o comprimento máximo de cadeia."""
        return max(len(bucket) for bucket in self.table)
    
    def size_count(self) -> int:
        """Retorna o número de elementos na tabela."""
        return self.total_elements
    
    def clear(self):
        """Limpa a tabela."""
        self.table = [[] for _ in range(self.size)]
        self.iterations = 0
        self.collisions = 0
        self.total_elements = 0


# ================================================================================
# SEÇÃO 3: SISTEMA DE MÉTRICAS
# ================================================================================

@dataclass
class PerformanceMetrics:
    """Classe para armazenar métricas de desempenho."""
    execution_time: float = 0.0
    memory_usage: float = 0.0  # Em MB
    peak_memory: float = 0.0  # Em MB
    cpu_percent: float = 0.0
    iterations: int = 0
    additional_metrics: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte métricas para dicionário."""
        return {
            'execution_time': self.execution_time,
            'memory_usage': self.memory_usage,
            'peak_memory': self.peak_memory,
            'cpu_percent': self.cpu_percent,
            'iterations': self.iterations,
            **self.additional_metrics
        }


class MetricsCollector:
    """Coletor de métricas de desempenho."""
    
    def __init__(self):
        self.process = psutil.Process(os.getpid())
    
    def measure_operation(self, operation: Callable, *args, **kwargs) -> Tuple[Any, PerformanceMetrics]:
        """
        Mede o desempenho de uma operação.
        
        Returns:
            Tupla (resultado da operação, métricas)
        """
        metrics = PerformanceMetrics()
        
        # Coleta CPU antes
        self.process.cpu_percent()  # Primeira chamada para inicializar
        
        # Inicia rastreamento de memória
        tracemalloc.start()
        
        # Memória inicial
        mem_before = self.process.memory_info().rss / 1024 / 1024  # MB
        
        # Executa operação e mede tempo
        start_time = time.perf_counter()
        result = operation(*args, **kwargs)
        end_time = time.perf_counter()
        
        # Coleta métricas
        metrics.execution_time = end_time - start_time
        
        # Memória
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        mem_after = self.process.memory_info().rss / 1024 / 1024  # MB
        
        metrics.memory_usage = (mem_after - mem_before)
        metrics.peak_memory = peak / 1024 / 1024  # MB
        
        # CPU
        metrics.cpu_percent = self.process.cpu_percent()
        
        return result, metrics


# ================================================================================
# SEÇÃO 4: EXPERIMENTOS
# ================================================================================

@dataclass
class ExperimentResult:
    """Resultado de um experimento."""
    structure_name: str
    data_size: int
    operation: str
    metrics: Dict[str, float]
    rounds: List[Dict[str, float]]
    parameters: Dict[str, Any]
    
    def get_statistics(self) -> Dict[str, float]:
        """Calcula estatísticas dos rounds."""
        if not self.rounds:
            return {}
        
        time_values = [r['execution_time'] for r in self.rounds]
        memory_values = [r.get('memory_usage', 0) for r in self.rounds]
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
    """Executor de experimentos comparativos."""
    
    def __init__(self, data_sizes: List[int] = None, num_rounds: int = 5):
        """
        Inicializa o executor de experimentos.
        
        Args:
            data_sizes: Tamanhos de dados para testar
            num_rounds: Número de rodadas por experimento
        """
        self.data_sizes = data_sizes or [1000, 5000, 10000]
        self.num_rounds = num_rounds
        self.collector = MetricsCollector()
        self.results: List[ExperimentResult] = []
    
    def run_all_experiments(self):
        """Executa todos os experimentos configurados."""
        print("\n" + "=" * 80)
        print(" INICIANDO EXPERIMENTOS ".center(80))
        print("=" * 80)
        
        for size in self.data_sizes:
            print(f"\n{'='*60}")
            print(f" Tamanho do Dataset: {size:,} registros ".center(60))
            print(f"{'='*60}")
            
            # Gera dados para este tamanho
            data = DataGenerator.generate_records(size, seed=42)
            
            # Experimentos com Array Linear
            print(f"\n→ Array Linear...")
            self._run_linear_array_experiment(data, size)
            
            # Experimentos com BST
            print(f"\n→ Árvore de Busca Binária (BST)...")
            self._run_bst_experiment(data, size)
            
            # Experimentos com AVL
            print(f"\n→ Árvore AVL...")
            self._run_avl_experiment(data, size)
            
            # Experimentos com Hash Table
            print(f"\n→ Tabela Hash...")
            for m_size in [100, 1000, 5000]:
                for hash_func in ['division', 'multiplication', 'folding']:
                    print(f"  • M={m_size}, função={hash_func}")
                    self._run_hash_table_experiment(data, size, m_size, hash_func)
        
        return self.results
    
    def _run_linear_array_experiment(self, data: List[Record], size: int):
        """Executa experimento com array linear."""
        insert_rounds = []
        search_rounds = []
        
        for round_num in range(self.num_rounds):
            # Inserção
            array = LinearArray()
            
            # Coleta métricas de sistema antes
            process = psutil.Process()
            mem_before = process.memory_info().rss / 1024 / 1024  # MB
            cpu_before = process.cpu_percent(interval=None)
            
            # Inicia rastreamento de memória
            tracemalloc.start()
            
            start_time = time.perf_counter()
            total_iterations = 0
            
            for record in data:
                iterations = array.insert(record)
                total_iterations += iterations
            
            insert_time = time.perf_counter() - start_time
            
            # Coleta métricas de sistema depois
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            mem_after = process.memory_info().rss / 1024 / 1024  # MB
            cpu_percent = process.cpu_percent(interval=0.1)
            
            insert_rounds.append({
                'execution_time': insert_time,
                'memory_usage': mem_after - mem_before,
                'peak_memory': peak / 1024 / 1024,  # MB
                'cpu_percent': cpu_percent,
                'iterations': total_iterations
            })
            
            # Busca (amostra aleatória)
            search_sample = random.sample(data, min(1000, len(data)))
            
            # Coleta métricas antes da busca
            mem_before = process.memory_info().rss / 1024 / 1024
            tracemalloc.start()
            
            start_time = time.perf_counter()
            total_iterations = 0
            
            for record in search_sample:
                _, iterations = array.search(record.matricula)
                total_iterations += iterations
            
            search_time = time.perf_counter() - start_time
            
            # Coleta métricas depois da busca
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            mem_after = process.memory_info().rss / 1024 / 1024
            cpu_percent = process.cpu_percent(interval=0.1)
            
            search_rounds.append({
                'execution_time': search_time / len(search_sample),
                'memory_usage': (mem_after - mem_before) / len(search_sample),
                'peak_memory': peak / 1024 / 1024 / len(search_sample),
                'cpu_percent': cpu_percent,
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
        """Executa experimento com BST."""
        insert_rounds = []
        search_rounds = []
        
        for round_num in range(self.num_rounds):
            # Embaralha dados para diferentes ordens de inserção
            shuffled_data = data.copy()
            random.shuffle(shuffled_data)
            
            # Inserção
            bst = BinarySearchTree()
            
            # Coleta métricas de sistema antes
            process = psutil.Process()
            mem_before = process.memory_info().rss / 1024 / 1024
            cpu_before = process.cpu_percent(interval=None)
            
            tracemalloc.start()
            
            start_time = time.perf_counter()
            total_iterations = 0
            
            for record in shuffled_data:
                iterations = bst.insert(record)
                total_iterations += iterations
            
            insert_time = time.perf_counter() - start_time
            height = bst.height()
            
            # Coleta métricas depois
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            mem_after = process.memory_info().rss / 1024 / 1024
            cpu_percent = process.cpu_percent(interval=0.1)
            
            insert_rounds.append({
                'execution_time': insert_time,
                'memory_usage': mem_after - mem_before,
                'peak_memory': peak / 1024 / 1024,
                'cpu_percent': cpu_percent,
                'iterations': total_iterations,
                'height': height
            })
            
            # Busca
            search_sample = random.sample(data, min(1000, len(data)))
            
            mem_before = process.memory_info().rss / 1024 / 1024
            tracemalloc.start()
            
            start_time = time.perf_counter()
            total_iterations = 0
            
            for record in search_sample:
                _, iterations = bst.search(record.matricula)
                total_iterations += iterations
            
            search_time = time.perf_counter() - start_time
            
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            mem_after = process.memory_info().rss / 1024 / 1024
            cpu_percent = process.cpu_percent(interval=0.1)
            
            search_rounds.append({
                'execution_time': search_time / len(search_sample),
                'memory_usage': (mem_after - mem_before) / len(search_sample),
                'peak_memory': peak / 1024 / 1024 / len(search_sample),
                'cpu_percent': cpu_percent,
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
        """Executa experimento com AVL."""
        insert_rounds = []
        search_rounds = []
        
        for round_num in range(self.num_rounds):
            # Embaralha dados
            shuffled_data = data.copy()
            random.shuffle(shuffled_data)
            
            # Inserção
            avl = AVLTree()
            
            process = psutil.Process()
            mem_before = process.memory_info().rss / 1024 / 1024
            tracemalloc.start()
            
            start_time = time.perf_counter()
            total_iterations = 0
            
            for record in shuffled_data:
                iterations = avl.insert(record)
                total_iterations += iterations
            
            insert_time = time.perf_counter() - start_time
            height = avl.height()
            
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            mem_after = process.memory_info().rss / 1024 / 1024
            cpu_percent = process.cpu_percent(interval=0.1)
            
            insert_rounds.append({
                'execution_time': insert_time,
                'memory_usage': mem_after - mem_before,
                'peak_memory': peak / 1024 / 1024,
                'cpu_percent': cpu_percent,
                'iterations': total_iterations,
                'height': height
            })
            
            # Busca
            search_sample = random.sample(data, min(1000, len(data)))
            
            mem_before = process.memory_info().rss / 1024 / 1024
            tracemalloc.start()
            
            start_time = time.perf_counter()
            total_iterations = 0
            
            for record in search_sample:
                _, iterations = avl.search(record.matricula)
                total_iterations += iterations
            
            search_time = time.perf_counter() - start_time
            
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            mem_after = process.memory_info().rss / 1024 / 1024
            cpu_percent = process.cpu_percent(interval=0.1)
            
            search_rounds.append({
                'execution_time': search_time / len(search_sample),
                'memory_usage': (mem_after - mem_before) / len(search_sample),
                'peak_memory': peak / 1024 / 1024 / len(search_sample),
                'cpu_percent': cpu_percent,
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
        """Executa experimento com tabela hash."""
        insert_rounds = []
        search_rounds = []
        
        for round_num in range(self.num_rounds):
            # Inserção
            hash_table = HashTable(size=m_size, hash_function=hash_func)
            
            process = psutil.Process()
            mem_before = process.memory_info().rss / 1024 / 1024
            tracemalloc.start()
            
            start_time = time.perf_counter()
            total_iterations = 0
            
            for record in data:
                iterations = hash_table.insert(record)
                total_iterations += iterations
            
            insert_time = time.perf_counter() - start_time
            
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            mem_after = process.memory_info().rss / 1024 / 1024
            cpu_percent = process.cpu_percent(interval=0.1)
            
            # Métricas específicas da tabela hash
            load_factor = hash_table.get_load_factor()
            collision_rate = hash_table.get_collision_rate()
            avg_chain = hash_table.get_average_chain_length()
            max_chain = hash_table.get_max_chain_length()
            
            insert_rounds.append({
                'execution_time': insert_time,
                'memory_usage': mem_after - mem_before,
                'peak_memory': peak / 1024 / 1024,
                'cpu_percent': cpu_percent,
                'iterations': total_iterations,
                'load_factor': load_factor,
                'collision_rate': collision_rate,
                'avg_chain_length': avg_chain,
                'max_chain_length': max_chain
            })
            
            # Busca
            search_sample = random.sample(data, min(1000, len(data)))
            
            mem_before = process.memory_info().rss / 1024 / 1024
            tracemalloc.start()
            
            start_time = time.perf_counter()
            total_iterations = 0
            
            for record in search_sample:
                _, iterations = hash_table.search(record.matricula)
                total_iterations += iterations
            
            search_time = time.perf_counter() - start_time
            
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            mem_after = process.memory_info().rss / 1024 / 1024
            cpu_percent = process.cpu_percent(interval=0.1)
            
            search_rounds.append({
                'execution_time': search_time / len(search_sample),
                'memory_usage': (mem_after - mem_before) / len(search_sample),
                'peak_memory': peak / 1024 / 1024 / len(search_sample),
                'cpu_percent': cpu_percent,
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
        """Calcula métricas médias dos rounds."""
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
    
    def save_results(self, filename: str = "experiment_results.csv", 
                    detailed_filename: str = "experiment_details.csv"):
        """Salva resultados em arquivo CSV."""
        results_data = []
        detailed_data = []
        
        for result in self.results:
            stats = result.get_statistics()
            metrics = result.metrics
            
            # Cria linha base com informações comuns
            row = {
                'structure': result.structure_name,
                'data_size': result.data_size,
                'operation': result.operation,
                'mean_time': stats.get('mean_time', 0),
                'std_time': stats.get('std_time', 0),
                'mean_memory': stats.get('mean_memory', 0),
                'std_memory': stats.get('std_memory', 0),
                'mean_iterations': stats.get('mean_iterations', 0),
                'std_iterations': stats.get('std_iterations', 0),
                # Adiciona métricas de recursos
                'avg_cpu_percent': metrics.get('avg_cpu_percent', 0),
                'avg_memory_usage_mb': metrics.get('avg_memory_usage', 0),
                'avg_peak_memory_mb': metrics.get('avg_peak_memory', 0)
            }
            
            # Salva dados detalhados por rodada
            for i, round_data in enumerate(result.rounds):
                detailed_row = {
                    'structure': result.structure_name,
                    'data_size': result.data_size,
                    'operation': result.operation,
                    'round': i + 1,
                    'execution_time': round_data.get('execution_time', 0),
                    'memory_usage_mb': round_data.get('memory_usage', 0),
                    'peak_memory_mb': round_data.get('peak_memory', 0),
                    'cpu_percent': round_data.get('cpu_percent', 0),
                    'iterations': round_data.get('iterations', 0)
                }
                
                # Adiciona parâmetros específicos
                if result.structure_name == "HashTable":
                    detailed_row['hash_table_size'] = result.parameters.get('M', 0)
                    detailed_row['hash_function'] = result.parameters.get('hash_function', '')
                    # Métricas específicas de hash
                    if 'load_factor' in round_data:
                        detailed_row['load_factor'] = round_data['load_factor']
                        detailed_row['collision_rate'] = round_data.get('collision_rate', 0)
                        detailed_row['avg_chain_length'] = round_data.get('avg_chain_length', 0)
                        detailed_row['max_chain_length'] = round_data.get('max_chain_length', 0)
                else:
                    detailed_row['hash_table_size'] = ''
                    detailed_row['hash_function'] = ''
                    detailed_row['load_factor'] = ''
                    detailed_row['collision_rate'] = ''
                    detailed_row['avg_chain_length'] = ''
                    detailed_row['max_chain_length'] = ''
                
                if result.structure_name in ["BST", "AVL"]:
                    detailed_row['balanced'] = result.parameters.get('balanced', False)
                    if 'height' in round_data:
                        detailed_row['tree_height'] = round_data['height']
                    else:
                        detailed_row['tree_height'] = ''
                else:
                    detailed_row['balanced'] = ''
                    detailed_row['tree_height'] = ''
                
                detailed_data.append(detailed_row)
            
            # Adiciona parâmetros específicos
            if result.structure_name == "HashTable":
                row['hash_table_size'] = result.parameters.get('M', '')
                row['hash_function'] = result.parameters.get('hash_function', '')
                row['avg_load_factor'] = metrics.get('avg_load_factor', 0)
                row['avg_collision_rate'] = metrics.get('avg_collision_rate', 0)
                row['avg_chain_length'] = metrics.get('avg_avg_chain_length', 0)
                row['max_chain_length'] = metrics.get('avg_max_chain_length', 0)
            else:
                row['hash_table_size'] = ''
                row['hash_function'] = ''
                row['avg_load_factor'] = ''
                row['avg_collision_rate'] = ''
                row['avg_chain_length'] = ''
                row['max_chain_length'] = ''
            
            if result.structure_name in ["BST", "AVL"]:
                row['balanced'] = result.parameters.get('balanced', False)
                row['avg_height'] = metrics.get('avg_height', 0)
            else:
                row['balanced'] = ''
                row['avg_height'] = ''
            
            results_data.append(row)
        
        # Salva arquivo resumo
        df = pd.DataFrame(results_data)
        df.to_csv(filename, index=False)
        
        # Salva arquivo detalhado com todas as rodadas
        df_detailed = pd.DataFrame(detailed_data)
        df_detailed.to_csv(detailed_filename, index=False)
        
        print(f"\n✓ Resultados salvos em:")
        print(f"  • {filename} - Resumo estatístico")
        print(f"  • {detailed_filename} - Dados detalhados por rodada")


# ================================================================================
# SEÇÃO 5: ANÁLISE E VISUALIZAÇÃO
# ================================================================================

class ResultAnalyzer:
    """Analisador de resultados dos experimentos."""
    
    def __init__(self, results: List[ExperimentResult]):
        self.results = results
        self.df = self._create_dataframe()
    
    def _create_dataframe(self) -> pd.DataFrame:
        """Cria DataFrame com os resultados."""
        data = []
        for result in self.results:
            stats = result.get_statistics()
            row = {
                'structure': result.structure_name,
                'data_size': result.data_size,
                'operation': result.operation,
                'mean_time': stats.get('mean_time', 0),
                'std_time': stats.get('std_time', 0),
                'mean_iterations': stats.get('mean_iterations', 0),
                'std_iterations': stats.get('std_iterations', 0),
                **result.parameters
            }
            data.append(row)
        return pd.DataFrame(data)
    
    def print_complexity_analysis(self):
        """Imprime análise de complexidade teórica vs observada."""
        print("\n" + "=" * 80)
        print(" ANÁLISE DE COMPLEXIDADE ".center(80))
        print("=" * 80)
        
        complexities = {
            'LinearArray': {
                'insert': 'O(1)',
                'search': 'O(n)'
            },
            'BST': {
                'insert': 'O(log n) médio, O(n) pior caso',
                'search': 'O(log n) médio, O(n) pior caso'
            },
            'AVL': {
                'insert': 'O(log n)',
                'search': 'O(log n)'
            },
            'HashTable': {
                'insert': 'O(1) médio, O(n) pior caso',
                'search': 'O(1) médio, O(n) pior caso'
            }
        }
        
        for structure, ops in complexities.items():
            print(f"\n{structure}:")
            for op, complexity in ops.items():
                print(f"  {op}: {complexity}")
                
                # Análise empírica
                struct_data = self.df[(self.df['structure'] == structure) & 
                                     (self.df['operation'] == op)]
                
                if not struct_data.empty:
                    # Calcula taxa de crescimento
                    sizes = struct_data['data_size'].values
                    times = struct_data['mean_time'].values
                    
                    if len(sizes) > 1:
                        growth_rate = self._calculate_growth_rate(sizes, times)
                        print(f"    Taxa de crescimento observada: {growth_rate}")
    
    def _calculate_growth_rate(self, sizes, times):
        """Calcula a taxa de crescimento empírica."""
        if len(sizes) < 2:
            return "N/A"
        
        # Calcula a taxa de crescimento entre pontos consecutivos
        growth_rates = []
        for i in range(1, len(sizes)):
            size_ratio = sizes[i] / sizes[i-1]
            time_ratio = times[i] / times[i-1] if times[i-1] > 0 else 0
            
            if time_ratio > 0:
                # Estima o expoente: time = O(n^k)
                k = np.log(time_ratio) / np.log(size_ratio)
                growth_rates.append(k)
        
        if growth_rates:
            avg_k = np.mean(growth_rates)
            if avg_k < 0.5:
                return "~O(1) - Constante"
            elif avg_k < 1.5:
                return f"~O(n) - Linear (k≈{avg_k:.2f})"
            elif avg_k < 2.5:
                return f"~O(n²) - Quadrático (k≈{avg_k:.2f})"
            else:
                return f"~O(n^{avg_k:.2f})"
        
        return "Indeterminado"
    
    def generate_plots(self):
        """Gera gráficos de análise."""
        # Cria diretório para plots
        os.makedirs('plots', exist_ok=True)
        
        # Plot 1: Tempo de inserção por estrutura
        self._plot_insertion_times()
        
        # Plot 2: Tempo de busca por estrutura
        self._plot_search_times()
        
        # Plot 3: Comparação de iterações
        self._plot_iterations_comparison()
        
        # Plot 4: Análise específica de Hash Table
        self._plot_hash_analysis()
        
        # Plot 5: Altura das árvores
        self._plot_tree_heights()
        
        print("\n✓ Gráficos salvos no diretório 'plots/'")
    
    def _plot_insertion_times(self):
        """Plota tempos de inserção."""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        structures = ['LinearArray', 'BST', 'AVL']
        
        for struct in structures:
            data = self.df[(self.df['structure'] == struct) & 
                          (self.df['operation'] == 'insert')]
            if not data.empty:
                sizes = data['data_size'].values
                times = data['mean_time'].values
                errors = data['std_time'].values
                
                ax.errorbar(sizes, times, yerr=errors, 
                          label=struct, marker='o', capsize=5)
        
        ax.set_xlabel('Tamanho do Dataset (N)')
        ax.set_ylabel('Tempo de Inserção Total (s)')
        ax.set_title('Comparação de Tempo de Inserção entre Estruturas')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_xscale('log')
        ax.set_yscale('log')
        
        plt.tight_layout()
        plt.savefig('plots/insertion_times.png', dpi=150)
        plt.close()
    
    def _plot_search_times(self):
        """Plota tempos de busca."""
        fig, ax = plt.subplots(figsize=(12, 6))
        
        structures = ['LinearArray', 'BST', 'AVL']
        
        for struct in structures:
            data = self.df[(self.df['structure'] == struct) & 
                          (self.df['operation'] == 'search')]
            if not data.empty:
                sizes = data['data_size'].values
                times = data['mean_time'].values * 1000  # Converter para ms
                errors = data['std_time'].values * 1000
                
                ax.errorbar(sizes, times, yerr=errors, 
                          label=struct, marker='s', capsize=5)
        
        ax.set_xlabel('Tamanho do Dataset (N)')
        ax.set_ylabel('Tempo Médio de Busca (ms)')
        ax.set_title('Comparação de Tempo de Busca entre Estruturas')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_xscale('log')
        ax.set_yscale('log')
        
        plt.tight_layout()
        plt.savefig('plots/search_times.png', dpi=150)
        plt.close()
    
    def _plot_iterations_comparison(self):
        """Plota comparação de iterações."""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Inserção
        for struct in ['LinearArray', 'BST', 'AVL']:
            data = self.df[(self.df['structure'] == struct) & 
                          (self.df['operation'] == 'insert')]
            if not data.empty:
                sizes = data['data_size'].values
                iterations = data['mean_iterations'].values
                ax1.plot(sizes, iterations, label=struct, marker='o')
        
        ax1.set_xlabel('Tamanho do Dataset (N)')
        ax1.set_ylabel('Número de Iterações')
        ax1.set_title('Iterações durante Inserção')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        ax1.set_xscale('log')
        ax1.set_yscale('log')
        
        # Busca
        for struct in ['LinearArray', 'BST', 'AVL']:
            data = self.df[(self.df['structure'] == struct) & 
                          (self.df['operation'] == 'search')]
            if not data.empty:
                sizes = data['data_size'].values
                iterations = data['mean_iterations'].values
                ax2.plot(sizes, iterations, label=struct, marker='s')
        
        ax2.set_xlabel('Tamanho do Dataset (N)')
        ax2.set_ylabel('Número de Iterações')
        ax2.set_title('Iterações durante Busca')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_xscale('log')
        ax2.set_yscale('log')
        
        plt.tight_layout()
        plt.savefig('plots/iterations_comparison.png', dpi=150)
        plt.close()
    
    def _plot_hash_analysis(self):
        """Plota análise específica de tabela hash."""
        hash_data = self.df[(self.df['structure'] == 'HashTable') & 
                           (self.df['operation'] == 'insert')]
        
        if hash_data.empty:
            return
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        
        # Por função hash
        for func in ['division', 'multiplication', 'folding']:
            func_data = hash_data[hash_data.get('hash_function', '') == func]
            if not func_data.empty:
                # Tempo por M
                for m in [100, 1000, 5000]:
                    m_data = func_data[func_data.get('M', 0) == m]
                    if not m_data.empty:
                        sizes = m_data['data_size'].values
                        times = m_data['mean_time'].values
                        ax1.plot(sizes, times, label=f'{func} (M={m})', marker='o')
        
        ax1.set_xlabel('Tamanho do Dataset (N)')
        ax1.set_ylabel('Tempo de Inserção (s)')
        ax1.set_title('Desempenho por Função Hash e Tamanho da Tabela')
        ax1.legend(fontsize=8)
        ax1.grid(True, alpha=0.3)
        
        # Load Factor
        for m in [100, 1000, 5000]:
            m_data = hash_data[hash_data.get('M', 0) == m]
            if not m_data.empty:
                sizes = m_data['data_size'].values
                load_factors = sizes / m
                times = m_data['mean_time'].values
                ax2.plot(load_factors, times, label=f'M={m}', marker='s')
        
        ax2.set_xlabel('Load Factor (N/M)')
        ax2.set_ylabel('Tempo de Inserção (s)')
        ax2.set_title('Impacto do Load Factor')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Placeholder para análise adicional
        ax3.text(0.5, 0.5, 'Análise de Colisões\n(dados específicos necessários)', 
                ha='center', va='center')
        ax3.set_title('Taxa de Colisões')
        
        # Comparação geral
        ax4.bar(['Linear', 'BST', 'AVL', 'Hash'], 
               [1, np.log2(10000), np.log2(10000), 1],
               color=['blue', 'green', 'orange', 'red'])
        ax4.set_ylabel('Complexidade Esperada (escala relativa)')
        ax4.set_title('Complexidade Teórica para N=10.000')
        
        plt.tight_layout()
        plt.savefig('plots/hash_analysis.png', dpi=150)
        plt.close()
    
    def _plot_tree_heights(self):
        """Plota alturas das árvores."""
        bst_heights = []
        avl_heights = []
        sizes = []
        
        for result in self.results:
            if result.operation == 'insert':
                if result.structure_name == 'BST':
                    if result.rounds and 'height' in result.rounds[0]:
                        heights = [r['height'] for r in result.rounds]
                        bst_heights.append(np.mean(heights))
                        if result.data_size not in sizes:
                            sizes.append(result.data_size)
                elif result.structure_name == 'AVL':
                    if result.rounds and 'height' in result.rounds[0]:
                        heights = [r['height'] for r in result.rounds]
                        avl_heights.append(np.mean(heights))
        
        if not sizes:
            return
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Plota alturas observadas
        if bst_heights:
            ax.plot(sizes[:len(bst_heights)], bst_heights, 
                   label='BST (observado)', marker='o')
        if avl_heights:
            ax.plot(sizes[:len(avl_heights)], avl_heights, 
                   label='AVL (observado)', marker='s')
        
        # Plota alturas teóricas
        theoretical_sizes = np.array(sizes)
        theoretical_log = np.log2(theoretical_sizes)
        ax.plot(theoretical_sizes, theoretical_log, 
               label='log₂(n) (ótimo)', linestyle='--', alpha=0.7)
        
        ax.set_xlabel('Tamanho do Dataset (N)')
        ax.set_ylabel('Altura da Árvore')
        ax.set_title('Altura das Árvores: BST vs AVL')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_xscale('log')
        
        plt.tight_layout()
        plt.savefig('plots/tree_heights.png', dpi=150)
        plt.close()


# ================================================================================
# SEÇÃO 6: FUNÇÕES DE APRESENTAÇÃO
# ================================================================================

def print_header():
    """Imprime cabeçalho do programa."""
    print("=" * 80)
    print(" ANÁLISE COMPARATIVA DE ESTRUTURAS DE DADOS ".center(80))
    print(" PUCPR - Fundamentos de Algoritmos ".center(80))
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
    """Imprime tabela resumo dos resultados."""
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
            # Filtra apenas estruturas principais para clareza
            main_structures = op_df[op_df['Estrutura'].isin(['LinearArray', 'BST', 'AVL'])]
            if not main_structures.empty:
                print("\n> Estruturas Principais:")
                print(tabulate(main_structures, headers='keys', tablefmt='grid', showindex=False))
            
            # Hash tables separadamente
            hash_tables = op_df[op_df['Estrutura'] == 'HashTable']
            if not hash_tables.empty:
                print("\n> Tabelas Hash:")
                # Mostra apenas uma amostra para não poluir a saída
                sample = hash_tables.groupby(['N', 'Parâmetros']).first().reset_index()
                print(tabulate(sample.head(10), headers='keys', tablefmt='grid', showindex=False))


def print_hash_analysis(results):
    """Imprime análise específica de tabela hash."""
    print("\n" + "=" * 80)
    print(" ANÁLISE ESPECÍFICA - TABELA HASH ".center(80))
    print("=" * 80)
    
    hash_results = [r for r in results if r.structure_name == "HashTable" and r.operation == "insert"]
    
    if not hash_results:
        return
    
    analysis_data = []
    
    for result in hash_results[:10]:  # Limita para não poluir saída
        metrics = result.metrics
        analysis_data.append({
            'N': result.data_size,
            'M': result.parameters['M'],
            'Função Hash': result.parameters['hash_function'],
            'Load Factor': f"{metrics.get('avg_load_factor', 0):.3f}",
            'Taxa Colisão': f"{metrics.get('avg_collision_rate', 0):.3f}",
            'Comp. Médio': f"{metrics.get('avg_avg_chain_length', 0):.2f}",
            'Comp. Máx': f"{metrics.get('avg_max_chain_length', 0):.0f}"
        })
    
    df = pd.DataFrame(analysis_data)
    print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))


def print_tree_analysis(results):
    """Imprime análise específica de árvores."""
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
            'Altura Teórica': f"{math.log2(result.data_size):.1f}",
            'Iterações': f"{metrics.get('avg_iterations', 0):.1f}",
            'Tempo (s)': f"{result.get_statistics().get('mean_time', 0):.6f}"
        })
    
    df = pd.DataFrame(analysis_data)
    print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))


# ================================================================================
# SEÇÃO 7: FUNÇÃO PRINCIPAL
# ================================================================================

def main():
    """Função principal do programa."""
    try:
        # Imprime cabeçalho
        print_header()
        
        # Configuração dos experimentos
        data_sizes = [1000, 5000, 10000]
        num_rounds = 5
        
        # Cria executor de experimentos
        runner = ExperimentRunner(data_sizes=data_sizes, num_rounds=num_rounds)
        
        # Executa experimentos
        print("\nIniciando experimentos...")
        print("(Isso pode levar alguns minutos...)")
        
        results = runner.run_all_experiments()
        
        # Salva resultados
        runner.save_results("experiment_results.csv")
        
        # Exibe resumo
        print_summary_table(results)
        print_hash_analysis(results)
        print_tree_analysis(results)
        
        # Análise de complexidade
        analyzer = ResultAnalyzer(results)
        analyzer.print_complexity_analysis()
        
        # Gera gráficos
        print("\nGerando gráficos de análise...")
        analyzer.generate_plots()
        
        print("\n" + "=" * 80)
        print(" EXPERIMENTO CONCLUÍDO COM SUCESSO ".center(80))
        print("=" * 80)
        print("\nArquivos gerados:")
        print("  • experiment_results.csv - Resumo estatístico com médias e desvios")
        print("  • experiment_details.csv - Dados detalhados de cada rodada")
        print("  • plots/ - Diretório com gráficos de análise")
        print("\nMétricas coletadas:")
        print("  • Tempo de processamento (alta precisão)")
        print("  • Consumo de CPU (%)")
        print("  • Uso de memória (MB)")
        print("  • Pico de memória (MB)")  
        print("  • Número de iterações")
        print("\nPara executar novamente:")
        print(f"  python {sys.argv[0]}")
        
    except KeyboardInterrupt:
        print("\n\nExperimento interrompido pelo usuário.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nErro durante execução: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


# ================================================================================
# PONTO DE ENTRADA
# ================================================================================

if __name__ == "__main__":
    # Verifica dependências
    required_packages = ['numpy', 'pandas', 'matplotlib', 'psutil', 'tabulate']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("ERRO: Pacotes necessários não instalados!")
        print(f"Execute: pip install {' '.join(missing_packages)}")
        sys.exit(1)
    
    # Executa programa principal
    main()