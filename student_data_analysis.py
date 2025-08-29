import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import Counter
import seaborn as sns

def analyze_student_data_characteristics():
    """Analisa características dos dados gerados para validar realismo"""
    
    # Carrega dataset maior para análise
    with open('student_data_25000.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Converte para DataFrame para facilitar análise
    df = pd.DataFrame(data)
    
    # Análise de distribuições
    fig, ((ax1, ax2), (ax3, ax4), (ax5, ax6)) = plt.subplots(3, 2, figsize=(16, 20))
    
    # 1. Distribuição salarial
    ax1.hist(df['salario'], bins=50, alpha=0.7, color='skyblue', edgecolor='black')
    ax1.set_xlabel('Salário (R$)')
    ax1.set_ylabel('Frequência')
    ax1.set_title('Distribuição Salarial')
    ax1.grid(True, alpha=0.3)
    
    # Adiciona estatísticas
    mean_sal = df['salario'].mean()
    median_sal = df['salario'].median()
    ax1.axvline(mean_sal, color='red', linestyle='--', label=f'Média: R$ {mean_sal:.2f}')
    ax1.axvline(median_sal, color='green', linestyle='--', label=f'Mediana: R$ {median_sal:.2f}')
    ax1.legend()
    
    # 2. Distribuição por setor
    setor_counts = df['codigo_setor'].value_counts().sort_index()
    ax2.bar(setor_counts.index, setor_counts.values, alpha=0.7, color='lightcoral')
    ax2.set_xlabel('Código do Setor')
    ax2.set_ylabel('Número de Funcionários')
    ax2.set_title('Distribuição por Setor')
    ax2.grid(True, alpha=0.3)
    
    # 3. Distribuição por status
    status_counts = df['status'].value_counts()
    ax3.pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%', startangle=90)
    ax3.set_title('Distribuição por Status')
    
    # 4. Distribuição por cargo
    cargo_counts = df['cargo'].value_counts().head(10)  # Top 10 cargos
    ax4.barh(cargo_counts.index, cargo_counts.values, alpha=0.7, color='lightgreen')
    ax4.set_xlabel('Número de Funcionários')
    ax4.set_title('Top 10 Cargos')
    ax4.grid(True, alpha=0.3)
    
    # 5. Distribuição temporal (ano de ingresso baseado na matrícula)
    df['ano_matricula'] = df['matricula'].astype(str).str[:4].astype(int)
    ano_counts = df['ano_matricula'].value_counts().sort_index()
    ax5.plot(ano_counts.index, ano_counts.values, marker='o', linewidth=2, color='purple')
    ax5.set_xlabel('Ano da Matrícula')
    ax5.set_ylabel('Número de Ingressos')
    ax5.set_title('Ingressos por Ano')
    ax5.grid(True, alpha=0.3)
    
    # 6. Correlação Salário vs Cargo (boxplot)
    # Seleciona apenas cargos com mais representatividade
    top_cargos = cargo_counts.head(8).index.tolist()
    df_filtered = df[df['cargo'].isin(top_cargos)]
    
    sns.boxplot(data=df_filtered, x='cargo', y='salario', ax=ax6)
    ax6.set_xticklabels(ax6.get_xticklabels(), rotation=45, ha='right')
    ax6.set_xlabel('Cargo')
    ax6.set_ylabel('Salário (R$)')
    ax6.set_title('Distribuição Salarial por Cargo')
    ax6.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('plots/student_data_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Gera relatório estatístico
    stats_report = {
        'dataset_info': {
            'total_records': len(df),
            'unique_matriculas': df['matricula'].nunique(),
            'unique_cpfs': df['cpf'].nunique(),
            'date_range': {
                'oldest_entry': df['data_ingresso'].min(),
                'newest_entry': df['data_ingresso'].max()
            }
        },
        'salary_statistics': {
            'mean': float(df['salario'].mean()),
            'median': float(df['salario'].median()),
            'std': float(df['salario'].std()),
            'min': float(df['salario'].min()),
            'max': float(df['salario'].max()),
            'quartiles': {
                'q1': float(df['salario'].quantile(0.25)),
                'q2': float(df['salario'].quantile(0.5)),
                'q3': float(df['salario'].quantile(0.75))
            }
        },
        'sector_distribution': df['codigo_setor'].value_counts().to_dict(),
        'status_distribution': df['status'].value_counts().to_dict(),
        'position_distribution': df['cargo'].value_counts().to_dict(),
        'level_distribution': df['nivel'].value_counts().to_dict(),
        'yearly_distribution': df['ano_matricula'].value_counts().sort_index().to_dict()
    }
    
    # Salva relatório estatístico
    with open('student_data_statistics.json', 'w', encoding='utf-8') as f:
        json.dump(stats_report, f, indent=2, ensure_ascii=False, default=str)
    
    return stats_report

def create_performance_comparison():
    """Cria comparação visual dos resultados de performance"""
    
    # Dados dos benchmarks (extraídos dos resultados anteriores)
    dataset_sizes = [1000, 5000, 10000, 25000]
    
    # Dados de inserção (ms por registro)
    insertion_times = [0.0004, 0.0005, 0.0005, 0.0006]
    
    # Dados de busca
    hash_search_times = [0.0002, 0.0003, 0.0004, 0.0004]
    linear_search_times = [0.0088, 0.0864, 0.0845, 0.2314]
    
    # Speedup
    speedup = [l/h for l, h in zip(linear_search_times, hash_search_times)]
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Tempo de Inserção
    ax1.plot(dataset_sizes, insertion_times, marker='o', linewidth=3, markersize=8, color='blue')
    ax1.set_xlabel('Tamanho do Dataset')
    ax1.set_ylabel('Tempo de Inserção (ms/registro)')
    ax1.set_title('Performance de Inserção')
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log')
    
    # Adiciona anotações
    for i, (x, y) in enumerate(zip(dataset_sizes, insertion_times)):
        ax1.annotate(f'{y:.4f} ms', (x, y), textcoords="offset points", xytext=(0,10), ha='center')
    
    # 2. Comparação de Buscas
    ax2.plot(dataset_sizes, hash_search_times, marker='o', linewidth=3, markersize=8, 
             color='green', label='Hash Table')
    ax2.plot(dataset_sizes, linear_search_times, marker='s', linewidth=3, markersize=8, 
             color='red', label='Linear Search')
    ax2.set_xlabel('Tamanho do Dataset')
    ax2.set_ylabel('Tempo de Busca (ms)')
    ax2.set_title('Comparação de Performance de Busca')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    
    # 3. Speedup Hash vs Linear
    ax3.bar(range(len(dataset_sizes)), speedup, alpha=0.7, color='orange')
    ax3.set_xlabel('Tamanho do Dataset')
    ax3.set_ylabel('Speedup (vezes mais rápido)')
    ax3.set_title('Speedup: Hash Table vs Busca Linear')
    ax3.set_xticks(range(len(dataset_sizes)))
    ax3.set_xticklabels([f'{size:,}' for size in dataset_sizes])
    ax3.grid(True, alpha=0.3)
    
    # Adiciona valores no topo das barras
    for i, v in enumerate(speedup):
        ax3.text(i, v + 10, f'{v:.1f}x', ha='center', va='bottom', fontweight='bold')
    
    # 4. Eficiência por Operação (operações por segundo)
    operations_per_second = {
        'Inserção': [1/t * 1000 for t in insertion_times],  # ops/second
        'Busca Hash': [1/t * 1000 for t in hash_search_times],
        'Busca Linear': [1/t * 1000 for t in linear_search_times]
    }
    
    x_pos = np.arange(len(dataset_sizes))
    width = 0.25
    
    for i, (op_type, values) in enumerate(operations_per_second.items()):
        offset = (i - 1) * width
        bars = ax4.bar(x_pos + offset, values, width, label=op_type, alpha=0.7)
        
        # Adiciona valores no topo das barras (apenas para dataset menor para clareza)
        if op_type == 'Inserção':
            for j, bar in enumerate(bars):
                if j == 0:  # Apenas primeira barra
                    height = bar.get_height()
                    ax4.text(bar.get_x() + bar.get_width()/2., height,
                            f'{height:,.0f}', ha='center', va='bottom', fontsize=8)
    
    ax4.set_xlabel('Tamanho do Dataset')
    ax4.set_ylabel('Operações por Segundo')
    ax4.set_title('Throughput por Tipo de Operação')
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels([f'{size:,}' for size in dataset_sizes])
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig('plots/student_performance_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    """Executa análise completa dos dados do sistema de cadastro"""
    
    print("Executando análise dos dados do sistema de cadastro...")
    
    # Análise das características dos dados
    print("1. Analisando características dos dados...")
    stats = analyze_student_data_characteristics()
    
    # Comparação de performance
    print("2. Criando comparação de performance...")
    create_performance_comparison()
    
    print("\nResumo das análises:")
    print(f"- Total de registros analisados: {stats['dataset_info']['total_records']:,}")
    print(f"- Salário médio: R$ {stats['salary_statistics']['mean']:,.2f}")
    print(f"- Setores únicos: {len(stats['sector_distribution'])}")
    print(f"- Cargos únicos: {len(stats['position_distribution'])}")
    print(f"- Faixa de anos: {min(stats['yearly_distribution'].keys())}-{max(stats['yearly_distribution'].keys())}")
    
    print("\nTop 5 cargos mais frequentes:")
    top_positions = sorted(stats['position_distribution'].items(), key=lambda x: x[1], reverse=True)[:5]
    for cargo, count in top_positions:
        print(f"  {cargo}: {count} funcionários")
    
    print("\nArquivos gerados:")
    print("- plots/student_data_analysis.png")
    print("- plots/student_performance_comparison.png") 
    print("- student_data_statistics.json")

if __name__ == "__main__":
    main()