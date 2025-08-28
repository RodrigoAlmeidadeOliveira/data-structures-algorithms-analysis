import time
import tracemalloc
import psutil
import os
from typing import Dict, Any, Callable
from dataclasses import dataclass, field


@dataclass
class PerformanceMetrics:
    execution_time: float = 0.0
    memory_usage: float = 0.0  # Em MB
    peak_memory: float = 0.0  # Em MB
    cpu_percent: float = 0.0
    iterations: int = 0
    additional_metrics: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'execution_time': self.execution_time,
            'memory_usage': self.memory_usage,
            'peak_memory': self.peak_memory,
            'cpu_percent': self.cpu_percent,
            'iterations': self.iterations,
            **self.additional_metrics
        }


class MetricsCollector:
    def __init__(self):
        self.process = psutil.Process(os.getpid())
        
    def measure_operation(self, operation: Callable, *args, **kwargs) -> tuple[Any, PerformanceMetrics]:
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
    
    def measure_batch_operations(self, operations: list, 
                               operation_func: Callable,
                               description: str = "") -> Dict[str, Any]:
        all_metrics = []
        
        print(f"Executando: {description}")
        
        for i, op_args in enumerate(operations):
            if i % 100 == 0 and i > 0:
                print(f"  Progresso: {i}/{len(operations)}")
            
            _, metrics = self.measure_operation(operation_func, *op_args)
            all_metrics.append(metrics)
        
        # Calcula estatísticas
        avg_time = sum(m.execution_time for m in all_metrics) / len(all_metrics)
        avg_memory = sum(m.memory_usage for m in all_metrics) / len(all_metrics)
        max_memory = max(m.peak_memory for m in all_metrics)
        avg_cpu = sum(m.cpu_percent for m in all_metrics) / len(all_metrics)
        total_iterations = sum(m.iterations for m in all_metrics)
        
        return {
            'total_operations': len(operations),
            'avg_execution_time': avg_time,
            'total_execution_time': sum(m.execution_time for m in all_metrics),
            'avg_memory_usage': avg_memory,
            'peak_memory_usage': max_memory,
            'avg_cpu_percent': avg_cpu,
            'total_iterations': total_iterations,
            'avg_iterations': total_iterations / len(operations) if operations else 0
        }