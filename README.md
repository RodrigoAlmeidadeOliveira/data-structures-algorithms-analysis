# Análise Comparativa de Estruturas de Dados

## Descrição
Sistema de análise comparativa de estruturas de dados implementado para o trabalho de Fundamentos de Algoritmos e Estrutura de Dados da PUCPR.

## Estruturas Implementadas
- **Array Linear**: Implementação simples com inserção O(1) e busca O(n)
- **Árvore de Busca Binária (BST)**: Implementação sem balanceamento
- **Árvore AVL**: BST com balanceamento automático
- **Tabela Hash**: Com 3 funções hash (divisão, multiplicação, folding) e tratamento de colisões por encadeamento

## Instalação

```bash
# Instalar dependências
pip install -r requirements.txt
```

## Execução

```bash
# Executar análise completa
python main.py
```

## Estrutura do Projeto

```
├── main.py               # Script principal
├── models.py            # Classes Record e DataGenerator
├── linear_array.py      # Implementação do Array Linear
├── binary_search_tree.py # Implementação da BST
├── avl_tree.py          # Implementação da AVL
├── hash_table.py        # Implementação da Tabela Hash
├── metrics.py           # Sistema de coleta de métricas
├── experiments.py       # Módulo de experimentos
├── analysis.py          # Análise e visualização
└── requirements.txt     # Dependências
```

## Resultados

Os resultados são salvos em:
- `experiment_results.json`: Dados brutos dos experimentos
- `plots/`: Gráficos de análise
- `results_tables.tex`: Tabelas em formato LaTeX

## Métricas Coletadas

- **Tempo de execução**: Medido para cada operação
- **Número de iterações**: Contagem de operações internas
- **Memória**: Uso de memória durante operações
- **CPU**: Percentual de uso do processador
- **Métricas específicas**:
  - Hash: Load factor, taxa de colisões, comprimento de cadeias
  - Árvores: Altura da estrutura

## Parâmetros dos Experimentos

- **Tamanhos de dados**: N = {10.000, 50.000, 100.000}
- **Rodadas por experimento**: 5
- **Tamanhos da tabela hash**: M = {100, 1.000, 5.000}
- **Funções hash**: Divisão, Multiplicação, Folding

## Análises Realizadas

1. **Comparação de tempos**: Inserção e busca
2. **Análise de complexidade**: Teórica vs. observada
3. **Análise de iterações**: Número de operações internas
4. **Análise específica de hash**: Colisões e load factor
5. **Análise de árvores**: Altura e balanceamento