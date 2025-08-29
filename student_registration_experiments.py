import json
import time
import psutil
import os
import random
from typing import List, Dict, Any, Tuple
from student_registration_data import StudentRecord, StudentDataGenerator
import matplotlib.pyplot as plt
import numpy as np
from dataclasses import asdict

class StudentRegistrationSystem:
    """Sistema de cadastro usando diferentes estruturas de dados"""
    
    def __init__(self):
        self.records = []
        self.hash_table_matricula = {}
        self.hash_table_cpf = {}
        self.hash_table_setor = {}
        self.sorted_by_matricula = []
        self.sorted_by_nome = []
        
    def add_record(self, record: StudentRecord):
        """Adiciona um registro ao sistema"""
        self.records.append(record)
        self.hash_table_matricula[record.matricula] = record
        self.hash_table_cpf[record.cpf] = record
        
        # Hash table por setor (lista de registros por setor)
        if record.codigo_setor not in self.hash_table_setor:
            self.hash_table_setor[record.codigo_setor] = []
        self.hash_table_setor[record.codigo_setor].append(record)
    
    def search_by_matricula_linear(self, matricula: str) -> StudentRecord:
        """Busca linear por matrícula"""
        for record in self.records:
            if record.matricula == matricula:
                return record
        return None
    
    def search_by_matricula_hash(self, matricula: str) -> StudentRecord:
        """Busca por hash table - matrícula"""
        return self.hash_table_matricula.get(matricula)
    
    def search_by_cpf_hash(self, cpf: str) -> StudentRecord:
        """Busca por hash table - CPF"""
        return self.hash_table_cpf.get(cpf)
    
    def search_by_setor(self, codigo_setor: int) -> List[StudentRecord]:
        """Retorna todos registros de um setor"""
        return self.hash_table_setor.get(codigo_setor, [])
    
    def search_by_nome_linear(self, nome: str) -> List[StudentRecord]:
        """Busca linear por nome (busca parcial)"""
        results = []
        nome_lower = nome.lower()
        for record in self.records:
            if nome_lower in record.nome.lower():
                results.append(record)
        return results
    
    def search_by_salary_range(self, min_salary: float, max_salary: float) -> List[StudentRecord]:
        """Busca por faixa salarial"""
        results = []
        for record in self.records:
            if min_salary <= record.salario <= max_salary:
                results.append(record)
        return results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Retorna estatísticas do sistema"""
        if not self.records:
            return {}
        
        salarios = [r.salario for r in self.records]
        setores = {}
        status_count = {}
        cargos = {}
        
        for record in self.records:
            setores[record.codigo_setor] = setores.get(record.codigo_setor, 0) + 1
            status_count[record.status] = status_count.get(record.status, 0) + 1
            cargos[record.cargo] = cargos.get(record.cargo, 0) + 1
        
        return {
            'total_records': len(self.records),
            'salary_stats': {
                'mean': np.mean(salarios),
                'median': np.median(salarios),
                'std': np.std(salarios),
                'min': min(salarios),
                'max': max(salarios)
            },
            'sector_distribution': setores,
            'status_distribution': status_count,
            'position_distribution': cargos
        }

class StudentRegistrationBenchmark:
    """Benchmark para operações no sistema de cadastro"""
    
    def __init__(self):
        self.results = []
        
    def measure_resources(self, func, *args, **kwargs):
        """Mede tempo, memória e CPU de uma função"""
        # Medição inicial
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        initial_cpu_percent = process.cpu_percent()
        
        # Execução e medição de tempo
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        
        # Medição final
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        final_cpu_percent = process.cpu_percent()
        
        execution_time = end_time - start_time
        memory_used = final_memory - initial_memory
        cpu_usage = final_cpu_percent
        
        return result, execution_time, memory_used, cpu_usage
    
    def benchmark_insertion(self, records: List[StudentRecord]) -> Dict[str, Any]:
        """Benchmark de inserção de registros"""
        system = StudentRegistrationSystem()
        
        insert_times = []
        memory_usage = []
        
        for i, record in enumerate(records):
            _, exec_time, mem_used, cpu_usage = self.measure_resources(system.add_record, record)
            insert_times.append(exec_time)
            memory_usage.append(mem_used)
            
            # Log a cada 1000 inserções para datasets grandes
            if (i + 1) % 1000 == 0:
                print(f"Inseridos {i + 1}/{len(records)} registros")
        
        return {
            'operation': 'insertion',
            'total_records': len(records),
            'total_time': sum(insert_times),
            'avg_time_per_record': np.mean(insert_times),
            'std_time_per_record': np.std(insert_times),
            'avg_memory_usage': np.mean(memory_usage),
            'max_memory_usage': max(memory_usage) if memory_usage else 0,
            'system': system
        }
    
    def benchmark_search_operations(self, system: StudentRegistrationSystem, records: List[StudentRecord], num_searches: int = 1000) -> Dict[str, Any]:
        """Benchmark de operações de busca"""
        
        # Seleciona registros aleatórios para busca
        search_records = random.sample(records, min(num_searches, len(records)))
        
        results = {
            'search_by_matricula_linear': [],
            'search_by_matricula_hash': [],
            'search_by_cpf_hash': [],
            'search_by_nome_partial': [],
            'search_by_setor': [],
            'search_by_salary_range': []
        }
        
        print(f"Executando {num_searches} buscas de cada tipo...")
        
        # Busca por matrícula (linear)
        for record in search_records:
            _, exec_time, mem_used, cpu_usage = self.measure_resources(
                system.search_by_matricula_linear, record.matricula
            )
            results['search_by_matricula_linear'].append({
                'time': exec_time,
                'memory': mem_used,
                'cpu': cpu_usage
            })
        
        # Busca por matrícula (hash)
        for record in search_records:
            _, exec_time, mem_used, cpu_usage = self.measure_resources(
                system.search_by_matricula_hash, record.matricula
            )
            results['search_by_matricula_hash'].append({
                'time': exec_time,
                'memory': mem_used,
                'cpu': cpu_usage
            })
        
        # Busca por CPF (hash)
        for record in search_records:
            _, exec_time, mem_used, cpu_usage = self.measure_resources(
                system.search_by_cpf_hash, record.cpf
            )
            results['search_by_cpf_hash'].append({
                'time': exec_time,
                'memory': mem_used,
                'cpu': cpu_usage
            })
        
        # Busca por nome (parcial)
        for record in search_records:
            first_name = record.nome.split()[0]
            _, exec_time, mem_used, cpu_usage = self.measure_resources(
                system.search_by_nome_linear, first_name
            )
            results['search_by_nome_partial'].append({
                'time': exec_time,
                'memory': mem_used,
                'cpu': cpu_usage
            })
        
        # Busca por setor
        setores_unicos = list(set(record.codigo_setor for record in records))
        for _ in range(num_searches):
            setor = random.choice(setores_unicos)
            _, exec_time, mem_used, cpu_usage = self.measure_resources(
                system.search_by_setor, setor
            )
            results['search_by_setor'].append({
                'time': exec_time,
                'memory': mem_used,
                'cpu': cpu_usage
            })
        
        # Busca por faixa salarial
        for _ in range(num_searches):
            min_sal = random.uniform(1000, 5000)
            max_sal = min_sal + random.uniform(2000, 10000)
            _, exec_time, mem_used, cpu_usage = self.measure_resources(
                system.search_by_salary_range, min_sal, max_sal
            )
            results['search_by_salary_range'].append({
                'time': exec_time,
                'memory': mem_used,
                'cpu': cpu_usage
            })
        
        return results
    
    def run_complete_benchmark(self, dataset_sizes: List[int]) -> List[Dict[str, Any]]:
        """Executa benchmark completo para diferentes tamanhos de dataset"""
        
        generator = StudentDataGenerator()
        all_results = []
        
        for size in dataset_sizes:
            print(f"\n=== Benchmark para dataset de {size} registros ===")
            
            # Carrega ou gera dados
            try:
                records = generator.load_from_json(f"student_data_{size}.json")
            except FileNotFoundError:
                print(f"Gerando dataset de {size} registros...")
                records = generator.generate_dataset(size)
                generator.save_to_json(records, f"student_data_{size}.json")
            
            # Benchmark de inserção
            print("Executando benchmark de inserção...")
            insertion_results = self.benchmark_insertion(records)
            
            # Benchmark de buscas
            print("Executando benchmark de buscas...")
            num_searches = min(1000, size // 10)  # Ajusta número de buscas baseado no tamanho
            search_results = self.benchmark_search_operations(
                insertion_results['system'], records, num_searches
            )
            
            # Consolida resultados
            result = {
                'dataset_size': size,
                'insertion': insertion_results,
                'searches': search_results,
                'system_stats': insertion_results['system'].get_statistics()
            }
            
            all_results.append(result)
            print(f"Benchmark para {size} registros concluído!")
        
        return all_results

def generate_benchmark_report(results: List[Dict[str, Any]]):
    """Gera relatório detalhado dos benchmarks"""
    
    # Cria gráficos de performance
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    sizes = [r['dataset_size'] for r in results]
    
    # Gráfico 1: Tempo de inserção
    insertion_times = [r['insertion']['avg_time_per_record'] * 1000 for r in results]  # em ms
    ax1.plot(sizes, insertion_times, marker='o', color='blue', linewidth=2)
    ax1.set_xlabel('Tamanho do Dataset')
    ax1.set_ylabel('Tempo Médio de Inserção (ms)')
    ax1.set_title('Performance de Inserção por Registro')
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log')
    
    # Gráfico 2: Comparação de buscas
    search_types = ['search_by_matricula_linear', 'search_by_matricula_hash', 'search_by_cpf_hash']
    colors = ['red', 'green', 'blue']
    
    for search_type, color in zip(search_types, colors):
        times = []
        for r in results:
            avg_time = np.mean([s['time'] for s in r['searches'][search_type]]) * 1000  # em ms
            times.append(avg_time)
        
        label = search_type.replace('_', ' ').title()
        ax2.plot(sizes, times, marker='o', label=label, color=color, linewidth=2)
    
    ax2.set_xlabel('Tamanho do Dataset')
    ax2.set_ylabel('Tempo Médio de Busca (ms)')
    ax2.set_title('Performance de Busca por Tipo')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    
    # Gráfico 3: Uso de memória durante inserção
    memory_usage = [r['insertion']['max_memory_usage'] for r in results]
    ax3.plot(sizes, memory_usage, marker='o', color='purple', linewidth=2)
    ax3.set_xlabel('Tamanho do Dataset')
    ax3.set_ylabel('Pico de Uso de Memória (MB)')
    ax3.set_title('Consumo de Memória na Inserção')
    ax3.grid(True, alpha=0.3)
    ax3.set_xscale('log')
    
    # Gráfico 4: Distribuição salarial
    last_result = results[-1]  # Usa o maior dataset
    salary_stats = last_result['system_stats']['salary_stats']
    
    # Cria histograma de salários (simulado)
    np.random.seed(42)
    salaries = np.random.normal(salary_stats['mean'], salary_stats['std'], 1000)
    salaries = np.clip(salaries, salary_stats['min'], salary_stats['max'])
    
    ax4.hist(salaries, bins=30, alpha=0.7, color='orange', edgecolor='black')
    ax4.axvline(salary_stats['mean'], color='red', linestyle='--', label=f'Média: R$ {salary_stats["mean"]:.2f}')
    ax4.axvline(salary_stats['median'], color='green', linestyle='--', label=f'Mediana: R$ {salary_stats["median"]:.2f}')
    ax4.set_xlabel('Salário (R$)')
    ax4.set_ylabel('Frequência')
    ax4.set_title('Distribuição Salarial')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('plots/student_registration_benchmark.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Salva resultados em JSON
    with open('student_registration_benchmark_results.json', 'w', encoding='utf-8') as f:
        # Remove objeto system antes de salvar (não é serializável)
        results_for_json = []
        for r in results:
            r_copy = r.copy()
            r_copy['insertion'] = {k: v for k, v in r['insertion'].items() if k != 'system'}
            results_for_json.append(r_copy)
        
        json.dump(results_for_json, f, indent=2, ensure_ascii=False, default=str)

def main():
    """Executa benchmark completo do sistema de cadastro"""
    
    benchmark = StudentRegistrationBenchmark()
    
    # Define tamanhos de dataset para teste
    dataset_sizes = [1000, 5000, 10000, 25000]
    
    print("Iniciando benchmark do sistema de cadastro de matrículas...")
    print(f"Tamanhos de dataset: {dataset_sizes}")
    
    # Executa benchmarks
    results = benchmark.run_complete_benchmark(dataset_sizes)
    
    # Gera relatório
    print("\nGerando relatório de benchmark...")
    generate_benchmark_report(results)
    
    # Resumo final
    print("\n=== RESUMO FINAL ===")
    for result in results:
        size = result['dataset_size']
        avg_insert_time = result['insertion']['avg_time_per_record'] * 1000
        
        # Tempo médio de busca por matrícula (hash)
        hash_search_times = [s['time'] for s in result['searches']['search_by_matricula_hash']]
        avg_hash_search = np.mean(hash_search_times) * 1000
        
        # Tempo médio de busca linear
        linear_search_times = [s['time'] for s in result['searches']['search_by_matricula_linear']]
        avg_linear_search = np.mean(linear_search_times) * 1000
        
        print(f"\nDataset: {size} registros")
        print(f"  Inserção média: {avg_insert_time:.4f} ms/registro")
        print(f"  Busca hash: {avg_hash_search:.4f} ms")
        print(f"  Busca linear: {avg_linear_search:.4f} ms")
        print(f"  Speedup hash vs linear: {avg_linear_search/avg_hash_search:.1f}x")
    
    print("\nArquivos gerados:")
    print("- plots/student_registration_benchmark.png")
    print("- student_registration_benchmark_results.json")

if __name__ == "__main__":
    main()