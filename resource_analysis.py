import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple

def load_experiment_data(filename: str) -> List[Dict]:
    """Load experiment data from JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)

def analyze_iterations(data: List[Dict]) -> Dict:
    """Analyze the number of iterations for different operations and structures."""
    iterations_analysis = {
        'insert': {},
        'search': {}
    }
    
    for experiment in data:
        structure = experiment['structure']
        operation = experiment['operation']
        data_size = experiment['data_size']
        params = experiment.get('parameters', {})
        iterations = experiment['metrics']['avg_iterations']
        
        key = f"{structure}"
        if structure == 'HashTable':
            hash_func = params.get('hash_function', 'unknown')
            M = params.get('M', 'unknown')
            key = f"{structure}_{hash_func}_M{M}"
        elif structure in ['BST', 'AVL']:
            balanced = params.get('balanced', False)
            key = f"{structure}_{'balanced' if balanced else 'unbalanced'}"
        
        if key not in iterations_analysis[operation]:
            iterations_analysis[operation][key] = {}
        
        iterations_analysis[operation][key][data_size] = iterations
    
    return iterations_analysis

def analyze_memory_usage(data: List[Dict]) -> Dict:
    """Analyze memory usage patterns (though all are 0 in this dataset)."""
    memory_analysis = {
        'insert': {},
        'search': {}
    }
    
    for experiment in data:
        structure = experiment['structure']
        operation = experiment['operation']
        data_size = experiment['data_size']
        memory = experiment['metrics']['avg_memory_usage']
        
        if structure not in memory_analysis[operation]:
            memory_analysis[operation][structure] = {}
        
        memory_analysis[operation][structure][data_size] = memory
    
    return memory_analysis

def analyze_cpu_usage_by_execution_time(data: List[Dict]) -> Dict:
    """Analyze CPU usage by execution time and complexity."""
    cpu_analysis = {
        'insert': {},
        'search': {}
    }
    
    for experiment in data:
        structure = experiment['structure']
        operation = experiment['operation']
        data_size = experiment['data_size']
        params = experiment.get('parameters', {})
        exec_time = experiment['metrics']['avg_execution_time']
        
        key = f"{structure}"
        if structure == 'HashTable':
            hash_func = params.get('hash_function', 'unknown')
            M = params.get('M', 'unknown')
            key = f"{structure}_{hash_func}_M{M}"
        elif structure in ['BST', 'AVL']:
            balanced = params.get('balanced', False)
            key = f"{structure}_{'balanced' if balanced else 'unbalanced'}"
        
        if key not in cpu_analysis[operation]:
            cpu_analysis[operation][key] = {}
        
        cpu_analysis[operation][key][data_size] = exec_time
    
    return cpu_analysis

def create_iterations_plots(iterations_data: Dict):
    """Create plots for iterations analysis."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Insert operations
    for structure, size_data in iterations_data['insert'].items():
        sizes = sorted(size_data.keys())
        iterations = [size_data[size] for size in sizes]
        ax1.plot(sizes, iterations, marker='o', label=structure, linewidth=2)
    
    ax1.set_xlabel('Data Size')
    ax1.set_ylabel('Number of Iterations')
    ax1.set_title('Iterations Count - Insert Operations')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    
    # Search operations
    for structure, size_data in iterations_data['search'].items():
        sizes = sorted(size_data.keys())
        iterations = [size_data[size] for size in sizes]
        ax2.plot(sizes, iterations, marker='o', label=structure, linewidth=2)
    
    ax2.set_xlabel('Data Size')
    ax2.set_ylabel('Number of Iterations')
    ax2.set_title('Iterations Count - Search Operations')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig('plots/resource_iterations.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_cpu_utilization_plots(cpu_data: Dict):
    """Create plots for CPU utilization based on execution time."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Insert operations
    for structure, size_data in cpu_data['insert'].items():
        sizes = sorted(size_data.keys())
        times = [size_data[size] for size in sizes]
        ax1.plot(sizes, times, marker='o', label=structure, linewidth=2)
    
    ax1.set_xlabel('Data Size')
    ax1.set_ylabel('Execution Time (seconds)')
    ax1.set_title('CPU Utilization (Execution Time) - Insert Operations')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    
    # Search operations
    for structure, size_data in cpu_data['search'].items():
        sizes = sorted(size_data.keys())
        times = [size_data[size] for size in sizes]
        ax2.plot(sizes, times, marker='o', label=structure, linewidth=2)
    
    ax2.set_xlabel('Data Size')
    ax2.set_ylabel('Execution Time (seconds)')
    ax2.set_title('CPU Utilization (Execution Time) - Search Operations')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig('plots/resource_cpu_utilization.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_resource_efficiency_comparison(data: List[Dict]):
    """Create comparison of resource efficiency across structures."""
    
    # Group data by operation
    insert_data = [d for d in data if d['operation'] == 'insert']
    search_data = [d for d in data if d['operation'] == 'search']
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
    
    # Insert efficiency: Iterations vs Data Size
    for exp in insert_data:
        structure = exp['structure']
        params = exp.get('parameters', {})
        data_size = exp['data_size']
        iterations = exp['metrics']['avg_iterations']
        
        label = structure
        if structure == 'HashTable':
            hash_func = params.get('hash_function', 'unknown')
            M = params.get('M', 'unknown')
            label = f"{structure}_{hash_func}_M{M}"
        elif structure in ['BST', 'AVL']:
            balanced = params.get('balanced', False)
            label = f"{structure}_{'balanced' if balanced else 'unbalanced'}"
        
        ax1.scatter(data_size, iterations, label=label, s=60, alpha=0.7)
    
    ax1.set_xlabel('Data Size')
    ax1.set_ylabel('Iterations')
    ax1.set_title('Insert Operations: Iterations vs Data Size')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    
    # Insert efficiency: Time vs Data Size
    for exp in insert_data:
        structure = exp['structure']
        params = exp.get('parameters', {})
        data_size = exp['data_size']
        time = exp['metrics']['avg_execution_time']
        
        label = structure
        if structure == 'HashTable':
            hash_func = params.get('hash_function', 'unknown')
            M = params.get('M', 'unknown')
            label = f"{structure}_{hash_func}_M{M}"
        elif structure in ['BST', 'AVL']:
            balanced = params.get('balanced', False)
            label = f"{structure}_{'balanced' if balanced else 'unbalanced'}"
        
        ax2.scatter(data_size, time, label=label, s=60, alpha=0.7)
    
    ax2.set_xlabel('Data Size')
    ax2.set_ylabel('Execution Time (seconds)')
    ax2.set_title('Insert Operations: Execution Time vs Data Size')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax2.grid(True, alpha=0.3)
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    
    # Search efficiency: Iterations vs Data Size
    for exp in search_data:
        structure = exp['structure']
        params = exp.get('parameters', {})
        data_size = exp['data_size']
        iterations = exp['metrics']['avg_iterations']
        
        label = structure
        if structure == 'HashTable':
            hash_func = params.get('hash_function', 'unknown')
            M = params.get('M', 'unknown')
            label = f"{structure}_{hash_func}_M{M}"
        elif structure in ['BST', 'AVL']:
            balanced = params.get('balanced', False)
            label = f"{structure}_{'balanced' if balanced else 'unbalanced'}"
        
        ax3.scatter(data_size, iterations, label=label, s=60, alpha=0.7)
    
    ax3.set_xlabel('Data Size')
    ax3.set_ylabel('Iterations')
    ax3.set_title('Search Operations: Iterations vs Data Size')
    ax3.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax3.grid(True, alpha=0.3)
    ax3.set_xscale('log')
    ax3.set_yscale('log')
    
    # Search efficiency: Time vs Data Size
    for exp in search_data:
        structure = exp['structure']
        params = exp.get('parameters', {})
        data_size = exp['data_size']
        time = exp['metrics']['avg_execution_time']
        
        label = structure
        if structure == 'HashTable':
            hash_func = params.get('hash_function', 'unknown')
            M = params.get('M', 'unknown')
            label = f"{structure}_{hash_func}_M{M}"
        elif structure in ['BST', 'AVL']:
            balanced = params.get('balanced', False)
            label = f"{structure}_{'balanced' if balanced else 'unbalanced'}"
        
        ax4.scatter(data_size, time, label=label, s=60, alpha=0.7)
    
    ax4.set_xlabel('Data Size')
    ax4.set_ylabel('Execution Time (seconds)')
    ax4.set_title('Search Operations: Execution Time vs Data Size')
    ax4.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax4.grid(True, alpha=0.3)
    ax4.set_xscale('log')
    ax4.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig('plots/resource_efficiency_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_resource_consumption_summary(data: List[Dict]) -> Dict:
    """Generate a comprehensive summary of resource consumption."""
    summary = {
        'iterations_summary': {},
        'time_summary': {},
        'efficiency_metrics': {}
    }
    
    # Group by structure and operation
    for experiment in data:
        structure = experiment['structure']
        operation = experiment['operation']
        data_size = experiment['data_size']
        params = experiment.get('parameters', {})
        
        # Create unique key for each structure variant
        key = structure
        if structure == 'HashTable':
            hash_func = params.get('hash_function', 'unknown')
            M = params.get('M', 'unknown')
            key = f"{structure}_{hash_func}_M{M}"
        elif structure in ['BST', 'AVL']:
            balanced = params.get('balanced', False)
            key = f"{structure}_{'balanced' if balanced else 'unbalanced'}"
        
        # Initialize structure in summary
        if key not in summary['iterations_summary']:
            summary['iterations_summary'][key] = {'insert': {}, 'search': {}}
            summary['time_summary'][key] = {'insert': {}, 'search': {}}
            summary['efficiency_metrics'][key] = {'insert': {}, 'search': {}}
        
        # Store metrics
        iterations = experiment['metrics']['avg_iterations']
        exec_time = experiment['metrics']['avg_execution_time']
        
        summary['iterations_summary'][key][operation][data_size] = iterations
        summary['time_summary'][key][operation][data_size] = exec_time
        
        # Calculate efficiency (iterations per unit time)
        if exec_time > 0:
            efficiency = iterations / exec_time
            summary['efficiency_metrics'][key][operation][data_size] = efficiency
    
    return summary

def main():
    # Load data
    data = load_experiment_data('experiment_results.json')
    
    # Perform analysis
    iterations_data = analyze_iterations(data)
    memory_data = analyze_memory_usage(data)
    cpu_data = analyze_cpu_usage_by_execution_time(data)
    
    # Generate plots
    create_iterations_plots(iterations_data)
    create_cpu_utilization_plots(cpu_data)
    create_resource_efficiency_comparison(data)
    
    # Generate summary
    summary = generate_resource_consumption_summary(data)
    
    # Save summary to file
    with open('resource_consumption_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("Resource analysis completed. Generated:")
    print("- plots/resource_iterations.png")
    print("- plots/resource_cpu_utilization.png")
    print("- plots/resource_efficiency_comparison.png")
    print("- resource_consumption_summary.json")

if __name__ == "__main__":
    main()