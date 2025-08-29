import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import List, Dict, Any
from experiments import ExperimentResult


class ResultAnalyzer:
    def __init__(self, results: List[ExperimentResult]):
        self.results = results
        self.df = self._create_dataframe()
    
    def _create_dataframe(self) -> pd.DataFrame:
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
        print("\nComplexidade Teórica vs. Observada:")
        print("-" * 60)
        
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
    
    def generate_plots(self, suffix: str = ""):
        # Cria diretório para plots
        os.makedirs('plots', exist_ok=True)
        
        # Plot 1: Tempo de inserção por estrutura
        self._plot_insertion_times(suffix)
        
        # Plot 2: Tempo de busca por estrutura
        self._plot_search_times(suffix)
        
        # Plot 3: Comparação de iterações
        self._plot_iterations_comparison(suffix)
        
        # Plot 4: Análise específica de Hash Table
        self._plot_hash_analysis()
        
        # Plot 5: Altura das árvores
        self._plot_tree_heights()
    
    def _plot_insertion_times(self, suffix: str = ""):
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
        plt.savefig(f'plots/insertion_times{suffix}.png', dpi=150)
        plt.close()
    
    def _plot_search_times(self, suffix: str = ""):
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
        plt.savefig(f'plots/search_times{suffix}.png', dpi=150)
        plt.close()
    
    def _plot_iterations_comparison(self, suffix: str = ""):
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
        plt.savefig(f'plots/iterations_comparison{suffix}.png', dpi=150)
        plt.close()
    
    def _plot_hash_analysis(self):
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
        
        # Colisões
        # Placeholder - seria necessário adicionar métricas de colisão
        ax3.text(0.5, 0.5, 'Análise de Colisões\n(dados específicos necessários)', 
                ha='center', va='center')
        ax3.set_title('Taxa de Colisões')
        
        # Comparação geral
        ax4.bar(['Linear', 'BST', 'AVL', 'Hash'], 
               [1, np.log2(100000), np.log2(100000), 1],
               color=['blue', 'green', 'orange', 'red'])
        ax4.set_ylabel('Complexidade Esperada (escala relativa)')
        ax4.set_title('Complexidade Teórica para N=100.000')
        
        plt.tight_layout()
        plt.savefig('plots/hash_analysis.png', dpi=150)
        plt.close()
    
    def _plot_tree_heights(self):
        # Extrai alturas das árvores dos resultados originais
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
        ax.plot(theoretical_sizes, theoretical_sizes * 0.1, 
               label='n/10 (degradado)', linestyle=':', alpha=0.5)
        
        ax.set_xlabel('Tamanho do Dataset (N)')
        ax.set_ylabel('Altura da Árvore')
        ax.set_title('Altura das Árvores: BST vs AVL')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_xscale('log')
        
        plt.tight_layout()
        plt.savefig('plots/tree_heights.png', dpi=150)
        plt.close()
    
    def export_latex_tables(self, filename: str = "results_tables.tex"):
        """Exporta tabelas em formato LaTeX para o artigo"""
        with open(filename, 'w') as f:
            # Tabela de tempos de inserção
            f.write("% Tabela de Tempos de Inserção\n")
            insert_data = self.df[self.df['operation'] == 'insert']
            pivot = insert_data.pivot_table(values='mean_time', 
                                           index='data_size', 
                                           columns='structure')
            f.write(pivot.to_latex(float_format="%.6f"))
            f.write("\n\n")
            
            # Tabela de tempos de busca
            f.write("% Tabela de Tempos de Busca\n")
            search_data = self.df[self.df['operation'] == 'search']
            pivot = search_data.pivot_table(values='mean_time', 
                                           index='data_size', 
                                           columns='structure')
            f.write(pivot.to_latex(float_format="%.6f"))
        
        print(f"Tabelas LaTeX exportadas para: {filename}")