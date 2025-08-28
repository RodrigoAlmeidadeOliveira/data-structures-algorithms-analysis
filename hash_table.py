from typing import Optional, List, Callable
from models import Record


class HashTable:
    def __init__(self, size: int = 100, hash_function: str = 'division'):
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
        return key % self.size
    
    def _hash_multiplication(self, key: int) -> int:
        A = 0.6180339887  # (√5 - 1) / 2 - Constante de Knuth
        return int(self.size * ((key * A) % 1))
    
    def _hash_folding(self, key: int) -> int:
        # Divide a chave em partes e soma
        key_str = str(key)
        chunk_size = 3
        chunks = [key_str[i:i+chunk_size] for i in range(0, len(key_str), chunk_size)]
        total = sum(int(chunk) for chunk in chunks)
        return total % self.size
    
    def insert(self, record: Record) -> int:
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
    
    def search(self, matricula: int) -> tuple[Optional[Record], int]:
        self.iterations = 1
        index = self.hash_func(matricula)
        
        for record in self.table[index]:
            self.iterations += 1
            if record.matricula == matricula:
                return record, self.iterations
        
        return None, self.iterations
    
    def get_load_factor(self) -> float:
        return self.total_elements / self.size
    
    def get_collision_rate(self) -> float:
        if self.total_elements == 0:
            return 0.0
        return self.collisions / self.total_elements
    
    def get_average_chain_length(self) -> float:
        non_empty_buckets = sum(1 for bucket in self.table if bucket)
        if non_empty_buckets == 0:
            return 0.0
        return self.total_elements / non_empty_buckets
    
    def get_max_chain_length(self) -> int:
        return max(len(bucket) for bucket in self.table)
    
    def size_count(self) -> int:
        return self.total_elements
    
    def clear(self):
        self.table = [[] for _ in range(self.size)]
        self.iterations = 0
        self.collisions = 0
        self.total_elements = 0