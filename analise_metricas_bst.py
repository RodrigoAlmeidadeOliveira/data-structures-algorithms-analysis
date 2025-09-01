import csv
import statistics

# ler dados do csv
dados = []
with open('resultados_bst.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        dados.append(row)

print("=== ANÁLISE COMPARATIVA DE MÉTRICAS - BST ===\n")

# separar dados por tipo e volume
volumes = [10000, 50000, 100000]
tipos = ['sem_balanceamento', 'com_balanceamento']

for volume in volumes:
    print(f"VOLUME: {volume:,} registros")
    print("-" * 50)
    
    for tipo in tipos:
        # filtrar dados para o tipo e volume atual
        dados_filtrados = [d for d in dados if d['tipo_bst'] == tipo and int(d['volume']) == volume]
        
        if not dados_filtrados:
            continue
            
        # extrair metricas para calculo estatistico
        tempos_insercao = [float(d['tempo_insercao']) for d in dados_filtrados]
        tempos_busca = [float(d['tempo_busca']) for d in dados_filtrados]
        memorias_pico = [int(d['memoria_pico']) for d in dados_filtrados]
        cpu_percents = [float(d['cpu_percent']) for d in dados_filtrados]
        iteracoes_insercao = [int(d['iteracoes_insercao']) for d in dados_filtrados]
        iteracoes_busca = [int(d['iteracoes_busca']) for d in dados_filtrados]
        alturas = [int(d['altura_arvore']) for d in dados_filtrados]
        
        print(f"\n{tipo.upper().replace('_', ' ')}")
        print("  Tempo Inserção:")
        print(f"    Média: {statistics.mean(tempos_insercao):.4f}s")
        print(f"    Desvio: {statistics.stdev(tempos_insercao):.4f}s") if len(tempos_insercao) > 1 else print("    Desvio: N/A")
        print(f"    Min-Max: {min(tempos_insercao):.4f}s - {max(tempos_insercao):.4f}s")
        
        print("  Tempo Busca:")
        print(f"    Média: {statistics.mean(tempos_busca):.4f}s")
        print(f"    Desvio: {statistics.stdev(tempos_busca):.4f}s") if len(tempos_busca) > 1 else print("    Desvio: N/A")
        print(f"    Min-Max: {min(tempos_busca):.4f}s - {max(tempos_busca):.4f}s")
        
        print("  Memória Pico:")
        print(f"    Média: {statistics.mean(memorias_pico)/1024/1024:.2f} MB")
        print(f"    Desvio: {statistics.stdev(memorias_pico)/1024/1024:.2f} MB") if len(memorias_pico) > 1 else print("    Desvio: N/A")
        
        print("  CPU (%):")
        print(f"    Média: {statistics.mean(cpu_percents):.1f}%")
        print(f"    Desvio: {statistics.stdev(cpu_percents):.1f}%") if len(cpu_percents) > 1 else print("    Desvio: N/A")
        
        print("  Iterações Inserção:")
        print(f"    Média: {statistics.mean(iteracoes_insercao):,.0f}")
        print(f"    Desvio: {statistics.stdev(iteracoes_insercao):,.0f}") if len(iteracoes_insercao) > 1 else print("    Desvio: N/A")
        
        print("  Iterações Busca:")
        print(f"    Média: {statistics.mean(iteracoes_busca):,.0f}")
        print(f"    Desvio: {statistics.stdev(iteracoes_busca):,.0f}") if len(iteracoes_busca) > 1 else print("    Desvio: N/A")
        
        print("  Altura da Árvore:")
        print(f"    Média: {statistics.mean(alturas):.1f}")
        print(f"    Desvio: {statistics.stdev(alturas):.1f}") if len(alturas) > 1 else print("    Desvio: N/A")
        print(f"    Min-Max: {min(alturas)} - {max(alturas)}")
    
    print("\n")

# comparacao geral
print("=== COMPARAÇÃO GERAL ===")
print("Observações importantes:")
print("- BST sem balanceamento: altura cresce descontroladamente")
print("- BST com balanceamento: altura mantém-se logarítmica")
print("- Tempo de inserção maior na BST balanceada devido às rotações")
print("- Tempo de busca geralmente menor na BST balanceada")
print("- Número de iterações varia com a altura da árvore")
print("- Consumo de memória similar entre as duas abordagens")

# calcular complexidades empiricas
print("\n=== ANÁLISE DE COMPLEXIDADE EMPÍRICA ===")
for tipo in tipos:
    print(f"\n{tipo.upper().replace('_', ' ')}")
    
    # coletar medias por volume
    medias_tempo_insercao = []
    medias_iteracoes_busca = []
    alturas_medias = []
    
    for volume in volumes:
        dados_vol = [d for d in dados if d['tipo_bst'] == tipo and int(d['volume']) == volume]
        if dados_vol:
            tempo_ins = statistics.mean([float(d['tempo_insercao']) for d in dados_vol])
            iter_busca = statistics.mean([int(d['iteracoes_busca']) for d in dados_vol])
            altura_media = statistics.mean([int(d['altura_arvore']) for d in dados_vol])
            
            medias_tempo_insercao.append(tempo_ins)
            medias_iteracoes_busca.append(iter_busca)
            alturas_medias.append(altura_media)
            
            print(f"  Vol {volume:,}: Tempo={tempo_ins:.4f}s, Iter.Busca={iter_busca:.0f}, Altura={altura_media:.1f}")
    
    # razoes de crescimento
    if len(medias_tempo_insercao) >= 2:
        razao_tempo_1 = medias_tempo_insercao[1] / medias_tempo_insercao[0]
        razao_tempo_2 = medias_tempo_insercao[2] / medias_tempo_insercao[1]
        print(f"  Razão crescimento tempo: {razao_tempo_1:.1f}x, {razao_tempo_2:.1f}x")
        
        razao_altura_1 = alturas_medias[1] / alturas_medias[0]
        razao_altura_2 = alturas_medias[2] / alturas_medias[1]
        print(f"  Razão crescimento altura: {razao_altura_1:.1f}x, {razao_altura_2:.1f}x")