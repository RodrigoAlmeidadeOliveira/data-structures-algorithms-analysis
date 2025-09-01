import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats

# Configurar estilo dos gráficos
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Carregar dados
df_raw = pd.read_csv('/Users/rodrigoalmeidadeoliveira/Documents/Doutorado/Disciplinas/FundamentosAlgoritmos/DataStructuresAndAlgorithms/Tarefas/resultados_bst.csv')
df_summary = pd.read_csv('/Users/rodrigoalmeidadeoliveira/Documents/Doutorado/Disciplinas/FundamentosAlgoritmos/DataStructuresAndAlgorithms/Tarefas/resumo_metricas_bst.csv')

# Converter memoria para MB
df_raw['memoria_mb'] = df_raw['memoria_pico'] / (1024 * 1024)
df_summary['memoria_mb_media'] = df_summary['memoria_mb_media']

# Configurações globais
volumes = [10000, 50000, 100000]
cores = {'sem_balanceamento': '#FF6B6B', 'com_balanceamento': '#4ECDC4'}
fig_size = (12, 8)

# Função para calcular intervalos de confiança
def confidence_interval(data, confidence=0.95):
    n = len(data)
    mean = np.mean(data)
    se = stats.sem(data)
    h = se * stats.t.ppf((1 + confidence) / 2., n-1)
    return h

# 1. GRÁFICO DE TEMPO DE INSERÇÃO
print("Gerando gráfico de tempo de inserção...")
plt.figure(figsize=fig_size)

for tipo in ['sem_balanceamento', 'com_balanceamento']:
    tempos_media = []
    tempos_erro = []
    
    for volume in volumes:
        subset = df_raw[(df_raw['tipo_bst'] == tipo) & (df_raw['volume'] == volume)]
        media = subset['tempo_insercao'].mean()
        erro = confidence_interval(subset['tempo_insercao'])
        tempos_media.append(media)
        tempos_erro.append(erro)
    
    label = 'BST sem balanceamento' if tipo == 'sem_balanceamento' else 'BST com balanceamento'
    plt.errorbar(volumes, tempos_media, yerr=tempos_erro, 
                marker='o', linewidth=2, markersize=8, capsize=5,
                color=cores[tipo], label=label)

plt.xlabel('Volume de Dados', fontsize=12, fontweight='bold')
plt.ylabel('Tempo de Inserção (segundos)', fontsize=12, fontweight='bold')
plt.title('Comparação de Performance - Tempo de Inserção\n(Intervalos de Confiança 95%)', 
          fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.yscale('log')
plt.xscale('log')
plt.xticks(volumes, [f'{v//1000}K' for v in volumes])
plt.tight_layout()
plt.savefig('/Users/rodrigoalmeidadeoliveira/Documents/Doutorado/Disciplinas/FundamentosAlgoritmos/DataStructuresAndAlgorithms/Tarefas/tempo_insercao.png', 
            dpi=300, bbox_inches='tight')
plt.close()

# 2. GRÁFICO DE TEMPO DE BUSCA
print("Gerando gráfico de tempo de busca...")
plt.figure(figsize=fig_size)

for tipo in ['sem_balanceamento', 'com_balanceamento']:
    tempos_media = []
    tempos_erro = []
    
    for volume in volumes:
        subset = df_raw[(df_raw['tipo_bst'] == tipo) & (df_raw['volume'] == volume)]
        media = subset['tempo_busca'].mean()
        erro = confidence_interval(subset['tempo_busca'])
        tempos_media.append(media)
        tempos_erro.append(erro)
    
    label = 'BST sem balanceamento' if tipo == 'sem_balanceamento' else 'BST com balanceamento'
    plt.errorbar(volumes, tempos_media, yerr=tempos_erro, 
                marker='s', linewidth=2, markersize=8, capsize=5,
                color=cores[tipo], label=label)

plt.xlabel('Volume de Dados', fontsize=12, fontweight='bold')
plt.ylabel('Tempo de Busca (segundos)', fontsize=12, fontweight='bold')
plt.title('Comparação de Performance - Tempo de Busca\n(Intervalos de Confiança 95%)', 
          fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.xscale('log')
plt.xticks(volumes, [f'{v//1000}K' for v in volumes])
plt.tight_layout()
plt.savefig('/Users/rodrigoalmeidadeoliveira/Documents/Doutorado/Disciplinas/FundamentosAlgoritmos/DataStructuresAndAlgorithms/Tarefas/tempo_busca.png', 
            dpi=300, bbox_inches='tight')
plt.close()

# 3. GRÁFICO DE CONSUMO DE MEMÓRIA
print("Gerando gráfico de consumo de memória...")
plt.figure(figsize=fig_size)

memoria_sem = df_summary[df_summary['tipo_bst'] == 'sem_balanceamento']['memoria_mb_media'].values
memoria_com = df_summary[df_summary['tipo_bst'] == 'com_balanceamento']['memoria_mb_media'].values

x = np.arange(len(volumes))
width = 0.35

plt.bar(x - width/2, memoria_sem, width, label='BST sem balanceamento', 
        color=cores['sem_balanceamento'], alpha=0.8)
plt.bar(x + width/2, memoria_com, width, label='BST com balanceamento', 
        color=cores['com_balanceamento'], alpha=0.8)

plt.xlabel('Volume de Dados', fontsize=12, fontweight='bold')
plt.ylabel('Consumo de Memória (MB)', fontsize=12, fontweight='bold')
plt.title('Comparação de Consumo de Memória', fontsize=14, fontweight='bold')
plt.xticks(x, [f'{v//1000}K' for v in volumes])
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3, axis='y')

# Adicionar valores nas barras
for i, (sem, com) in enumerate(zip(memoria_sem, memoria_com)):
    plt.text(i - width/2, sem + 0.1, f'{sem:.1f}', ha='center', va='bottom', fontweight='bold')
    plt.text(i + width/2, com + 0.1, f'{com:.1f}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('/Users/rodrigoalmeidadeoliveira/Documents/Doutorado/Disciplinas/FundamentosAlgoritmos/DataStructuresAndAlgorithms/Tarefas/memoria.png', 
            dpi=300, bbox_inches='tight')
plt.close()

# 4. GRÁFICO DE NÚMERO DE ITERAÇÕES
print("Gerando gráfico de iterações...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Iterações de inserção
for tipo in ['sem_balanceamento', 'com_balanceamento']:
    iter_media = []
    iter_erro = []
    
    for volume in volumes:
        subset = df_raw[(df_raw['tipo_bst'] == tipo) & (df_raw['volume'] == volume)]
        media = subset['iteracoes_insercao'].mean()
        erro = confidence_interval(subset['iteracoes_insercao'])
        iter_media.append(media)
        iter_erro.append(erro)
    
    label = 'BST sem balanceamento' if tipo == 'sem_balanceamento' else 'BST com balanceamento'
    ax1.errorbar(volumes, iter_media, yerr=iter_erro, 
                marker='o', linewidth=2, markersize=8, capsize=5,
                color=cores[tipo], label=label)

ax1.set_xlabel('Volume de Dados', fontsize=12, fontweight='bold')
ax1.set_ylabel('Número de Iterações (Inserção)', fontsize=12, fontweight='bold')
ax1.set_title('Iterações na Inserção', fontsize=14, fontweight='bold')
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)
ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_xticks(volumes)
ax1.set_xticklabels([f'{v//1000}K' for v in volumes])

# Iterações de busca
for tipo in ['sem_balanceamento', 'com_balanceamento']:
    iter_media = []
    iter_erro = []
    
    for volume in volumes:
        subset = df_raw[(df_raw['tipo_bst'] == tipo) & (df_raw['volume'] == volume)]
        media = subset['iteracoes_busca'].mean()
        erro = confidence_interval(subset['iteracoes_busca'])
        iter_media.append(media)
        iter_erro.append(erro)
    
    label = 'BST sem balanceamento' if tipo == 'sem_balanceamento' else 'BST com balanceamento'
    ax2.errorbar(volumes, iter_media, yerr=iter_erro, 
                marker='s', linewidth=2, markersize=8, capsize=5,
                color=cores[tipo], label=label)

ax2.set_xlabel('Volume de Dados', fontsize=12, fontweight='bold')
ax2.set_ylabel('Número de Iterações (Busca)', fontsize=12, fontweight='bold')
ax2.set_title('Iterações na Busca', fontsize=14, fontweight='bold')
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.3)
ax2.set_xscale('log')
ax2.set_xticks(volumes)
ax2.set_xticklabels([f'{v//1000}K' for v in volumes])

plt.tight_layout()
plt.savefig('/Users/rodrigoalmeidadeoliveira/Documents/Doutorado/Disciplinas/FundamentosAlgoritmos/DataStructuresAndAlgorithms/Tarefas/iteracoes.png', 
            dpi=300, bbox_inches='tight')
plt.close()

# 5. GRÁFICO DE ALTURA DA ÁRVORE
print("Gerando gráfico de altura da árvore...")
plt.figure(figsize=fig_size)

for tipo in ['sem_balanceamento', 'com_balanceamento']:
    alturas_media = []
    alturas_erro = []
    
    for volume in volumes:
        subset = df_raw[(df_raw['tipo_bst'] == tipo) & (df_raw['volume'] == volume)]
        media = subset['altura_arvore'].mean()
        erro = confidence_interval(subset['altura_arvore'])
        alturas_media.append(media)
        alturas_erro.append(erro)
    
    label = 'BST sem balanceamento' if tipo == 'sem_balanceamento' else 'BST com balanceamento'
    plt.errorbar(volumes, alturas_media, yerr=alturas_erro, 
                marker='D', linewidth=2, markersize=8, capsize=5,
                color=cores[tipo], label=label)

# Adicionar linha teórica log2(n)
alturas_teoricas = [np.log2(v) for v in volumes]
plt.plot(volumes, alturas_teoricas, '--', color='gray', linewidth=2, 
         label='Altura teórica ótima (log₂n)', alpha=0.7)

plt.xlabel('Volume de Dados', fontsize=12, fontweight='bold')
plt.ylabel('Altura da Árvore', fontsize=12, fontweight='bold')
plt.title('Comparação de Altura das Árvores\n(Intervalos de Confiança 95%)', 
          fontsize=14, fontweight='bold')
plt.legend(fontsize=11)
plt.grid(True, alpha=0.3)
plt.xscale('log')
plt.xticks(volumes, [f'{v//1000}K' for v in volumes])
plt.tight_layout()
plt.savefig('/Users/rodrigoalmeidadeoliveira/Documents/Doutorado/Disciplinas/FundamentosAlgoritmos/DataStructuresAndAlgorithms/Tarefas/altura_arvore.png', 
            dpi=300, bbox_inches='tight')
plt.close()

# 6. GRÁFICO COMPARATIVO DE EFICIÊNCIA (Speedup)
print("Gerando gráfico de eficiência comparativa...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Speedup na inserção (BST sem bal. / BST com bal.)
speedup_insercao = []
for volume in volumes:
    tempo_sem = df_summary[(df_summary['tipo_bst'] == 'sem_balanceamento') & 
                          (df_summary['volume'] == volume)]['tempo_insercao_media'].values[0]
    tempo_com = df_summary[(df_summary['tipo_bst'] == 'com_balanceamento') & 
                          (df_summary['volume'] == volume)]['tempo_insercao_media'].values[0]
    speedup_insercao.append(tempo_com / tempo_sem)

ax1.bar(range(len(volumes)), speedup_insercao, color='lightcoral', alpha=0.8)
ax1.axhline(y=1, color='red', linestyle='--', alpha=0.7, label='Paridade')
ax1.set_xlabel('Volume de Dados', fontsize=12, fontweight='bold')
ax1.set_ylabel('Razão de Tempo\n(BST Balanceada / BST Simples)', fontsize=12, fontweight='bold')
ax1.set_title('Overhead de Inserção\n(Valores > 1 indicam BST balanceada mais lenta)', 
              fontsize=12, fontweight='bold')
ax1.set_xticks(range(len(volumes)))
ax1.set_xticklabels([f'{v//1000}K' for v in volumes])
ax1.grid(True, alpha=0.3, axis='y')
ax1.legend()

# Speedup na busca (BST sem bal. / BST com bal.)
speedup_busca = []
for volume in volumes:
    tempo_sem = df_summary[(df_summary['tipo_bst'] == 'sem_balanceamento') & 
                          (df_summary['volume'] == volume)]['tempo_busca_media'].values[0]
    tempo_com = df_summary[(df_summary['tipo_bst'] == 'com_balanceamento') & 
                          (df_summary['volume'] == volume)]['tempo_busca_media'].values[0]
    speedup_busca.append(tempo_sem / tempo_com)

ax2.bar(range(len(volumes)), speedup_busca, color='lightgreen', alpha=0.8)
ax2.axhline(y=1, color='red', linestyle='--', alpha=0.7, label='Paridade')
ax2.set_xlabel('Volume de Dados', fontsize=12, fontweight='bold')
ax2.set_ylabel('Razão de Tempo\n(BST Simples / BST Balanceada)', fontsize=12, fontweight='bold')
ax2.set_title('Ganho de Performance na Busca\n(Valores > 1 indicam BST balanceada mais rápida)', 
              fontsize=12, fontweight='bold')
ax2.set_xticks(range(len(volumes)))
ax2.set_xticklabels([f'{v//1000}K' for v in volumes])
ax2.grid(True, alpha=0.3, axis='y')
ax2.legend()

# Adicionar valores nas barras
for i, (ins, bus) in enumerate(zip(speedup_insercao, speedup_busca)):
    ax1.text(i, ins + 0.05, f'{ins:.1f}x', ha='center', va='bottom', fontweight='bold')
    ax2.text(i, bus + 0.01, f'{bus:.1f}x', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('/Users/rodrigoalmeidadeoliveira/Documents/Doutorado/Disciplinas/FundamentosAlgoritmos/DataStructuresAndAlgorithms/Tarefas/eficiencia_comparativa.png', 
            dpi=300, bbox_inches='tight')
plt.close()

# 7. HEATMAP DE CORRELAÇÃO DAS MÉTRICAS
print("Gerando heatmap de correlação...")
plt.figure(figsize=(10, 8))

# Preparar dados para correlação
metrics_cols = ['volume', 'tempo_insercao', 'tempo_busca', 'memoria_pico', 
               'iteracoes_insercao', 'iteracoes_busca', 'altura_arvore']
corr_data = df_raw[metrics_cols].corr()

# Criar heatmap
sns.heatmap(corr_data, annot=True, cmap='RdBu_r', center=0, square=True,
            fmt='.3f', cbar_kws={'shrink': 0.8})

plt.title('Matriz de Correlação das Métricas de Performance\n(Todas as configurações BST)', 
          fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('/Users/rodrigoalmeidadeoliveira/Documents/Doutorado/Disciplinas/FundamentosAlgoritmos/DataStructuresAndAlgorithms/Tarefas/correlacao_metricas.png', 
            dpi=300, bbox_inches='tight')
plt.close()

# 8. BOXPLOT COMPARATIVO DE TODAS AS MÉTRICAS
print("Gerando boxplot comparativo...")
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()

metricas = [
    ('tempo_insercao', 'Tempo de Inserção (s)'),
    ('tempo_busca', 'Tempo de Busca (s)'),
    ('memoria_mb', 'Memória (MB)'),
    ('iteracoes_insercao', 'Iterações Inserção'),
    ('iteracoes_busca', 'Iterações Busca'),
    ('altura_arvore', 'Altura da Árvore')
]

for idx, (metrica, titulo) in enumerate(metricas):
    data_plot = []
    labels_plot = []
    
    for volume in volumes:
        for tipo in ['sem_balanceamento', 'com_balanceamento']:
            subset = df_raw[(df_raw['tipo_bst'] == tipo) & (df_raw['volume'] == volume)]
            if metrica in subset.columns:
                data_plot.append(subset[metrica].values)
                tipo_label = 'Sem Bal.' if tipo == 'sem_balanceamento' else 'Com Bal.'
                labels_plot.append(f'{volume//1000}K\n{tipo_label}')
    
    bp = axes[idx].boxplot(data_plot, labels=labels_plot, patch_artist=True)
    
    # Colorir os boxplots
    colors = []
    for i in range(len(labels_plot)):
        if 'Sem Bal.' in labels_plot[i]:
            colors.append(cores['sem_balanceamento'])
        else:
            colors.append(cores['com_balanceamento'])
    
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    axes[idx].set_title(titulo, fontsize=12, fontweight='bold')
    axes[idx].grid(True, alpha=0.3)
    axes[idx].tick_params(axis='x', rotation=45)
    
    if metrica in ['tempo_insercao', 'iteracoes_insercao']:
        axes[idx].set_yscale('log')

plt.tight_layout()
plt.savefig('/Users/rodrigoalmeidadeoliveira/Documents/Doutorado/Disciplinas/FundamentosAlgoritmos/DataStructuresAndAlgorithms/Tarefas/boxplot_comparativo.png', 
            dpi=300, bbox_inches='tight')
plt.close()

print("\nTodos os gráficos foram gerados com sucesso!")
print("Arquivos criados:")
print("1. tempo_insercao.png - Comparação de tempos de inserção")
print("2. tempo_busca.png - Comparação de tempos de busca")
print("3. memoria.png - Comparação de consumo de memória")
print("4. iteracoes.png - Análise do número de iterações")
print("5. altura_arvore.png - Comparação de alturas das árvores")
print("6. eficiencia_comparativa.png - Análise de speedup/overhead")
print("7. correlacao_metricas.png - Matriz de correlação")
print("8. boxplot_comparativo.png - Distribuição de todas as métricas")