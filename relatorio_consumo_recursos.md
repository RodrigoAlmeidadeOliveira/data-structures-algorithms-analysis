# Relatório de Análise de Consumo de Recursos

## Avaliação do Consumo de Recursos: Iterações, Memória e CPU

### Resumo Executivo

Este relatório apresenta uma análise detalhada do consumo de recursos durante operações de inserção e busca em diferentes estruturas de dados, incluindo número de iterações, utilização de memória e carga de CPU. Os experimentos foram conduzidos com tamanhos de dados variando de 10.000 a 100.000 elementos.

### Metodologia

A análise foi baseada em dados experimentais coletados de quatro estruturas de dados principais:
- **Linear Array**: Array linear simples
- **BST (Binary Search Tree)**: Árvore de busca binária não balanceada
- **AVL Tree**: Árvore de busca binária auto-balanceada
- **Hash Table**: Tabela hash com diferentes funções hash (divisão, multiplicação, folding) e tamanhos (M=100, M=1000, M=5000)

### 1. Análise de Número de Iterações

#### Operações de Inserção

**Estruturas com melhor eficiência (menor número de iterações):**

1. **Linear Array**: Apresenta complexidade linear O(n), com número de iterações igual ao tamanho dos dados:
   - 10.000 elementos: 10.000 iterações
   - 50.000 elementos: 50.000 iterações
   - 100.000 elementos: 100.000 iterações

2. **Hash Table M=5000**: Mostra excelente eficiência para inserção:
   - Divisão: 19.936 - 1.102.378 iterações (dependendo do tamanho)
   - Multiplicação: 19.985 - 1.099.643 iterações
   - Folding: 38.666 - 2.945.912 iterações (pior desempenho devido a colisões)

**Estruturas com maior consumo de iterações:**

1. **Hash Table M=100**: Extremamente ineficiente devido ao alto fator de carga:
   - 510.000+ iterações para 10.000 elementos
   - 50+ milhões de iterações para 100.000 elementos

2. **BST não balanceada**: Apresenta degradação significativa com o crescimento dos dados:
   - 159.813 iterações (10K) → 2.011.410 iterações (100K)

#### Operações de Busca

**Melhores desempenhos:**

1. **Hash Table M=5000**: 
   - Divisão/Multiplicação: 3-12 iterações em média
   - Folding: 5-30 iterações (ainda excelente)

2. **AVL Tree**: Mantém log(n) consistente:
   - 12,6 iterações (10K) → 15,9 iterações (100K)

3. **BST**: Desempenho logarítmico razoável:
   - 17 iterações (10K) → 21 iterações (100K)

### 2. Análise de Utilização de CPU (Tempo de Execução)

#### Inserção - Tempos de Execução

**Estruturas mais eficientes:**

1. **Linear Array**: 
   - Escala linearmente: 0,59ms → 5,65ms
   - Melhor para conjuntos pequenos de dados

2. **Hash Table M=5000** (Divisão/Multiplicação):
   - 2,8ms → 131ms (crescimento controlado)
   - Excelente custo-benefício

**Estruturas menos eficientes:**

1. **Hash Table M=100**: 
   - Degradação severa: 18ms → 3.12s
   - Inviável para grandes volumes

2. **AVL Tree**: 
   - 49ms → 797ms (overhead de balanceamento)

#### Busca - Tempos de Execução

**Melhores desempenhos:**

1. **Hash Table M=5000**: 
   - Tempos na ordem de microsegundos (0,2-1,7μs)
   - Crescimento quase constante

2. **AVL/BST Trees**: 
   - 1-3 microsegundos
   - Crescimento logarítmico previsível

### 3. Análise de Eficiência de Recursos

#### Métrica: Iterações por Unidade de Tempo

**Maior eficiência (iterações/tempo):**

1. **Linear Array**: 
   - Inserção: ~17M iterações/segundo
   - Busca: ~19M iterações/segundo
   - Consistência notável

2. **Hash Table M=100** (paradoxo da ineficiência):
   - Apesar do alto número absoluto de iterações, mantém taxa alta de processamento
   - Inserção: 16-28M iterações/segundo

**Menor eficiência:**

1. **AVL Tree**: 
   - Inserção: 2,1-2,8M iterações/segundo
   - Overhead significativo de balanceamento

2. **Hash Table M=5000 Folding**: 
   - Inserção: 3,7-10,4M iterações/segundo
   - Função hash mais custosa computacionalmente

### 4. Análise de Utilização de Memória

**Observação Importante**: Todos os experimentos reportaram utilização de memória como 0,0, indicando que:
- A medição de memória não foi implementada adequadamente no framework de testes
- Ou o overhead de memória das operações é insignificante comparado à resolução da medição

**Análise Teórica de Consumo de Memória:**

1. **Linear Array**: O(n) - linear com o tamanho dos dados
2. **BST/AVL**: O(n) - cada elemento requer um nó
3. **Hash Table**: O(M + n) - onde M é o tamanho da tabela

### 5. Recomendações por Caso de Uso

#### Para Inserção Intensiva:
1. **Pequenos volumes (< 50K)**: Linear Array
2. **Médios/Grandes volumes**: Hash Table M=5000 (Divisão/Multiplicação)
3. **Evitar**: Hash Table M=100, AVL em cenários de alta inserção

#### Para Busca Intensiva:
1. **Primeira escolha**: Hash Table M=5000 (qualquer função hash)
2. **Segunda escolha**: AVL Tree (busca balanceada)
3. **Terceira escolha**: BST (aceitável para dados moderadamente balanceados)

#### Para Operações Mistas:
1. **Hash Table M=1000-5000**: Melhor compromisso geral
2. **AVL Tree**: Quando ordem é importante
3. **Linear Array**: Apenas para volumes muito pequenos

### 6. Conclusões

1. **Hash Tables bem dimensionadas** (M=1000-5000) oferecem o melhor desempenho geral
2. **Fator de carga** é crucial - M=100 resulta em degradação severa
3. **AVL Trees** apresentam overhead significativo na inserção mas excelente para busca
4. **Função hash Folding** introduz overhead computacional adicional
5. **Linear Arrays** mantêm eficiência surpreendente para operações simples

### 7. Limitações do Estudo

1. **Medição de memória** não funcional nos experimentos
2. **Ausência de análise de cache** e localidade de referência
3. **Dados sintéticos** podem não refletir padrões reais de uso
4. **Configurações de hash table** limitadas (apenas 3 valores de M)

### 8. Recomendações para Estudos Futuros

1. Implementar medição adequada de consumo de memória
2. Avaliar impacto de diferentes padrões de dados de entrada
3. Analisar comportamento com operações de remoção
4. Estudar impacto de diferentes estratégias de resolução de colisões
5. Avaliar consumo energético além de tempo/iterações