import random
import string
from typing import Any, Optional


class Record:
    def __init__(self, matricula: int, nome: str, salario: float, codigo_setor: int):
        self.matricula = matricula  # 9 dígitos
        self.nome = nome
        self.salario = salario
        self.codigo_setor = codigo_setor
    
    def __repr__(self):
        return f"Record(matricula={self.matricula}, nome='{self.nome}', salario={self.salario:.2f}, codigo_setor={self.codigo_setor})"
    
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
    @staticmethod
    def generate_records(n: int, seed: Optional[int] = None) -> list[Record]:
        if seed is not None:
            random.seed(seed)
        
        records = []
        used_matriculas = set()
        
        for _ in range(n):
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
        
        return records