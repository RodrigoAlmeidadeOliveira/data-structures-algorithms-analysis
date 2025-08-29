import random
import json
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Any
import string

@dataclass
class StudentRecord:
    """Estrutura de dados para registro de matrícula de estudante/funcionário"""
    matricula: str          # 9 dígitos
    nome: str              # Nome completo
    salario: float         # Salário/Bolsa
    codigo_setor: int      # Código do setor/departamento
    cpf: str               # CPF (para buscas alternativas)
    data_ingresso: str     # Data de ingresso
    status: str            # Ativo, Inativo, Afastado
    email: str             # Email institucional
    telefone: str          # Telefone de contato
    endereco: str          # Endereço
    cargo: str             # Cargo/Função
    nivel: str             # Graduação, Mestrado, Doutorado, etc.
    
    def __hash__(self):
        """Permite usar como chave em dicionários"""
        return hash(self.matricula)
    
    def __eq__(self, other):
        """Comparação por matrícula"""
        if isinstance(other, StudentRecord):
            return self.matricula == other.matricula
        return False
    
    def __lt__(self, other):
        """Ordenação por matrícula"""
        if isinstance(other, StudentRecord):
            return self.matricula < other.matricula
        return False

class StudentDataGenerator:
    """Gerador de dados sintéticos para experimentos com cadastro de matrículas"""
    
    def __init__(self):
        self.nomes = [
            "Ana Silva Santos", "João Pereira Lima", "Maria Oliveira Costa", "Carlos Rodrigues Alves",
            "Fernanda Souza Martins", "Pedro Santos Oliveira", "Juliana Costa Ferreira", "Rafael Lima Santos",
            "Amanda Alves Rodrigues", "Thiago Martins Silva", "Camila Ferreira Costa", "Lucas Santos Pereira",
            "Beatriz Oliveira Lima", "Gabriel Costa Santos", "Larissa Silva Alves", "Mateus Pereira Costa",
            "Isabela Lima Martins", "André Santos Silva", "Carolina Alves Ferreira", "Diego Martins Lima",
            "Vanessa Costa Pereira", "Bruno Silva Santos", "Priscila Oliveira Alves", "Felipe Lima Costa",
            "Natália Santos Martins", "Ricardo Pereira Silva", "Patrícia Costa Alves", "Rodrigo Lima Santos",
            "Márcia Silva Costa", "Eduardo Santos Pereira", "Daniela Alves Lima", "Fábio Costa Santos",
            "Cristina Lima Silva", "Leandro Santos Costa", "Mônica Pereira Alves", "Alessandro Lima Santos",
            "Renata Costa Silva", "Marcelo Santos Lima", "Adriana Silva Costa", "Gustavo Lima Pereira",
            "Luciana Santos Alves", "Vinicius Costa Lima", "Simone Silva Santos", "Paulo Pereira Costa",
            "Letícia Lima Alves", "Fernando Santos Silva", "Roberta Costa Pereira", "Henrique Lima Santos",
            "Carla Silva Costa", "Antônio Santos Lima", "Jéssica Costa Silva"
        ]
        
        self.setores = {
            1001: "Administração Acadêmica",
            1002: "Recursos Humanos", 
            1003: "Tecnologia da Informação",
            1004: "Biblioteca",
            1005: "Laboratório de Pesquisa",
            1006: "Coordenação de Curso",
            1007: "Secretaria",
            1008: "Financeiro",
            1009: "Manutenção",
            1010: "Segurança"
        }
        
        self.cargos = [
            "Estudante Graduação", "Estudante Mestrado", "Estudante Doutorado",
            "Professor Adjunto", "Professor Associado", "Professor Titular",
            "Técnico Administrativo", "Analista de Sistemas", "Bibliotecário",
            "Coordenador", "Secretário", "Auxiliar", "Pesquisador",
            "Monitor", "Bolsista IC", "Bolsista PIBIC"
        ]
        
        self.niveis = [
            "Ensino Médio", "Graduação", "Especialização", 
            "Mestrado", "Doutorado", "Pós-Doutorado"
        ]
        
        self.status_options = ["Ativo", "Inativo", "Afastado", "Licença"]
        
        # Para garantir matrículas únicas
        self.used_matriculas = set()
        
    def generate_matricula(self) -> str:
        """Gera uma matrícula única de 9 dígitos"""
        while True:
            # Formato: YYYYNNNNN (Ano + 5 dígitos sequenciais)
            year = random.randint(2015, 2024)
            sequence = random.randint(10000, 99999)
            matricula = f"{year}{sequence}"
            
            if matricula not in self.used_matriculas:
                self.used_matriculas.add(matricula)
                return matricula
    
    def generate_cpf(self) -> str:
        """Gera um CPF fictício no formato XXX.XXX.XXX-XX"""
        cpf_digits = [random.randint(0, 9) for _ in range(11)]
        cpf_str = ''.join(map(str, cpf_digits))
        return f"{cpf_str[:3]}.{cpf_str[3:6]}.{cpf_str[6:9]}-{cpf_str[9:11]}"
    
    def generate_phone(self) -> str:
        """Gera um telefone fictício no formato (XX) XXXXX-XXXX"""
        area_code = random.randint(11, 99)
        number = random.randint(900000000, 999999999)
        return f"({area_code:02d}) {str(number)[:5]}-{str(number)[5:]}"
    
    def generate_email(self, nome: str) -> str:
        """Gera email institucional baseado no nome"""
        nome_parts = nome.lower().split()
        if len(nome_parts) >= 2:
            username = f"{nome_parts[0]}.{nome_parts[-1]}"
        else:
            username = nome_parts[0]
        
        # Remove acentos e caracteres especiais
        username = username.replace('ã', 'a').replace('ç', 'c').replace('é', 'e')
        username = ''.join(c for c in username if c.isalnum() or c == '.')
        
        domains = ["universidade.edu.br", "instituto.edu.br", "faculdade.edu.br"]
        return f"{username}@{random.choice(domains)}"
    
    def generate_address(self) -> str:
        """Gera endereço fictício"""
        street_names = [
            "Rua das Flores", "Av. Principal", "Rua do Comércio", "Av. Universitária",
            "Rua da Paz", "Av. Central", "Rua São José", "Av. Independência"
        ]
        number = random.randint(1, 9999)
        neighborhood = random.choice(["Centro", "Jardim América", "Vila Nova", "Bairro Alto"])
        city = random.choice(["São Paulo", "Rio de Janeiro", "Belo Horizonte", "Salvador"])
        return f"{random.choice(street_names)}, {number} - {neighborhood}, {city}"
    
    def generate_salary(self, cargo: str) -> float:
        """Gera salário baseado no cargo"""
        salary_ranges = {
            "Estudante": (400, 1200),
            "Monitor": (500, 800),
            "Bolsista": (600, 1500),
            "Técnico": (2500, 4500),
            "Analista": (4000, 8000),
            "Professor Adjunto": (6000, 12000),
            "Professor Associado": (8000, 15000),
            "Professor Titular": (12000, 25000),
            "Coordenador": (7000, 15000),
            "Bibliotecário": (3000, 6000)
        }
        
        # Determina faixa salarial baseada no cargo
        for key, (min_sal, max_sal) in salary_ranges.items():
            if key.lower() in cargo.lower():
                return round(random.uniform(min_sal, max_sal), 2)
        
        # Padrão se não encontrar categoria
        return round(random.uniform(1000, 5000), 2)
    
    def generate_date(self) -> str:
        """Gera data de ingresso aleatória"""
        start_date = datetime(2010, 1, 1)
        end_date = datetime(2024, 12, 31)
        time_between = end_date - start_date
        days_between = time_between.days
        random_days = random.randrange(days_between)
        random_date = start_date + timedelta(days=random_days)
        return random_date.strftime("%Y-%m-%d")
    
    def generate_student_record(self) -> StudentRecord:
        """Gera um registro completo de estudante/funcionário"""
        nome = random.choice(self.nomes)
        cargo = random.choice(self.cargos)
        
        return StudentRecord(
            matricula=self.generate_matricula(),
            nome=nome,
            salario=self.generate_salary(cargo),
            codigo_setor=random.choice(list(self.setores.keys())),
            cpf=self.generate_cpf(),
            data_ingresso=self.generate_date(),
            status=random.choice(self.status_options),
            email=self.generate_email(nome),
            telefone=self.generate_phone(),
            endereco=self.generate_address(),
            cargo=cargo,
            nivel=random.choice(self.niveis)
        )
    
    def generate_dataset(self, size: int) -> List[StudentRecord]:
        """Gera um conjunto de dados de tamanho especificado"""
        return [self.generate_student_record() for _ in range(size)]
    
    def save_to_json(self, records: List[StudentRecord], filename: str):
        """Salva registros em arquivo JSON"""
        data = [asdict(record) for record in records]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load_from_json(self, filename: str) -> List[StudentRecord]:
        """Carrega registros de arquivo JSON"""
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return [StudentRecord(**record) for record in data]

def main():
    """Gera conjuntos de dados para diferentes tamanhos"""
    generator = StudentDataGenerator()
    
    # Gera datasets de diferentes tamanhos
    sizes = [1000, 5000, 10000, 25000, 50000]
    
    for size in sizes:
        print(f"Gerando dataset com {size} registros...")
        records = generator.generate_dataset(size)
        filename = f"student_data_{size}.json"
        generator.save_to_json(records, filename)
        print(f"Dataset salvo em: {filename}")
        
        # Mostra estatísticas básicas
        setores_count = {}
        salario_total = 0
        
        for record in records:
            setores_count[record.codigo_setor] = setores_count.get(record.codigo_setor, 0) + 1
            salario_total += record.salario
        
        print(f"  - Total de registros: {len(records)}")
        print(f"  - Setores únicos: {len(setores_count)}")
        print(f"  - Salário médio: R$ {salario_total/len(records):.2f}")
        print(f"  - Matrícula menor: {min(record.matricula for record in records)}")
        print(f"  - Matrícula maior: {max(record.matricula for record in records)}")
        print()

if __name__ == "__main__":
    main()