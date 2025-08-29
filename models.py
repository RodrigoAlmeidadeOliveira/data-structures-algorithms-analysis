import random
import string
from typing import Any, Optional, List
import os

# Importa módulo de geração de dados de estudantes
try:
    from student_registration_data import StudentDataGenerator, StudentRecord
    STUDENT_DATA_AVAILABLE = True
except ImportError:
    STUDENT_DATA_AVAILABLE = False
    print("Módulo student_registration_data não encontrado. Usando gerador básico.")


class Record:
    """Classe de registro compatível com StudentRecord e dados básicos."""
    
    def __init__(self, matricula: int, nome: str, salario: float, codigo_setor: int, 
                 cpf: str = None, email: str = None, telefone: str = None, 
                 cargo: str = None, status: str = "Ativo", **kwargs):
        # Campos básicos (compatibilidade com versão original)
        self.matricula = int(matricula)  # Garante que seja int
        self.nome = nome
        self.salario = salario
        self.codigo_setor = codigo_setor
        
        # Campos estendidos (compatibilidade com StudentRecord)
        self.cpf = cpf or self._generate_cpf()
        self.email = email or self._generate_email(nome)
        self.telefone = telefone or self._generate_phone()
        self.cargo = cargo or "Não informado"
        self.status = status
        
        # Campos adicionais do StudentRecord
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def _generate_cpf(self) -> str:
        """Gera CPF fictício."""
        cpf_digits = [random.randint(0, 9) for _ in range(11)]
        cpf_str = ''.join(map(str, cpf_digits))
        return f"{cpf_str[:3]}.{cpf_str[3:6]}.{cpf_str[6:9]}-{cpf_str[9:11]}"
    
    def _generate_phone(self) -> str:
        """Gera telefone fictício."""
        area_code = random.randint(11, 99)
        number = random.randint(900000000, 999999999)
        return f"({area_code:02d}) {str(number)[:5]}-{str(number)[5:]}"
    
    def _generate_email(self, nome: str) -> str:
        """Gera email baseado no nome."""
        nome_parts = nome.lower().split()
        if len(nome_parts) >= 2:
            username = f"{nome_parts[0]}.{nome_parts[-1]}"
        else:
            username = nome_parts[0] if nome_parts else "user"
        
        # Remove caracteres especiais
        username = ''.join(c for c in username if c.isalnum() or c == '.')
        return f"{username}@university.edu"
    
    def __repr__(self):
        return f"Record(matricula={self.matricula}, nome='{self.nome}', salario={self.salario:.2f}, setor={self.codigo_setor})"
    
    def __eq__(self, other):
        if isinstance(other, (Record, StudentRecord)):
            return str(self.matricula) == str(other.matricula)
        return False
    
    def __lt__(self, other):
        if isinstance(other, (Record, StudentRecord)):
            return str(self.matricula) < str(other.matricula)
        return NotImplemented
    
    def __hash__(self):
        return hash(str(self.matricula))
    
    @classmethod
    def from_student_record(cls, student_record: 'StudentRecord') -> 'Record':
        """Converte StudentRecord para Record."""
        return cls(
            matricula=int(student_record.matricula),
            nome=student_record.nome,
            salario=student_record.salario,
            codigo_setor=student_record.codigo_setor,
            cpf=student_record.cpf,
            email=student_record.email,
            telefone=student_record.telefone,
            cargo=student_record.cargo,
            status=student_record.status,
            data_ingresso=getattr(student_record, 'data_ingresso', None),
            endereco=getattr(student_record, 'endereco', None),
            nivel=getattr(student_record, 'nivel', None)
        )


class DataGenerator:
    """Gerador de dados com suporte a dados realísticos de estudantes."""
    
    def __init__(self, use_realistic_data: bool = True, data_source: str = "generate"):
        """
        Args:
            use_realistic_data: Se True, usa dados realísticos quando disponível
            data_source: 'generate' para gerar novos dados, 'file' para carregar de arquivo
        """
        self.use_realistic_data = use_realistic_data and STUDENT_DATA_AVAILABLE
        self.data_source = data_source
        
        if self.use_realistic_data:
            self.student_generator = StudentDataGenerator()
    
    def generate_records(self, n: int, seed: Optional[int] = None) -> List[Record]:
        """Gera registros usando dados realísticos ou básicos."""
        if seed is not None:
            random.seed(seed)
        
        if self.use_realistic_data:
            return self._generate_realistic_records(n)
        else:
            return self._generate_basic_records(n)
    
    def _generate_realistic_records(self, n: int) -> List[Record]:
        """Gera registros realísticos usando StudentDataGenerator."""
        
        # Verifica se existe arquivo pré-gerado
        filename = f"student_data_{n}.json"
        
        if self.data_source == "file" and os.path.exists(filename):
            try:
                print(f"Carregando dados de {filename}...")
                student_records = self.student_generator.load_from_json(filename)
                
                # Se o arquivo tem menos registros que o necessário, complementa
                if len(student_records) < n:
                    print(f"Arquivo contém {len(student_records)} registros. Gerando {n - len(student_records)} adicionais...")
                    additional_records = self.student_generator.generate_dataset(n - len(student_records))
                    student_records.extend(additional_records)
                
                # Se tem mais registros que o necessário, seleciona uma amostra
                if len(student_records) > n:
                    student_records = random.sample(student_records, n)
                
            except Exception as e:
                print(f"Erro ao carregar {filename}: {e}. Gerando novos dados...")
                student_records = self.student_generator.generate_dataset(n)
        else:
            print(f"Gerando {n} registros realísticos...")
            student_records = self.student_generator.generate_dataset(n)
        
        # Converte para Record
        records = [Record.from_student_record(sr) for sr in student_records]
        
        print(f"Gerados {len(records)} registros realísticos")
        return records
    
    def _generate_basic_records(self, n: int) -> List[Record]:
        """Gera registros básicos (versão original)."""
        print(f"Gerando {n} registros básicos...")
        
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
    
    def load_from_file(self, filename: str, n: int) -> List[Record]:
        """Carrega registros de arquivo JSON."""
        if not STUDENT_DATA_AVAILABLE:
            print("StudentDataGenerator não disponível. Gerando dados básicos.")
            return self._generate_basic_records(n)
        
        try:
            student_records = self.student_generator.load_from_json(filename)
            
            # Ajusta quantidade
            if len(student_records) > n:
                student_records = random.sample(student_records, n)
            
            records = [Record.from_student_record(sr) for sr in student_records]
            print(f"Carregados {len(records)} registros de {filename}")
            return records
            
        except Exception as e:
            print(f"Erro ao carregar {filename}: {e}. Gerando dados básicos.")
            return self._generate_basic_records(n)
    
    def get_data_statistics(self, records: List[Record]) -> dict:
        """Retorna estatísticas dos dados gerados."""
        if not records:
            return {}
        
        stats = {
            'total_records': len(records),
            'salary_stats': {
                'min': min(r.salario for r in records),
                'max': max(r.salario for r in records),
                'mean': sum(r.salario for r in records) / len(records)
            },
            'unique_sectors': len(set(r.codigo_setor for r in records)),
            'data_type': 'realistic' if self.use_realistic_data else 'basic'
        }
        
        # Estatísticas por setor
        sector_counts = {}
        for record in records:
            sector_counts[record.codigo_setor] = sector_counts.get(record.codigo_setor, 0) + 1
        
        stats['sector_distribution'] = sector_counts
        
        return stats